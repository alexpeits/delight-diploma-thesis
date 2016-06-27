"""
Delight gui app factory
~~~~~~~~~~~~~~~~~~~~~~~

"""

from flask import Flask

from delight.config import GUIConfig
from delight.gui.main import main


def create_app():
    app = Flask(__name__)
    app.config.from_object(GUIConfig)
    app.register_blueprint(main)
    return app
