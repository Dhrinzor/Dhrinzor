OutFile "TheMagicCardInstaller.exe"    ; Nombre del instalador
InstallDir "$PROGRAMFILES\\MagicCorp" ; Ruta de instalación

Section
  SetOutPath $INSTDIR              ; Directorio de instalación
  File "D:\\APP\\MagicCorp\\archivo_necesario.txt" ; Agregar archivo necesario al instalador
  WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\MagicCorp" "DisplayName" "MagicCorp"
  WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\MagicCorp" "UninstallString" "$INSTDIR\\uninstall.exe"
  WriteUninstaller "$INSTDIR\\uninstall.exe" ; Crear desinstalador
SectionEnd