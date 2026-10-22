-- Kiem tra va chuyen sang FULL recovery de co the backup Transaction Log
SELECT name, recovery_model_desc FROM sys.databases WHERE name = 'AdventureWorks2022';
ALTER DATABASE AdventureWorks2022 SET RECOVERY FULL;
-- Bat buoc co 1 ban FULL truoc khi backup LOG
BACKUP DATABASE AdventureWorks2022 TO DISK = N'D:\Backups\AW\AW_FULL_init.bak' WITH INIT, CHECKSUM, STATS = 10;
