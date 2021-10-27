from datetime import datetime
import time
import backup


backup_of_host = "pointel.pointto.us"


def backup_periodically():
    backup.backup_globals_and_databases(backup.Backup(
        target_backup_host=backup_of_host,
        data_relative_to="periodically"))


if __name__ == "__main__":
    minutes_passed = 0
    while True:
        now_str = datetime.now().strftime("%Y-%m-%d %H-%M")
        if minutes_passed > 60:
            minutes_passed = 0
            print(now_str + 
                " - Have passed one hour so we must to do the periodically backup.")
            backup_periodically()
        time.sleep(60)
        minutes_passed += 1