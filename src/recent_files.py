# This Python file uses the following encoding: utf-8
import json
import os
from datetime import datetime
from appdirs import user_data_dir

APP_NAME = "Architec"
APP_AUTHOR = "HoangNguyen"
MAX_RECENT = 10

config_dir = user_data_dir(APP_NAME, APP_AUTHOR)
os.makedirs(config_dir, exist_ok=True)
recent_file_path = os.path.join(config_dir, "recent_files.json")

def load_recent_files():
    if os.path.exists(recent_file_path):
        files = open(recent_file_path, "r", encoding="utf-8")
        data = json.load(files)
        return data.get("recent_files", [])
    return []

def save_recent_files(recent_files):
    files = open(recent_file_path, "w", encoding="utf-8")
    json.dump({"recent_files": recent_files}, files, indent=2)

def add_recent_file(path):
    path = os.path.abspath(path)
    recent_files = load_recent_files()

    recent_files = [f for f in recent_files if f["path"] != path]

    recent_files.insert(0, {
        "path": path,
        "last_opened": datetime.now().isoformat(timespec='seconds')
    })

    recent_files = recent_files[:MAX_RECENT]
    save_recent_files(recent_files)
