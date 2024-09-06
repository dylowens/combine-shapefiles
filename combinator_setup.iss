   #define MyAppName "Shapefile Combinator"
   #define MyAppVersion "1.0"
   #define MyAppPublisher "Dylan Owens"
   #define MyAppExeName "Combinatronics_GUI.exe"
   #define MyAppInstallDir "C:\ShapefileCombinator"

   [Setup]
   AppName={#MyAppName}
   AppVersion={#MyAppVersion}
   AppPublisher={#MyAppPublisher}
   DefaultDirName={#MyAppInstallDir}
   DisableDirPage=yes
   DefaultGroupName={#MyAppName}
   OutputDir=C:\Users\dylow\OneDrive\Desktop\ShapefileCombinatorSetup
   OutputBaseFilename=ShapefileCombinatorSetup
   Compression=lzma
   SolidCompression=yes

   [Files]
   Source: "dist\Combinatronics_GUI\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

   [Icons]
   Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
   Name: "{commondesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"

   [Run]
   Filename: "{app}\{#MyAppExeName}"; Description: "Launch application"; Flags: postinstall nowait