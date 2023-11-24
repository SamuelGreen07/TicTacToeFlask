import argparse
import os

os.environ.setdefault("SETTINGS_FILE", "settings.default")

from flask import Flask

from services.db_wrapper import DataBaseWrapper
from urls import *

app = Flask(__name__)

db = DataBaseWrapper()


def app_run():
    app.run()
    db.init_engines_for_all_configs()


def run_server():
    from app import app_run
    app_run()



def run_migrations():
    os.system('alembic upgrade head')


def run_tests():
    os.system('pipenv run pytest .')


parser = argparse.ArgumentParser(description='Process some integers.')

if __name__ == '__main__':
    FUNCTION_MAP = {
        'runserver': run_server,
        'test': run_tests,
        'migrate': run_migrations
    }

    parser.add_argument('command', choices=FUNCTION_MAP.keys())
    args = parser.parse_args()
    func = FUNCTION_MAP[args.command]
    func()
