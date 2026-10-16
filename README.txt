G Apps Launcher — confirmed WebView dependency fix

IMPORTANT: Replace the repository's existing main.py AND .github/workflows/build-windows.yml with these files, commit the changes, then download the artifact from the NEW successful workflow run.

This workflow:
- Uses Python 3.11 for a consistent Windows build.
- Installs pywebview and PyInstaller explicitly.
- Verifies `import webview` before packaging.
- Uses PyInstaller --collect-all webview and explicit WebView platform hidden imports.
- Produces dist/GAppsLauncher.exe, artifact GAppsLauncher-Windows.

Requires Microsoft Edge WebView2 Runtime on the Windows PC. Google may restrict embedded sign-in in webview windows.

Google product icons: the app fetches official product favicons from Google-owned service domains on first display and caches them under %APPDATA%\\GAppsLauncher\\icons. Internet access is required the first time; if a favicon cannot load, a letter fallback is shown.
