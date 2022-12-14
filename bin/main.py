from VarlaLib import Varla, Verbosity
from services.backup.main import run_backups
from os import getenv
from dotenv import load_dotenv
import subprocess

load_dotenv()

BACKUP_CONFIG_PATH: str = getenv("BACKUP_CONFIG_PATH")

Varla.verbosity = Verbosity.VERBOSE

run_backups(BACKUP_CONFIG_PATH)
