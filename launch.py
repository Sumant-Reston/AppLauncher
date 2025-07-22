import os
import json
import requests
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

# To use a remote manifest, replace 'manifest.json' with your manifest URL (e.g., 'https://yourserver.com/manifest.json')
# Make sure your Python HTTP server is running in the 'RestonApps' folder on your Desktop.
MANIFEST_URL = "http://192.168.1.187:8080/manifest.json"
DEFAULT_INSTALL_DIR = os.path.join(os.path.expanduser("~"), "Desktop", "RestonDownload")

def download_from_gdrive(url, dest_path):
    session = requests.Session()
    response = session.get(url, stream=True)
    if "content-disposition" in response.headers:
        pass  # Direct download
    else:
        for key, value in response.cookies.items():
            if key.startswith("download_warning"):
                confirm_token = value
                params = {"confirm": confirm_token}
                response = session.get(url, params=params, stream=True)
                break
    with open(dest_path, "wb") as f:
        for chunk in response.iter_content(32768):
            if chunk:
                f.write(chunk)

class AppLauncher(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Reston Launcher")
        self.geometry("600x400")
        self.install_dir = DEFAULT_INSTALL_DIR
        self.manifest = {}
        self.create_widgets()
        self.load_manifest()

    def create_widgets(self):
        # IP/Port entry at the top
        self.server_url_var = tk.StringVar(value=MANIFEST_URL)
        server_frame = tk.Frame(self)
        server_frame.pack(pady=(10, 0))
        tk.Label(server_frame, text="Manifest URL:").pack(side=tk.LEFT, padx=5)
        self.server_entry = tk.Entry(server_frame, textvariable=self.server_url_var, width=50, justify="center")
        self.server_entry.pack(side=tk.LEFT, padx=5)
        tk.Button(server_frame, text="Set", command=self.change_server_url).pack(side=tk.LEFT, padx=5)

        self.header_label = tk.Label(self, text="Reston Launcher", font=("Arial", 16, "bold"))
        self.header_label.pack(pady=(10, 10))

        loc_frame = tk.Frame(self)
        loc_frame.pack(pady=5)
        tk.Label(loc_frame, text="Install location:").pack(side=tk.LEFT, padx=5)
        self.loc_var = tk.StringVar(value=self.install_dir)
        tk.Entry(loc_frame, textvariable=self.loc_var, width=40, justify="center").pack(side=tk.LEFT, padx=5)
        tk.Button(loc_frame, text="Browse", command=self.choose_folder).pack(side=tk.LEFT)

        # Fixed-size frame for app list, centered
        self.app_list_frame = tk.Frame(self)
        self.app_list_frame.pack(pady=20)

        # Header row
        header = tk.Frame(self.app_list_frame)
        header.pack()
        tk.Label(header, text="App Name", width=18, font=("Arial", 10, "bold"), anchor="center").pack(side=tk.LEFT, padx=2)
        tk.Label(header, text="Version", width=12, font=("Arial", 10, "bold"), anchor="center").pack(side=tk.LEFT, padx=2)
        tk.Label(header, text="Status", width=16, font=("Arial", 10, "bold"), anchor="center").pack(side=tk.LEFT, padx=2)
        tk.Label(header, text="Action", width=12, font=("Arial", 10, "bold"), anchor="center").pack(side=tk.LEFT, padx=2)

        self.app_rows = []

        # Add a stretchable empty frame to push the refresh button to the bottom
        self.bottom_spacer = tk.Frame(self)
        self.bottom_spacer.pack(expand=True, fill=tk.BOTH)

        # Refresh button at the bottom, centered
        self.refresh_btn = tk.Button(self, text="Refresh", command=self.load_manifest)
        self.refresh_btn.pack(pady=(0, 20))

    def clear_app_rows(self):
        for row in self.app_rows:
            row.destroy()
        self.app_rows = []

    def populate_tree(self):
        self.clear_app_rows()
        # Show up to 6 apps, centered
        for idx, (app_name, info) in enumerate(self.manifest.items()):
            if idx >= 6:
                break
            local_version = self.get_local_version(app_name)
            status = "Not installed" if not local_version else (
                "Up to date" if local_version == info["version"] else "Update available"
            )
            action_text = "Install" if not local_version else (
                "Update" if local_version != info["version"] else "Launch"
            )
            row = tk.Frame(self.app_list_frame)
            row.pack(pady=2)
            tk.Label(row, text=app_name, width=18, anchor="center").pack(side=tk.LEFT, padx=2)
            tk.Label(row, text=info["version"], width=12, anchor="center").pack(side=tk.LEFT, padx=2)
            tk.Label(row, text=status, width=16, anchor="center").pack(side=tk.LEFT, padx=2)
            btn = tk.Button(row, text=action_text, width=12,
                            command=lambda n=app_name, a=action_text: self.handle_action(n, a))
            btn.pack(side=tk.LEFT, padx=2)
            self.app_rows.append(row)

    def handle_action(self, app_name, action):
        if action in ("Install", "Update"):
            self.install_or_update_app(app_name)
        elif action == "Launch":
            self.launch_app(app_name)

    def choose_folder(self):
        folder = filedialog.askdirectory(initialdir=self.install_dir)
        if folder:
            self.install_dir = folder
            self.loc_var.set(folder)
            self.populate_tree()

    def load_manifest(self):
        try:
            resp = requests.get(MANIFEST_URL)
            self.manifest = resp.json()
            self.populate_tree()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load manifest: {e}")

    def get_local_version(self, app_name):
        version_path = os.path.join(self.install_dir, app_name, ".version")
        if os.path.exists(version_path):
            with open(version_path, "r") as f:
                return f.read().strip()
        return None

    def set_local_version(self, app_name, version):
        app_dir = os.path.join(self.install_dir, app_name)
        os.makedirs(app_dir, exist_ok=True)
        with open(os.path.join(app_dir, ".version"), "w") as f:
            f.write(version)

    def install_or_update_app(self, app_name):
        info = self.manifest[app_name]
        exe_name = f"{app_name}.exe"
        app_dir = os.path.join(self.install_dir, app_name)
        os.makedirs(app_dir, exist_ok=True)
        exe_path = os.path.join(app_dir, exe_name)
        try:
            self.populate_tree()  # To show status change
            download_from_gdrive(info["url"], exe_path)
            self.set_local_version(app_name, info["version"])
            messagebox.showinfo("Success", f"{app_name} installed/updated.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to download {app_name}: {e}")
        self.populate_tree()

    def launch_app(self, app_name):
        exe_path = os.path.join(self.install_dir, app_name, f"{app_name}.exe")
        if not os.path.exists(exe_path):
            messagebox.showerror("Error", "Executable not found. Please install/update the app.")
            return
        try:
            os.startfile(exe_path)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to launch: {e}")

    def change_server_url(self):
        global MANIFEST_URL
        new_url = self.server_url_var.get().strip()
        if new_url:
            MANIFEST_URL = new_url
            self.load_manifest()

if __name__ == "__main__":
    app = AppLauncher()
    app.mainloop()
