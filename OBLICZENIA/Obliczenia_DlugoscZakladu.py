# OBLICZENIA/Obliczenia_DlugoscZakladu.py

"""
Moduł obliczeniowy długości zakładu prętów zbrojeniowych
wg PN-EN 1992-1-1 (EC2).
"""

from __future__ import annotations
from dataclasses import dataclass
from TABLICE.ParametryBetonu import get_concrete_params

def _pobierz_parametry_betonu(klasa_betonu: str) -> dict:
    params = get_concrete_params(klasa_betonu)
    fctm = params.fctm
    fctk_005 = 0.7 * fctm
    gamma_c = 1.5
    alpha_ct = 1.0
    fctd = alpha_ct * fctk_005 / gamma_c
    return {
        "fctm": fctm,
        "fctk_005": fctk_005,
        "fctd": fctd,
    }


def ObliczDlugoscZakladu(
    fi_mm: float,
    klasa_betonu: str,
    fyk_MPa: float,
    procent_naprezenia: float,
    eta1: float,
    wsp_cd: float,
    alfa1: float,
    alfa2: float,
    alfa3: float,
    alfa4: float,
    alfa5: float,
    alfa6: float,
) -> dict:
    if fi_mm <= 0:
        raise ValueError("Średnica pręta musi być dodatnia.")
    if not (0 <= procent_naprezenia <= 100):
        raise ValueError("Procent wykorzystania naprężeń powinien być w zakresie 0–100 %.")

    # 1. Parametry materiałowe
    bet = _pobierz_parametry_betonu(klasa_betonu)
    fctd = bet["fctd"]
    gamma_s = 1.15
    f_yd = fyk_MPa / gamma_s
    sigma_sd = (procent_naprezenia / 100.0) * f_yd

    # 2. Podstawowa długość zakotwienia l_b,rqd
    if fi_mm <= 32:
        eta2 = 1.0
    else:
        eta2 = (132 - fi_mm) / 100.0
        
    f_bd = 2.25 * eta1 * eta2 * fctd
    
    if f_bd > 0:
        l_b_rqd_mm = (fi_mm / 4.0) * (sigma_sd / f_bd)
    else:
        l_b_rqd_mm = 0.0

    # 3. Współczynnik α (łączny) z limitem 0.7
    # Norma EC2 8.4.4(1): a2 * a3 * a5 >= 0.7
    iloczyn_235_raw = alfa2 * alfa3 * alfa5
    limit_active = False

    if iloczyn_235_raw < 0.7:
        iloczyn_235_eff = 0.7
        limit_active = True
    else:
        iloczyn_235_eff = iloczyn_235_raw

    # Alfa globalna = a1 * (a2*a3*a5)_eff * a4 * a6
    alfa = alfa1 * iloczyn_235_eff * alfa4 * alfa6

    # 4. Podstawowa długość zakładu L0 (EC2 8.7)
    L0_mm = alfa * l_b_rqd_mm

    # 5. Minimalna długość ZAKŁADU l0,min
    val1 = 0.3 * alfa6 * l_b_rqd_mm
    val2 = 15.0 * fi_mm
    val3 = 200.0
    
    L0_min_mm = max(val1, val2, val3)

    # Wymagana długość zakładu
    L_z_mm = max(L0_mm, L0_min_mm)

    return {
        "fi_mm": fi_mm,
        "klasa_betonu": klasa_betonu,
        "fyk_MPa": fyk_MPa,
        "procent_naprezenia": procent_naprezenia,
        "eta1": eta1,
        "eta2": eta2,
        "wsp_cd": wsp_cd,
        "alfa1": alfa1,
        "alfa2": alfa2,
        "alfa3": alfa3,
        "alfa4": alfa4,
        "alfa5": alfa5,
        "alfa6": alfa6,
        "alfa": alfa,
        "f_bd_MPa": f_bd,
        "sigma_sd_MPa": sigma_sd,
        "f_yd_MPa": f_yd,
        "fctd_MPa": fctd,
        "l_b_rqd_mm": l_b_rqd_mm,
        "L0_mm": L0_mm,
        "L0_min_mm": L0_min_mm,
        "L_z_mm": L_z_mm,
        # Dodatkowe do raportu
        "iloczyn_235_raw": iloczyn_235_raw,
        "iloczyn_235_eff": iloczyn_235_eff,
        "limit_active": limit_active
    }