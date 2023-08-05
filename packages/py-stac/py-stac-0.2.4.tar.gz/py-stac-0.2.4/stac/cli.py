# -*- coding: utf-8 -*-

"""Console script for py-stac."""

import click
# from .iserv.iserv import cli as iserv


@click.group()
def main(args=None):
    """Console script for py-stac."""
    click.echo("Replace this message by putting your code into "
               "stac.cli.main")
    click.echo("See click documentation at http://click.pocoo.org/")


# main.add_command(iserv)

if __name__ == "__main__":
    main()
