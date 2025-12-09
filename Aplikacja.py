import sys
import os
import streamlit as st
from pathlib import Path

# --- FUNKCJA WYSZUKUJĄCA ŚCIEŻKĘ GŁÓWNĄ ---
def get_base_path_safe():
    """Wyszukuje katalog 'KALKULATORY' niezależnie od głębokości zagnieżdżenia."""
    current_path = Path(os.path.abspath(__file__))
    for parent in current_path.parents:
        if parent.name.upper() == "KALKULATORY":
            return str(parent)
    return str(current_path.parent)

# --- 1. KONFIGURACJA STRONY ---
st.set_page_config(
    page_title="PLATFORMA OBLICZEŃ INŻYNIERSKICH – Bartłomiej Konopka",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- 2. STYLE CSS ---
st.markdown(
    """
<style>
/* Zmniejszenie marginesu na samej górze strony */
.block-container {
    padding-top: 1rem !important;
    padding-bottom: 2rem !important;
}

/* Zmniejszenie odstępów nagłówków h1 */
h1 {
    margin-bottom: 0px !important;
    padding-bottom: 0px !important;
}

/* Stylizacja komunikatów "W fazie opracowania" */
.work-in-progress {
    padding: 20px;
    border-radius: 10px;
    background-color: #f0f2f6;
    border-left: 6px solid #ffbd45;
    color: #31333F;
}
.work-in-progress h3 {
    margin-top: 0;
    color: #ffbd45;
}
</style>
""",
    unsafe_allow_html=True,
)

# --- 3. USTAWIANIE ŚCIEŻEK ---
KATALOG_GLOWNY = os.path.dirname(os.path.abspath(__file__))
sciezka_moduly = os.path.join(KATALOG_GLOWNY, "_MODULY")

# Podfoldery istniejące
sciezka_zaklad      = os.path.join(sciezka_moduly, "PODSTAWOWE DANE_DLUGOSC ZAKLADU")
sciezka_zakotwienie = os.path.join(sciezka_moduly, "PODSTAWOWE DANE_DLUGOSC ZAKOTWIENIA")
sciezka_otulina     = os.path.join(sciezka_moduly, "PODSTAWOWE DANE_OTULINA ZBROJENIA")
sciezka_beton       = os.path.join(sciezka_moduly, "PODSTAWOWE DANE_PARAMETRY BETONU")
sciezka_stal        = os.path.join(sciezka_moduly, "PODSTAWOWE DANE_PARAMETRY STALI")

sciezki_do_sys = [
    KATALOG_GLOWNY,
    sciezka_moduly,
    sciezka_zaklad,
    sciezka_zakotwienie,
    sciezka_otulina,
    sciezka_beton,
    sciezka_stal,
]

for sciezka in sciezki_do_sys:
    if os.path.exists(sciezka):
        if sciezka not in sys.path:
            sys.path.append(sciezka)

# --- 4. IMPORTY MODUŁÓW ISTNIEJĄCYCH ---
try:
    from DlugoscZakladu import StronaDlugoscZakladu
    from DlugoscZakotwienia import StronaDlugoscZakotwienia
    from OtulinaZbrojenia import StronaOtulinaZbrojenia
    from ParametryBetonuStrona import StronaParametryBetonu
    from ParametryStaliStrona import StronaParametryStali
except ImportError:
    pass # Obsługa błędów w routingu

# --- 5. EKRAN LOGOWANIA ---
if "zalogowany" not in st.session_state:
    st.session_state["zalogowany"] = False

if not st.session_state["zalogowany"]:
    st.markdown(
        """
        <div style="text-align:center; margin-top:2rem; margin-bottom:0rem;">
            <span style="font-size:42px; font-weight:800; letter-spacing:1px; color:#dddddd;">
                PLATFORMA OBLICZEŃ INŻYNIERSKICH
            </span>
        </div>
        <div style="text-align:center; font-size:14px; color:#aaaaaa; margin-top:-5px; margin-bottom:0.6rem;">
            made by Bartłomiej Konopka
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        login_input = st.text_input("Login")
        haslo_input = st.text_input("Hasło", type="password")

        if st.button("Zaloguj się", type="primary", use_container_width=True):
            if login_input == "BARTEK" and haslo_input == "12345":
                st.session_state["zalogowany"] = True
                st.rerun()
            else:
                st.error("Błędny login lub hasło!")
    st.stop()

# --- 6. PANEL BOCZNY I NAWIGACJA ---
with st.sidebar:
    st.markdown("### 🗂️ DZIAŁY PROJEKTOWE")
    
    # Główne działy
    wybrany_dzial = st.radio(
        "Wybierz dział:",
        options=[
            "1. OBCIĄŻENIA (EC0/EC1)",
            "2. KONSTRUKCJE ŻELBETOWE (EC2)",
            "3. KONSTRUKCJE STALOWE (EC3)",
            "4. KONSTRUKCJE DREWNIANE (EC5)"
        ],
        index=1 # Domyślnie Żelbet
    )
    
    st.markdown("---")
    
    # Zmienna do przechowywania wybranego narzędzia wewnątrz działu
    wybrane_narzedzie = None

    # --- LOGIKA WYŚWIETLANIA PODMENU ---
    
    if wybrany_dzial == "2. KONSTRUKCJE ŻELBETOWE (EC2)":
        st.markdown("**📂 KATEGORIE**")
        
        # 1. PODSTAWOWE DANE (Istniejące)
        with st.expander("🔧 PODSTAWOWE DANE", expanded=True):
            narzedzie_podstawowe = st.radio(
                "Wybierz kalkulator:",
                options=[
                    "Parametry betonu",
                    "Parametry stali",
                    "Otulina zbrojenia",
                    "Długość zakotwienia",
                    "Długość zakładu"
                ],
                label_visibility="collapsed"
            )
            wybrane_narzedzie = narzedzie_podstawowe

        # 2. WYMIAROWANIE (Nowe - Placeholdery)
        with st.expander("📐 WYMIAROWANIE ZBROJENIA (SGN)", expanded=False):
            narzedzie_wymiarowanie = st.radio(
                "Wybierz element:",
                options=[
                    "Zginanie - Przekrój prostokątny",
                    "Ścinanie - V_Ed vs V_Rd,c"
                ],
                index=None,
                label_visibility="collapsed"
            )
            if narzedzie_wymiarowanie:
                wybrane_narzedzie = narzedzie_wymiarowanie

        # 3. ZBROJENIE MINIMALNE (Nowe - Placeholdery)
        with st.expander("🛡️ ZBROJENIE MINIMALNE", expanded=False):
            narzedzie_min = st.radio(
                "Wybierz element:",
                options=[
                    "Płyty",
                    "Belki",
                    "Słupy",
                    "Ściany"
                ],
                index=None,
                label_visibility="collapsed"
            )
            if narzedzie_min:
                wybrane_narzedzie = narzedzie_min

    # Pozostałe działy nie mają podmenu (są w budowie)
    
    st.markdown("---")
    
    # INFO O AUTORZE
    st.markdown(
        """
        <div style="text-align: center; color: #888888; font-size: 0.75rem; margin-bottom: 15px;">
            PLATFORMA OBLICZEŃ INŻYNIERSKICH<br>
            <span style="font-style: italic;">made by Bartłomiej Konopka</span>
        </div>
        """, 
        unsafe_allow_html=True
    )

    c_left, c_center, c_right = st.columns([1, 4, 1])
    with c_center:
        if st.button("Wyloguj", use_container_width=True):
            st.session_state["zalogowany"] = False
            st.rerun()

# --- 7. ROUTING I TREŚĆ GŁÓWNA ---

def show_w_opracowaniu(tytul):
    st.markdown(f"## {tytul}")
    st.markdown(
        """
        <div class="work-in-progress">
            <h3>🚧 MODUŁ W FAZIE OPRACOWANIA</h3>
            <p>Ten dział jest obecnie przygotowywany i zostanie udostępniony wkrótce.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

# A. DZIAŁY "W BUDOWIE"
if wybrany_dzial == "1. OBCIĄŻENIA (EC0/EC1)":
    show_w_opracowaniu("OBCIĄŻENIA I KOMBINACJE (EC0 / EC1)")

elif wybrany_dzial == "3. KONSTRUKCJE STALOWE (EC3)":
    show_w_opracowaniu("KONSTRUKCJE STALOWE (EC3)")

elif wybrany_dzial == "4. KONSTRUKCJE DREWNIANE (EC5)":
    show_w_opracowaniu("KONSTRUKCJE DREWNIANE (EC5)")

# B. DZIAŁ ŻELBET (EC2)
elif wybrany_dzial == "2. KONSTRUKCJE ŻELBETOWE (EC2)":
    
    # -- PODSTAWOWE DANE (Działające moduły) --
    if wybrane_narzedzie == "Parametry betonu":
        if 'StronaParametryBetonu' in globals():
            StronaParametryBetonu()
        else:
            st.error("Błąd: Nie znaleziono modułu Parametry Betonu")

    elif wybrane_narzedzie == "Parametry stali":
        if 'StronaParametryStali' in globals():
            StronaParametryStali()
        else:
            st.error("Błąd: Nie znaleziono modułu Parametry Stali")

    elif wybrane_narzedzie == "Otulina zbrojenia":
        if 'StronaOtulinaZbrojenia' in globals():
            StronaOtulinaZbrojenia()
        else:
            st.error("Błąd: Nie znaleziono modułu Otulina Zbrojenia")

    elif wybrane_narzedzie == "Długość zakotwienia":
        if 'StronaDlugoscZakotwienia' in globals():
            StronaDlugoscZakotwienia()
        else:
            st.error("Błąd: Nie znaleziono modułu Długość Zakotwienia")

    elif wybrane_narzedzie == "Długość zakładu":
        if 'StronaDlugoscZakladu' in globals():
            StronaDlugoscZakladu()
        else:
            st.error("Błąd: Nie znaleziono modułu Długość Zakładu")

    # -- WYMIAROWANIE (SGN) --
    elif wybrane_narzedzie in ["Zginanie - Przekrój prostokątny", "Ścinanie - V_Ed vs V_Rd,c"]:
        show_w_opracowaniu(f"WYMIAROWANIE: {wybrane_narzedzie.upper()}")

    # -- ZBROJENIE MINIMALNE --
    elif wybrane_narzedzie in ["Płyty", "Belki", "Słupy", "Ściany"]:
        show_w_opracowaniu(f"ZBROJENIE MINIMALNE: {wybrane_narzedzie.upper()}")
    
    else:
        st.info("👈 Wybierz narzędzie z menu po lewej stronie.")