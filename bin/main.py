from os import getenv

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from Services import BackupRouter
from VarlaLib import Varla, Verbosity

load_dotenv()
PORT: int = int(getenv("FILE_MANAGER_SERVICE_PORT"))

app = FastAPI(title="Varla-FileManager")
app.include_router(BackupRouter, prefix="/FileManager")
Varla.verbosity = Verbosity.VERBOSE


@app.on_event("startup")
async def startup_event():
    Varla.info("FileManager is up!")


if __name__ == "__main__":
    uvicorn.run("main:app", port=PORT, host="0.0.0.0")
