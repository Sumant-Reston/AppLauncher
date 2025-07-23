# Reston Launcher: Setup & Usage Guide

## 1. Initial Setup

### A. Folder Structure

1. On your Desktop, create a folder named `RestonApps`.
2. Place your application `.exe` files and `manifest.json` in this folder.

---

### B. Start the Internal Web Server

1. Open **Command Prompt**.
2. Navigate to the `RestonApps` folder:
   ```sh
   cd %USERPROFILE%\Desktop\RestonApps
   ```
3. Start the Python HTTP server:
   ```sh
   python -m http.server 8080
   ```
   This will serve files at: [http://<your-ip>:8080/](http://<your-ip>:8080/)
4. Leave this window open while the server is running.
5. To find your IP address:
   - Run `ipconfig` in Command Prompt.
   - Look for **IPv4 Address** (e.g., `192.168.1.100`).

---

### C. Configure the Launcher

In your `launch.py` file, set:

```python
MANIFEST_URL = "http://<your-ip>:8080/manifest.json"
```
Replace `<your-ip>` with your actual IP address from the previous step.

---

## 2. How to Add a New Application

1. Copy the new `.exe` into the `RestonApps` folder.
2. Edit `manifest.json` to include the new app. Example:

```json
{
  "QSC": {
    "version": "1.0.0",
    "url": "http://<your-ip>:8080/QSC.exe"
  },
  "NewApp": {
    "version": "1.0.0",
    "url": "http://<your-ip>:8080/NewApp.exe"
  }
}
```

3. Save `manifest.json`.
4. Refresh the launcher.

---

## 3. How to Update an Existing Application

1. Replace the old `.exe` with the new one (keep the filename the same).
2. Update the version in `manifest.json`. Example:

```json
"QSC": {
  "version": "1.1.0",
  "url": "http://<your-ip>:8080/QSC.exe"
}
```

3. Save `manifest.json`.
4. Users will see “Update available” in the launcher.

---

## 4. Download Location

Apps are saved to:
```
C:\Users\<YourName>\Desktop\RestonDownload\<AppName>\<AppName>.exe
```
