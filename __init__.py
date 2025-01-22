import os
import shutil
import subprocess

import typer
from rich import print
from rich.prompt import Prompt

from config.utils import load_install_state
from .typedef import PRODUCTION_DIR,START_COMMAND, SOURCE_FILES

def install():
    state = load_install_state()
    if state.get("installed", False):
        print("Application already installed. Remove with stop")
        raise typer.Abort()


    domain_name = Prompt.ask("Enter your domain name which will host your app")

    os.makedirs(PRODUCTION_DIR, exist_ok=True)
    for file, destination in SOURCE_FILES.items():
        target_path = os.path.join(PRODUCTION_DIR, destination)
        shutil.copy(file, target_path)
    try:
        subprocess.run(START_COMMAND)
    except KeyboardInterrupt:
        print("Installation was cancelled by user")
        raise typer.Abort()

