# OBLICZENIA/Obliczenia_DlugoscZakotwienia.py

"""
Moduł obliczeniowy długości zakotwienia prętów zbrojeniowych
wg PN-EN 1992-1-1 (EC2).
"""

from __future__ import annotations
from dataclasses import dataclass
from TABLICE.ParametryBetonu import get_concrete_params

@dataclass
class WynikZakotwienia:
    l_b_rqd_mm: float
    L_bd_mm: float
    L_b_min_mm: float
    L_req_mm: float
    alfa: float
    fi_mm: float
    klasa_betonu: str
    fyk_MPa: float
    procent_naprezenia: float
    eta1: float
    eta2: float
    alfa1: float
    alfa2: float
    alfa3: float
    alfa4: float
    alfa5: float
    f_bd_MPa: float
    sigma_sd_MPa: float
    f_yd_MPa: float
    fctd_MPa: float


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


def ObliczDlugoscZakotwienia(
    fi_mm: float,
    klasa_betonu: str,
    fyk_MPa: float,
    procent_naprezenia: float,
    eta1: float,
    alfa1: float,
    alfa2: float,
    alfa3: float,
    alfa4: float,
    alfa5: float,
) -> dict:
    if fi_mm <= 0:
        raise ValueError("Średnica pręta musi być dodatnia.")
    
    # 1. Parametry materiałowe
    bet = _pobierz_parametry_betonu(klasa_betonu)
    fctd = bet["fctd"]
    gamma_s = 1.15
    f_yd = fyk_MPa / gamma_s
    sigma_sd = (procent_naprezenia / 100.0) * f_yd

    # 2. Podstawowa długość zakotwienia l_b,rqd
    # ZMIANA: Obliczenie eta2
    if fi_mm <= 32:
        eta2 = 1.0
    else:
        eta2 = (132 - fi_mm) / 100.0

    # ZMIANA: Wzór na f_bd z eta2
    f_bd = 2.25 * eta1 * eta2 * fctd
    
    if f_bd > 0:
        l_b_rqd_mm = (fi_mm / 4.0) * (sigma_sd / f_bd)
    else:
        l_b_rqd_mm = 0.0

    # 3. Współczynnik alfa globalny
    alfa = alfa1 * alfa2 * alfa3 * alfa4 * alfa5

    # 4. Obliczeniowa długość zakotwienia l_bd
    L_bd_mm = alfa * l_b_rqd_mm

    # 5. Minimalna długość zakotwienia l_b,min
    val1 = 0.3 * l_b_rqd_mm
    val2 = 10.0 * fi_mm
    val3 = 100.0
    
    L_b_min_mm = max(val1, val2, val3)

    # Wynik końcowy
    L_req_mm = max(L_bd_mm, L_b_min_mm)

    return {
        "l_b_rqd_mm": l_b_rqd_mm,
        "L_bd_mm": L_bd_mm,
        "L_b_min_mm": L_b_min_mm,
        "L_req_mm": L_req_mm,
        "alfa": alfa,
        "fi_mm": fi_mm,
        "klasa_betonu": klasa_betonu,
        "fyk_MPa": fyk_MPa,
        "procent_naprezenia": procent_naprezenia,
        "eta1": eta1,
        "eta2": eta2, # Dodano
        "alfa1": alfa1,
        "alfa2": alfa2,
        "alfa3": alfa3,
        "alfa4": alfa4,
        "alfa5": alfa5,
        "f_bd_MPa": f_bd,
        "sigma_sd_MPa": sigma_sd,
        "f_yd_MPa": f_yd,
        "fctd_MPa": fctd,
    }