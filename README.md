Reston Launcher: Setup & Usage Guide

1. Initial Setup

A. Folder Structure

- On your Desktop, create a folder named: RestonApps
- Place your application .exe files and manifest.json in this folder.

---

B. Start the Internal Web Server

1. Open Command Prompt.
2. Navigate to the RestonApps folder:
3. Start the Python HTTP server:
python -m http.server 8080
(This will serve files at http://<your-ip>:8080/)
4. Leave this window open while the server is running.
5. To find your IP address: (DONT CHANGE SHOULD BE SAME NOW)
Run ipconfig in Command Prompt.
Look for "IPv4 Address" (e.g., **********).

---

C. Configure the Launcher
In your [launch.py](http://launch.py/) file, set:
MANIFEST_URL = "http://**********/manifest.json"
(Replace with your actual IP address)

1. How to Add a New Application
2. Copy the new .exe into the RestonApps folder.
3. Edit manifest.json to include the new app:

{
"QSC": {
"version": "1.0.0",
"url": "http://**********/QSC.exe"
},
"NewApp": {
"version": "1.0.0",
"url": "http://**********/NewApp.exe"
}
}

1. Save manifest.json.
2. Refresh the launcher.
3. How to Update an Existing Application
4. Replace the old .exe with the new one (keep the filename the same).
5. Update the version in manifest.json:

"QSC": {
"version": "1.1.0",
"url": "http://**********/QSC.exe"
}

1. Save manifest.json.
2. Users will see “Update available” in the launcher.

Apps are saved to:
C:\Users\<YourName>\Desktop\RestonDownload\<AppName>\<AppName>.exe
