USE AdventureWorks2022;
-- 1. Tao bang demo, backup DIFF + LOG, ghi lai thoi diem an toan
SELECT * INTO dbo.DemoCustomer FROM Sales.Customer;
SELECT SYSDATETIME() AS ThoiDiemAnToan;   -- vi du: 2026-10-22 10:30:00

-- 2. Su co: xoa nham bang
DROP TABLE dbo.DemoCustomer;

-- 3. Khoi phuc
USE master;
BACKUP LOG AdventureWorks2022 TO DISK = N'D:\Backups\AW\AW_TAIL.trn' WITH NORECOVERY, CHECKSUM;
RESTORE DATABASE AdventureWorks2022 FROM DISK = N'D:\Backups\AW\AW_FULL.bak' WITH NORECOVERY, REPLACE;
RESTORE DATABASE AdventureWorks2022 FROM DISK = N'D:\Backups\AW\AW_DIFF.bak' WITH NORECOVERY;
RESTORE LOG AdventureWorks2022 FROM DISK = N'D:\Backups\AW\AW_LOG.trn' WITH NORECOVERY;
RESTORE LOG AdventureWorks2022 FROM DISK = N'D:\Backups\AW\AW_TAIL.trn' WITH STOPAT = '2026-10-22 10:30:00', RECOVERY;

-- 4. Kiem tra
SELECT COUNT(*) FROM AdventureWorks2022.dbo.DemoCustomer;
