DISTANCES = {
    "London to Paris": 344,
    "Berlin to Prague": 280,
    "Dublin to Belfast": 142,
    "London to Edinburgh": 534,
    "Paris to Barcelona": 831,
    "Madrid to Lisbon": 503,
    "Rome to Venice": 394,
    "Amsterdam to Brussels": 174,
    "London to Berlin": 931,
    "Paris to Rome": 1106,
    "London to New York": 5570,
    "New York to Los Angeles": 3936,
    "New York to Chicago": 1144,
    "Los Angeles to Tokyo": 8815,
    "Tokyo to Seoul": 1158,
    "Beijing to Shanghai": 1068,
    "Singapore to Bangkok": 1432,
    "London to Dubai": 5471,
    "Sydney to Melbourne": 706,
    "Mumbai to Delhi": 1141,
}

ELEVATIONS = {
    "Mount Everest": 8849,
    "K2": 8611,
    "Kangchenjunga": 8586,
    "Lhotse": 8516,
    "Makalu": 8485,
    "Aconcagua": 6961,
    "Denali": 6190,
    "Kilimanjaro": 5895,
    "Mount Elbrus": 5642,
    "Chimborazo": 6267,
    "the Burj Khalifa": 829,
    "the Merdeka 118": 679,
    "the Shanghai Tower": 632,
    "the Abraj Al Bait Clock Tower": 601,
    "the One World Trade Center": 541,
    "the Taipei 101": 508,
    "the Empire State Building": 381,
    "the Eiffel Tower": 324,
    "the Statue of Liberty": 93,
    "Big Ben": 96,
}


def _format_pace(time_seconds: int | float, distance_meters: int | float) -> str:
    """Return a formatted pace string for a given time and distance."""
    if distance_meters == 0:
        return "N/A"

    pace_sec_per_meter = time_seconds / distance_meters
    pace_sec_per_km = pace_sec_per_meter * 1000
    pace_min_per_km = pace_sec_per_km / 60

    minutes = int(pace_min_per_km)
    seconds = int((pace_min_per_km - minutes) * 60)

    return f"{minutes}:{seconds:02d}"


def create_pace_list(time: list[str], distance: list[str]) -> list[str]:
    """Create a list of paces from a list of times and distances."""
    paces = []
    for time_str, distance_str in zip(time, distance):
        try:
            time_val = float(time_str)
            distance_val = float(distance_str)
            if distance_val == 0:
                pace = "N/A"
            else:
                pace = _format_pace(time_val, distance_val)
        except (ValueError, ZeroDivisionError):
            pace = "0"
        paces.append(pace)

    return paces


def pace_to_minutes(pace_str: str) -> float | None:
    """Return a pace string as minutes."""
    if pace_str == "N/A":
        return None

    min_str, sec_str = pace_str.split(":")
    return int(min_str) + int(sec_str) / 60.0
