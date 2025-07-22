import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import requests
from bs4 import BeautifulSoup

# === FUNKCJA: pobierz aktualny WIBOR 1M ===
@st.cache_data(ttl=3600)
def get_wibor_1m():
    try:
        url = "https://gpwbenchmark.pl/"
        response = requests.get(url, timeout=5)
        soup = BeautifulSoup(response.text, "html.parser")
        rows = soup.select(".table-custom tr")
        for row in rows:
            cols = row.find_all("td")
            if len(cols) >= 2:
                label = cols[0].text.lower().replace("®", "").replace(" ", "")
                if "wibor1m" in label:
                    value_text = cols[1].text.strip().replace(",", ".")
                    return float(value_text)
    except Exception as e:
        print(f"Błąd podczas pobierania WIBOR: {e}")
        return None

# === INTERFEJS ===
st.title("📊 Kalkulator leasingowy z prowizją i wykupem")

cena_netto = 178_780.50
st.write(f"💼 Cena netto przedmiotu leasingu: **{cena_netto:,.2f} PLN**")

wibor_1m = get_wibor_1m()
oprocentowanie = st.number_input("Roczna stopa procentowa (%):", min_value=0.0, max_value=30.0, value=5.11, step=0.01)

if wibor_1m is not None:
    st.info(f"📌 Aktualny WIBOR 1M (GPW Benchmark): **{wibor_1m:.2f}%**")
else:
    st.warning("⚠️ Nie udało się pobrać aktualnego WIBOR 1M")

wplata_pierwsza_proc = st.slider("Pierwsza wpłata (% ceny netto)", 0, 100, 15, step=1)
wykup_proc = st.slider("Wartość wykupu (% ceny netto)", 0, 100, 15, step=1)
liczba_miesiecy = st.selectbox("Okres leasingu (miesiące)", [24, 36, 48, 60, 72], value=60)
prowizja_proc = st.number_input("Prowizja leasingowa (% kwoty finansowanej)", 0.0, 10.0, value=2.65, step=0.01)
oplata_dodatkowa = st.number_input("Dodatkowe koszty jednorazowe (PLN)", 0.0, 10000.0, value=0.0, step=100.0)
uwzglednij_n_minus_1 = st.checkbox("Odjąć 1 ratę (np. leasing 60 miesięcy = 59 rat)?", value=True)
n = liczba_miesiecy - 1 if uwzglednij_n_minus_1 else liczba_miesiecy

# === OBLICZENIA ===
if st.button("Oblicz leasing"):
    wplata_pierwsza = cena_netto * (wplata_pierwsza_proc / 100)
    wartosc_wykupu = cena_netto * (wykup_proc / 100)
    kwota_finansowana = cena_netto - wplata_pierwsza
    prowizja_kwota = kwota_finansowana * (prowizja_proc / 100)
    kwota_do_sfinansowania = kwota_finansowana + prowizja_kwota

    stopa_miesieczna = (oprocentowanie / 100) / 12

    if stopa_miesieczna > 0:
        rata = np.pmt(stopa_miesieczna, n, -kwota_do_sfinansowania, fv=wartosc_wykupu)
    else:
        rata = (kwota_do_sfinansowania - wartosc_wykupu) / n

    suma_rat = rata * n
    suma_wplat = wplata_pierwsza + suma_rat + wartosc_wykupu + oplata_dodatkowa
    procent_netto = (suma_wplat / cena_netto) * 100

    # === WYNIKI ===
    st.subheader("📈 Wyniki obliczeń:")
    st.write(f"📦 Kwota finansowana (bez prowizji): **{kwota_finansowana:,.2f} PLN**")
    st.write(f"➕ Prowizja leasingowa (wliczona w raty): **{prowizja_kwota:,.2f} PLN**")
    st.write(f"💳 Kwota całkowicie finansowana: **{kwota_do_sfinansowania:,.2f} PLN**")
    st.write(f"📆 Liczba rat: **{n}**")
    st.write(f"💰 Miesięczna rata: **{rata:,.2f} PLN**")
    st.write(f"📑 Suma rat leasingowych: **{suma_rat:,.2f} PLN**")
    st.write(f"💼 Całkowita suma wpłat (łącznie): **{suma_wplat:,.2f} PLN**")
    st.write(f"📊 Całkowite wpłaty to **{procent_netto:.2f}%** ceny netto")

    # === WYKRES ===
    fig, ax = plt.subplots()
    kategorie = ["Pierwsza wpłata", "Suma rat", "Wartość wykupu", "Koszty dodatkowe"]
    wartosci = [wplata_pierwsza, suma_rat, wartosc_wykupu, oplata_dodatkowa]

    ax.bar(kategorie, wartosci)
    ax.set_title("Struktura całkowitych kosztów leasingu")
    ax.set_ylabel("Kwota (PLN)")
    for i, v in enumerate(wartosci):
        ax.text(i, v + cena_netto * 0.01, f"{v:,.0f}", ha="center")

    st.pyplot(fig)
