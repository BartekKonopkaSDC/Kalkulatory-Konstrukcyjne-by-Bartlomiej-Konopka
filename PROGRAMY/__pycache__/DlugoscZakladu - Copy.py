"""
PROGRAMY/DlugoscZakladu.py

Strona Streamlit do obliczania długości zakładu prętów zbrojeniowych
wg PN-EN 1992-1-1 (EC2).

Wymaga:
- OBLICZENIA/Obliczenia_DlugoscZakladu.py -> funkcja ObliczDlugoscZakladu
- TABLICE/ParametryBetonu.py               -> get_concrete_params, list_concrete_classes
- TABLICE/ParametryStali.py                -> get_steel_params, list_steel_grades
"""

from __future__ import annotations

from pathlib import Path

import streamlit as st

from OBLICZENIA.Obliczenia_DlugoscZakladu import ObliczDlugoscZakladu
from TABLICE.ParametryBetonu import get_concrete_params, list_concrete_classes
from TABLICE.ParametryStali import get_steel_params, list_steel_grades

# Ścieżka do folderu DODATKI (rysunki normowe)
SCIEZKA_BAZOWA = Path(__file__).resolve().parents[1]
SCIEZKA_DODATKI = SCIEZKA_BAZOWA / "DODATKI"


def StronaDlugoscZakladu() -> None:
    """Główna funkcja rysująca stronę z kalkulatorem długości zakładu."""
    st.title("DŁUGOŚĆ ZAKŁADU PRĘTÓW – EC2")

    # jedna kolumna robocza (druga nam już niepotrzebna)
    col_lewa, _ = st.columns([2.0, 1.3])

    # ======================================================================
    # LEWA KOLUMNA – dane wejściowe i współczynniki
    # ======================================================================
    with col_lewa:
        st.subheader("DANE WEJŚCIOWE")

        # --------------------------------------------------------------
        # Średnica pręta
        # --------------------------------------------------------------
        dostepne_fi = [6, 8, 10, 12, 14, 16, 18, 20, 22, 25, 28, 32, 40]
        fi_mm = st.selectbox("ŚREDNICA PRĘTA φ [mm]", dostepne_fi, index=3)

        # --------------------------------------------------------------
        # Klasa betonu – z TABLICE.ParametryBetonu
        # --------------------------------------------------------------
        klasy_betonu = list_concrete_classes()
        if "C30/37" in klasy_betonu:
            index_beton = klasy_betonu.index("C30/37")
        elif "C20/25" in klasy_betonu:
            index_beton = klasy_betonu.index("C20/25")
        else:
            index_beton = 0
        klasa_betonu = st.selectbox("KLASA BETONU", klasy_betonu, index=index_beton)

        # Parametry betonu (obecnie nieużywane w UI, ale czytamy dla spójności)
        beton = get_concrete_params(klasa_betonu)  # noqa: F841

        # --------------------------------------------------------------
        # Stal – wybór gatunku i pobranie fyk [MPa]
        # --------------------------------------------------------------
        dostepne_stale = list_steel_grades()
        wybrana_stal = st.selectbox(
            "KLASA STALI ZBROJENIOWEJ",
            dostepne_stale,
            index=0,
        )
        stal = get_steel_params(wybrana_stal)
        fyk_MPa = stal.fyk  # [MPa]

        # --------------------------------------------------------------
        # NAPRĘŻENIA W STALI – procent wykorzystania
        # --------------------------------------------------------------
        naprezenia_stali = st.number_input(
            "NAPRĘŻENIA W STALI σ_sd / f_yd [%]",
            min_value=0.0,
            max_value=100.0,
            value=100.0,
            step=1.0,
            format="%.0f",
        )

        st.markdown("---")
        st.subheader("WARUNKI PRZYCZEPNOŚCI")

        # Rysunek – warunki przyczepności
        with st.expander("Warunki przyczepności (rysunek)"):
            rys = SCIEZKA_DODATKI / "DlugoscZakotwieniaIZakladu_WarunkiPrzyczepnosci.png"
            if rys.exists():
                st.image(rys, use_container_width=True)
            else:
                st.info(
                    "Brak pliku rysunku: "
                    "DlugoscZakotwieniaIZakladu_WarunkiPrzyczepnosci.png"
                )

        warunki = st.radio(
            "Warunki przyczepności",
            ["Dobre", "Złe"],
            index=0,
            horizontal=True,
        )
        eta1 = 1.0 if warunki == "Dobre" else 0.7

        st.markdown("---")
        st.subheader("WSPÓŁCZYNNIKI α₁–α₆")

        # ------------------------------------------------------------
        # Rysunki α₁–α₅
        # ------------------------------------------------------------
        with st.expander("Współczynniki α₁–α₅ (rysunek)"):
            rys15 = SCIEZKA_DODATKI / "DlugoscZakotwieniaIZakladu_alfa1-alfa5.png"
            if rys15.exists():
                st.image(rys15, use_container_width=True)
            else:
                st.info(
                    "Brak pliku rysunku: "
                    "DlugoscZakotwieniaIZakladu_alfa1-alfa5.png"
                )

        # --------------------------------------------------------------
        # Rodzaj pręta – decyduje o c_d, α₃, α₅
        # --------------------------------------------------------------
        rodzaj_preta = st.radio(
            "Rodzaj pręta",
            ["Rozciągany", "Ściskany"],
            index=1,  # domyślnie pręt ściskany
            horizontal=True,
        )

        alfa1 = 1.0
        alfa2 = 1.0
        alfa3 = 1.0
        alfa4 = 0.7  # pręt prosty
        alfa5 = 1.0
        alfa6 = 1.0
        wsp_cd = 30.0  # bazowo 30 mm

        # ======================================================================
        # PRĘT ROZCIĄGANY – α₂, α₃, α₅
        # ======================================================================
        if rodzaj_preta == "Rozciągany":

            # ----------------------------------------------------------
            # α₂ — c_d
            # ----------------------------------------------------------
            st.markdown(
                "### Odległości / rozmieszczenie prętów, współczynnik "
                "c<sub>d</sub> – α₂",
                unsafe_allow_html=True,
            )

            uwzgl_cd = st.radio(
                "Czy uwzględnić wpływ położenia pręta na długość zakładu (α₂)?",
                ["Nie", "Tak"],
                index=0,
                horizontal=True,
            )

            if uwzgl_cd == "Tak":

                with st.expander("Współczynnik c_d (rysunek)"):
                    rys_cd = (
                        SCIEZKA_DODATKI
                        / "DlugoscZakotwieniaIZakladu_Wspolczynnik cd.png"
                    )
                    if rys_cd.exists():
                        st.image(rys_cd, use_container_width=True)
                    else:
                        st.info(
                            "Brak pliku rysunku: "
                            "DlugoscZakotwieniaIZakladu_Wspolczynnik cd.png"
                        )

                st.markdown(
                    "Współczynnik c<sub>d</sub> [mm]",
                    unsafe_allow_html=True,
                )
                wsp_cd = st.number_input(
                    "",
                    min_value=0.0,
                    value=30.0,
                    step=1.0,
                )

                # α₂ – wzór normowy z ograniczeniem 0.7–1.0
                if fi_mm > 0:
                    alfa2_raw = 1.0 - 0.15 * ((wsp_cd - fi_mm) / fi_mm)
                    alfa2 = max(0.7, min(1.0, alfa2_raw))
                else:
                    alfa2 = 1.0

            else:
                alfa2 = 1.0

            # ----------------------------------------------------------
            # α₃ — zbrojenie poprzeczne
            # ----------------------------------------------------------
            st.markdown("### Ograniczenie odkształceń zbrojeniem poprzecznym – α₃")

            uwzgl_a3 = st.radio(
                "Czy uwzględnić wpływ zbrojenia poprzecznego (α₃)?",
                ["Nie", "Tak"],
                index=0,
                horizontal=True,
            )

            if uwzgl_a3 == "Tak":

                with st.expander("Współczynnik K (rysunek)"):
                    rys_K = (
                        SCIEZKA_DODATKI
                        / "DlugoscZakotwieniaIZakladu_WspolczynnikK.png"
                    )
                    if rys_K.exists():
                        st.image(rys_K, use_container_width=True)
                    else:
                        st.info(
                            "Brak pliku rysunku: "
                            "DlugoscZakotwieniaIZakladu_WspolczynnikK.png"
                        )

                K = st.selectbox("Współczynnik K [-]", [0.00, 0.05, 0.10], index=1)

                st.markdown("**Wyliczenia współczynnika λ**")

                Ast_sum = st.number_input(
                    "ΣAst – pole zbrojenia poprzecznego [cm²]",
                    min_value=0.0,
                    step=0.1,
                    value=3.0,
                )
                Ast_min_sum = st.number_input(
                    "ΣAst,min – minimalne wymagane pole zbrojenia poprzecznego [cm²]",
                    min_value=0.0,
                    step=0.1,
                    value=3.0,
                )

                As_mm2 = 3.14159 * (fi_mm**2) / 4.0
                As = As_mm2 / 100.0  # cm²

                if Ast_sum > Ast_min_sum and As > 0:
                    lambda_val = (Ast_sum - Ast_min_sum) / As
                else:
                    lambda_val = 0.0

                alfa3_raw = 1.0 - K * lambda_val
                alfa3 = max(0.7, min(1.0, alfa3_raw))

            else:
                alfa3 = 1.0

            # ----------------------------------------------------------
            # α₅ – nacisk poprzeczny
            # ----------------------------------------------------------
            st.markdown("### Ograniczenie odkształceń przez nacisk poprzeczny – α₅")

            uwzgl_a5 = st.radio(
                "Czy uwzględnić wpływ nacisku poprzecznego (α₅)?",
                ["Nie", "Tak"],
                index=0,
                horizontal=True,
            )

            if uwzgl_a5 == "Tak":
                st.markdown(
                    "Nacisk poprzeczny p [MPa] wzdłuż l<sub>bd</sub> "
                    "w stanie granicznym nośności",
                    unsafe_allow_html=True,
                )
                p = st.number_input(
                    "",
                    min_value=0.0,
                    value=8.0,
                    step=0.1,
                )
                alfa5 = max(0.7, min(1.0, 1.0 - 0.04 * p))
            else:
                alfa5 = 1.0

        # ======================================================================
        # α₆ — procent prętów łączonych
        # ======================================================================
        st.markdown("### Procent prętów łączonych w przekroju – α₆")

        with st.expander("Współczynnik α₆ (rysunek)"):
            rys6 = SCIEZKA_DODATKI / "DlugoscZakladu_alfa6.png"
            if rys6.exists():
                st.image(rys6, use_container_width=True)
            else:
                st.info("Brak pliku rysunku: DlugoscZakladu_alfa6.png")

        procent_lacz = st.selectbox("ρ₁ [%]", [100, 50, 33, 25], index=2)

        mapa_alfa6 = {100: 1.50, 50: 1.4, 33: 1.15, 25: 1.00}
        alfa6 = mapa_alfa6.get(procent_lacz, 1.0)

        # ======================================================================
        # Podsumowanie współczynników α
        # ======================================================================
        with st.expander("Podsumowanie współczynników α"):
            st.markdown(
                f"""
            - α₁ = {alfa1:.3f}  
            - α₂ = {alfa2:.3f}  
            - α₃ = {alfa3:.3f}  
            - α₄ = {alfa4:.3f}  
            - α₅ = {alfa5:.3f}  
            - α₆ = {alfa6:.3f} *(ρ₁ = {procent_lacz}%)*  
            """
            )
            alfa_sum = alfa1 * alfa2 * alfa3 * alfa4 * alfa5 * alfa6
            st.markdown(f"**Iloczyn α = {alfa_sum:.3f}**")

        st.markdown("---")

        # ======================================================================
        # PRZYCISK LICZENIA
        # ======================================================================
        if st.button("OBLICZ DŁUGOŚĆ ZAKŁADU"):
            wynik = ObliczDlugoscZakladu(
                fi_mm=fi_mm,
                klasa_betonu=klasa_betonu,
                fyk_MPa=float(fyk_MPa),
                procent_naprezenia=float(naprezenia_stali),
                eta1=eta1,
                wsp_cd=wsp_cd,
                alfa1=alfa1,
                alfa2=alfa2,
                alfa3=alfa3,
                alfa4=alfa4,
                alfa5=alfa5,
                alfa6=alfa6,
            )

            l_b_rqd_mm = wynik.get("l_b_rqd_mm")
            L0_mm = wynik.get("L0_mm")
            L0_min_mm = wynik.get("L0_min_mm")
            L_z_mm = wynik.get("L_z_mm")  # traktujemy jako l0,req

            # Wymagana długość zakładu – wynik główny (l0,req)
            if L_z_mm is not None:
                st.markdown(
                    f"""
                    <h3 style="margin-top:0.2rem; margin-bottom:0.2rem;">
                    Wymagana długość zakładu:
                    <span style="color:#00FF00">
                    l<sub>0,req</sub> = {L_z_mm:.1f} mm
                    </span>
                    </h3>
                    """,
                    unsafe_allow_html=True,
                )

            # ----------------- Szczegóły obliczeń ----------------------
            with st.expander("Szczegóły obliczeń"):
                fi_val = wynik.get("fi_mm")
                eta1_val = wynik.get("eta1")
                alfa_val = wynik.get("alfa")
                sigma_sd = wynik.get("sigma_sd_MPa")
                f_bd = wynik.get("f_bd_MPa")

                def f1(x: float) -> float:
                    return float(x) if isinstance(x, (int, float)) else float("nan")

                st.markdown("### Główne wielkości pośrednie")

                # ------------------------------------------------------
                # l_b,rqd
                # ------------------------------------------------------
                if l_b_rqd_mm is not None:
                    st.markdown("**Podstawowa długość zakotwienia [mm]:**")

                    st.latex(
                        r"l_{b,rqd} = \frac{\varphi}{4}\cdot"
                        r"\frac{\sigma_{sd}}{\eta_{1}\,f_{bd}}"
                    )

                    if (
                        fi_val is not None
                        and sigma_sd is not None
                        and eta1_val is not None
                        and f_bd is not None
                    ):
                        st.latex(
                            rf"l_{{b,rqd}} = \frac{{{fi_val:.1f}}}{{4}}"
                            rf"\cdot\frac{{{sigma_sd:.1f}}}{{{eta1_val:.3f}"
                            rf"\cdot {f_bd:.3f}}}"
                        )
                        st.latex(
                            rf"l_{{b,rqd}} = {l_b_rqd_mm:.1f}\ \text{{mm}}"
                        )

                st.markdown("---")

                # ------------------------------------------------------
                # l0
                # ------------------------------------------------------
                if (
                    L0_mm is not None
                    and l_b_rqd_mm is not None
                    and alfa_val is not None
                ):
                    st.markdown("**Obliczeniowa długość zakładu l₀ [mm]:**")
                    st.latex(r"l_{0} = \alpha \cdot l_{b,rqd}")
                    st.latex(
                        rf"l_0 = {alfa_val:.3f}\cdot {l_b_rqd_mm:.1f}"
                    )
                    st.latex(rf"l_0 = {L0_mm:.1f}\ \text{{mm}}")

                st.markdown("---")

                # ------------------------------------------------------
                # l0,min
                # ------------------------------------------------------
                if (
                    L0_min_mm is not None
                    and l_b_rqd_mm is not None
                    and fi_val is not None
                ):
                    st.markdown("**Minimalna długość zakładu l₀,min [mm]:**")

                    st.latex(
                        r"l_{0,\min} = \max\left(0.3\,l_{b,rqd},\,"
                        r"10\,\varphi,\,100\,\text{mm}\right)"
                    )

                    c1 = 0.3 * f1(l_b_rqd_mm)
                    c2 = 10.0 * f1(fi_val)
                    c3 = 100.0

                    st.latex(
                        rf"l_{{0,\min}} = \max\left("
                        rf"0.3\cdot {l_b_rqd_mm:.1f};\ "
                        rf"10\cdot {fi_val:.1f};\ 100.0\right)"
                    )
                    st.latex(
                        rf"l_{{0,\min}} = \max\left("
                        rf"{c1:.1f};\ {c2:.1f};\ {c3:.1f}\right)"
                    )
                    st.latex(
                        rf"l_{{0,\min}} = {L0_min_mm:.1f}\ \text{{mm}}"
                    )

                st.markdown("---")

                # ------------------------------------------------------
                # l0,req
                # ------------------------------------------------------
                if (
                    L_z_mm is not None
                    and L0_mm is not None
                    and L0_min_mm is not None
                ):
                    st.markdown("**Wymagana długość zakładu l₀,req [mm]:**")

                    st.latex(
                        r"l_{0,req} = \max\left(l_{0},\ l_{0,\min}\right)"
                    )
                    st.latex(
                        rf"l_{{0,req}} = \max\left({L0_mm:.1f};\ {L0_min_mm:.1f}\right)"
                    )
                    st.latex(
                        rf"l_{{0,req}} = {L_z_mm:.1f}\ \text{{mm}}"
                    )

                st.markdown("---")

                # ------------------------------------------------------
                # Parametry materiałowe i współczynniki
                # ------------------------------------------------------
                st.markdown("### Parametry materiałowe i współczynniki")

                if eta1_val is not None:
                    st.markdown(
                        f"- Współczynnik przyczepności η<sub>1</sub> [-]: "
                        f"{eta1_val:.3f}",
                        unsafe_allow_html=True,
                    )
                if fi_val is not None:
                    st.markdown(
                        f"- Średnica pręta φ [mm]: {fi_val:.1f} mm",
                    )
                if fyk_MPa is not None:
                    st.markdown(
                        f"- Granica plastyczności stali f<sub>yk</sub> [MPa]: "
                        f"{fyk_MPa:.1f} MPa",
                        unsafe_allow_html=True,
                    )
                if klasa_betonu is not None:
                    st.markdown(f"- Klasa betonu: {klasa_betonu}")
                if alfa_val is not None:
                    st.markdown(
                        f"- Iloczyn współczynników α<sub>1</sub>–α<sub>6</sub>: "
                        f"{alfa_val:.3f}",
                        unsafe_allow_html=True,
                    )
                if sigma_sd is not None:
                    st.markdown(
                        f"- Naprężenie w stali σ<sub>sd</sub> [MPa]: "
                        f"{sigma_sd:.1f} MPa",
                        unsafe_allow_html=True,
                    )
                if f_bd is not None:
                    st.markdown(
                        f"- Projektowa przyczepność betonu f<sub>bd</sub> [MPa]: "
                        f"{f_bd:.3f} MPa",
                        unsafe_allow_html=True,
                    )

    # ======================================================================
    # DOLNE UWAGI / ZAŁOŻENIA – na samym dole, rozwijane
    # ======================================================================
    st.markdown("---")
    with st.expander("Uwagi / założenia obliczeń"):
        st.markdown(
            """
            - Obliczenia dotyczą zakładu **prostych prętów żebrowanych**
              wg PN-EN 1992-1-1 (EC2).  
            - Współczynniki α₁–α₅ zostały dobrane dla **prętów prostych**
              (bez haków, prostowań i dodatkowych zagięć).
            """
        )


# Pozwala uruchomić stronę bezpośrednio: python DlugoscZakladu.py
if __name__ == "__main__":
    StronaDlugoscZakladu()
