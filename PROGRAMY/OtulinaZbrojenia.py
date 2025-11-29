import streamlit as st

def StronaOtulinaZbrojenia():
    # ZMIANA: Pełny tytuł spójny z resztą aplikacji
    st.title("OBLICZENIE OTULINY ZBROJENIA wg PN-EN 1992-1-1")
    
    st.markdown("---")
    
    # Wyświetlenie komunikatu o budowie
    st.warning("🚧 **MODUŁ W TRAKCIE BUDOWY**")
    
    st.markdown(
        """
        <div style="text-align: center; padding: 20px;">
            <p style="font-size: 18px; color: #555;">
                Kalkulator otuliny zbrojenia wg PN-EN 1992-1-1 jest obecnie przygotowywany.<br>
                Zapraszamy wkrótce!
            </p>
        </div>
        """, 
        unsafe_allow_html=True
    )