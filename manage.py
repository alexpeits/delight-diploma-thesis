"""
Command line tool to facilitate project usage.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""

import click


@click.group()
def cli():
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


if __name__ == '__main__':
    cli()
