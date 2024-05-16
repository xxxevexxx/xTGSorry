import os
import sys
import warnings
import platform
import subprocess

from loguru import logger

warnings.filterwarnings("ignore")
warnings.filterwarnings("ignore", category=DeprecationWarning)


def create_service():
    name = os.path.basename(os.getcwd())
    service_path = f"/etc/systemd/system/{name}.service"
    if not os.path.exists(service_path):
        logger.info("Creating service")
        file_path = os.path.abspath(__file__)
        main_path = os.path.dirname(file_path)
        config = (
            f"[Unit]\n"
            f"Description={name}\n"
            f"After=network.target\n\n"

            f"[Service]\n"
            f"User=root\n"
            f"WorkingDirectory={main_path}\n"
            f"ExecStart=poetry run python {main_path}/main.py\n\n"

            f"[Install]\n"
            f"WantedBy=multi-user.target\n"
        )
        with open(service_path, 'w') as service:
            service.write(config)
        os.system(f"systemctl enable {name}")
        os.system("systemctl daemon-reload")
        logger.info("Service created")


def update_and_migrate():
    if platform.system() == "Linux":
        create_service()
        logger.info("Updating git")
        subprocess.run(["git", "stash"])
        subprocess.run(["git", "pull"])
        logger.info("Git updated")

    if not os.path.exists("migrations"):
        logger.info("Creating migrations")
        subprocess.run(["poetry", "run", "aerich", "init", "-t", "config.TORTOISE_ORM"])
        subprocess.run(["poetry", "run", "aerich", "init-db"])
        logger.info("Migrations created")

    logger.info("Migrating database")
    subprocess.run(["poetry", "run", "aerich", "migrate"])
    subprocess.run(["poetry", "run", "aerich", "upgrade"])
    logger.info("Database migrated")

    logger.info("Updating dependencies")
    subprocess.run(["poetry", "update", ])
    logger.info("Dependencies updated")
    logger.remove()
    logger.add(sink=sys.stdout, level="ERROR")
