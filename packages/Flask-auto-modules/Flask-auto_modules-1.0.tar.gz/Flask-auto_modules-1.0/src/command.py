import os
import click
from flask import Flask

app = Flask(__name__)
'''
    Создание модуля через команду create ./path/module_name
'''
@app.cli.command()
@click.argument('arg')
def create_module(arg):
    print(arg)
    if arg[-1] == '/':
        arg = arg[0:-1]
    if not os.path.exists(arg):
        os.makedirs(arg)
        os.makedirs(f"{arg}/views")
        os.makedirs(f"{arg}/models")

        view = open(f"{arg}/views/views.py","w+")
        view.writelines("from ..app import module\n")
        view.close()

        app = open(f"{arg}/app.py","w+")
        app.writelines("from flask import Blueprint\n")
        app.writelines(f"module=Blueprint('{arg.split('/')[-1]}', __name__, url_prefix='/')\n")
        app.writelines("from .views.views import *\n")
        app.close()
    else:
        raise ["Error dublicate dir"]