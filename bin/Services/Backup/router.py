from conf import settings
from fastapi import APIRouter, BackgroundTasks, Response, status

from .main import Backup

backup = APIRouter(prefix="/backup", tags=["backups"])


@backup.post("/trigger/{backup_name}")
def trigger_backup(
    backup_name: str, background_tasks: BackgroundTasks, response: Response
):
    if not Backup.Busy:
        background_tasks.add_task(
            Backup.run_backups, settings.BACKUP_CONFIG_PATH, backup_name
        )
        response.status_code = status.HTTP_202_ACCEPTED
        return {"message": "Accepted"}
    else:
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
        return {"message": "Busy"}


@backup.post("/trigger_all")
async def trigger_backup_all(background_tasks: BackgroundTasks, response: Response):
    if not Backup.Busy:
        background_tasks.add_task(Backup.run_backups, settings.BACKUP_CONFIG_PATH)
        response.status_code = status.HTTP_202_ACCEPTED
        return {"message": "Accepted"}
    else:
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
        return {"message": "Busy"}


@backup.post("/list")
async def list_backups(response: Response):

    response.status_code = status.HTTP_202_ACCEPTED
    return {"message": Backup.list_backups()}
