@echo off
python -m pip install --upgrade pywebview pyinstaller
pyinstaller --noconfirm --clean --onefile --windowed --name GAppsLauncher --collect-all webview --hidden-import webview.platforms.edgechromium main.py
pause
