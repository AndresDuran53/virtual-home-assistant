import pytz
from datetime import datetime, timezone, timedelta

def datetime_from_str_person(date_str: str) -> datetime | None:
    if not date_str:
        return None
    datetime_obj = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S.%f%z").replace(tzinfo=pytz.UTC)
    datetime_minus_6 = pytz.timezone('America/Costa_Rica')
    datetime_utc_minus_6 = datetime_obj.astimezone(datetime_minus_6)
    return datetime_utc_minus_6

def datetime_from_str_event(date_str):
    if not date_str:
        return None
    try:
        date_obj = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S%z')
    except:
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        date_obj = date_obj.replace(tzinfo=timezone(timedelta(hours=-6)))
    return date_obj

def get_happening_text(event):
    tz = pytz.timezone('America/Costa_Rica')
    now = datetime.now(tz=tz)
    if (event.end_time < now):
        return "Event already occurred"
    elif (event.start_time <= now and event.end_time >= now):
        return "Event happening now"
    else:
        return "Upcoming event"