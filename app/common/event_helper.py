from faststream import Logger

from common.pg_helper import executeInPG, readFromPG
from common.date_helper import getDateTimestamp

async def readEvent(eventid, log: Logger):
    log.debug("readEvent:::Request Parameters: {0}", eventid)
    try:
        query = "SELECT id, eventname, eventtype, payload, createdby FROM event_schema.event WHERE id=(%s);"
        
        result = await readFromPG(query, (eventid,))

        log.debug("readEvent:::Event retrieved: {0}", result[0])

        return result[0]
    except Exception as e:
        log.error("Error while creating event: {0}", str(e))
        return False, None
    
async def createEventLog(eventid, status, log: Logger):
    log.debug("createEventLog:::Request Parameters: {0}", eventid)
    try:
        query = "INSERT INTO event_schema.event_log (id, eventid, eventstatus, createdon) VALUES (%s, %s, %s, %s) RETURNING id;"
        
        result = await executeInPG(query, [eventid, status, getDateTimestamp()])

        log.debug("readEvent:::Event retrieved: {0}", result[0])

        return result[0]
    except Exception as e:
        log.error("Error while creating event log: {0}", str(e))
        return False, None    