import json
import nats
from faststream.nats import NatsBroker, PullSub
from config.config import Config

class NatsHelper():
    def __init__(self):
        self.config = Config()
        self.nats = None
    
    async def get_nats_connection():
        # if nats is None:
        nats_server = await nats.connect(Config.Nats.server)

        return nats_server
    
    async def get_nats_broker_connection():
        broker = NatsBroker(Config.Nats.server)

        return broker

    async def publish(self, event_name, payload):
        nats = self.get_nats_connection()
        jet_stream = nats.jetstream()

        await jet_stream.publish(event_name, payload)
