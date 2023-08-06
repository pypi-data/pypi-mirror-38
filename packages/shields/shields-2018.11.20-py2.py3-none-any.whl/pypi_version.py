#!/usr/bin/env python
"""get pypi.org project version"""
import json
import public
import requests
import os
import sys
import click


@public.add
def get(name):
    """get pypi.org project version"""
    url = "https://pypi.org/pypi/%s/json" % name
    r = requests.get(url)
    if r.ok:
        data = json.loads(r.text)
        if "info" in data:
            return data["info"]["version"]


@click.command()
@click.argument('name', required=True)
def _cli(name):
    name = sys.argv[1]
    version = get(name)
    if version:
        print(version)


MODULE_NAME = os.path.splitext(os.path.basename(__file__))[0]
PROG_NAME = 'python -m %s' % MODULE_NAME


if __name__ == "__main__":
    _cli(prog_name=PROG_NAME)
