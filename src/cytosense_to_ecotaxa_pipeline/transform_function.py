
from datetime import datetime


def remove_extension(value):
    """
    Function to remove the extension name from a file name.
    """
    if value and isinstance(value, str):
        return os.path.splitext(value)[0]
    return value




def extract_date_utc(iso_datetime):
    """
    Extrait la date au format YYYYMMDD UTC à partir d'une chaîne ISO 8601.
    Convert an ISO 8601 datetime string to YYYYMMDD UTC format.
    """
    try:
        dt = datetime.fromisoformat(iso_datetime.rstrip("Z")).astimezone()  # Conversion vers UTC
        return dt.strftime("%Y%m%d UTC")
    except ValueError:
        return "INVALID_DATE"

def extract_time_utc(iso_datetime):
    """
    Extrait l'heure au format HHMMSS UTC à partir d'une chaîne ISO 8601.
    Convert an ISO 8601 datetime string to HHMMSS UTC format.
    """
    try:
        dt = datetime.fromisoformat(iso_datetime.rstrip("Z")).astimezone()  # Conversion vers UTC
        return dt.strftime("%H%M%S UTC")
    except ValueError:
        return "INVALID_TIME"


