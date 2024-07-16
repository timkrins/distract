import json
import requests
import os
import ics
import arrow


def get_text(url):
    print("get_text...")
    r = requests.get(url)
    if r.text:
        print("get_text: done")
        return r.text


def download_file(url, filename):
    print("download_file...")
    content = get_text(url)
    if content:
        with open(filename, "wb") as f:
            f.write(content)
            print("download_file: done")


def save_json(data, filename):
    print("save_json...")
    if data:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            print("save_json: done")


def load_json(filename):
    print("load_json...")
    with open(filename, "r") as f:
        data = json.loads(f.read())
        print("load_json: done")
        return data


def parse_events(data):
    print("parse_events...")
    cal = ics.Calendar(data)
    events = [
        {"name": x.name, "begin": x.begin.for_json(), "end": x.end.for_json()}
        for x in cal.events
    ]
    print("parse_events: done")
    return events


def parse_events_file(filename):
    print("parse_events_file...")
    with open(filename, "r") as f:
        events = parse_events(f.read())
        print("parse_events_file: done")
        return events


def load_calendar_events(url, cache_prefix="tmp/distract-cal"):
    print("load_calendar_events...")
    content = get_text(url)
    events = parse_events(content)

    # cache_ics_path = f"{cache_prefix}.ics"
    # cache_json_path = f"{cache_prefix}.json"

    # if not os.path.isfile(cache_ics_path):
    #     download_file(url, cache_ics_path)

    # if not os.path.isfile(cache_json_path):
    #     events = parse_events_file(cache_ics_path)
    #     save_json(events, cache_json_path)

    # events = load_json(cache_json_path)
    print("load_calendar_events: done")
    return events


def filter_future_events(events):
    print("filter_future_events...")
    now = arrow.now()
    next_24_hours = now.shift(hours=24)
    future_events = [
        event for event in events if now <= arrow.get(event["begin"]) < next_24_hours
    ]
    sorted_future_events = sorted(future_events, key=lambda x: arrow.get(x["begin"]))
    print(f"filter_future_events: done ({len(sorted_future_events)})")
    return sorted_future_events


def format_date(date):
    now = arrow.now()
    return arrow.get(date).to(now.tzinfo).format("YYYY-MM-DD HH:mm:ss")


def is_in_next_minute(date):
    now = arrow.now()
    next_minute = now.shift(minutes=1)
    arrow_date = arrow.get(date)

    return arrow_date >= now and arrow_date < next_minute
