import streamlit as st
from PROGRAMY.DlugoscZakladu import StronaDlugoscZakladu
from PROGRAMY.DlugoscZakotwienia import StronaDlugoscZakotwienia
from PROGRAMY.OtulinaZbrojenia import StronaOtulinaZbrojenia

# --- KONFIGURACJA STRONY ---
st.set_page_config(
    page_title="KALKULATORY KONSTRUKCYJNE – Bartłomiej Konopka",
    layout="wide",
)

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
    
    # Lista narzędzi (Pierwszy element jest domyślny przy starcie)
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
    
    # Podrozdział 2: Wymiarowanie (Miejsce na przyszłość)
    st.markdown("**📐 Wymiarowanie elementów**")
    st.markdown(
        """
        <div class="sidebar-text">
        <i>Kalkulatory zbrojenia na zginanie, ścinanie i przebicie - wkrótce...</i>
        </div>
        """, 
        unsafe_allow_html=True
    )


# --- LOGIKA WYŚWIETLANIA STRON ---

if wybor_detale == "Długość zakładu prętów":
    StronaDlugoscZakladu()

elif wybor_detale == "Długość zakotwienia prętów":
    StronaDlugoscZakotwienia()

elif wybor_detale == "Otulina zbrojenia":
    StronaOtulinaZbrojenia()