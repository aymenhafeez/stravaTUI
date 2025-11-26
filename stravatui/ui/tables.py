from typing import TYPE_CHECKING

from rich.text import Text
from textual.widgets import DataTable

from ..activity_utils import (
    calculate_activity_totals,
    filter_valid_activities,
    float_convert,
)
from ..formatters import create_pace_list

if TYPE_CHECKING:
    from ..app import StravaTUIApp


def populate_activities_table(app: "StravaTUIApp", last_five_data: list[dict]) -> None:
    """Populate the activities table with last five activities data."""
    names = [d["names"] for d in last_five_data]
    times = [d["times"] for d in last_five_data]
    distances = [d["distances"] for d in last_five_data]

    paces = create_pace_list(times, distances)

    table_1 = app.query_one("#table-1", DataTable)
    table_1.add_columns("Activity", "Distance (km)", "Time (mins)", "Pace (min/km)")

    formatted_rows = []
    for name, distance, time, pace in zip(names, distances, times, paces):
        try:
            distance_km = round(float(distance) / 1000, 2)
            time_mins = round(float(time) / 60, 2)
            formatted_rows.append((name, f"{distance_km}", f"{time_mins}", f"{pace}"))
        except (ValueError, ZeroDivisionError):
            formatted_rows.append((name, "0.0", "0.0", "N/A"))

    table_1.add_rows(formatted_rows)


def populate_comparison_table(
    app: "StravaTUIApp",
    all_time_data: dict[str, str],
    ytd_data: dict[str, str],
    recent_data: dict[str, list[str]],
) -> None:
    """Populate comparison table with common stats across all three periods."""

    all_time_count = all_time_data["all_time_count"]
    all_time_distance = float_convert(all_time_data["all_time_distance"]) / 1000
    all_time_time = float_convert(all_time_data["all_time_moving_time"]) / 60
    all_time_elevation_gain = all_time_data["all_time_elevation_gain"]

    ytd_count = ytd_data["ytd_count"]
    ytd_distance = float_convert(ytd_data["ytd_distance"]) / 1000
    ytd_time = float_convert(ytd_data["ytd_moving_time"]) / 60
    ytd_elevation_gain = ytd_data["ytd_elevation_gain"]

    run_indices = filter_valid_activities(
        recent_data["activity_type"],
        recent_data["distances"],
        recent_data["times"],
        recent_data["total_elevation_gain"],
    )
    recent_count = str(len(run_indices))
    recent_distance, recent_time, recent_elevation = calculate_activity_totals(
        recent_data["distances"],
        recent_data["times"],
        recent_data["total_elevation_gain"],
        run_indices,
    )

    table_2 = app.query_one("#table-2", DataTable)

    # only show fields available for all three periods
    table_2.add_columns(
        "Period",
        "Activities",
        "Distance (km)",
        "Time (mins)",
        "Elevation (m)",
    )

    table_2.add_rows(
        [
            (
                "Last 60 Days",
                f"{recent_count}",
                f"{recent_distance:.2f}",
                f"{recent_time:.2f}",
                f"{str(recent_elevation)}",
            ),
            (
                "YTD",
                f"{ytd_count}",
                f"{ytd_distance:.2f}",
                f"{ytd_time:.2f}",
                f"{int(float(ytd_elevation_gain)):.0f}",
            ),
            (
                "All Time",
                f"{all_time_count}",
                f"{all_time_distance:.2f}",
                f"{all_time_time:.2f}",
                f"{int(float(all_time_elevation_gain)):.0f}",
            ),
        ]
    )


def populate_best_efforts_table(
    app: "StravaTUIApp", best_efforts_summary: list[dict]
) -> None:
    """Populate the best efforts table with aggregated best efforts data."""
    table_4 = app.query_one("#best-efforts-table", DataTable)

    # clear existing table
    table_4.clear()

    # add fixed columns
    table_4.add_columns("Distance", "Time (mins)", "Pace (min/km)", "Activity", "Date")

    for effort in best_efforts_summary:
        table_4.add_row(
            Text(effort["distance"], justify="center"),
            Text(effort["best_time"], justify="center"),
            Text(effort["pace"], justify="center"),
            effort["activity_name"],
            effort["date"],
        )
