import os
import sys
import datetime as dt
import utils


class Backup:
    target_backup_week = "(now::week)"
    target_backup_host = "localhost"
    data_relative_to = "periodically"

    def __init__(self,
                 target_backup_host: str = "",
                 target_backup_week: str = "",
                 data_relative_to: str = ""):
        if target_backup_host:
            self.target_backup_host = target_backup_host
        if target_backup_week:
            self.target_backup_week = target_backup_week
        if data_relative_to:
            self.data_relative_to = data_relative_to

    def get_target_week(self) -> str:
        if self.target_backup_week == "(now::week)":
            return str(dt.datetime.today().weekday())
        else:
            return self.target_backup_week


def backup_globals(backup: Backup):
    new_name = utils.get_data_path(
        backup.data_relative_to,
        "globals-" + backup.get_target_week() + "-new.bkp")
    if os.path.exists(new_name):
        os.remove(new_name)
    if os.system("pg_dumpall -h " + backup.target_backup_host +
                 " --clean -U postgres -v --globals-only " + "-f " + new_name) == 0:
        old_name = utils.get_data_path(
            backup.data_relative_to,
            "globals-" + backup.get_target_week() + "-old.bkp")
        now_name = utils.get_data_path(
            backup.data_relative_to,
            "globals-" + backup.get_target_week() + ".bkp")
        if os.path.exists(old_name):
            os.remove(old_name)
        if os.path.exists(now_name):
            os.rename(now_name, old_name)
        os.rename(new_name, now_name)
        print("Successfully finish to backup of globals")
    else:
        if os.path.exists(new_name):
            os.remove(new_name)
        print("Fail backup the globals.")
        sys.exit(-1)


def list_databases(backup: Backup):
    db_list = []
    process = os.popen('psql -h ' + backup.target_backup_host +
                       ' -U postgres -c "SELECT datname FROM pg_database;"')
    result_text = process.read()
    result_code = process.close()
    if not (result_code == None or result_code == 0):
        print("Fail to list databases.")
        sys.exit(-1)
    started = False
    for line in result_text.splitlines():
        line = line.strip()
        if not started:
            if line.startswith('-'):
                started = True
        else:
            if line.startswith('('):
                started = False
            elif not line.startswith('template') and line != "postgres":
                db_list.append(line)
    return db_list


def backup_database(backup: Backup, db_name: str):
    new_name = utils.get_data_path(
        backup.data_relative_to,
        "db-" + db_name + "-" + backup.get_target_week() + "-new.bkp")
    if os.path.exists(new_name):
        os.remove(new_name)
    if os.system("pg_dump -h " + backup.target_backup_host +
                 " -d " + db_name + " -U postgres " +
                 "--format tar --blobs --encoding UTF8 --verbose " +
                 "-f " + new_name) == 0:
        old_name = utils.get_data_path(
            backup.data_relative_to,
            "db-" + db_name + "-" + backup.get_target_week() + "-old.bkp")
        now_name = utils.get_data_path(
            backup.data_relative_to,
            "db-" + db_name + "-" + backup.get_target_week() + ".bkp")
        if os.path.exists(old_name):
            os.remove(old_name)
        if os.path.exists(now_name):
            os.rename(now_name, old_name)
        os.rename(new_name, now_name)
        print("Successfully finish to backup database " + db_name)
    else:
        if os.path.exists(new_name):
            os.remove(new_name)
        print("Fail backup database " + db_name)


def backup_globals_and_databases(backup: Backup):
    backup_globals(backup)
    for db_name in list_databases(backup):
        backup_database(backup, db_name)
    print("Successfully finish to backup the globals and all databases.")


if __name__ == "__main__":
    backup_globals_and_databases(Backup())
