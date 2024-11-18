@echo off
TITLE Python Installer and Application Launcher
color 0A

:: Log file for debugging
echo Starting script... > install_log.txt

echo Checking for Python installation... >> install_log.txt

:: Check if Python is installed
where python > nul 2>&1
if errorlevel 1 (
    echo Python is not installed. Installing Python... >> install_log.txt
    
    :: Download Python installer
    powershell -Command "(New-Object Net.WebClient).DownloadFile('https://www.python.org/ftp/python/3.9.7/python-3.9.7-amd64.exe', 'python_installer.exe')"
    
    if not exist python_installer.exe (
        echo Failed to download Python installer. >> install_log.txt
        pause
        exit /B 1
    )
    
    :: Install Python silently
    python_installer.exe /quiet InstallAllUsers=1 PrependPath=1 Include_pip=1
    if errorlevel 1 (
        echo Python installation failed. >> install_log.txt
        pause
        exit /B 1
    )
    
    :: Clean up installer
    del python_installer.exe
    
    echo Python installation completed. >> install_log.txt
) else (
    echo Python is already installed. >> install_log.txt
)

:: Wait for Python to be available in PATH
timeout /t 5

:: Refresh environment variables without external script
setx PATH "%PATH%" > nul

:: Install required packages
echo Installing required packages... >> install_log.txt
python -m pip install --upgrade pip >> install_log.txt 2>&1
python -m pip install tkinter pynput requests >> install_log.txt 2>&1

:: Check if combinations.py exists before copying
if exist "%~dp0Combinations.py" (
    echo Combinations.py found. >> install_log.txt
) else (
    echo Error: combinations.py not found in the current directory. >> install_log.txt
    pause
    exit /B 1
)

:: Create desktop shortcut
echo Creating desktop shortcut... >> install_log.txt
echo Set oWS = WScript.CreateObject("WScript.Shell") > CreateShortcut.vbs
echo sLinkFile = oWS.ExpandEnvironmentStrings("%USERPROFILE%\Desktop\Column Combinations Generator.lnk") >> CreateShortcut.vbs
echo Set oLink = oWS.CreateShortcut(sLinkFile) >> CreateShortcut.vbs
echo oLink.TargetPath = "pythonw.exe" >> CreateShortcut.vbs
echo oLink.Arguments = """%~dp0combinations.py""" >> CreateShortcut.vbs
echo oLink.WorkingDirectory = "%~dp0" >> CreateShortcut.vbs
echo oLink.Description = "Column Combinations Generator" >> CreateShortcut.vbs
echo oLink.Save >> CreateShortcut.vbs
cscript //nologo CreateShortcut.vbs
del CreateShortcut.vbs

:: Run the application
echo Starting the application... >> install_log.txt
start pythonw "%~dp0Combinations.py"

echo Installation completed successfully! >> install_log.txt
pause
