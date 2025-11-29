# TABLICE/ParametryStali.py

from dataclasses import dataclass


@dataclass(frozen=True)
class SteelParams:
    """
    Podstawowe parametry stali zbrojeniowej.
    Na razie wykorzystujemy tylko fyk, ale parametry są gotowe na przyszłość.
    """
    grade: str   # np. "B500B"
    fyk: float   # granica plastyczności [MPa]
    Es: float    # moduł sprężystości [MPa]
    ftk: float | None = None  # wytrzymałość na rozciąganie (opcjonalnie)


STEEL_TABLE: dict[str, SteelParams] = {
    "B500": SteelParams(
        grade="B500",
        fyk=500.0,
        Es=200_000.0,
        ftk=None,
    ),
    "B600": SteelParams(
        grade="B600",
        fyk=600.0,
        Es=200_000.0,
        ftk=None,
    ),
    "B700": SteelParams(
        grade="B700",
        fyk=700.0,
        Es=200_000.0,
        ftk=None,
    ),
    # Jak będziesz chciał inne gatunki – po prostu dopisz kolejne wpisy.
}


def get_steel_params(grade: str) -> SteelParams:
    """
    Zwraca parametry stali dla danego gatunku, np. "B500".
    """
    try:
        return STEEL_TABLE[grade]
    except KeyError as exc:
        raise KeyError(
            f"Nieznany gatunek stali: {grade!r}. "
            f"Dostępne: {', '.join(STEEL_TABLE.keys())}"
        ) from exc


def list_steel_grades() -> list[str]:
    """Lista dostępnych gatunków stali (do selectboxów w UI)."""
    return list(STEEL_TABLE.keys())
