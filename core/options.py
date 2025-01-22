import os, json,typer, shutil, subprocess, socket, logging
from logging import Logger

from pathlib import Path

from rich.prompt import Prompt
from certbot.main import main as certbot_main

from config.typedef import CONFIG

logging.basicConfig(
    filemode='a',
    datefmt='%H:%M:%S',
    level=logging.DEBUG,
    filename=CONFIG.LOG_DIR,
    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
)

class CLI:
    _logger: Logger = logging.getLogger("MEETCLI")
    @staticmethod
    def _load_install_state():
        if os.path.exists(CONFIG.INSTALL_STATE_FILE):
            with open(CONFIG.INSTALL_STATE_FILE, "r") as f:
                return json.load(f)
        return {}

    @staticmethod
    def _save_install_state(state: dict):
        with open(CONFIG.INSTALL_STATE_FILE, "w") as f:
            json.dump(state, f, indent=4)

    @staticmethod
    def _is_installed() -> bool:
        state = CLI._load_install_state()
        return state.get(CONFIG.KEY_INSTALLED, False)

    @staticmethod
    def install_app():
        ssl_active = False
        if CLI._is_installed():
            print("Application already installed. Remove with stop")
            return

        domain_name = Prompt.ask("Enter your domain name which will host your app")
        enable_ssl = Prompt.ask("Enable SSL? Y/N")

        if enable_ssl:
            email = Prompt.ask("Enter your email address for ssl notices")
            ssl_active = CLI.obtain_cert(domain_name,email)

        protocol = "https" if ssl_active else "http"

        variables = {
            CONFIG.BASE_DOMAIN: domain_name,
            CONFIG.KEY_APP_DOMAIN: domain_name,
            CONFIG.KEY_SERVICE_NAME: "Attendance-Service",
            CONFIG.KEY_PROD_ENV_PUSHER_APP_SCHEME: protocol,
            CONFIG.KEY_APP_URL: f"{protocol}://{domain_name}",
            CONFIG.KEY_SANCTUM_DOMAINS: f"{protocol}://{domain_name}",
            CONFIG.KEY_MEILISEARCH_HOST: f"{protocol}://{domain_name}:7700",
            CONFIG.KEY_PROD_ENV_MEILISEARCH_HOST: f"{protocol}://{domain_name}:7700"
        }

        os.makedirs(CONFIG.PRODUCTION_DIR, exist_ok=True)
        for file, destination in CONFIG.SOURCE_FILES.items():
            target_path = os.path.join(CONFIG.PRODUCTION_DIR, destination)
            shutil.copy(file, target_path)

        env_path = Path(f"{CONFIG.PRODUCTION_DIR}/{CONFIG.PRODUCTION_ENV}")
        with env_path.open("a") as env_file:
            env_file.write("\n")
            for key, value in variables.items():
                env_file.write(f"{key}={value}\n")
        try:
            subprocess.run(CONFIG.START_COMMAND)
            state = {
                CONFIG.KEY_INSTALLED: True,
            }
            CLI._save_install_state(state)
        except KeyboardInterrupt:
            print("Installation was cancelled by user")
            raise typer.Abort()

    @staticmethod
    def start_app():
        if not CLI._is_installed():
            print("Application not installed. Install with install")
            raise typer.Abort()
        try:
            subprocess.run(CONFIG.START_COMMAND)
        except KeyboardInterrupt:
            print("Installation was cancelled by user")
            raise typer.Abort()

    @staticmethod
    def stop_app():
        if not CLI._is_installed():
            print("Application not installed. Install with install")
            raise typer.Abort()
        try:
            subprocess.run(CONFIG.STOP_COMMAND)
            state = {
                CONFIG.KEY_INSTALLED: False,
            }
            CLI._save_install_state(state)
            print("Application stopped successfully")
        except KeyboardInterrupt:
            print("Installation was cancelled by user")
            raise typer.Abort()

    @staticmethod
    def uninstall_app():
        if not CLI._is_installed():
            print("Application not installed. Install with install")
            raise typer.Abort()
        try:
            subprocess.run(CONFIG.STOP_COMMAND)
            shutil.rmtree(CONFIG.PROJECT_DIR)
            print("Application uninstalled successfully")
        except KeyboardInterrupt:
            print("Installation was cancelled by user")
            raise typer.Abort()

    @staticmethod
    def get_status():
        if not CLI._is_installed():
            print("Application not installed. Install with install")
            raise typer.Abort()
        option = option = Prompt.ask(
        "Select service to view logs for\n1. Install\n2. Start\n3. Status\n4. Upgrade\n5. View Logs\n6. Exit\nAction[1]"
        )
        match int(option):
            case 1:
                print("Okay")

    @staticmethod
    def obtain_cert(domain_name, email):
        result = False
        port = CLI._find_free_port()
        for dir in CONFIG.SSL_PATHS:
            os.makedirs(dir, exist_ok=True)
        try:
            certbot_args = [
                "certonly",
                "--standalone",
                f"--http-01-port={port}",
                "-d", domain_name,
                "--agree-tos",
                "--non-interactive",
                "--email", email,
                "--config-dir", CONFIG.SSL_CONFIG_DIR,
                "--work-dir", CONFIG.SSL_WORK_DIR,
                "--logs-dir", CONFIG.SSL_LOG_DIR_DIR
            ]
            certbot_main(certbot_args)
            result = True
        except Exception as e:
            CLI._logger.error(f"An error occurred: {e}")
        return result

    @staticmethod
    def _find_free_port():
        with socket.socket() as s:
            s.bind(('', 0))
            return s.getsockname()[1]





