import uvicorn
from conf import settings
from fastapi import FastAPI
from Services import BackupRouter
from VarlaLib import Varla, Verbosity
from VarlaLib.Shell import varla_header

app = FastAPI(title="Varla-FileManager")
app.include_router(BackupRouter, prefix="/FileManager")
Varla.verbosity = Verbosity.VERBOSE


@app.on_event("startup")
async def startup_event() -> None:
    Varla.info(f"{settings.APP_NAME} is up!")


@app.on_event("shutdown")
async def shutdown_event() -> None:
    Varla.info(f"{settings.APP_NAME} is down!")


if __name__ == "__main__":
    varla_header()
    uvicorn.run(
        "main:app",
        port=settings.FILE_MANAGER_PORT,
        host=settings.FILE_MANAGER_HOST,
    )
