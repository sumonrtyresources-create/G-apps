G Apps Launcher — WebView2 edition

Features:
- Google-style app grid, search and categories
- Add custom web apps
- Left-click a card to open that website in its own app window
- Right-click a card to remove it
- App windows run in separate processes so the launcher stays open and multiple app windows can be used

Build on GitHub:
1. Upload/commit all project files to your GitHub repository (replace old files).
2. Open Actions > Build Windows EXE > Run workflow, or push to main/master.
3. Download the GAppsLauncher-Windows artifact from the completed workflow.

Requirements:
- Windows 10/11
- Microsoft Edge WebView2 Runtime
- Google may restrict sign-in or some features inside embedded webviews; this depends on Google's current security policies.

Local build:
Install Python 3.11, then run build_exe.bat.
