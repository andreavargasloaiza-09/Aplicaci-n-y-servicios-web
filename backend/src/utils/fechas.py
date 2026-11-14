"""Utilidades de fecha y hora."""
from datetime import datetime, timezone


def ahora() -> datetime:
    """Momento actual en UTC (así se guardan todas las fechas)."""
    return datetime.now(timezone.utc)
