
class CONFIG:
    # ------------------------------------------------------------
    # PROJECT CONFIG
    PROJECT_DIR = "Meetcount"
    CONFIG_DIR = "./config"
    PRODUCTION_DIR = f"{PROJECT_DIR}"
    LOG_DIR = f"{PROJECT_DIR}/app.log"

    FILES_PATH = f"{CONFIG_DIR}/files"
    CONFIG_ENV_PATH = f"{FILES_PATH}/variables.env"
    CONFIG_COMPOSE = f"{FILES_PATH}/docker-compose.yml"

    PRODUCTION_COMPOSE = f".deploy.yaml"
    PRODUCTION_ENV = f".env"

    SOURCE_FILES = {
        CONFIG_COMPOSE : PRODUCTION_COMPOSE,
        CONFIG_ENV_PATH: PRODUCTION_ENV
    }

    INSTALL_STATE_FILE = f"{PROJECT_DIR}/.meetcount.json"
    KEY_INSTALLED = "installed"

    # ------------------------------------------------------------
    # COMMANDS
    START_COMMAND = [
        "docker",
        "compose",
        "-f", f"{PRODUCTION_DIR}/{PRODUCTION_COMPOSE}",
        "--env-file", f"{PRODUCTION_DIR}/{PRODUCTION_ENV}",
        "up",
        "-d"
    ]

    STOP_COMMAND = [
        "docker",
        "compose",
        "-f", f"{PRODUCTION_DIR}/{PRODUCTION_COMPOSE}",
        "--env-file", f"{PRODUCTION_DIR}/{PRODUCTION_ENV}",
        "down",
    ]

    # ------------------------------------------------------------
    # ENV VARS KEYS
    KEY_APP_URL = "APP_URL"
    BASE_DOMAIN = "BASE_DOMAIN"
    KEY_APP_DOMAIN = "APP_DOMAIN"
    KEY_SERVICE_NAME = "SERVICE_NAME"
    KEY_MEILISEARCH_HOST = "MEILISEARCH_HOST"
    KEY_SANCTUM_DOMAINS = "SANCTUM_STATEFUL_DOMAINS"
    KEY_PROD_ENV_MEILISEARCH_HOST = "PROD_ENV_MEILISEARCH_HOST"
    KEY_PROD_ENV_PUSHER_APP_SCHEME = "PROD_ENV_PUSHER_APP_SCHEME"


    # ------------------------------------------------------------
    # SSL CONFIG KEYS
    SSL_CONFIG_DIR = f"{PROJECT_DIR}/ssl/config"
    SSL_WORK_DIR = f"{PROJECT_DIR}/ssl/work"
    SSL_LOG_DIR_DIR = f"{PROJECT_DIR}/ssl/dir"
    SSL_PATHS = [SSL_CONFIG_DIR,SSL_LOG_DIR_DIR,SSL_WORK_DIR]

    DOMAIN_PATTERN = r"^(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z0-9][a-z0-9-]{0,61}[a-z0-9]$"
    EMAIL_PATTERN = r"^[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?$"


