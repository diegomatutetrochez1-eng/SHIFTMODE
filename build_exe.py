# -*- coding: utf-8 -*-
# This script generates a .exe using PyInstaller.
# Run it on Windows after installing requirements.

import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
APP_ROOT = os.path.dirname(ROOT)


def main():
    cmd = [
        sys.executable,
        "-m",
        "PyInstaller",
        "--onefile",
        "--windowed",
        "--name",
        "SHIFTMODE",
        "--icon",
        os.path.join(APP_ROOT, "assets", "icon.ico"),
        os.path.join(APP_ROOT, "main.py"),
    ]
    print("Ejecutando compilación...")
    subprocess.run(cmd, cwd=APP_ROOT, check=True)
    print("Compilación terminada. Busca SHIFTMODE.exe en la carpeta dist/")


if __name__ == "__main__":
    main()
