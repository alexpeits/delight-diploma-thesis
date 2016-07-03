"""
Command line tool to facilitate project usage.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""

import code

import click

from delight.config import GUIConfig


@click.group()
def cli():
    """Base click group for commands"""
    pass


@cli.command()
def initdb():
    """Create database tables"""
    from delight.db.utils import create_tables
    create_tables()
    click.echo('Database tables created.')


@cli.command()
def test():
    """Run all tests in the tests/ directory"""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


@cli.command()
@click.option('--host', '-h', default=GUIConfig.HOST)
@click.option('--port', '-p', default=GUIConfig.PORT)
def runserver(host, port):
    """Create app and run it"""
    from delight.gui import create_app
    app = create_app()
    app.run(host=host, port=port)


def _get_shell_context():
    from delight.db.session import session
    from delight.gui import create_app
    app = create_app()
    return dict(session=session, app=app)


def interactive_shell(_use_py=True):
    locals().update(**_get_shell_context())
    if not _use_py:
        try:
            import IPython
            IPython.embed()
        except ImportError:
            import code
            code.interact(local=locals())
    else:
        import code
        code.interact(local=locals())


@cli.command()
@click.option('--python', '-p', is_flag=True)
def shell(python):
    """Interactive shell with custom context"""
    interactive_shell(_use_py=python)


if __name__ == '__main__':
    cli()
