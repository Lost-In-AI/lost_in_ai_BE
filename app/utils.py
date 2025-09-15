from datetime import datetime, timezone


def utc_now_isoformat():
    now = datetime.now(timezone.utc)
    return now.strftime("%Y-%m-%dT%H:%M:%SZ")
