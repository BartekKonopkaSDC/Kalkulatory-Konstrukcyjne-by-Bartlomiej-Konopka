import streamlit as st
from PROGRAMY.DlugoscZakladu import StronaDlugoscZakladu
from PROGRAMY.DlugoscZakotwienia import StronaDlugoscZakotwienia
from PROGRAMY.OtulinaZbrojenia import StronaOtulinaZbrojenia

# --- 1. KONFIGURACJA STRONY ---
st.set_page_config(
    page_title="KALKULATORY KONSTRUKCYJNE – Bartłomiej Konopka",
    layout="wide",
    initial_sidebar_state="expanded" # ZMIANA: Pasek zawsze rozwinięty
)

# --- 2. ZABEZPIECZENIE - EKRAN LOGOWANIA ---
if 'zalogowany' not in st.session_state:
    st.session_state['zalogowany'] = False

if not st.session_state['zalogowany']:
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        # Nagłówek na ekranie logowania
        st.markdown(
            """
            <div style="text-align: center; margin-bottom: 30px;">
                <h1 style="margin-bottom: 0.1em; letter-spacing: 1px;">
                    KALKULATORY KONSTRUKCYJNE
                </h1>
                <div style="font-size: 1.1em; color: #aaa; margin-top: -8px;">
                    made by Bartłomiej Konopka
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        
        login_input = st.text_input("Login")
        haslo_input = st.text_input("Hasło", type="password")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        if st.button("Zaloguj się", type="primary", use_container_width=True):
            if login_input == "BARTEK" and haslo_input == "12345":
                st.session_state['zalogowany'] = True
                st.rerun()
            else:
                st.error("⚠️ Błędny login lub hasło!")

    st.stop()


# --- 3. WŁAŚCIWA APLIKACJA (PO ZALOGOWANIU) ---

# --- STYL CSS ---
st.markdown("""
    <style>
    .stRadio > div {gap: 8px;}
    .sidebar-text {font-size: 14px; color: #888;}
    </style>
""", unsafe_allow_html=True)

# --- NAGŁÓWEK GŁÓWNY ---
st.markdown(
    """
    <div style="text-align: center; margin-top: -20px; margin-bottom: 20px;">
        <h1 style="margin-bottom: 0.1em; letter-spacing: 1px;">
            KALKULATORY KONSTRUKCYJNE
        </h1>
        <div style="font-size: 1.1em; color: #aaa; margin-top: -8px;">
            made by Bartłomiej Konopka
        </div>
    </div>
    <hr style="margin-top: 0px; margin-bottom: 30px;">
    """,
    unsafe_allow_html=True,
)

# --- MENU BOCZNE (SIDEBAR) ---
with st.sidebar:
    # Sekcja główna
    st.markdown("### 🏗️ KONSTRUKCJE ŻELBETOWE (EC2)")
    
    # Podrozdział 1: Podstawowe dane
    st.markdown("**🔧 Podstawowe dane**") 
    
    # Lista narzędzi
    wybor_detale = st.radio(
        "Wybierz narzędzie:",
        options=[
            "Długość zakładu prętów",
            "Długość zakotwienia prętów",
            "Otulina zbrojenia",
        ],
        label_visibility="collapsed",
        key="nav_detale"
    )

    st.markdown("---")
    
    # Podrozdział 2: Wymiarowanie
    st.markdown("**📐 Wymiarowanie elementów**")
    st.markdown(
        """
        <div class="sidebar-text">
        <i>Kalkulatory zbrojenia na zginanie, ścinanie i przebicie - wkrótce...</i>
        </div>
        """, 
        unsafe_allow_html=True
    )
    
    st.markdown("---")
    if st.button("Wyloguj"):
        st.session_state['zalogowany'] = False
        st.rerun()


# --- LOGIKA WYŚWIETLANIA STRON ---

if wybor_detale == "Długość zakładu prętów":
    StronaDlugoscZakladu()

elif wybor_detale == "Długość zakotwienia prętów":
    StronaDlugoscZakotwienia()

elif wybor_detale == "Otulina zbrojenia":
    StronaOtulinaZbrojenia()