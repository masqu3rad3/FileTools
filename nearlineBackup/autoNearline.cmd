ECHO OFF
ECHO Nearline Project Backup Running
set sourcePath=%~dp0
python %sourcePath%nearlineBackup.py -e --drivebyname "nearline_backup"