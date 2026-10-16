@echo off
python -m pip install --upgrade pywebview pyinstaller
pyinstaller --noconfirm --clean --onefile --windowed --name GAppsLauncher main.py
pause
