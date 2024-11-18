@echo off
TITLE Python Installer and Application Launcher
color 0A

:: Log file for debugging
echo Starting script... > install_log.txt

:: Check for admin privileges
NET FILE 1>NUL 2>NUL
if '%errorlevel%' == '0' ( goto START ) else ( goto getAdmin )

:getAdmin
echo Requesting administrative privileges... >> install_log.txt
echo Set UAC = CreateObject^("Shell.Application"^) > "%temp%\getadmin.vbs"
set params = %*:"=""
echo UAC.ShellExecute "cmd.exe", "/c %~s0 %params%", "", "runas", 1 >> "%temp%\getadmin.vbs"
"%temp%\getadmin.vbs"
del "%temp%\getadmin.vbs"
exit /B

:START
echo Checking for Python installation... >> install_log.txt

:: Check if Python is installed
python --version >> install_log.txt 2>&1
if errorlevel 1 (
    echo Python is not installed. Installing Python... >> install_log.txt
    
    :: Download Python installer
    curl -o python_installer.exe https://www.python.org/ftp/python/3.9.7/python-3.9.7-amd64.exe
    
    :: Install Python silently
    start /wait python_installer.exe /quiet InstallAllUsers=1 PrependPath=1 Include_pip=1
    
    :: Clean up installer
    del python_installer.exe
    
    echo Python installation completed. >> install_log.txt
) else (
    echo Python is already installed. >> install_log.txt
)

:: Refresh environment variables
call RefreshEnv.cmd || (
    echo @echo off > RefreshEnv.cmd
    echo echo Refreshing environment variables... >> RefreshEnv.cmd
    echo for /f "tokens=3* delims==" %%%%a in ('set') do @echo %%%%a=%%%%b >> RefreshEnv.cmd
    call RefreshEnv.cmd
    del RefreshEnv.cmd
)

:: Install required packages
echo Installing required packages... >> install_log.txt
python -m pip install --upgrade pip >> install_log.txt 2>&1
python -m pip install tkinter pynput requests >> install_log.txt 2>&1

:: Create a copy of the Python script in the same directory
echo Copying application files... >> install_log.txt
copy /Y "%~dp0combinations.py" "%~dp0combinations.py"

:: Create desktop shortcut
echo Creating desktop shortcut... >> install_log.txt
echo Set oWS = WScript.CreateObject("WScript.Shell") > CreateShortcut.vbs
echo sLinkFile = oWS.ExpandEnvironmentStrings("%USERPROFILE%\Desktop\Column Combinations Generator.lnk") >> CreateShortcut.vbs
echo Set oLink = oWS.CreateShortcut(sLinkFile) >> CreateShortcut.vbs
echo oLink.TargetPath = "python" >> CreateShortcut.vbs
echo oLink.Arguments = """%~dp0combinations.py""" >> CreateShortcut.vbs
echo oLink.WorkingDirectory = "%~dp0" >> CreateShortcut.vbs
echo oLink.Save >> CreateShortcut.vbs
cscript //nologo CreateShortcut.vbs
del CreateShortcut.vbs

:: Run the application
echo Starting the application... >> install_log.txt
python "%~dp0combinations.py"

pause

