import tkinter as tk
from tkinter import messagebox, filedialog, simpledialog
from pathlib import Path
import json
import hashlib
import os
import sys
import subprocess
import webbrowser

# --------- Configuration / storage ----------
CONFIG_PATH = Path("C:/Users/AMIT KUMAR/OneDrive/Pictures/Lock_wall/config.json")

def sha256_hex(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()

def load_config() -> dict:
    if CONFIG_PATH.exists():
        try:
            return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
        except Exception:
            return {}
    return {}

def save_config(cfg: dict):
    CONFIG_PATH.write_text(json.dumps(cfg, indent=2), encoding="utf-8")

# Initialize config with defaults if missing
cfg = load_config()
if "username" not in cfg:
    # default demo creds (you can change them via UI)
    cfg.setdefault("username", "admin")
    cfg.setdefault("password_hash", sha256_hex("1234"))
    cfg.setdefault("stored_link", "")  # file path or URL
    save_config(cfg)

# ---------- OS open helper ----------
def open_path_or_url(link: str):
    if not link:
        messagebox.showinfo("No stored link", "No file or link has been stored yet.")
        return
    # treat as URL if it starts with http:// or https://
    if link.startswith("http://") or link.startswith("https://"):
        webbrowser.open(link)
        return

    path = Path(link)
    if not path.exists():
        messagebox.showerror("Not found", f"Stored file does not exist:\n{link}")
        return

    try:
        if sys.platform.startswith("win"):
            os.startfile(str(path))
        elif sys.platform == "darwin":
            subprocess.run(["open", str(path)], check=False)
        else:
            subprocess.run(["xdg-open", str(path)], check=False)
    except Exception as e:
        messagebox.showerror("Error opening", f"Could not open:\n{link}\n\n{e}")

# ---------- GUI callbacks ----------
def refresh_stored_label():
    stored = cfg.get("stored_link", "")
    display = stored if stored else "(no stored file or URL)"
    stored_label.config(text=display)

def browse_and_store_file():
    # allow user to select a file and store its path
    f = filedialog.askopenfilename(title="Select file to store (will be opened after login)")
    if f:
        cfg["stored_link"] = f
        save_config(cfg)
        refresh_stored_label()
        messagebox.showinfo("Stored", f"Stored file:\n{f}")

def store_url():
    url = simpledialog.askstring("Store URL", "Enter URL to store (include http/https):")
    if url:
        cfg["stored_link"] = url.strip()
        save_config(cfg)
        refresh_stored_label()
        messagebox.showinfo("Stored", f"Stored URL:\n{cfg['stored_link']}")

def change_credentials():
    # simple flow to change username/password
    cur = simpledialog.askstring("Current username", "Enter current username:")
    cur_pwd = simpledialog.askstring("Current password", "Enter current password:", show="*")
    if cur is None or cur_pwd is None:
        return
    if cur != cfg.get("username") or sha256_hex(cur_pwd) != cfg.get("password_hash"):
        messagebox.showerror("Forbidden", "Current credentials are incorrect.")
        return
    new_user = simpledialog.askstring("New username", "Enter new username:")
    new_pwd = simpledialog.askstring("New password", "Enter new password:", show="*")
    if not new_user or not new_pwd:
        messagebox.showinfo("Cancelled", "Username/password not changed.")
        return
    cfg["username"] = new_user
    cfg["password_hash"] = sha256_hex(new_pwd)
    save_config(cfg)
    messagebox.showinfo("Saved", "Credentials updated.")

def login_action():
    user = entry_user.get().strip()
    pwd = entry_pass.get()
    if not user or not pwd:
        messagebox.showwarning("Missing", "Please enter both ID and password.")
        return

    if user == cfg.get("username") and sha256_hex(pwd) == cfg.get("password_hash"):
        # success -> open stored link
        link = cfg.get("stored_link", "")
        if not link:
            messagebox.showinfo("No stored file", "Login successful — but no stored file/URL to open.")
            return
        open_path_or_url(link)
    else:
        messagebox.showerror("Login Failed", "ID or password incorrect.")

# ---------- Build GUI ----------
root = tk.Tk()
root.title("Login & Open Stored File/URL")
root.geometry("520x260")
root.resizable(False, False)

pad = 12
frame = tk.Frame(root)
frame.pack(fill="both", expand=True, padx=pad, pady=pad)

tk.Label(frame, text="Stored file / URL (will open on successful login):").pack(anchor="w")
stored_label = tk.Label(frame, text="", fg="blue", wraplength=480, justify="left")
stored_label.pack(anchor="w", pady=(0,8))
refresh_stored_label()

btn_row = tk.Frame(frame)
btn_row.pack(anchor="w", pady=(0,10))
tk.Button(btn_row, text="Browse & Store File...", command=browse_and_store_file).pack(side="left", padx=(0,8))
tk.Button(btn_row, text="Store URL...", command=store_url).pack(side="left", padx=(0,8))

# Login inputs
inputs = tk.Frame(frame)
inputs.pack(fill="x", pady=(6,0))
tk.Label(inputs, text="ID:").grid(row=0, column=0, sticky="w")
entry_user = tk.Entry(inputs, width=36)
entry_user.grid(row=0, column=1, padx=(6,0), pady=4)

tk.Label(inputs, text="Password:").grid(row=1, column=0, sticky="w")
entry_pass = tk.Entry(inputs, width=36, show="*")
entry_pass.grid(row=1, column=1, padx=(6,0), pady=4)

# Buttons
action_row = tk.Frame(frame)
action_row.pack(pady=(14,0))
tk.Button(action_row, text="Login & Open Stored", width=18, command=login_action).pack(side="left", padx=6)
tk.Button(action_row, text="Change Credentials", width=18, command=change_credentials).pack(side="left", padx=6)
tk.Button(action_row, text="Quit", width=10, command=root.destroy).pack(side="left", padx=6)

# Helpful hint showing current stored username (no password)
tk.Label(frame, text=f"(Current stored ID: {cfg.get('username')})", fg="gray").pack(anchor="w", pady=(10,0))

entry_user.focus_set()
root.mainloop()
