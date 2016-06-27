"""

Delight gui main page views
~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""

from flask import Blueprint


main = Blueprint('main', __name__, static_folder='./static/main')
