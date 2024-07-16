from setuptools import setup

APP = ["main.py"]
DATA_FILES = ["icon.icns"]
OPTIONS = {
    "iconfile": "icon.icns",
    "argv_emulation": True,
    "plist": {
        "LSUIElement": True,
    },
    "packages": ["rumps", "requests", "chardet", "arrow", "ics"],
}

setup(
    name="Distract",
    app=APP,
    data_files=DATA_FILES,
    options={"py2app": OPTIONS},
    setup_requires=["py2app"],
)
