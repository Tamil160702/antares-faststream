from psycopg_pool import AsyncConnectionPool, ConnectionPool
from cassandra.cluster import Cluster
from psycopg.rows import dict_row
from faststream import Logger

from config.config import Config

config = Config()

def getDBConnStr() -> str:
  return (
    f"dbname={config.Postgres.database} "
    f"user={config.Postgres.user} "
    f"password={config.Postgres.password} "
    f"host={config.Postgres.host} "
    f"port={config.Postgres.port}"
  )

async def readFromPG(query, *args, log: Logger):
  try:
    async with AsyncConnectionPool(conninfo=getDBConnStr(), open=False, kwargs={"row_factory": dict_row}) as pool:
        async with pool.connection() as conn:       
          cursor = await conn.execute(query, *args)
          result = await cursor.fetchall()
          #log.debug("readFromPG:::Result from postgres: {0}", result)
          return result

  except Exception as err:
    log.error("Error in ReadFromPG: {0}", detail={'query': query, 'args': args, 'Detail': str(err)})

async def executeInPG(query, *args, log: Logger):
  try:
    async with AsyncConnectionPool(conninfo=getDBConnStr(), open=False, kwargs={"row_factory": dict_row}) as pool:
        async with pool.connection() as conn:       
          cursor = await conn.execute(query, *args)
          result = await cursor.fetchone()
          #log.debug("executeInPG:::Result from postgres: {0}", result)
          return result  

  except Exception as err:
    log.error("Error in ExecuteInPG: {0}", detail={'query': query, 'args': args, 'Detail': str(err)})
    
