"""
Command line tool to facilitate project usage.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""

import code

import click

from delight.config import GUIConfig


@click.group()
def cli():
    """Base click group for commands."""
    pass


@cli.command()
def initdb():
    """Create database tables."""
    from delight.db.utils import create_tables
    create_tables()
    click.echo('Database tables created.')


@cli.command()
def test():
    """Run all tests in the tests/ directory."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


@cli.command()
@click.option('--host', '-h', default=GUIConfig.HOST)
@click.option('--port', '-p', default=GUIConfig.PORT)
def runserver(host, port):
    """Create app and run it."""
    from delight.gui import create_app
    app = create_app()
    app.run(host=host, port=port)

@cli.command()
def shell():
    from delight.db.session import session
    code.interact(local=locals())


if __name__ == '__main__':
    cli()
