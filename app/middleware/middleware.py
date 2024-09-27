from faststream import BaseMiddleware, Logger

from common.event_helper import createEventLog
from common.date_helper import getDateTimestamp
from config.config import Config

class CustomMiddleware(BaseMiddleware):

    def __init__(self, app):
        super().__init__(app)
        self.config = Config()

    async def on_receive(self, log: Logger):
        log.debug("In Middleware:::on_receive: {0}", self.message)
        #Create event log for start
        return await super().on_receive()

    async def after_processed(self, exc_type, exc_val, exc_tb, log: Logger):
        log.debug("In Middleware:::after_processed: {0} - {1} - {2} - {3}", self.message, exc_type, exc_val, exc_tb)
        #Create Event log for completed
        return await super().after_processed(exc_type, exc_val, exc_tb)