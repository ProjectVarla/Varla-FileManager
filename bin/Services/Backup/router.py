from fastapi import APIRouter,BackgroundTasks,Response,status
from dotenv import load_dotenv
from os import getenv
from .main import Backup

load_dotenv()

BACKUP_CONFIG_PATH: str = getenv("BACKUP_CONFIG_PATH")

backup = APIRouter(prefix="/backup", tags=["backups"])


@backup.post("/trigger/{backup_name}")
def trigger_backup(backup_name: str,background_tasks: BackgroundTasks,response: Response):
    if not Backup.Busy:
        background_tasks.add_task(Backup.run_backups,BACKUP_CONFIG_PATH,backup_name)
        response.status_code = status.HTTP_202_ACCEPTED
        return {"message":"Accepted"}
    else:
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
        return {"message":"Busy"}

     
@backup.post("/trigger_all/")
async def trigger_backup_all(background_tasks: BackgroundTasks,response: Response):
    if not Backup.Busy:
        background_tasks.add_task(Backup.run_backups,BACKUP_CONFIG_PATH)
        response.status_code = status.HTTP_202_ACCEPTED
        return {"message":"Accepted"}
    else:
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
        return {"message":"Busy"}
