import logging
from .config import AiscalatorConfig, find_user_config_file
from .utils import subprocess_run


def airflow_setup(conf: AiscalatorConfig):
    """
    Setup the airflow configuration files and environment

    Parameters
    ----------
    conf : AiscalatorConfig
        Configuration object for the application

    """

    pass


def airflow_up(conf: AiscalatorConfig):
    """
    Starts an airflow environment

    Parameters
    ----------
    conf : AiscalatorConfig
        Configuration object for the application

    """
    dockerfile = find_user_config_file(
        "config/docker-compose-CeleryExecutor.yml"
    )
    # TODO copy dockerfile to temp folder to redefine some paths
    # logging.info("Starting airflow with dockerfile: " + dockerfile)
    commands = [
        "docker-compose", "-f",
        dockerfile,
        "up", "-d"
    ]
    subprocess_run(commands, no_redirect=True)


def airflow_down(conf: AiscalatorConfig):
    """
    Stop an airflow environment

    Parameters
    ----------
    conf : AiscalatorConfig
        Configuration object for the application

    """
    dockerfile = find_user_config_file(
        "config/docker-compose-CeleryExecutor.yml"
    )
    # logging.info("Stopping airflow with dockerfile: " + dockerfile)
    commands = [
        "docker-compose", "-f",
        dockerfile,
        "down"
    ]
    subprocess_run(commands, no_redirect=True)


def airflow_cmd(conf: AiscalatorConfig, cmd=None):
    """
    Execute an airflow subcommand

    Parameters
    ----------
    conf : AiscalatorConfig
        Configuration object for the application
    cmd : list
        subcommands to run
    """
    dockerfile = find_user_config_file(
        "config/docker-compose-CeleryExecutor.yml"
    )
    # logging.info("Running airflow with dockerfile: " + dockerfile)
    commands = [
        "docker-compose", "-f",
        dockerfile,
        "run", "--rm", "webserver", "airflow",
    ]
    if cmd is not None:
        commands += cmd
    subprocess_run(commands, no_redirect=True)
