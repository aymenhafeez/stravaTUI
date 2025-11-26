"""Helper functions for frequent data checks and filtering."""

from typing import Any

NULL_VALUES = (None, "None", "0", "")
VALID_RUN_TYPES = (
    "root='Run'",
    "root='VirtualRun'",
    "root='TrailRun'",
    "root='IndoorRun'",
)


def is_valid_value(value: Any, allow_zero: bool = False) -> bool:
    """Check if a value is valid."""
    if value in NULL_VALUES:
        return False

    if not allow_zero:
        try:
            return float(value) > 0
        except (ValueError, TypeError):
            return False

    return True


def is_valid_run_activity(
    activity_type: str,
    distance: str,
    time: str,
    elevation: str | None = None,
    heartrate: str | None = None,
) -> bool:
    """Check a given activity has all requried data."""
    if activity_type not in VALID_RUN_TYPES:
        return False

    if not is_valid_value(distance):
        return False
    if not is_valid_value(time):
        return False

    if elevation is not None and not is_valid_value(elevation):
        return False
    if heartrate is not None and not is_valid_value(heartrate):
        return False

    return True


def filter_valid_activities(
    activity_type: list[str],
    distances: list[str],
    times: list[str],
    elevation_gains: list[str],
    average_heartrates: list[str] | None = None,
) -> list[int]:
    """Get indices of valid activities."""
    valid_indices = []
    for i, (act_type, dist, time, elav) in enumerate(
        zip(activity_type, distances, times, elevation_gains)
    ):
        if not is_valid_run_activity(act_type, dist, time, elav):
            continue

        if average_heartrates is not None:
            hr = average_heartrates[i]
            if not is_valid_value(hr):
                continue

        valid_indices.append(i)

    return valid_indices


def filter_activities_with_heartrate(
    activity_type: list[str],
    distances: list[str],
    times: list[str],
    elevation_gains: list[str],
    average_heartrates: list[str],
    paces: list[str],
) -> list[int]:
    """Get indices of runs with valid heartrate data."""
    valid_indices = []

    for i, (act_type, dist, time, elev, hr, pace) in enumerate(
        zip(activity_type, distances, times, elevation_gains, average_heartrates, paces)
    ):
        if not is_valid_run_activity(act_type, dist, time, elev, hr):
            continue

        if pace in ("N/A", "0"):
            continue

        if dist == "0":
            continue

        valid_indices.append(i)

    return valid_indices


def extract_by_indices(data: list[str], indices: list[int]) -> list[str]:
    """Extract elements from list by valid indices."""
    return [data[i] for i in indices]


def float_convert(value: str, default: float = 0.0, scale_factor: float = 1.0) -> float:
    """Convert string to float."""
    if value in NULL_VALUES:
        return default

    try:
        return float(value) / scale_factor
    except (ValueError, ZeroDivisionError):
        return default


def calculate_activity_totals(
    distances: list[str], times: list[str], elevations: list[str], indices: list[int]
) -> tuple[float, float, float]:
    """Calculate total stat values."""
    total_distance_m = sum(float(distances[i]) for i in indices)
    total_time_s = sum(float(times[i]) for i in indices)
    total_elevation_m = sum(float(elevations[i]) for i in indices)

    return total_distance_m / 1000, total_time_s / 60, total_elevation_m
