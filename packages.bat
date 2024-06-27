@echo off
echo Installing required Python packages...

REM Upgrade pip
python -m pip install --upgrade pip

REM Install required packages
pip install tkinter
pip install pillow
pip install pynput
pip install lxml
pip install paramiko

echo Installation complete.
pause
