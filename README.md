# stravaTUI

**WIP**



A TUI for viewing Strava run stats with a built-in race time prediction
calculator

<center>
  <figure> 
    <img src="https://raw.githubusercontent.com/aymenhafeez/stravaTUI/refs/heads/master/media/recent.png" width="600" /> 
  </figure>
</center>

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
