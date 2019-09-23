---------------------------------------------------------------------
Zback - Backup and synchronization tool.
For Windows 10 (32 & 64 bit), Win8, Win7, Vista, Win XP, Win 2000

* FREEWARE FOR PERSONAL USE *

(c) by Davor Zorc, Zagreb, Croatia
http://www.fsb.hr/~dzorc/zback.html  
http://dzorc.droppages.com/zback.html
mailto:davor.zorc@fsb.hr
* Visit the site for updates and a detailed User's Manual.
---------------------------------------------------------------------

Installation - Setup version
--------------------------------
Just run Setup package and follow instructions.
You will need administrator privileges to be able to install.

The difference between setup and portable version is that
setup version includes INSTALL.INI file. This file forces Zback 
to use "<user>\documents\Zback" folder to store batch and INI files.
Remove or rename this file to make portable version.


Installation portable version
--------------------------------
-just unzip package to any directory on a fixed or removable drive. 
 (for example "My Documents"\Zbackup or "Desktop"\Zbackup or c:\zbackup,
  but not in "Program files").
-start Zback.exe. To get User Guide help press [F1].
-optionally you may also download Zback Manual from Zback homepage.
-to create desktop shortcut go to Options tab and click on [Icon] button.
-to install upgrade just overwrite all old files with new ones or use
 checkver.exe for automatic upgrade (you should close Zback first). 
-Uninstall is done by deleting Zback directory.

Remarks:
-You may need administrator privileges to write files outside "User" folders.
-If you get blank page using help file, Right-click the ZGUIDE.CHM file, 
 select Properties/ General, then click the [Unblock] and [Apply] button.
-some antivirus programs may block Zback execution (or other portable
 or "unknown" applications). If Zback does not start you may open
 antivirus configuration and unblock Zback execution.


Install portable to Windows Vista, 7, 8, 10 -User Account Control (UAC)
----------------------------------------------------------------------
-It is recommended to uzip package to c:\Users\<name>\Documents\Zbackup
 or on a removable drive.
-You need administrator privileges to write files outside "User" folders.
-By default Zback will ask for admin rights at startup. If you do not need
 to write files in Windows system folders or other user's folders you may 
 use Ctrl-F8 command in Zback. This will create ZbackA.exe file, a clone of
 Zback that will not ask for admin rights and will run as restricted user.
-If such ZbackA is unable to copy files due to rights restrictions:
  right click on ZbackA.exe and choose: Properties/Compatibility and
  check [x] "Run this program as an administrator" (or use context menu
  to run it and choose "Run as administrator").

Release notes this version (What is new)
-------------------------------------------
-version 2.89.0.a   
-update compiler and libraries
-sleepPC beep and wait 3min, Reset Filters button, %computername%
-small fixes and additions in application and guide


Version history (What is new/ changelog)
-------------------------------------------
2.89.0.a - 04.2019 compiler(xe2), sleepPC beep + wait 3min, Reset Filters, %computername%
2.87.0.d - 09.2018 form changes and colors for comments, new EXE compressor and installer
2.87.0.c - 11.2017 better Exception handling, No prompt for overwrite R/O files if quietmode
2.87.0.b - 07.2017 ReportPanel w. 2 buttons, BreakButton1, Add2Batch split
           button, More Options, option [x] Scrollers, LAN TryConnect(),
2.87.0.a - 03.2017 exclude unique path, save report in Unicode, #'? AskMsg, 

2.85.0.c - 12.2016 RenameLeftSelDir1, Courier font Aliased on win7, fix /v /i options,
2.85.0.b - 09.2016 WaitMsg goes to Caption if QuietMode, 2x ReplaceSt =>
2.85.0.a - 02.2016 wildcards (* ?) allowed in masks, settings to manual, ZbackA.exe

2.80.0.d - 10.2015 small fixes, [x] use recycle bin, checkver.exe fixed for win10
2.80.0.c - 06.2015 Win native copy method set as default, preview Target 
           path in status bar, Copy report to Clipboard, menu glyphs
2.80.0.b - 02.2015 speed optimizations, allows more then 260 chars in pathnames 
2.80.0.a - 11.2014 Help tab redesign, improved job monitoring and user action response

2.75.0.c - 07.2014 enhanced define line ?=, progressBar and taskbar animation 
2.75.0.b - 04.2014 Quetmode Max mode, Search in To-do list, #' comment line
2.75.0.a - 02.2014 Pause/ Resume using Esc key, small fixes and additions

2.70.0.c - 11.2013 small fixes and additions
2.70.0.b - 07.2013 Windows 8 compatibility, small fixes
2.70.0.a - 04.2013 show hidden/sys dirs on manual tab, Zmanual.chm, /i, /mi, /j

2.65.0.c - 02.2013 fixed Drive Combo Box, Save Batch file overwrite prompt,
2.65.0.b - 01.2013 new version checker/ updater, small fixes
2.65.0.a - 10.2012 new checker/updater, Shred /h, $swap1<>swap2, /Rs, small fixes

2.60.0.b - 07.2012 changes in dialogs, fix TestUncPath, SkipLongPaths,
2.60.0.a - 05.2012 drives can be specified by its names, BAL Save Unicode

2.55.0.c - 02.2012 better dialogs and error handling, Sleep PC when done 
2.55.0.b - 01.2012 CheckVer.exe upgrade, small fixes
2.55.0.a - 11.2011 CheckVer.exe,

2.50.0.a - 09.2011 verify copied files,
2.45.0.a - 08.2011 batch code %user%, date filter separator changed to "_"
2.40.0.a - 06.2011 Unicode support, searchSt=>replaceSt (replace in batch)

------(ver 2.3 is the last version working also on Win 95, 98, ME)-----
2.30.1c - 05.2011 Manifest for Vista elevation (UAC), no int. WinXP,
2.30.0a - 03.2011 LAN support 
 
2.25.0a - 01.2011 Drag & Drop support, Make Desktop Icon, CHM help, 
2.22.0a - 11.2010 Simple Sync panel,
2.20.0c - 09.2010  /f=IncDirMask, /g=ExcDirMask, /q=NewDirsOnly, 
          Destdir \=, \==, \===, 
2.10.0a - 08.2010 KeepOldVer /v,
2.00.0c - 04.2010 NT_SetDateTime, k=[TEMP.BAL,TEST.DOC,*.tmp], %backup%,
1.90.0a - 02.2010 Simple backup panel,

<eof>
