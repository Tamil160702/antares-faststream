import sys
sys.path.append('./..')
from fastapi import FastAPI
from app.router.druid import fs_dataload_to_druid


app = FastAPI()
app.include_router(fs_dataload_to_druid.router)
