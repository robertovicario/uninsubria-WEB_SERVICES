# =========================
# Dependencies
# =========================

from datetime import datetime, timezone

# =========================
# Configurations
# =========================

# Timestamp
now = datetime.now(timezone.utc)

# -------------------------

dynamic = {
    'time': {
        'timestamp': now.timestamp(),
        'year': now.year,
        'month': now.month,
        'day': now.day,
        'hour': now.hour,
        'minute': now.minute,
        'second': now.second,
        'isoformat': now.isoformat()
    }
}
