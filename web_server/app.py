from flask import Flask, render_template, request, flash, redirect, url_for, g
from flask.ext.bootstrap import Bootstrap
import requests
import MySQLdb
import time
import json


SQL_DB = 'thesis'
SQL_TABLE = 'power'

IP_SERVICE = 'http://ipv4.icanhazip.com'

app = Flask(__name__)
app.config['SECRET_KEY'] = 'null'
bootstrap = Bootstrap(app)

@app.before_request
def before_request():
    g.db = MySQLdb.connect(host='localhost', user='root',
                           passwd='raspberry', db=SQL_DB)
    g.cur = g.db.cursor()

@app.teardown_request
def teardown_request(exception):
    cur = getattr(g, 'cur', None)
    if cur is not None:
        cur.close()
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()


@app.route('/', methods=['GET', 'POST'])
def index():
    req = request.args.get('time', None)
    if req:
        print req
        g.cur.execute("""SELECT * FROM {} WHERE datetime >= (NOW() - INTERVAL {})""".format(SQL_TABLE, req))
        data = g.cur.fetchall()
        arr_send = [[str(time.mktime(i[0].timetuple())), str(int(i[1])), str(int(i[2]))]
                    for i in data]
        data_send = json.dumps(arr_send)
        return data_send
    else:
        flash('Current threshold: {}'.format(int(json.loads(init_gui())['thresh']))) 
        return render_template('index.html', number=666)

@app.route('/setvals', methods=['GET', 'POST'])
def set_config():
    recv_conf = {key: val for key, val in request.form.items()}
    print recv_conf
    with open('data/gui.conf', 'r') as f:
        prev_data = json.loads(f.read())
    if prev_data != recv_conf:
        with open('data/gui.conf', 'w') as f:
            f.write(json.dumps(recv_conf))
    return ('', 204)

@app.route('/initvals', methods=['GET', 'POST'])
def init_gui():
    with open('data/gui.conf', 'r') as f:
        ret_conf = json.loads(f.read())
    return json.dumps(ret_conf)

@app.route('/publicip')
def get_public_ip():
    public_ip = requests.get(IP_SERVICE).content.strip('\n')
    print 'Public IP:', public_ip
    return json.dumps(public_ip)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')