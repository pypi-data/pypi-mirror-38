#!/usr/bin/env bash

TRY_LOOP="20"

AIRFLOW__CORE__EXECUTOR=SequentialExecutor

ln -s $HOME/work/$1 $HOME/dags/$1

# Install custom python package if requirements.txt is present
if [ -e "/requirements.txt" ]; then
    $(which pip) install --user -r /requirements.txt
fi

airflow initdb
# With the "Local" executor it should all run in one container.
airflow scheduler &
airflow webserver &

exec jupyter-lab
