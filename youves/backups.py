import subprocess
from datetime import datetime
from os import listdir
from os.path import isfile, join

from dipdup.config import PostgresDatabaseConfig


def backup(database_config: PostgresDatabaseConfig):
    """Generates the database backup(s)."""

    backup_folder = "mainnet_dump"
    backup_file = "{}.sql".format(datetime.now().strftime("%Y-%m-%d-%H:%M:%S"))
    database = f"postgresql://{database_config.user}:{database_config.password}@{database_config.host}:{database_config.port}/{database_config.database}"

    backup_path = "{}/{}".format(backup_folder, backup_file)
    with open(backup_path, "wb") as fout:
        process = subprocess.Popen(
            ["pg_dump", "-d", database],
            stdout=fout,
            stderr=subprocess.PIPE,
            universal_newlines=True,
        )
        _, stderr = process.communicate()
        if process.returncode == 0:
            print(f"Database backup successful to: {backup_path}")
            delete_all_but(backup_folder, backup_file)
        else:
            print(f"Database backup failed with error: {stderr}")


def restore(backup_path, database_config):
    """Restore the database to the spefied backup file."""

    database = f"postgresql://{database_config.user}:{database_config.password}@{database_config.host}:{database_config.port}/{database_config.database}"
    with open(backup_path, "rb") as fin:
        process = subprocess.Popen(
            ["psql", database],
            stdin=fin,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
        )
        _, stderr = process.communicate()
        if process.returncode == 0:
            print(f"Database restored successfully to: {backup_path}")
        else:
            print(f"Database restore failed with error: {stderr}")


def get_all_backups():
    """Returns a list with all the database backups."""
    backups_folder = "mainnet_dump"
    return [f for f in listdir(backups_folder) if isfile(join(backups_folder, f))]


def get_most_recent_backup():
    """Returns the most recently created backup."""
    all_backup_files = get_all_backups()
    if not all_backup_files:
        return None

    files_with_timestamp = [
        (
            f,
            datetime.timestamp(
                datetime.strptime(f.replace(".sql", ""), "%Y-%m-%d-%H:%M:%S")
            ),
        )
        for f in all_backup_files
    ]
    most_recent = max(files_with_timestamp, key=lambda item: item[1])
    return join("mainnet_dump/", most_recent[0])


def delete_all_but(folder, file):
    """Deletes all but the file from the given folder."""

    process = subprocess.Popen(
        ["find", folder, "-type", "f" "-not" "-name", file, "-delete"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
    )
    print("Deleting old backups.")

    stdout, stderr = process.communicate()
    if process.returncode == 0:
        print("Old backups deleted successfully")
    else:
        print(f"Old backups deletion failed with error: {stderr}")
