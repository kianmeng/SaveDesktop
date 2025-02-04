#!/usr/bin/python3
from pathlib import Path
from datetime import datetime
from datetime import date
from localization import _, CACHE, DATA, IPAddr, system_dir, flatpak, snap, home
import os
import locale
import json
import gi
import socket
import shutil
import filecmp
from gi.repository import Gio, GLib

dt = datetime.now()

# Load GSettings database for show user app settings
settings = Gio.Settings.new_with_path("io.github.vikdevelop.SaveDesktop", "/io/github/vikdevelop/SaveDesktop/")

# Remove content in CACHE folder before syncing
#os.system(f"rm -rf {CACHE}/*")

# Check if syncing directory exists
if not os.path.exists(f"{CACHE}/syncing"):
    os.mkdir(f"{CACHE}/syncing")

class Syncing:
    def __init__(self):
        # Check if user has same or empty IP adress property
        if IPAddr in settings["url-for-syncing"]:
            print("You have same IP adress.")
        elif settings["url-for-syncing"] == "":
            self.get_sync_type()
            print("Synchronization is not set up.")
        else:
            self.get_file_info()

    # Get info about synchronization
    def get_file_info(self):
        # Download file-settings.json file to getting information about it
        os.chdir(f"{CACHE}/syncing")
        if os.path.exists("file-settings.json"):
            os.remove("file-settings.json")
        os.system(f"wget {settings['url-for-syncing']}/file-settings.json")
        with open("file-settings.json") as j:
            self.jF = json.load(j)
        self.file = self.jF["file-name"]
        if self.jF["periodic-import"] == "Never2":
            self.create_backup = False
            self.get_sync_type()
            print("Synchronization is not set up.")
        elif self.jF["periodic-import"] == "Daily2":
            self.create_backup = True
            self.get_sync_type()
            self.check_sync()
        elif self.jF["periodic-import"] == "Weekly2":
            self.create_backup = False
            self.get_sync_type()
            if date.today().weekday() == 1:
                self.check_sync()
            else:
                print("Today is not Tuesday.")
        elif self.jF["periodic-import"] == "Monthly2":
            self.create_backup = False
            self.get_sync_type()
            if dt.day == 2:
                self.check_sync()
            else:
                print("Today is not second day of month.")
        elif self.jF["periodic-import"] == "Manually2":
            self.create_backup = False
            self.get_sync_type_not()
            self.check_sync()

    # Set manually sync to false if IS NOT selected Manually option
    def get_sync_type(self):
        if settings["manually-sync"] == True:
            settings["manually-sync"] = False

    # Set manually sync to false if IS selected Manually option
    def get_sync_type_not(self):
        if settings["manually-sync"] == False:
            settings["manually-sync"] = True

    # Check if whether the synchronization has already taken place on this day
    def check_sync(self):
        if os.path.exists(f"{DATA}/sync-info.json"):
            with open(f"{DATA}/sync-info.json") as s:
                jl = json.load(s)
            if jl["sync-date"] == f'{date.today()}':
                print("The configuration has already been imported today.")
                exit()
            else:
                if self.jF["periodic-import"] == "Manually2":
                    if os.path.exists(f"{CACHE}/.from_app"):
                        self.download_config()
                    else:
                        print("Please sync from SaveDesktop app")
                else:
                    self.download_config()
        else:
            if self.jF["periodic-import"] == "Manually2":
                if os.path.exists(f"{CACHE}/.from_app"):
                    self.download_config()
                else:
                    print("Please sync from SaveDesktop app")
            else:
                self.download_config()
               
    # Download archive from URL
    def download_config(self):
        os.system(f"wget {settings['url-for-syncing']}/{self.file}")
        if os.path.exists(f"{self.file}"):
            os.system(f"tar -xf {self.file} ./")
        else:
            os.system(f"tar -xf {self.file}.1 ./")
        
        print("Downloading tar ...")
        self.import_config()
            
    # Sync configuration
    def import_config(self):
        os.system(f"python3 {system_dir}/config.py --import_")
        self.done()

    # Message about done synchronization
    def done(self):
        if not settings["manually-sync"] == True:
            with open(f"{DATA}/sync-info.json", "w") as s:
                s.write('{\n "sync-date": "%s"\n}' % date.today())
        if not os.path.exists(f"{CACHE}/syncing/copying_flatpak_data"):
            os.system(f"rm -rf {CACHE}/syncing/*")
        #os.system(f"rm {CACHE}/.from_app")
        print("Configuration has been synced successfully.")
        os.system(f"notify-send 'SaveDesktop ({self.file[:-10]})' '{_['config_imported']} {_['periodic_saving_desc']}' -i io.github.vikdevelop.SaveDesktop-symbolic")
        #os.system("pkill -15 python3 && pkill -15 python")

Syncing()
