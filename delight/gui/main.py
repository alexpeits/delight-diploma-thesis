"""

Delight gui main page views
~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""

from multiprocessing.connection import Client

from flask import Blueprint, render_template, request, redirect, url_for

from delight.utils.ipc import send


main = Blueprint('main', __name__, static_folder='./static/main')


@main.route('/')
def index():
    return render_template('main/index.html')


# debug ipc
@main.route('/submit', methods=['GET', 'POST'])
def submit():
    a = request.form.get('sample')
    send(a)
    return redirect(url_for('main.index'))
