"""Race time prediction using Riegel's formula."""

# Distance mappings in meters
RACE_DISTANCES = {
    "5k": 5000,
    "10k": 10000,
    "half": 21097.5,
    "marathon": 42195,
}


def _parse_time_input(time_str: str) -> int | None:
    """
    Parse time input string into total seconds.

    Args:
        time_str: Time in format MM:SS or HH:MM:SS

    Returns:
        Total seconds as int, or None if invalid format
    """
    time_str = time_str.strip()
    if not time_str:
        return None

    try:
        time_parts = time_str.split(":")
        if len(time_parts) == 2:  # MM:SS
            minutes, seconds = int(time_parts[0]), int(time_parts[1])
            return minutes * 60 + seconds
        elif len(time_parts) == 3:  # HH:MM:SS
            hours, minutes, seconds = (
                int(time_parts[0]),
                int(time_parts[1]),
                int(time_parts[2]),
            )
            return hours * 3600 + minutes * 60 + seconds
    except (ValueError, IndexError):
        return None

    return None


def _format_race_time(seconds: float) -> str:
    """
    Format seconds into race time string (HH:MM:SS or MM:SS).

    Args:
        seconds: Time in seconds

    Returns:
        Formatted time string
    """
    seconds = int(seconds)
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60

    if hours > 0:
        return f"{hours}:{minutes:02d}:{secs:02d}"
    else:
        return f"{minutes}:{secs:02d}"


def _predict_race_times(
    input_distance_key: str, input_time_seconds: int
) -> dict[str, float]:
    """
    Calculate predicted race times using Riegel's formula.

    Riegel's formula: T2 = T1 * (D2 / D1)^1.06
    Where:
        T1 = known time
        D1 = known distance
        T2 = predicted time
        D2 = target distance

    Args:
        input_distance_key: Key from RACE_DISTANCES ('5k', '10k', 'half', 'marathon')
        input_time_seconds: Known race time in seconds

    Returns:
        Dictionary mapping distance keys to predicted times in seconds
    """
    if input_distance_key not in RACE_DISTANCES:
        return {}

    input_distance = RACE_DISTANCES[input_distance_key]
    predictions = {}

    for distance_key, target_distance in RACE_DISTANCES.items():
        predicted_seconds = input_time_seconds * (
            (target_distance / input_distance) ** 1.06
        )
        predictions[distance_key] = predicted_seconds

    return predictions


def get_race_predictions_formatted(
    input_distance_key: str, input_time_str: str
) -> list[tuple[str, str]] | None:
    """
    Get formatted race predictions from input.

    Args:
        input_distance_key: Key from RACE_DISTANCES
        input_time_str: Time string in MM:SS or HH:MM:SS format

    Returns:
        List of (distance_name, formatted_time) tuples, or None if invalid input
    """
    input_seconds = _parse_time_input(input_time_str)
    if input_seconds is None:
        return None

    predictions = _predict_race_times(input_distance_key, input_seconds)
    if not predictions:
        return None

    # Format for display
    distance_names = {
        "5k": "5K",
        "10k": "10K",
        "half": "Half Marathon",
        "marathon": "Marathon",
    }

    results = []
    for key in ["5k", "10k", "half", "marathon"]:
        name = distance_names[key]
        time_formatted = _format_race_time(predictions[key])
        results.append((name, time_formatted))

    return results
