#!/usr/bin/env python
"""create Mac app from a shell script"""
import click
from _mac_appify.code import Code
from _mac_appify.script import Script
import public

public.add(Code,Script)

@public.add
def appify(script,app,image=None):
    """create Mac app from a shell script"""
    Script(script).appify(app,image)

MODULE_NAME = "mac_appify"
PROG_NAME = 'python -m %s' % MODULE_NAME
USAGE = 'python -m %s script app [image]' % MODULE_NAME


@click.command()
@click.argument('script', required=True)
@click.argument('app', required=True)
@click.argument('image', required=False)
def _cli(script, app, image=None):
    Script(script).appify(app, image)


if __name__ == '__main__':
    _cli(prog_name=PROG_NAME)
