# Bai tap qua trinh - Backup AdventureWorks2022 (SQL Server)
SV: Nguyen Pham Viet Huy - MSSV K254060687

## Cai dat
1. Cai SQL Server Express/Developer + SSMS + ODBC Driver 18.
2. Restore AdventureWorks2022.bak (Microsoft): https://github.com/Microsoft/sql-server-samples/releases/tag/adventureworks
3. Chay sql/01_setup_recovery.sql
4. `pip install -r requirements.txt`
5. Sua SERVER, BACKUP_DIR trong backup_manager.py cho dung may cua ban.

## Chay
- Tu dong backup: `python backup_manager.py` (hoac dat trong Windows Task Scheduler, trigger At startup)
- Giao dien: `streamlit run app.py`
- Kich ban su co + khoi phuc: sql/02_incident_and_restore.sql
