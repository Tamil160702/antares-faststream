from datetime import datetime, timedelta, timezone
from faststream import Logger

def checkDateExpiry(startTime, minutes, log: Logger):
    log.debug("checkDateExpiry:::Parameters {0} - {1}", startTime, minutes)
    # Create a timedelta object
    timeDelta = timedelta(hours=0, minutes=int(minutes), seconds=0)
    # Add timedelta to datetime
    expiryTime = startTime + timeDelta
    log.debug("Timestamp for Comparison {0} - {1}", datetime.now(timezone.utc), expiryTime)
    expired = datetime.now(timezone.utc) > expiryTime
    log.debug("Checked Expiry and returing {0}", expired)
    return expired

def getDateTimestamp():
    return datetime.isoformat(datetime.now(timezone.utc))

def validate_isoformat(value: str) -> datetime:
    try:
        # Try to parse the datetime string in ISO 8601 format
        return datetime.fromisoformat(value)
    except ValueError:
        raise ValueError('timestamp must be in ISO 8601 format')