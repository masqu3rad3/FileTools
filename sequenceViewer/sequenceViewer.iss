; -- Example1.iss --
; Demonstrates copying 3 files and creating an icon.

; SEE THE DOCUMENTATION FOR DETAILS ON CREATING .ISS SCRIPT FILES!

[Setup]
AppName=Sequence Viewer
AppVersion=0.1.1
DefaultDirName={pf}\Sequence Viewer
DefaultGroupName=Sequence Viewer
UninstallDisplayIcon={app}\SequenceViewer.exe
Compression=lzma2
SolidCompression=yes
OutputDir=userdocs:Inno Setup Examples Output

[Files]
Source: "C:\Users\User\PycharmProjects\FileTools\sequenceViewer\dist\sequenceViewer\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs

[Icons]
Name: "{group}\Sequence Viewer"; Filename: "{app}\SequenceViewer.exe"
