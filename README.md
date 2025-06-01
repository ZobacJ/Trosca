# TrOSCa – Tracking Oscillator Control Application

Aplikace TrOSCa (Tracking Oscillator Control Application) slouží k ovládání
digitálního oscilátoru pomocí CANOpen protokolu.
Program obsahuje grafické uživatelské rozhraní (GUI) v PyQt5 a backend pro komunikaci
s kartou, vizualizaci dat, výpočet spekter a export.

Autor: Jindřich Zobač
kontakt: jindra@isibrno.cz
součást Bakalářská práce, Vysoké Učení Technické, 2025
Zdrojové soubory jsou dostupné na githubu: https://github.com/ZobacJ/Trosca.git

# Struktura souborů pro správné fungování:
TROSCA
    |--- main.py
    |--- main.exe
    |--- canusb32.dll
    |--- [netcans]
    |--- [candevices]
    |--- [docs]
    |    |--- help.html
    |    \--- [obrazky]
    |
    |--- [images]
    |    |--- schema.png
    |    |--- arrow_down.png
    |    |--- checkbox.png
    |    \--- UPT_text_en_white_15.png
    |
    |--- fnc.can (nebo jiný .can soubor specifikovaný v app_config.json)
    |--- app_icon.ico
    |--- app_config.json (vytvořený automaticky))
    |--- trosca.log (vytvořený automaticky)
    |
    |--- LICENSE
    |--- requirements.txt
    \--- README.md

## Způsoby spuštění

### 1. Předkompilovaná verze (.exe)
- Doporučený způsob pro běžné uživatele.
- **Není potřeba instalovat Python ani žádné závislosti.**
- Stačí spustit soubor `main.exe` v adresáři `dist`
- Ujistěte se, že v adresáři jsou také další soubory definované výše.

### 2. Spuštění v Pythonu
- Pro vývojáře nebo pokročilé uživatele.
- **Vyžaduje 32bitovou verzi Pythonu 3.8+** (kvůli kompatibilitě s `canusb32.dll`).
- Je nutné doinstalovat následující závislosti:
  `pip install pyqt5 pyqtgraph numpy psutil qtwidgets`
- Spuštění programu:
`python main.py`

## Licence

Tento projekt je poskytován pod licencí MIT. Viz soubor [LICENSE](LICENSE)