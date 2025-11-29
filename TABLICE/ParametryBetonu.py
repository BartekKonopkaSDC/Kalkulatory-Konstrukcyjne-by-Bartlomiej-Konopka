# TABLICE/ParametryBetonu.py

from dataclasses import dataclass


@dataclass(frozen=True)
class ConcreteParams:
    """
    Podstawowe parametry betonu wg EC2 (wartości charakterystyczne).
    Wszystkie wartości w MPa (Ecm również w MPa – czyli GPa * 1000).
    """
    fck: float        # wytrzymałość charakterystyczna na ściskanie
    fcm: float        # wytrzymałość średnia na ściskanie
    fctm: float       # średnia wytrzymałość na rozciąganie
    fctk_0_05: float  # 5% kwantyl wytrzymałości na rozciąganie
    fctk_0_95: float  # 95% kwantyl wytrzymałości na rozciąganie
    Ecm: float        # moduł sprężystości


# Tabela – klasy normalnowytrzymałe wg EC2 (wartości lekko zaokrąglone)
# Jednostki: MPa, Ecm w MPa
CONCRETE_TABLE: dict[str, ConcreteParams] = {
    "C12/15": ConcreteParams(
        fck=12.0,
        fcm=20.0,
        fctm=1.6,
        fctk_0_05=1.1,
        fctk_0_95=2.0,
        Ecm=27_000.0,
    ),
    "C16/20": ConcreteParams(
        fck=16.0,
        fcm=24.0,
        fctm=1.9,
        fctk_0_05=1.3,
        fctk_0_95=2.5,
        Ecm=29_000.0,
    ),
    "C20/25": ConcreteParams(
        fck=20.0,
        fcm=28.0,
        fctm=2.2,
        fctk_0_05=1.5,
        fctk_0_95=2.9,
        Ecm=30_000.0,
    ),
    "C25/30": ConcreteParams(
        fck=25.0,
        fcm=33.0,
        fctm=2.6,
        fctk_0_05=1.8,
        fctk_0_95=3.5,
        Ecm=31_000.0,
    ),
    "C30/37": ConcreteParams(
        fck=30.0,
        fcm=38.0,
        fctm=2.9,
        fctk_0_05=2.0,
        fctk_0_95=3.8,
        Ecm=32_000.0,
    ),
    "C35/45": ConcreteParams(
        fck=35.0,
        fcm=43.0,
        fctm=3.2,
        fctk_0_05=2.2,
        fctk_0_95=4.2,
        Ecm=34_000.0,
    ),
    "C40/50": ConcreteParams(
        fck=40.0,
        fcm=48.0,
        fctm=3.5,
        fctk_0_05=2.5,
        fctk_0_95=4.6,
        Ecm=35_000.0,
    ),
    "C45/55": ConcreteParams(
        fck=45.0,
        fcm=53.0,
        fctm=3.8,
        fctk_0_05=2.7,
        fctk_0_95=4.9,
        Ecm=37_000.0,
    ),
    "C50/60": ConcreteParams(
        fck=50.0,
        fcm=58.0,
        fctm=4.1,
        fctk_0_05=2.9,
        fctk_0_95=5.3,
        Ecm=38_000.0,
    ),
    # Jak kiedyś będziesz chciał wyższe klasy – łatwo dopisać C55/67 ... C90/105.
}


def get_concrete_params(klasa_betonu: str) -> ConcreteParams:
    """
    Zwraca parametry betonu dla podanej klasy, np. "C20/25".

    Raises
    ------
    KeyError
        Jeśli klasa betonu nie jest zdefiniowana w tabeli.
    """
    try:
        return CONCRETE_TABLE[klasa_betonu]
    except KeyError as exc:
        raise KeyError(
            f"Nieznana klasa betonu: {klasa_betonu!r}. "
            f"Dostępne: {', '.join(CONCRETE_TABLE.keys())}"
        ) from exc


def list_concrete_classes() -> list[str]:
    """Zwraca listę dostępnych klas betonu (do selectboxów w UI)."""
    return list(CONCRETE_TABLE.keys())
