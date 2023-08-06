import os
import envdir

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "exportme.standalone.settings")

CONFIG_DIR = os.path.expanduser('~/.config/exporters')

if os.path.exists(CONFIG_DIR):
    envdir.open(CONFIG_DIR)
