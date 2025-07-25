# Reston Launcher: Setup & Usage Guide

## 1. Initial Setup

### A. Folder Structure

- The launcher will automatically install applications to your Desktop in a folder named `Reston_Applications`.
- No setup is required for the install location; users cannot change this location.

---

## 2. Hosting Your Apps and Manifest

- The `manifest.json` and application files are hosted on GitHub.
- The launcher fetches the manifest from:
  ```
  https://raw.githubusercontent.com/Sumant-Reston/AppLauncher/main/manifest.json
  ```
- Each app's download URL in the manifest should point to a GitHub Releases direct link, e.g.:
  ```
  https://github.com/Sumant-Reston/Quote_Sheet_JSON_Conversion/releases/download/v1.0.0/QSC.exe
  ```

---

## 3. How to Add a New Application

1. Upload the new `.exe` (or `.zip`) to your GitHub Releases.
2. Edit `manifest.json` in your GitHub repo to include the new app. Example:

```json
{
  "QSC": {
    "version": "1.0.0",
    "url": "https://github.com/Sumant-Reston/Quote_Sheet_JSON_Conversion/releases/download/v1.0.0/QSC.exe"
  },
  "NewApp": {
    "version": "1.0.0",
    "url": "https://github.com/Sumant-Reston/YourRepo/releases/download/v1.0.0/NewApp.exe"
  }
}
```

3. Save and commit `manifest.json` to GitHub.
4. Refresh the launcher.

---

## 4. How to Update an Existing Application

1. Upload the new version of the `.exe` (or `.zip`) to a new GitHub Release.
2. Update the version and URL in `manifest.json`.

```json
"QSC": {
  "version": "1.1.0",
  "url": "https://github.com/Sumant-Reston/Quote_Sheet_JSON_Conversion/releases/download/v1.1.0/QSC.exe"
}
```

3. Save and commit `manifest.json` to GitHub.
4. Users will see “Update available” in the launcher.

---

## 5. Download Location

Apps are saved to:
```
C:\Users\<YourName>\Desktop\Reston_Applications\<AppName>\<AppName>.exe
```

---

## 6. Notes
- The install location is fixed and cannot be changed by the user.
- The manifest URL is set in the code (`launch.py`) and cannot be changed from the launcher GUI.
- No local server is required; everything is fetched from GitHub.
