from ..activity_utils import (
    calculate_activity_totals,
    extract_by_indices,
    filter_activities_with_heartrate,
    filter_valid_activities,
    float_convert,
)
from ..formatters import create_pace_list, pace_to_minutes


def prepare_overview_data(
    names: list[str],
    distances: list[str],
    times: list[str],
    average_heartrate: list[str],
    total_elevation_gain: list[str],
    activity_type: list[str],
) -> dict[str, list]:
    """Filter data for overview page subplot."""
    paces = create_pace_list(times, distances)

    valid_indices = filter_activities_with_heartrate(
        activity_type, distances, times, total_elevation_gain, average_heartrate, paces
    )

    # create filtered lists using valid indices
    filtered_average_heartrate = extract_by_indices(average_heartrate, valid_indices)
    filtered_total_elevation_gain = extract_by_indices(
        total_elevation_gain, valid_indices
    )
    filtered_pace = extract_by_indices(paces, valid_indices)
    filtered_distance = extract_by_indices(distances, valid_indices)
    filtered_names = extract_by_indices(names, valid_indices)
    filtered_times = extract_by_indices(times, valid_indices)
    pace_mins = [pace_to_minutes(pace) for pace in filtered_pace]

    # convert all data for other plots
    filtered_average_heartrate_float = [float(hr) for hr in filtered_average_heartrate]
    filtered_total_elevation_gain_float = [
        float(eg) for eg in filtered_total_elevation_gain
    ]
    filtered_distances_float = [float(d) / 1000 for d in filtered_distance]
    filtered_times_float = [float(t) / 60 for t in filtered_times]

    return {
        "names": filtered_names,
        "distances": filtered_distances_float,
        "times": filtered_times_float,
        "average_heartrate": filtered_average_heartrate_float,
        "total_elevation_gain": filtered_total_elevation_gain_float,
        "pace_mins": pace_mins,
    }


def prepare_comparison_data(
    activity_type: list[str],
    distances: list[str],
    times: list[str],
    total_elevation_gain: list[str],
    ytd_stats: dict,
    all_time_stats: dict,
) -> dict[str, list[str] | list[float]]:
    """Prepare all time and YTD data for overview page data comparison plot."""

    ytd_distance = ytd_stats["ytd_distance"]
    ytd_elapsed_time = ytd_stats["ytd_elapsed_time"]
    ytd_elevation_gain = ytd_stats["ytd_elevation_gain"]

    ytd_distance_km = float_convert(ytd_distance) / 1000
    ytd_time_mins = float_convert(ytd_elapsed_time) / 60
    ytd_elevation = float_convert(ytd_elevation_gain)

    all_time_distance = all_time_stats["all_time_distance"]
    all_time_elapsed_time = all_time_stats["all_time_elapsed_time"]
    all_time_elevation_gain = all_time_stats["all_time_elevation_gain"]

    all_time_distance_km = float_convert(all_time_distance) / 1000
    all_time_time_mins = float_convert(all_time_elapsed_time) / 60
    all_time_elevation = float_convert(all_time_elevation_gain)

    run_indices = filter_valid_activities(
        activity_type, distances, times, total_elevation_gain
    )

    # calculate recent totals using run_indices
    recent_distance, recent_time, recent_elevation = calculate_activity_totals(
        distances, times, total_elevation_gain, run_indices
    )

    return {
        "periods": ["Recent", "YTD", "All Time"],
        "total_distances": [recent_distance, ytd_distance_km, all_time_distance_km],
        "total_times": [recent_time, ytd_time_mins, all_time_time_mins],
        "total_elevation_gains": [recent_elevation, ytd_elevation, all_time_elevation],
    }


def prepare_best_efforts_data(
    best_efforts: list[dict],
) -> dict[str, list[float] | list[str]]:
    """Prepare data for plot showing best efforts data."""
    best_distances = [float(effort["distance"]) for effort in best_efforts]
    best_distance_m = [float(effort["distance_m"]) for effort in best_efforts]
    best_paces = [effort["pace"] for effort in best_efforts]
    best_times = [effort["time_seconds"] for effort in best_efforts]

    pace_values = [
        float(effort["pace"].split(":")[0]) + float(effort["pace"].split(":")[1]) / 60
        for effort in best_efforts
    ]

    rounded_pace = [round(pace, 2) for pace in pace_values]
    time_mins = [time / 60 for time in best_times]

    best_distance_km = [distance / 1000 for distance in best_distance_m]

    return {
        "distances": best_distances,
        "distance_km": best_distance_km,
        "pace": best_paces,
        "pace_values": rounded_pace,
        "times": time_mins,
    }
