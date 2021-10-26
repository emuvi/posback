import os
import sys
import datetime as dt
import utils


class Restore:
    target_restore_host = "localhost"
    origin_backup_week = str(dt.datetime.today().weekday())
    data_relative_to = "periodically"

    def __init__(self,
                 target_restore_host: str = "",
                 origin_backup_week: str = "",
                 data_relative_to: str = ""):
        if target_restore_host:
            self.target_restore_host = target_restore_host
        if origin_backup_week:
            self.origin_backup_week = origin_backup_week
        if data_relative_to:
            self.data_relative_to = data_relative_to


def restore_globals(restore: Restore):
    globals_name = utils.get_data_path(
        restore.data_relative_to,
        "globals-" + restore.origin_backup_week + ".bkp")
    if os.system("psql -h " + restore.target_restore_host +
                 " -U postgres -f " + globals_name) == 0:
        print("Successfully restore globals.")
    else:
        print("Fail on restore globals.")
        sys.exit(-1)


def restore_database(restore: Restore, path_name):
    print("Restoring path: " + path_name + "...")
    file_name = os.path.basename(path_name)
    db_name = file_name[3:len(file_name)-6]
    print("Restoring database: " + db_name)
    os.system('psql -h ' + restore.target_restore_host +
              ' -U postgres -c "DROP DATABASE ' + db_name + '"')
    if os.system('psql -h ' + restore.target_restore_host +
                 ' -U postgres -c "CREATE DATABASE ' + db_name + '"') != 0:
        print("Fail on create database " + db_name)
        sys.exit(-1)
    if os.system("pg_restore -h " + restore.target_restore_host +
                 " -U postgres -d " + db_name + " --format tar -v " + path_name) != 0:
        print("Fail on restore database " + db_name)
        sys.exit(-1)


def restore_globals_and_databases(restore: Restore):
    restore_globals(restore)
    origin_path = utils.get_data_folder(restore.data_relative_to)
    for inside_path in os.listdir(origin_path):
        if inside_path.startswith("db-") and inside_path.endswith(
                "-" + restore.origin_backup_week + ".bkp"):
            restore_database(restore, os.path.join(origin_path, inside_path))
    print("Successfully finish to restore the globals and all databases.")


if __name__ == "__main__":
    restore = Restore()
    confirm = input(
        "Do you wanna restore the globals and all databases?\n" +
        "  From data: '" + restore.data_relative_to + "'\n" +
        "  And of week: '" + restore.origin_backup_week + "'\n" +
        "  And to host: '" + restore.target_restore_host + "' ? (y/N) : ")
    if confirm != "y":
        sys.exit(0)
    restore_globals_and_databases(restore)
