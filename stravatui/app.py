from pathlib import Path

from rich.text import Text
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Center, Container, Horizontal, Vertical
from textual.widgets import (
    Button,
    ContentSwitcher,
    DataTable,
    Footer,
    Input,
    Label,
    LoadingIndicator,
    Select,
)
from textual_plotext import PlotextPlot

from .config import darktheme
from .data_manager import (
    _check_cache_modified_date,
    aggregate_best_efforts,
    all_time_run_stats,
    get_best_efforts,
    get_last_five_activities,
    get_recent_activities,
    ytd_run_stats,
)
from .race_calculator import get_race_predictions_formatted
from .ui.plot_setup import setup_plots
from .ui.tables import (
    populate_activities_table,
    populate_best_efforts_table,
    populate_comparison_table,
)
from .ui.text_labels import (
    about_page_bottom_text,
    about_page_text,
    best_efforts_label,
    create_overview_label,
    last_five_label,
)

PACKAGE_DIR = Path(__file__).parent
DATA_DIR = PACKAGE_DIR / "data"


class StravaTUIApp(App[None]):
    CSS_PATH = "app.tcss"

    BINDINGS = [
        Binding("1", "show_page('overview-page')", "overview", show=True),
        Binding("2", "show_page('last-five-page')", "data tables", show=True),
        Binding("3", "show_page('plot-page')", "calculator", show=True),
        Binding("4", "show_page('about-page')", "about", show=True),
        Binding("q", "quit", "quit", show=True),
    ]

    def compose(self) -> ComposeResult:
        """Compose the app layout."""
        with Center(id="loading-container"):
            yield LoadingIndicator(id="loading")

        with Container(id="main-content"):
            with Center():
                with Horizontal(id="buttons"):
                    yield Button("overview", id="overview-button", flat=True)
                    yield Button("recent", id="last-five-button", flat=True)
                    yield Button("calculator", id="plot-button", flat=True)
                    yield Button("about", id="about-button", flat=True)

            with ContentSwitcher(initial="overview-page", id="content-switcher"):
                with Container(id="overview-page"):
                    with Vertical(id="overview-left"):
                        # label with distance comparison text get's added in once API calls made in worker thread
                        yield Label("", id="overview-label")
                        with Center():
                            yield DataTable(id="table-2")
                        yield PlotextPlot(id="plot-3")
                    with Vertical(id="overview-right"):
                        yield PlotextPlot(id="plot-4")

                with Container(id="last-five-page"):
                    with Horizontal(id="last-five-horizontal"):
                        with Vertical(id="last-five-left"):
                            yield Label(last_five_label, id="table-1-label")
                            with Center():
                                yield DataTable(id="table-1", cell_padding=3)
                            yield PlotextPlot(id="last-five-subplot")
                        with Vertical(id="last-five-right"):
                            yield Label(
                                best_efforts_label,
                                id="efforts-plot-label",
                            )
                            with Center(id="label-with-efforts-table"):
                                yield DataTable(id="best-efforts-table", cell_padding=1)
                            yield PlotextPlot(id="effort-plot")
                            yield PlotextPlot(id="progression-plot")

                with Container(id="plot-page"):
                    with Vertical(id="calculator-container"):
                        yield Label(
                            "Race Time Calculator (Riegel's Formula)",
                            id="calculator-title",
                        )
                        yield Label(
                            "Enter a recent race result:", id="calculator-subtitle"
                        )

                        with Horizontal(id="calculator-inputs"):
                            yield Select(
                                [
                                    ("5K", "5k"),
                                    ("10K", "10k"),
                                    ("Half Marathon", "half"),
                                    ("Marathon", "marathon"),
                                ],
                                prompt="select distance",
                                id="race-distance-select",
                            )
                            yield Input(
                                placeholder="MM:SS or HH:MM:SS",
                                id="race-time-input",
                            )
                            yield Button(
                                "calculate",
                                id="calculate-button",
                                variant="primary",
                            )

                        with Center(classes="race-results-container"):
                            yield DataTable(id="race-results-table", cell_padding=10)

                with Container(id="about-page"):
                    yield Label(about_page_text, id="about-label")
                    yield Label(about_page_bottom_text, id="about-label-bottom")

            yield Footer(show_command_palette=False)

    def on_mount(self) -> None:
        self.register_theme(darktheme)
        self.theme = "darktheme"

        self.run_worker(self._load_data, exclusive=True, thread=True)

        # hide results table on mount
        self.query_one("#race-results-table", DataTable).display = False

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Mapp button presses to corresponding pages."""
        BUTTON_MAP = {
            "overview-button": "overview-page",
            "last-five-button": "last-five-page",
            "plot-button": "plot-page",
            "about-button": "about-page",
        }
        button_id = event.button.id

        if button_id == "calculate-button":
            self._calculate_race_times()
        elif button_id in BUTTON_MAP:
            self.query_one(ContentSwitcher).current = BUTTON_MAP[button_id]

    def action_show_page(self, page: str) -> None:
        """Show the selected page and hide others."""
        pages = ["overview-page", "last-five-page", "plot-page", "about-page"]
        for p in pages:
            self.query_one(f"#{p}").display = p == page

    def _calculate_race_times(self) -> None:
        """Calculate predicted race times using Riegel's formula."""
        distance_select = self.query_one("#race-distance-select", Select)
        time_input = self.query_one("#race-time-input", Input)
        results_table = self.query_one("#race-results-table", DataTable)

        # get selected distance
        if distance_select.value == Select.BLANK:
            return

        distance_key = str(distance_select.value)
        time_str = time_input.value.strip()

        if not time_str:
            return

        # get predictions using race_calculator module
        results = get_race_predictions_formatted(distance_key, time_str)
        if results is None:
            return

        # setup table if not already done
        if not results_table.columns:
            results_table.add_columns(
                Text("Distance", justify="center"),
                Text("Predicted Time", justify="center"),
            )

        # show table now that there are results
        results_table.display = True

        # clear and populate results
        results_table.clear()
        for distance_name, formatted_time in results:
            results_table.add_row(
                Text(distance_name, justify="center"),
                Text(formatted_time, justify="center"),
            )

    def _load_data(self) -> None:
        """Load and populate all data in background thread."""
        _check_cache_modified_date()
        recent_data = get_recent_activities()
        all_time_data = all_time_run_stats()
        ytd_run_data = ytd_run_stats()
        best_efforts_data = get_best_efforts()
        best_efforts_summary = aggregate_best_efforts(best_efforts_data)

        self.call_from_thread(
            self._populate_ui,
            recent_data,
            all_time_data,
            ytd_run_data,
            best_efforts_summary,
        )

    def _populate_ui(
        self,
        recent_data: dict[str, list[str]],
        all_time_data: dict[str, str],
        ytd_run_data: dict[str, str],
        aggregate_best_efforts: list[dict],
    ) -> None:
        """Populate all UI elements (must run on main thread)."""

        # update distance comparison label
        ytd_distance_km = float(ytd_run_data["ytd_distance"]) / 1000
        overview_label_widget = self.query_one("#overview-label", Label)
        overview_label_widget.update(
            create_overview_label(ytd_distance_km, recent_data)
        )

        populate_activities_table(
            self, get_last_five_activities(get_recent_activities())
        )
        setup_plots(
            self,
            recent_data,
            ytd_run_data,
            all_time_data,
            aggregate_best_efforts,
        )

        populate_comparison_table(self, all_time_data, ytd_run_data, recent_data)

        populate_best_efforts_table(
            self,
            aggregate_best_efforts,
        )

        self.query_one("#loading-container").display = False
        self.query_one("#main-content").display = True
