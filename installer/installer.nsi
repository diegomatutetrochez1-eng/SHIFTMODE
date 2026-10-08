; NSIS script for SHIFTMODE installer
; Requires NSIS to be installed.

Name "SHIFTMODE"
OutFile "dist\SHIFTMODE-Installer.exe"
InstallDir "$PROGRAMFILES\SHIFTMODE"
RequestExecutionLevel admin

Page components
Page directory
Page instfiles

Section "SHIFTMODE"
    SetOutPath "$INSTDIR"
    File "/oname=$INSTDIR\SHIFTMODE.exe" "dist\SHIFTMODE.exe"
    CreateDirectory "$SMPROGRAMS\SHIFTMODE"
    CreateShortCut "$SMPROGRAMS\SHIFTMODE\SHIFTMODE.lnk" "$INSTDIR\SHIFTMODE.exe"
    CreateShortCut "$DESKTOP\SHIFTMODE.lnk" "$INSTDIR\SHIFTMODE.exe"
SectionEnd
