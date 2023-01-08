import subprocess
from os import system
from pathlib import Path
from shutil import rmtree
from typing import Generator

import yaml
from conf import settings
from Models import Configuration, RemoteBackup
from VarlaLib import Varla
from yaml.loader import SafeLoader

TEMP_PATH: str = settings.BACKUP_TEMPORARY_PATH


def backup_configurations(
    config_path: str, filter: str = None
) -> Generator[Configuration, None, None]:
    with open(config_path, "r") as f:
        configs = yaml.load(f, Loader=SafeLoader)
        for config in [Configuration(**config) for config in configs["backups"]]:
            if filter:
                if config.PREFIX.lower() == filter.lower():
                    yield config
            else:
                yield config


def directory_backup(
    source: str,
    destination: str,
    prefix: str,
    compress: bool = False,
    rename: bool = False,
):

    Varla.verbose(f"Backing-up ['{source}']")
    try:
        directory_name = subprocess.check_output(
            "bin/Services/Backup/scripts/backup.sh {0} {1} {2} {3} {4}".format(
                source,
                destination,
                prefix,
                "--compress" if compress else "",
                "--rename" if rename else "",
            ),
            stderr=subprocess.STDOUT,
            shell=True,
        )

        Varla.info(source, "has been backed-up")
        Varla.verbose(directory_name)

        return (
            str(directory_name.decode("unicode_escape"))
            .replace("\\ ", " ")
            .replace(" ", "\\ ")
        )
    except subprocess.CalledProcessError:
        Varla.error(source, "failed to back up")


def database_backup(database_name: str, destination: str):
    if not system(
        "bin/Services/Backup/scripts/database_backup.sh {0} {1}".format(
            database_name,
            destination.replace(" ", "\\ "),
        )
    ):
        Varla.info(f"Successfuly backed-up {database_name} database")
    else:
        Varla.error(f"Failed to back-up {database_name} database")


def create_temp_dir():
    delete_temp_dir()
    try:
        Varla.verbose(f"Creating '{TEMP_PATH}'")
        Path.mkdir(Path(TEMP_PATH))
        Varla.info(f"'{TEMP_PATH}' was successfuly Created!")

    except FileExistsError:
        Varla.verbose(f"'{TEMP_PATH}' already exists!")
    except Exception as e:
        Varla.error(f"Failed to create '{TEMP_PATH}'")
        Varla.error(e)


def delete_temp_dir():
    try:
        Varla.verbose(f"Deleting '{TEMP_PATH}'")
        rmtree(Path(TEMP_PATH))
        Varla.info(f"'{TEMP_PATH}' was successfuly deleted!")

    except FileNotFoundError:
        Varla.verbose(f"'{TEMP_PATH}' does not exist!")
    except Exception as e:
        Varla.error(f"Failed to delete '{TEMP_PATH}'")
        Varla.error(e)


def copy_source_directories(sources: list[str], prefix: str):
    if sources:
        for source in sources:
            directory_backup(
                source=source,
                destination=TEMP_PATH,
                prefix=prefix,
            )
    else:
        Varla.verbose("No source directories were defined!")
        Varla.verbose("Skipping copy source directories!")


def backup_databases(databases: list[str], destination: str):
    if databases:
        for database_name in databases:
            database_backup(database_name=database_name, destination=destination)
    else:
        Varla.verbose("No databases were defined!")
        Varla.verbose("Skipping backing-up databases!")


def copy_to_destination(
    destination: str,
    prefix: str,
    compress: bool = False,
):
    return directory_backup(
        source=TEMP_PATH,
        destination=destination,
        prefix=prefix,
        compress=compress,
        rename=True,
    )


def rename(source: str, destination: str):
    Varla.verbose(f"Renaming ['{source}'] to ['{destination}']")
    if not system(f"mv {source} {destination}"):
        Varla.verbose(f"Successfuly renamed '{source}' to '{destination}'")
    else:
        Varla.error(f"Failed to rename '{source}' to '{destination}'")


def remote_backup(remote_name: str, remote_host: RemoteBackup):
    Varla.verbose(f"Copying ['{remote_name}'] to ['{remote_host.host}']")

    if not system(f"scp -r {remote_name} {remote_host.host}:{remote_host.path}"):
        Varla.info(f"Successfuly copied ['{remote_name}'] to ['{remote_host.host}']")
    else:
        Varla.error(f"Failed to copy ['{remote_name}'] to ['{remote_host.host}']")


def copy_to_remote_destinations(
    remote_backups: list[RemoteBackup],
    directory_name: str,
    remote_name: str,
):

    if remote_backups:
        for remote_host in remote_backups:
            rename(source=directory_name, destination=remote_name)
            remote_backup(remote_name=remote_name, remote_host=remote_host)
            rename(source=remote_name, destination=directory_name)
    else:
        Varla.verbose("No remote backups defined!")
        Varla.verbose("Skipping remote backups!")


class Backup:

    Busy = False

    def list_backups(config_path: str = settings.BACKUP_CONFIG_PATH):
        return [config.PREFIX for config in backup_configurations(config_path)]

    def run_backups(config_path: str, filter: str = None):
        # Go over all backup configs
        print(filter)
        for config in backup_configurations(config_path, filter):
            Backup.run_backup(config)

    def run_backup(config: Configuration):

        Backup.Busy = True
        Varla.info(config.PREFIX, "backup has started!")
        # init TEMP_PATH
        create_temp_dir()

        Varla.debug(config.dict(), config.dict(), name="Configs")

        # Copy all directories to "TEMP_PATH"
        copy_source_directories(config.source_directories, config.PREFIX)

        backup_databases(databases=config.database_names, destination=TEMP_PATH)

        # Copy everything from "TEMP_PATH" to "config.destination_dir"
        directory_name = copy_to_destination(
            destination=config.destination_dir,
            prefix=config.PREFIX,
            compress=config.zip_compression,
        )

        copy_to_remote_destinations(
            remote_backups=config.remote_backups,
            directory_name=directory_name,
            remote_name=f'{config.destination_dir}/{config.PREFIX}.latest{".zip" if config.zip_compression else ""}',
        )

        # clean "TEMP_PATH"
        delete_temp_dir()

        Backup.Busy = False
        Varla.info(config.PREFIX, "backup has ended!")
