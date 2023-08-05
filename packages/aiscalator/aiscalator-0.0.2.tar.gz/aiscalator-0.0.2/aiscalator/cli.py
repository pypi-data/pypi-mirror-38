# -*- coding: utf-8 -*-
"""
Command Line Interface of the AIscalator tool.

Using the python click package (https://click.palletsprojects.com/en/7.x/),
this module defines all the entry points to the application.

"""
import sys
import click
import logging

from .config import AiscalatorConfig
from .docker_command import docker_run_lab, docker_run_papermill
from .airflow_command import airflow_setup, airflow_up, airflow_down, airflow_cmd


@click.group()
def main():
    """ Command Line Interface to Aiscalate your data pipelines """
    pass


####################
# Airflow commands #
####################


@main.command()
def setup():
    """Setup the airflow environment"""
    click.echo(airflow_setup(AiscalatorConfig()))


@main.command()
def start():
    """Start the airflow environment"""
    click.echo(airflow_up(AiscalatorConfig()))


@main.command()
def stop():
    """Stop the airflow environment"""
    click.echo(airflow_down(AiscalatorConfig()))


@main.command()
@click.argument('subcommand', nargs=-1)
def airflow(subcommand):
    """Execute the airflow subcommand """
    click.echo(airflow_cmd(AiscalatorConfig(), subcommand))


#############################
# Aiscalator Steps commands #
#############################


@main.command()
def new():
    """Assist the creation of a new step"""
    # TODO: ask questions and generates json + ipynb files
    # TODO: afterward edit the newly created step
    logging.warn("Not implemented yet")
    pass


@main.command()
@click.argument('conf')
@click.argument('notebook')
# TODO add parameters override from CLI
def edit(conf, notebook):
    """Start an environment to edit step's code"""
    click.echo(docker_run_lab(AiscalatorConfig(conf, notebook)))


@main.command()
@click.argument('conf')
@click.argument('notebook')
# TODO add parameters override from CLI
def run(conf, notebook):
    """Run step's code without GUI"""
    # TODO run multiple notebooks
    # we have to stage notebooks with same dockerfile together,
    # merge their requirements so that groups of notebooks can be
    # run together in the same container sequentially
    click.echo(docker_run_papermill(AiscalatorConfig(conf, notebook)))


# TODO - pull run docker pull to download all images that might be needed

# TODO - startproject command like cookiecutter to easily start a new
# TODO pipeline/step

# TODO - store config file path globally with an alias
# TODO and use those shorter alias for easier commands
# TODO - list steps/pipelines/data/etc


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
