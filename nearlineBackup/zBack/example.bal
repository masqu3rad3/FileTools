#'---------------------------------------------------------
#'- Example Zback script, see User's Manual for more info
#'---------------------------------------------------------
# Notes: 
# To activate an example line, remove first # char(uncomment line)
# It is not necessary to comment blank lines - Zback ignores them
# 
# Ex.01
# ?=e  # define ? drive for whole batch (?: is now drive = E:)
# ?=|XPORTER|    # define ? drive to be drive named |XPORTER|
# ?=\\Coreduo\xporter (u)  # LAN shared drive stick on COREDUO PC
# Ex.02
# Synchronize Downloads from home and work computers
# c:\downloads\*.* > ?:\downloads   /Usy
# Ex.03
# Sync. files from "My documents" (disabled with #)
# %mydocs%\Game\Data\*.* > ?:\backup\Game\Data /U
# Ex.04
# Backup Work directory to LAN computer Coreduo, folder share_c
# C:\work\*.* > \\Coreduo\share_c\work    /us
# Ex.05
# Backup music files from "My Documents" to two backup locations
# %mydocs%\My Music\*.mp3,*.wma > d:\backup\my Music /us
# %mydocs%\My Music\*.mp3,*.wma > f:\backup\my Music /us
# Ex.06
# Backup user files from "Documents and Settings\(user)" to backup location
# %user%\*.* > %backup%\== /us
# Ex.07
# Backup work directory, exclude "Temp", "Tempora" and "Trash" directories
# c:\Homework\*.* > %backup%\Homework  /us  g=[TEMP*,TRASH]
# Ex.08
# Backup files in work directory with some exclusions
# c:\Homework\*.* > %backup%\Homework  /us k=[*.BAK,TEMP.BAL]
# Ex.09
# Update (backup) homework with subdir, including system+hidden files 
# C:\Homework\*.* > D:\Backup\Homework  /usj
# Ex.10
# Daily backup to dated subdirectory Homework\[2010-05-30]\
# c:\Homework\*.* > %backup%\Homework  /d4s
# Ex.11
# Backup new photographs to stick (disabled with #)
# (date format must be adjusted for your regional settings) 
# c:\PHOTO\*.jpg  > ?:\photo  /us t=[07.10.2007_07.10.2009]
# Ex.12
# Erase temporary files from Homework
# c:\Homework\*.tmp >  (nul)  /es
# Ex.13
# Erase very old backuped files
# D:\backup\*.* >  (nul)  /es t=[1.6.2005_1.6.2009]
# Ex.14
# Make exact copy (mirror) of Homework to stick
# c:\Homework\*.* > ?:\Homework   /ms
# Ex.15
# Restore last backup to work directory
# C:\Homework\*.* > ?:\backup\Homework  /os
# Ex.16
# Sync only files and dirs existing on Source dir/drive
# both lines must be executed !
# C:\Source\*.* > D:\Target  /us
# C:\Source\*.* < D:\Target  /usrp
# Ex.17
# Backup using \= shortcut for Source directory name
# c:\beta\toto  >  d:\backup\=   /us
#    will do:
# c:\beta\toto  >  d:\backup\toto   /us 
# Ex.18        
# Backup using \==  shortcut for Source Path:
# c:\beta\toto  >  d:\backup\==  /us
#   will do:
# c:\beta\toto  >  d:\backup\beta\toto   /us
# Ex.19
# Backup using \===  shortcut for full Source Path 
# c:\beta\toto  >  d:\backup\===  /us
#   will do:
# c:\beta\toto  >  d:\backup\c(#)\beta\toto  /us
# Ex.20
# Specify drives by its names (|main_disk| -> c:)
# drives must have names (use windows explorer) !
# |main_disk|\temp 2\*.*  >  |usb_disk|\temp  /u
# Ex.21
# Replace string for all lines following (2 replacement statemets allowed)
# $%src=>C:\small\baca      #define %src
# $%trg=>D:\U\HTML\         #define %trg
# %src\*.*  > %trg  /u      #execute with replacment paths
# Ex.22
# Swap string "c:" to "d:" and "d:" to "c:" for all lines following
# $c:<>d: 
# Ex.23
# Move files from c: to d: (delete source after copy)
# C:\new\*.* > D:\new  /cxs
# Ex.24
# Secure Move files from c: to d: (shred source after copy)
# C:\new\*.* > D:\new  /chs
# Ex.25
# Mirror DOC and ZIP files to same name subdirectory on Google Drive
# D:\U\HTML\HOME-ALP\*.zip,*.doc > C:\Users\dave\Google disk\=  /ms
# Ex.26
# Mirror all but keep old and surplus files/dirs in @bak@\[Date_time]\ 
# C:\Tempdev2\zback\*.* > D:\Backup\Zback  /msi4
# Ex.27
# all lines are ignored after line started with 2 # characters 
# Ex.28
# define drive and optionally set root path (k:\M_latest\org)
# ?=k  / path=[M_latest\org]  
# C:\work\*.* > ?:\back\one  /us #target path= k:\M_latest\org\back\one
# Ex.29  
# multiple ?: lines. The last line with ready drive will be the target 
#    ?=|MY PASSPORT|
#    ?=|Elements|
# D:\U\*.* > ?:\U  /msy
# Ex.30 
# exclude single (unique) directory, referred to srcDir root
# D:\test\*.*  >  D:\_Backup\test  /us g=[\VIDEO\MISC]
#  (excluded directory is: D:\test\VIDEO\MISC and its sub-dirs)
# Ex.31 
# example of defining segment in batch list (process Yes-No-Cancel)
# #'?  first segment title = define segment of batch list
#      D:\test\*.*  >  D:\_Backup\test  /cbs  #line1 in this segment
#      D:\test\*.*  >  u:\_Backup\test  /cbs
# #'?. marker for end of this segment
#
## Ex.32
# backup myDocs to shared drive in folder backups\%computername%\docs
# %mydocs%\*.*  >  Z:\backups\%computername%\docs   /us 
#
#