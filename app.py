import streamlit as st

st.title("Kalkulator rat leasingowych")

# Dane wejściowe
cena_netto = st.number_input("Cena netto (PLN)", min_value=1000.0, step=100.0)
oprocentowanie = st.number_input("Roczna stopa procentowa (%)", min_value=0.0, max_value=100.0, step=0.1)
wplata_pierwsza_proc = st.slider("Wysokość pierwszej wpłaty (% ceny netto)", 0.0, 100.0, 10.0)
wykup_proc = st.slider("Wartość wykupu (% ceny netto)", 0.0, 100.0, 10.0)
liczba_miesiecy = st.selectbox("Okres leasingu (w miesiącach)", [24, 36, 48, 60, 72])

if st.button("Oblicz ratę leasingową"):
    # Obliczenia
    wplata_pierwsza = cena_netto * (wplata_pierwsza_proc / 100)
    wartosc_wykupu = cena_netto * (wykup_proc / 100)
    kwota_finansowana = cena_netto - wplata_pierwsza

    stopa_miesieczna = (oprocentowanie / 100) / 12

    # Obliczenie raty miesięcznej z wykupem końcowym (balonem)
    if stopa_miesieczna > 0:
        rata = (kwota_finansowana * stopa_miesieczna) / (1 - (1 + stopa_miesieczna) ** (-liczba_miesiecy)) \
               + (wartosc_wykupu / ((1 + stopa_miesieczna) ** liczba_miesiecy))
    else:
        rata = (kwota_finansowana + wartosc_wykupu) / liczba_miesiecy

    # Wyświetlenie wyników
    st.subheader("Wyniki:")
    st.write(f"💰 Kwota finansowana: **{kwota_finansowana:,.2f} PLN**")
    st.write(f"💵 Pierwsza wpłata: **{wplata_pierwsza:,.2f} PLN**")
    st.write(f"📦 Wartość wykupu: **{wartosc_wykupu:,.2f} PLN**")
    st.write(f"📆 Rata miesięczna: **{rata:,.2f} PLN**")