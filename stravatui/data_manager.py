import json
import os
from datetime import datetime, timedelta
from pathlib import Path

import stravalib.model as model

from .auth import _initialise_strava_client
from .formatters import _format_pace

NULL_VALUES = (None, "None", "0", "")
PACKAGE_DIR = Path(__file__).parent
DATA_DIR = PACKAGE_DIR / "data"


def _check_cache_modified_date(max_age: int = 24):
    """Remove cached files if they're older than max_age"""
    file_path = DATA_DIR / "activities.json"

    if not file_path.exists():
        return

    mod_date = os.path.getmtime(file_path)
    mod_date_dt = datetime.fromtimestamp(mod_date)
    age = datetime.now() - mod_date_dt

    if age > timedelta(hours=max_age):
        for cache_file in DATA_DIR.glob("*.json"):
            cache_file.unlink()


def all_time_run_stats() -> dict[str, str | int]:
    """
    Fetch and return a dictionary of all-time run stats. Data cached
    in DATA_DIR/all_time_run.json to avoid excessive API calls.
    """
    all_time_run_cache = DATA_DIR / "all_time_run.json"

    if all_time_run_cache.exists():
        with open(all_time_run_cache, "r") as f:
            all_time_run_data = json.load(f)

        all_time_ach_count = all_time_run_data["all_time_ach_count"]
        all_time_count = all_time_run_data["all_time_count"]
        all_time_distance = all_time_run_data["all_time_distance"]
        all_time_elapsed_time = all_time_run_data["all_time_elapsed_time"]
        all_time_elevation_gain = all_time_run_data["all_time_elevation_gain"]
        all_time_moving_time = all_time_run_data["all_time_moving_time"]

        return all_time_run_data
    else:
        client = _initialise_strava_client()

        if not client.access_token:
            return {}

        athlete_summary: model.SummaryAthlete = client.get_athlete()
        athlete_id = athlete_summary.id
        athlete_stats: model.AthleteStats = client.get_athlete_stats(athlete_id)
        all_run_stats = athlete_stats.all_run_totals

        if all_run_stats is None:
            all_time_ach_count = 0
            all_time_count = 0
            all_time_distance = 0
            all_time_elapsed_time = 0
            all_time_elevation_gain = 0
            all_time_moving_time = 0
        else:
            all_time_ach_count = str(all_run_stats.achievement_count)
            all_time_count = str(all_run_stats.count)
            all_time_distance = str(all_run_stats.distance)
            all_time_elapsed_time = str(all_run_stats.elapsed_time)
            all_time_elevation_gain = str(all_run_stats.elevation_gain)
            all_time_moving_time = str(all_run_stats.moving_time)

        all_time_run_data = {
            "all_time_ach_count": all_time_ach_count,
            "all_time_count": all_time_count,
            "all_time_distance": all_time_distance,
            "all_time_elapsed_time": all_time_elapsed_time,
            "all_time_elevation_gain": all_time_elevation_gain,
            "all_time_moving_time": all_time_moving_time,
        }

        with open(all_time_run_cache, "w") as f:
            json.dump(all_time_run_data, f)

        return all_time_run_data


def ytd_run_stats() -> dict[str, str | int]:
    """
    Fetch and return a dictionary of year-to-date run stas. Data cached
    in DATA_DIR/ytd_run.json to avoid excessive API calls.
    """
    ytd_run_cache = DATA_DIR / "ytd_run.json"

    if ytd_run_cache.exists():
        with open(ytd_run_cache, "r") as f:
            ytd_run_data = json.load(f)

        ytd_ach_count = ytd_run_data["ytd_ach_count"]
        ytd_count = ytd_run_data["ytd_count"]
        ytd_distance = ytd_run_data["ytd_distance"]
        ytd_elapsed_time = ytd_run_data["ytd_elapsed_time"]
        ytd_elevation_gain = ytd_run_data["ytd_elevation_gain"]
        ytd_moving_time = ytd_run_data["ytd_moving_time"]

        return ytd_run_data
    else:
        client = _initialise_strava_client()

        if not client.access_token:
            return {}

        athlete_summary: model.SummaryAthlete = client.get_athlete()
        athlete_id = athlete_summary.id
        athlete_stats: model.AthleteStats = client.get_athlete_stats(athlete_id)
        ytd_run_stats = athlete_stats.ytd_run_totals

        if ytd_run_stats is None:
            ytd_ach_count = 0
            ytd_count = 0
            ytd_distance = 0
            ytd_elapsed_time = 0
            ytd_elevation_gain = 0
            ytd_moving_time = 0
        else:
            ytd_ach_count = str(ytd_run_stats.achievement_count)
            ytd_count = str(ytd_run_stats.count)
            ytd_distance = str(ytd_run_stats.distance)
            ytd_elapsed_time = str(ytd_run_stats.elapsed_time)
            ytd_elevation_gain = str(ytd_run_stats.elevation_gain)
            ytd_moving_time = str(ytd_run_stats.moving_time)

        ytd_run_data = {
            "ytd_ach_count": ytd_ach_count,
            "ytd_count": ytd_count,
            "ytd_distance": ytd_distance,
            "ytd_elapsed_time": ytd_elapsed_time,
            "ytd_elevation_gain": ytd_elevation_gain,
            "ytd_moving_time": ytd_moving_time,
        }

        with open(ytd_run_cache, "w") as f:
            json.dump(ytd_run_data, f)

        return ytd_run_data


def get_recent_activities() -> dict[str, list[str]]:
    """
    Get detailed activity data for the last 60 days. Data cached
    in DATA_DIR/activities.json to avoid excessive API calls.
    """
    activities_cache = DATA_DIR / "activities.json"

    if activities_cache.exists():
        with open(activities_cache, "r") as f:
            activities_data = json.load(f)

        names = activities_data["names"]
        distances = activities_data["distances"]
        times = activities_data["times"]
        polylines = activities_data["polylines"]
        average_heartrate = activities_data["average_heartrate"]
        total_elevation_gain = activities_data["total_elevation_gain"]
        activity_type = activities_data["activity_type"]

        return activities_data

    else:
        client = _initialise_strava_client()

        if not client.access_token:
            return {
                "names": [],
                "distances": [],
                "times": [],
                "polylines": [],
                "average_heartrate": [],
                "total_elevation_gain": [],
                "activity_type": [],
            }

        one_month_ago = datetime.now() - timedelta(days=60)
        # 'after' returns activities in chronological order so reverse the list
        # to get newest first
        activities = list(reversed(list(client.get_activities(after=one_month_ago))))

        names = [str(act.name) for act in activities]
        distances = [str(act.distance) for act in activities]
        times = [str(act.moving_time) for act in activities]
        polylines = [
            str(act.map.summary_polyline) if act.map is not None else ""
            for act in activities
        ]
        average_heartrate = [str(act.average_heartrate) for act in activities]
        total_elevation_gain = [str(act.total_elevation_gain) for act in activities]
        activity_type = [str(act.type) for act in activities]
        activities_data = {
            "names": names,
            "distances": distances,
            "times": times,
            "polylines": polylines,
            "average_heartrate": average_heartrate,
            "total_elevation_gain": total_elevation_gain,
            "activity_type": activity_type,
        }

        with open(activities_cache, "w") as f:
            json.dump(activities_data, f)

        return activities_data


def get_last_five_activities(recent_data: dict[str, list[str]]) -> list[dict]:
    """Return the last five activities from the recent activity data."""
    return [
        {
            "names": recent_data["names"][i],
            "distances": recent_data["distances"][i],
            "times": recent_data["times"][i],
            "polylines": recent_data["polylines"][i],
            "average_heartrate": recent_data["average_heartrate"][i],
            "total_elevation_gain": recent_data["total_elevation_gain"][i],
            "activity_type": recent_data["activity_type"][i],
        }
        for i in range(min(5, len(recent_data["names"])))
    ]


def get_best_efforts() -> list[dict]:
    """
    Get best efforts data for the last five activities. Data cached
    in DATA_DIR/best_efforts.json to avoid excessive API calls.
    """
    best_efforts_cache = DATA_DIR / "best_efforts.json"

    if best_efforts_cache.exists():
        with open(best_efforts_cache, "r") as f:
            return json.load(f)

    client = _initialise_strava_client()
    if not client.access_token:
        return []

    activities = list(client.get_activities(limit=6))

    all_best_efforts = []

    for activity in activities:
        if not activity.id:
            continue

        detailed_activity = client.get_activity(activity.id)

        if detailed_activity.best_efforts and detailed_activity.start_date:
            activity_entry: dict[str, str | list[dict]] = {
                "activity_name": str(detailed_activity.name)
                if detailed_activity.name
                else "",
                "date": detailed_activity.start_date.strftime("%m/%d/%y"),
                "best_efforts": [],  # type: ignore
            }

            for effort in detailed_activity.best_efforts:
                if not effort.moving_time or not effort.distance:
                    continue

                time_seconds = int(effort.moving_time)
                distance_meters = float(effort.distance)

                # Format distance
                if distance_meters >= 1000:
                    distance_formatted = f"{distance_meters / 1000:.2f}"
                else:
                    distance_formatted = f"{distance_meters:.0f}"

                time_minutes = time_seconds // 60
                time_secs = time_seconds % 60
                time_formatted = f"{time_minutes}:{time_secs:02d}"

                pace = _format_pace(time_seconds, distance_meters)

                is_pr = effort.pr_rank == 1

                activity_entry["best_efforts"].append(  # type: ignore
                    {
                        "distance": distance_formatted,
                        "distance_m": distance_meters,
                        "time": time_formatted,
                        "time_seconds": time_seconds,
                        "pace": pace,
                        "is_pr": is_pr,
                    }
                )
            all_best_efforts.append(activity_entry)

    with open(best_efforts_cache, "w") as f:
        json.dump(all_best_efforts, f, indent=2)

    return all_best_efforts


def aggregate_best_efforts(best_efforts_data: list[dict]) -> list[dict]:
    """Sort and filter best efforts to get the fastest times for each distance."""
    best_by_distance: dict[str, dict] = {}

    for activity in best_efforts_data:
        activity_name = activity["activity_name"]
        activity_data = activity["date"]

        for effort in activity["best_efforts"]:
            distance_key = effort["distance"]
            time_seconds = effort["time_seconds"]

            if (
                distance_key not in best_by_distance
                or time_seconds < best_by_distance[distance_key]["time_seconds"]
            ):
                best_by_distance[distance_key] = {
                    "distance": distance_key,
                    "distance_m": effort["distance_m"],
                    "best_time": effort["time"],
                    "time_seconds": time_seconds,
                    "pace": effort["pace"],
                    "activity_name": activity_name,
                    "date": activity_data,
                }

    summary = sorted(best_by_distance.values(), key=lambda x: x["distance_m"])

    return summary
