from rich.text import Text

from ..activity_utils import calculate_activity_totals, filter_valid_activities
from ..formatters import DISTANCES, ELEVATIONS

last_five_label = Text()
last_five_label.append("Here's a look at your ")
last_five_label.append("last five runs:", style="#FBB86C bold italic")

best_efforts_label = Text.assemble(
    ("Check out your "),
    ("recent best efforts. ", "#40D585 bold italic"),
    ("Keep crushing it!"),
    justify="center",
)

about_page_text = Text.assemble(
    ("Thanks for using "),
    ("stravaTUI", "#FBB86C bold"),
    ("\n\nFeel free to check out the project out on "),
    (" Github", "link https://github.com/aymenhafeez/stravaTUI/ #FFFFFF"),
    ("\nIf you run into any problems/bugs please open an issue or "),
    ("get in touch", "link mailto:aymennh@gmail.com #FFFFFF"),
    (" directly"),
)

about_page_bottom_text = Text.assemble(
    ("built by ", "dim"),
    ("@aymenhafeez", "link https://github.com/aymenhafeez/ #FFFFFF"),
)


def _get_recent_elevation_gain_sum(recent_data):
    distances = recent_data["distances"]
    times = recent_data["times"]
    total_elevation_gain = recent_data["total_elevation_gain"]
    activity_type = recent_data["activity_type"]

    run_indices = filter_valid_activities(
        activity_type, distances, times, total_elevation_gain
    )

    recent_distance, recent_time, recent_elevation_gain = calculate_activity_totals(
        distances, times, total_elevation_gain, run_indices
    )

    return recent_elevation_gain


def create_overview_label(
    all_time_distance_km: float, recent_data: dict[str, list[str]]
) -> Text:
    """
    Create a label for the overview page based on user's all time distance and
    recent elevation gain.
    """
    recent_elevation_gain = _get_recent_elevation_gain_sum(recent_data)

    closest_distance = min(
        DISTANCES.items(), key=lambda x: abs(x[1] - all_time_distance_km)
    )[0]

    closest_elevation = min(
        ELEVATIONS.items(), key=lambda x: abs(x[1] - recent_elevation_gain)
    )[0]

    if all_time_distance_km == 0:
        return Text.assemble(
            ("Here's an overview of some of your "),
            ("running stats", "#4ec9b0 bold italic"),
            ("!"),
        )
    else:
        return Text.assemble(
            ("Here's an overview of some of your running stats.\n"),
            ("You've ran around to the distance of "),
            (f"{closest_distance} ", "#4ec9b0 bold italic"),
            ("during you Strava history, "),
            ("\nand climbed close the height of "),
            (f"{closest_elevation} ", "#f0a16c bold italic"),
            ("over the last 60 days!"),
        )
