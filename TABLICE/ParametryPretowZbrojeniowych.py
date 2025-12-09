# TABLICE/ParametryPretowZbrojeniowych.py

from __future__ import annotations
from dataclasses import dataclass
import math

@dataclass(frozen=True)
class ParametryPreta:
    """
    Zawiera podstawowe parametry pojedynczego pręta zbrojeniowego.
    - fi (φ) jest średnicą nominalną [mm].
    - As to pole przekroju [mm²].
    - masa_liniowa to ciężar na jednostkę długości [kg/m].
    """
    fi: int       # Średnica nominalna [mm]
    As: float     # Pole przekroju [mm²]
    masa_liniowa: float # Ciężar liniowy [kg/m]

# Gęstość stali (przyjęta 7850 kg/m³)
GESTOSC_STALI = 7850.0 # [kg/m³]

def oblicz_parametry(fi_mm: int) -> ParametryPreta:
    """Oblicza pole przekroju i masę liniową dla danej średnicy fi [mm]."""
    
    # Przeliczenie fi na metry
    fi_m = fi_mm / 1000.0 
    
    # 1. Pole przekroju As [mm²]
    As_mm2 = math.pi * (fi_mm / 2.0)**2
    
    # 2. Masa liniowa [kg/m]
    # Masa = Gęstość * Objętość (dla 1m długości: Objętość = Pole * 1m)
    # Pole przekroju w m²: As_m2 = math.pi * (fi_m / 2.0)**2
    # Masa liniowa [kg/m] = GESTOSC_STALI [kg/m³] * As_m2 [m²]
    As_m2 = math.pi * (fi_m / 2.0)**2
    masa_liniowa = GESTOSC_STALI * As_m2

    return ParametryPreta(
        fi=fi_mm,
        As=As_mm2,
        masa_liniowa=masa_liniowa
    )

# Tabela z parametrami dla standardowych średnic prętów (obliczone w kodzie)
PARAMETRY_PRETOW: dict[int, ParametryPreta] = {
    fi: oblicz_parametry(fi)
    for fi in [6, 8, 10, 12, 14, 16, 18, 20, 22, 25, 28, 32, 40]
}

def get_bar_params(fi_mm: int) -> ParametryPreta:
    """
    Zwraca obiekt ParametryPreta dla wybranej średnicy.
    """
    if fi_mm in PARAMETRY_PRETOW:
        return PARAMETRY_PRETOW[fi_mm]
    else:
        raise ValueError(f"Nieznana średnica pręta: {fi_mm} mm.")

def list_bar_diameters() -> list[int]:
    """
    Zwraca listę dostępnych średnic prętów.
    """
    return sorted(list(PARAMETRY_PRETOW.keys()))

if __name__ == '__main__':
    print("--- Parametry prętów zbrojeniowych (EC2) ---")
    for fi, params in PARAMETRY_PRETOW.items():
        print(f"φ{params.fi:02d} | As: {params.As:.2f} mm² | Masa: {params.masa_liniowa:.2f} kg/m")

    # Przykład użycia funkcji
    try:
        p18 = get_bar_params(18)
        print(f"\nParametry dla fi 18: As={p18.As:.2f} mm², Masa={p18.masa_liniowa:.2f} kg/m")
    except ValueError as e:
        print(e)