import tempfile
import subprocess
import os
import sys
import shutil

# Nazwa pliku źródłowego aplikacji Streamlit (musi być obok pliku start_app.py podczas budowania)
APP_FILENAME = "app.py"

def main():
    # Znajdź rzeczywistą ścieżkę do aplikacji (dołączonej do .exe)
    if getattr(sys, 'frozen', False):
        # Jeśli uruchomione jako .exe
        base_path = sys._MEIPASS  # folder tymczasowy PyInstaller
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))

    app_source_path = os.path.join(base_path, APP_FILENAME)

    if not os.path.exists(app_source_path):
        print(f"Nie znaleziono {APP_FILENAME} w {base_path}")
        sys.exit(1)

    # Utwórz tymczasowy folder i skopiuj app.py do niego
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_app_path = os.path.join(temp_dir, APP_FILENAME)
        shutil.copy2(app_source_path, temp_app_path)

        # Uruchom Streamlit na tymczasowej kopii app.py
        subprocess.run(["streamlit", "run", temp_app_path])

if __name__ == "__main__":
    main()
