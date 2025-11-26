from typing import TYPE_CHECKING, Any

from textual_plotext import PlotextPlot

if TYPE_CHECKING:
    from ..app import StravaTUIApp

from .plot_data import (
    prepare_best_efforts_data,
    prepare_comparison_data,
    prepare_overview_data,
)


def setup_overview_plots(
    app: "StravaTUIApp", overview_data: dict[str, list[Any]]
) -> None:
    """Setup subplot for overview page."""
    overview_subplot = app.query_one("#plot-3", PlotextPlot).plt
    overview_subplot.subplots(2, 2)

    overview_subplot.subplot(1, 1).scatter(
        overview_data["average_heartrate"],
        overview_data["total_elevation_gain"],
        marker="braille",
        color="green",
    )
    overview_subplot.subplot(1, 1).xlabel("Avg HR (bpm)")
    overview_subplot.subplot(1, 1).title("Avg HR (bpm) vs Elevation (m)")

    overview_subplot.subplot(1, 2).scatter(
        overview_data["distances"],
        overview_data["times"],
        marker="braille",
        color="orange",
    )
    overview_subplot.subplot(1, 2).xlabel("Distance (km)")
    overview_subplot.subplot(1, 2).title("Distance (km) vs Time (min)")

    overview_subplot.subplot(2, 1).scatter(
        overview_data["pace_mins"],
        overview_data["average_heartrate"],
        marker="braille",
        color="red",
    )
    overview_subplot.subplot(2, 1).xlabel("Avg pace(min/km)")
    overview_subplot.subplot(2, 1).title("Pace vs Avg HR (bpm)")

    overview_subplot.subplot(2, 2).scatter(
        overview_data["pace_mins"],
        overview_data["total_elevation_gain"],
        marker="braille",
        color="cyan",
    )
    overview_subplot.subplot(2, 2).xlabel("Avg pace (min/km)")
    overview_subplot.subplot(2, 2).title("Pace (min/km) vs Elevation (m)")

    app.query_one("#plot-3", PlotextPlot).refresh()


def setup_comparison_plots(
    app: "StravaTUIApp", comparison_data: dict[str, list[str] | list[float]]
) -> None:
    """Setup comparison subplot for overview page."""
    distance_comparison_bar = app.query_one("#plot-4", PlotextPlot).plt
    distance_comparison_bar.subplots(3, 1)

    distance_comparison_bar.subplot(1, 1).bar(
        comparison_data["periods"],
        comparison_data["total_distances"],
        orientation="horizontal",
        width=2 / 5,
        color="cyan",
    )
    distance_comparison_bar.subplot(1, 1).xlabel("Distance (km)")

    distance_comparison_bar.subplot(2, 1).bar(
        comparison_data["periods"],
        comparison_data["total_times"],
        orientation="horizontal",
        width=2 / 5,
    )
    distance_comparison_bar.subplot(2, 1).xlabel("Time (mins)")

    distance_comparison_bar.subplot(3, 1).bar(
        comparison_data["periods"],
        comparison_data["total_elevation_gains"],
        orientation="horizontal",
        width=2 / 5,
        color="orange",
    )
    distance_comparison_bar.subplot(3, 1).xlabel("Elevation gain (m)")

    app.query_one("#plot-4", PlotextPlot).refresh()


def setup_recent_plots(
    app: "StravaTUIApp", overview_data: dict[str, list[Any]]
) -> None:
    """Setup subplot with recent activities data."""
    recent_subplot = app.query_one("#last-five-subplot", PlotextPlot).plt
    recent_subplot.subplots(2, 2)

    recent_subplot.subplot(1, 1).bar(
        overview_data["names"][:5],
        overview_data["average_heartrate"][:5],
        orientation="horizontal",
        width=1 / 7,
        color="#DCD37C",
    )
    recent_subplot.subplot(1, 1).xlabel("Average heartrate")

    recent_subplot.subplot(1, 2).bar(
        overview_data["names"][:5],
        overview_data["distances"][:5],
        orientation="horizontal",
        width=1 / 5,
        color="orange",
    )
    recent_subplot.subplot(1, 2).xlabel("Distance (km)")

    recent_subplot.subplot(2, 1).bar(
        overview_data["names"][:5],
        overview_data["times"][:5],
        orientation="horizontal",
        width=1 / 5,
        color="red",
    )
    recent_subplot.subplot(2, 1).xlabel("Time (min)")

    recent_subplot.subplot(2, 2).bar(
        overview_data["names"][:5],
        overview_data["total_elevation_gain"][:5],
        orientation="horizontal",
        width=1 / 5,
        color="cyan",
    )
    recent_subplot.subplot(2, 2).xlabel("Total elevation gain (m)")

    app.query_one("#last-five-subplot", PlotextPlot).refresh()


def setup_best_efforts_plot(
    app: "StravaTUIApp", effort: dict[str, list[float] | list[str]]
) -> None:
    """Setup best effors time comparison plot."""
    efforts_plot = app.query_one("#effort-plot", PlotextPlot).plt
    efforts_plot.bar(
        effort["distance_km"],
        effort["times"],
        width=1,
        orientation="horizontal",
    )
    efforts_plot.yreverse(reverse=True)
    efforts_plot.xlabel("Time (mins)")
    efforts_plot.title("Best effort distance (km) vs Time (mins)")
    app.query_one("#effort-plot", PlotextPlot).refresh()


def setup_progression_plot(
    app: "StravaTUIApp", effort_data: dict[str, list[float] | list[str]]
) -> None:
    """Setup distance against pace progression plot."""
    # only use filly if there's data to plot
    has_data = len(effort_data["distance_km"]) > 0

    progression_plot = app.query_one("#progression-plot", PlotextPlot).plt
    progression_plot.plot(
        effort_data["distance_km"],
        effort_data["pace_values"],
        marker="fhd",
        color="orange",
        filly=has_data,
    )
    progression_plot.xlabel("Distance (km)")
    progression_plot.title("Change of pace (min/km) across best effort distances")
    app.query_one("#progression-plot", PlotextPlot).refresh()


def setup_plots(
    app,
    recent_data: dict,
    ytd_stats: dict,
    all_time_stats: dict,
    effort_data: list[dict],
) -> None:
    """Pass prepared data to plot widgets."""
    effort = prepare_best_efforts_data(effort_data)

    overview_data = prepare_overview_data(
        recent_data["names"],
        recent_data["distances"],
        recent_data["times"],
        recent_data["average_heartrate"],
        recent_data["total_elevation_gain"],
        recent_data["activity_type"],
    )
    comparison_data = prepare_comparison_data(
        recent_data["activity_type"],
        recent_data["distances"],
        recent_data["times"],
        recent_data["total_elevation_gain"],
        ytd_stats,
        all_time_stats,
    )

    setup_overview_plots(app, overview_data)

    setup_comparison_plots(app, comparison_data)

    setup_recent_plots(app, overview_data)

    setup_best_efforts_plot(app, effort)

    setup_progression_plot(app, effort)
