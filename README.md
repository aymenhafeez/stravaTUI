# stravaTUI

<!-- TODO: insert screenshots here -->
**WIP**

A TUI for viewing Strava run stats with a built-in race time prediction
calculator

## Requirements

* Python >= 3.10
* textual (latest)
* textual-plotext (latest)
* rich (latest)
* stravalib (latest)

## Usage

### Strava OAUTH

The Strava data fetching is done using the [Strava V3
API](https://developers.strava.com/) and requires OAUTH authorisation in order
to get an access token. To do this you first need to make a Strava application.
The steps to do so can be found
[here](https://developers.strava.com/docs/getting-started/#account). Once you've
made a Strava application you'll gain access to your Client ID and Client
Secret. Next, you can clone the repo and make a copy of the `.env` file:

```bash
git clone https://github.com/aymenhafeez/stravaTUI
cd stravaTUI
cp .env.example .env
```

Enter your Client ID and Client Secret into the `.env` file. Once you run the
authentication script, it will read these in order to generate an access token
and store the output in `strava_token.json`, which the app will read from to
pull your Strava stats. To authenticate:

```bash
pip install -r requirements.txt
make run
```

and go to the [authorisation link](http://127.0.0.1:5042/authorize). You'll be
prompted to login to Strava and allow authorisation access. Once you click
authorise you'll see a `json` output. This will save to `strava_token.json`, so
you can close the link and the authorisation script.

Onece you've authorised, you can run the app:

```bash
python main.py
```

<!-- ## Development -->
<!---->
<!-- ### Setup and running the app -->
<!---->
<!-- ```bash -->
<!-- git clone https://github.com/aymenhafeez/stravaTUI -->
<!-- cd stravaTUI -->
<!-- # Create virtual environment -->
<!-- python -m venv venv -->
<!-- source venv/bin/activate -->
<!-- pip install -r requirements.txt -->
<!-- ``` -->
<!---->
<!-- Running and type checking -->
<!---->
<!-- ```bash -->
<!-- python main.py -->
<!---->
<!-- mypy stravatui/ -->
<!-- ``` -->
<!---->
<!-- ### Project structure -->
<!---->
<!-- ```bash -->
<!--  stravatui/ -->
<!--  ├── main.py                 # Entry point -->
<!--  ├── stravatui/ -->
<!--  │   ├── app.py              # TUI ui and data loading -->
<!--  │   ├── data_manager.py     # Strava API data fetching -->
<!--  │   ├── race_calculator.py  # Race time prediction calculator -->
<!--  │   ├── activity_utils.py   # Data processing helpers -->
<!--  │   ├── formatters.py       # Data formatting helpers -->
<!--  │   ├── config.py           # Theme and configuration -->
<!--  │   ├── ui/ -->
<!--  │   │   ├── tables.py       # Data tables -->
<!--  │   │   ├── plot_setup.py   # Plot setup and config -->
<!--  │   │   ├── plot_data.py    # Plot data processing -->
<!--  │   │   └── text_labels.py  # Static text content -->
<!--  │   └── data/               # Cached JSON data -->
<!--  └── stravatui/app.tcss      # Styling -->
<!-- ``` -->
<!---->
<!-- ### Data caching -->
<!---->
<!-- The data pulled from Strava is cached in `stravatui/data` to reduce continuous -->
<!-- API calls every time the app gets run: -->
<!---->
<!-- ```bash -->
<!-- activities.json    # activity data from the last 60 days -->
<!-- all_time_run.json  # all time run stats -->
<!-- ytd_run.json       # year-to-date run stats -->
<!-- best_efforts.json  # best effort data from the last 5 runs -->
<!-- ``` -->

## License 

MIT License
