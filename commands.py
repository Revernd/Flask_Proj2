import click

from flask.cli import AppGroup

@click.command('command1')
@click.argument('name')
def mycommand(name):
    print(name)

group_cli = AppGroup('group1')

@group_cli.command('command1')
@click.argument('name')
def mycommand2(name):
    print(name)