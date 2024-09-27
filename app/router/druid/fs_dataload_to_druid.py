import json
import requests
from datetime import datetime
from faststream import FastStream
from faststream.nats import NatsBroker
from fastapi import APIRouter
from app.config.config import Config
from common.logger import Logger 


log = Logger()
router = APIRouter()
DRUID_URL = Config.Druid.server

async def start_subscriber():
    broker = NatsBroker(Config.Nats.server)
    app = FastStream(broker)
    # @broker.subscriber(subject="druidFaststream", stream="druidFaststream", durable="druid_durable",pull_sub=True,queue="druid_queue")
    @broker.subscriber(subject="druids", stream="druids", durable="druids_durable",pull_sub=True,queue="druids_queue")

    async def message_handler(msg):
        # Druid Overlord endpoint URL
        print(msg)
        keys = []
        for key in msg:
            if key != 'table':
                keys.append(key)
            else:
                tabelname = msg[key]
  
        # Simplified data ingestion specification
        simplified_data = {
            "type": "index_parallel",
            "spec": {
                "ioConfig": {
                    "type": "index_parallel",
                    "inputSource": {
                        "type": "inline",  # passing data in same spec so using inline
                        "data": json.dumps(msg)  # Convert message back to a JSON string
                    },
                    "inputFormat": {
                        "type": "json"
                    }
                },
                "tuningConfig": {
                    "type": "index_parallel",
                    "partitionsSpec": {
                        "type": "dynamic"
                    }
                },
                "dataSchema": {
                    "dataSource": tabelname,
                    "timestampSpec": {
                        "column": "__time",
                        "missingValue": datetime.now().isoformat()
                    },
                    "dimensionsSpec": {
                        "dimensions": keys
                    },
                    "granularitySpec": {
                        "queryGranularity": "none",
                        "rollup": False,
                        "segmentGranularity": "second"
                    }
                }
            }
        }

        try:
            response = requests.post(
                f"{DRUID_URL}/druid/indexer/v1/task",
                headers={"Content-Type": "application/json"},
                json=simplified_data
            )
            if response.status_code == 200:
                log.debug("Simplified data successfully ingested into Druid.")
            else:
                log.debug(f"Failed to ingest simplified data: {response.status_code} - {response.text}")
        except Exception as err:
            log.debug(f"An error occurred: {err}")
            
        
        
        
    try:
        # Run the FastStream application
        await app.run()
    except Exception as e:
        log.debug(f"Error occurred: {e}")
    finally:
        await broker.close()

@router.on_event("startup")
async def startup_event():
    import asyncio

    asyncio.create_task(start_subscriber())