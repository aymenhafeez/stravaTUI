from rich.text import Text

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


def create_overview_label(
    all_time_distance_km: float, all_time_elevation_gain: float
) -> Text:
    """Create a label for the overview page baesd on user's all time distance and elevation gain."""
    closest_distance = min(
        DISTANCES.items(), key=lambda x: abs(x[1] - all_time_distance_km)
    )[0]

    closest_elevation = min(
        ELEVATIONS.items(), key=lambda x: abs(x[1] - all_time_elevation_gain)
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
            ("You've ran around the distance of "),
            (f"{closest_distance} ", "#4ec9b0 bold italic"),
            ("this year, "),
            ("\nand climbed over the height of "),
            (f"{closest_elevation}", "#f0a16c bold italic"),
            ("!"),
        )
