OutFile "TheMagicCardInstaller.exe"    ; Nombre del instalador
InstallDir "$PROGRAMFILES\\The Magic Card" ; Ruta de instalación

Section
  SetOutPath $INSTDIR              ; Directorio de instalación
  File "D:\\APP\\the magic card program\\archivo_necesario.txt" ; Agregar archivo necesario al instalador
  WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\The Magic Card" "DisplayName" "The Magic Card"
  WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\The Magic Card" "UninstallString" "$INSTDIR\\uninstall.exe"
  WriteUninstaller "$INSTDIR\\uninstall.exe" ; Crear desinstalador
SectionEnd