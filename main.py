import os

import typer

from rich.prompt import Prompt

from core.options import CLI
from config.typedef import CONFIG


def main():
    # ------------------------------------------------------------
    # CONFIGURE LOGGING
    os.makedirs(CONFIG.PROJECT_DIR, exist_ok=True)
    if not os.path.exists(CONFIG.LOG_DIR):
        with open(CONFIG.LOG_DIR, 'w') as log_file:
            log_file.write("")

    # ------------------------------------------------------------
    # MAIN ENTRY PROMPT
    option = Prompt.ask(
        "Meetcount - Attendance Management System\n"
        "1. Install\n2. Start\n3. Status\n4. Upgrade\n5. View Logs\n6. Stop\n7. Uninstall\n6. Exit\nAction[1]"
    )

    match int(option):
        case 1:
            CLI.install_app()
        case 2:
            CLI.start_app()
        case 3:
            print("@@@")
        case 6:
            CLI.stop_app()
        case 7:
            CLI.uninstall_app()
        case _:
            CLI.install_app()




if __name__ == "__main__":
    typer.run(main)