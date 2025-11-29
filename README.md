# 🏗️ Kalkulatory Konstrukcyjne wg PN-EN 1992-1-1 (EC2)

Interaktywna aplikacja webowa dla inżynierów budownictwa, służąca do szybkich obliczeń konstrukcyjnych elementów żelbetowych zgodnie z Eurokodem 2.

## 🚀 Funkcjonalności

Aplikacja składa się z modułów obliczeniowych:

### 1. Długość Zakładu Prętów ($l_0$)
* Obliczanie wymaganej długości zakładu dla prętów rozciąganych i ściskanych.
* Pełna obsługa współczynników $\alpha_1 - \alpha_6$.
* Generowanie profesjonalnej **Notki Obliczeniowej** w formatach **PDF** i **DOCX**.
* Styl raportów: inżynierski (czcionka szeryfowa, wzory matematyczne, przejrzysty układ).

### 2. Długość Zakotwienia Prętów ($l_{bd}$)
* Obliczanie długości zakotwienia z uwzględnieniem kształtu pręta (prosty/hak).
* Automatyczne dobieranie współczynników $\eta_1, \eta_2$.
* Szczegółowy podgląd wzorów obliczeniowych na stronie.
* Eksport wyników do **PDF** i **DOCX**.

### 3. Otulina Zbrojenia ($c_{nom}$)
* *Moduł w przygotowaniu (Work in Progress).*

## 🛠️ Technologie

Projekt został zrealizowany w języku **Python** z wykorzystaniem bibliotek:
* **Streamlit** - interfejs użytkownika i silnik aplikacji.
* **FPDF** - generowanie raportów PDF z obsługą polskich znaków i symboli matematycznych.
* **python-docx** - generowanie edytowalnych raportów Word.

## 🌐 Wersja Online

Aplikacja jest dostępna online pod adresem:
https://kalkulatory-konstrukcyjne-by-bartlomiej-konopka-dnxb2tu5uappzm.streamlit.app/

---
**Autor:** Bartłomiej Konopka
