G Apps Launcher — WebView2 edition (dependency fix)

Fix included: PyInstaller explicitly collects the pywebview package and the Edge Chromium platform module. This addresses "No module named 'webview'" when opening an app.

IMPORTANT: You must rebuild the EXE after replacing these files. The existing EXE cannot repair itself.

GitHub steps:
1. Extract this ZIP.
2. Upload/replace the files in your repository, especially .github/workflows/build-windows.yml and build_exe.bat.
3. Commit the changes.
4. Open GitHub > Actions > Build Windows EXE > Run workflow (or wait for push-triggered build).
5. Download the new GAppsLauncher-Windows artifact and run the new EXE.

Windows 10/11 and Microsoft Edge WebView2 Runtime may be required. Google may restrict sign-in in embedded webviews.
