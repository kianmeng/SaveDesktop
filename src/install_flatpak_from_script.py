#!/usr/bin/python3
import os
from pathlib import Path

DATA_FLATPAK = f"{Path.home()}/.var/app/io.github.vikdevelop.SaveDesktop/data"
CACHE_FLATPAK = f"{Path.home()}/.var/app/io.github.vikdevelop.SaveDesktop/cache/tmp"

# Check Desktop Environment
if os.getenv("XDG_CURRENT_DESKTOP") == 'GNOME':
    environment = 'GNOME'
elif os.getenv("XDG_CURRENT_DESKTOP") == 'ubuntu:GNOME':
    environment = 'GNOME'
elif os.getenv("XDG_CURRENT_DESKTOP") == 'zorin:GNOME':
    environment = 'GNOME'
else:
    environment = 'None'

# Activate gsettings property
if environment == 'GNOME':
    os.system("gsettings set org.gnome.shell disable-user-extensions false")

if os.path.exists(f"{DATA_FLATPAK}/app"):
    with open(f"{CACHE_FLATPAK}/copying_flatpak_data", "w") as f:
        f.write("copying flatpak data ...")
    os.system(f"cp -R {CACHE_FLATPAK}/import_config/app {DATA_FLATPAK}/")
    os.system(f"cp -R {DATA_FLATPAK}/app ~/.var/")
    os.system(f"rm {CACHE_FLATPAK}/*")

# Install Flatpak apps from list
if os.path.exists(f"{DATA_FLATPAK}/installed_flatpaks.sh"):
    os.system(f"sh {DATA_FLATPAK}/installed_flatpaks.sh && sh {DATA_FLATPAK}/installed_user_flatpaks.sh")
    os.system(f"rm {DATA_FLATPAK}/*.sh")
else:
    print("List with installed Flatpak apps is not exists.")
    
