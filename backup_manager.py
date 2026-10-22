"""Backup Manager - tu dong backup SQL Server (FULL / DIFF / LOG), verify, xoa file cu."""
import os, time, logging, pyodbc, schedule
from datetime import datetime

SERVER = "localhost"
DB = ("AdventureWorks2025"
      )
BACKUP_DIR = r"D:\Backups\AW"
KEEP_DAYS = 14
CONN = (f"DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={SERVER};DATABASE=master;"
        "Trusted_Connection=yes;TrustServerCertificate=yes;")

os.makedirs(BACKUP_DIR, exist_ok=True)
logging.basicConfig(filename=os.path.join(BACKUP_DIR, "backup.log"),
                    level=logging.INFO, format="%(asctime)s %(message)s")


def run(sql):
    cn = pyodbc.connect(CONN, autocommit=True)
    cur = cn.cursor()
    cur.execute(sql)
    while cur.nextset():
        pass
    cn.close()


def backup(kind):
    """kind: FULL | DIFF | LOG"""
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    ext = "trn" if kind == "LOG" else "bak"
    path = os.path.join(BACKUP_DIR, f"{DB}_{kind}_{ts}.{ext}")
    try:
        if kind == "FULL":
            run(f"BACKUP DATABASE [{DB}] TO DISK=N'{path}' WITH INIT, CHECKSUM")
        elif kind == "DIFF":
            run(f"BACKUP DATABASE [{DB}] TO DISK=N'{path}' WITH DIFFERENTIAL, INIT, CHECKSUM")
        else:
            run(f"BACKUP LOG [{DB}] TO DISK=N'{path}' WITH INIT, CHECKSUM")
        run(f"RESTORE VERIFYONLY FROM DISK=N'{path}' WITH CHECKSUM")
        logging.info(f"OK   {kind} {path}")
        return True
    except Exception as e:
        logging.error(f"FAIL {kind}: {e}")
        return False
    finally:
        cleanup()


def cleanup():
    limit = time.time() - KEEP_DAYS * 86400
    for f in os.listdir(BACKUP_DIR):
        p = os.path.join(BACKUP_DIR, f)
        if f.endswith((".bak", ".trn")) and os.path.getmtime(p) < limit:
            os.remove(p)
            logging.info(f"DELETED {f}")


def start():
    schedule.every().sunday.at("01:00").do(backup, "FULL")
    for d in ("monday", "tuesday", "wednesday", "thursday", "friday", "saturday"):
        getattr(schedule.every(), d).at("01:00").do(backup, "DIFF")
    schedule.every(30).minutes.do(backup, "LOG")
    logging.info("Scheduler started")
    while True:
        schedule.run_pending()
        time.sleep(30)


if __name__ == "__main__":
    start()