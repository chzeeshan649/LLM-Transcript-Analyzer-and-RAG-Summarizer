def parse_timestamp_to_secs(ts: str) -> int:
    # accepts HH:MM:SS
    try:
        h, m, s = map(int, ts.strip().split(":"))
        return h*3600 + m*60 + s
    except Exception:
        return 0

def secs_to_hms(secs: int) -> str:
    h = secs // 3600
    m = (secs % 3600) // 60
    s = secs % 60
    return f"{h:02d}:{m:02d}:{s:02d}"
