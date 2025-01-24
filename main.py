import os, logging

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

    logging.basicConfig(
        filemode='a',
        datefmt='%H:%M:%S',
        level=logging.DEBUG,
        filename=CONFIG.LOG_DIR,
        format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
    )

    # ------------------------------------------------------------
    # MAIN ENTRY PROMPT
    option = Prompt.ask(
        "Meetcount - Attendance Management System\n"
        "1. Install\n2. Start\n3. Status\n4. Upgrade\n5. View Logs\n6. Stop\n7. Uninstall\n6. Exit\nAction[1]"
    )

    while not option.isdigit() or int(option) < 1 or int(option) > 6:
        option = Prompt.ask(
            "Invalid option, please enter a valid number\n"
            "1. Install\n2. Start\n3. Status\n4. Upgrade\n5. View Logs\n6. Stop\n7. Uninstall\n6. Exit\nAction[1]"
        )

    match int(option):
        case 1:
            CLI.install_app()
        case 2:
            CLI.start_app()
        case 3:
            CLI.get_status()
        case 6:
            CLI.stop_app()
        case 7:
            CLI.uninstall_app()
        case _:
            CLI.install_app()




if __name__ == "__main__":
    typer.run(main)