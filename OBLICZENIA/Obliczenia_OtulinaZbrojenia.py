def ObliczOtuline(klasa_eksploatacji: str, fi_mm: float) -> dict:
    """
    WERSJA PRZYKŁADOWA – BAZOWE c_min DLA KILKU KLAS EKSPLOATACJI.
    """

    bazowe = {
        "XC1": 20.0,
        "XC2": 25.0,
        "XC3": 30.0,
        "XC4": 35.0,
        "XD1": 35.0,
        "XS1": 40.0,
    }

    c_min = bazowe.get(klasa_eksploatacji, 25.0)

    return {
        "klasa_eksploatacji": klasa_eksploatacji,
        "fi_mm": fi_mm,
        "c_min_mm": c_min,
    }
