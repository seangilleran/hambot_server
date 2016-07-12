import os
import pygal
from time import time

import flask
from flask import current_app as app
from flask_httpauth import HTTPBasicAuth
from hashids import Hashids
from enigma_operator import EnigmaOperator

from hambot_server.models import CamPhoto, LogEntry


views = flask.Blueprint('views', __name__)
auth = HTTPBasicAuth()


@views.before_request
def write_to_log():
    if app.config.get('LOG_FILE'):
        lines = []
        for k, v in flask.request.headers.items():
            lines.append(k + ': ' + v)
        path = os.path.join(app.instance_path, app.config['LOG_FILE'])
        with open(path, 'a+') as f:
            f.writelines(lines)


@views.route('/')
def index():
    """GET index page."""

    return flask.render_template(
        'index.htm',
        images=CamPhoto.get_all(app.config['UPLOAD_PATH'])[-4:],
        temp_log=LogEntry.get_all(app.config['TEMP_LOG']),
        time_str=app.config['TIME_STR']
    )


@views.route('/time_str/')
def time_str():
    """GET the server's current time format string."""

    return flask.jsonify(time_str=app.config['TIME_STR'])


@views.route('/images/', methods=['GET'])
def images():
    """GET an index of uploaded images."""

    images = CamPhoto.get_all(app.config['UPLOAD_PATH'])[-4:]
    return flask.jsonify([dict(
        url=flask.url_for('views.image', filename=i.path)) for i in images])


@views.route('/images/', methods=['POST'])
@auth.login_required
def post_image():
    """POST an image from the webcam client."""

    f = flask.request.files.get('file')
    filename, ext = os.path.splitext(f.filename)
    if not f or f.filename == '' or ext != '.jpg':
        flask.abort(400)

    filehash = Hashids(app.config['SECRET_KEY']).encode(int(time()))
    f.save(os.path.join(app.config['UPLOAD_PATH'], filehash + ext))
    
    return flask.jsonify(dict(status='success')), 201


@views.route('/images/<filename>')
def image(filename):
    """GET an uploaded image by filename."""
    
    return flask.send_from_directory(app.config['UPLOAD_PATH'], filename)


@views.route('/log/')
def log():
    """GET a json string of all current temperature log entries."""

    return flask.jsonify([dict(
        timestamp=l.timestamp,
        temp=l.temperature
    ) for l in LogEntry.get_all(os.config['TEMP_LOG'])])


@views.route('/log/', methods=['POST'])
@auth.login_required
def post_log():
    """POST a new entry to the temperature log."""

    data = flask.request.get_json()
    if not data.get('timestamp') or not data.get('temp'):
        flask.abort(400)

    LogEntry.add_new(app.config['TEMP_LOG'], LogEntry.from_dict(data))

    return flask.jsonify(dict(status='success')), 201


@views.route('/log/chart/')
def log_chart():
    """Use PyGal to GET an svg chart of the latest log data."""

    data = LogEntry.get_latest(app.config['TEMP_LOG'])

    chart = pygal.Line(x_label_rotation=75)
    chart.x_labels = map(
        lambda d: d.strftime(app.config['TIME_STR']),
        [t.timestamp for t in data]
    )
    chart.add('Temperature', [t.temperature for t in data])

    return chart.render(is_unicode=True)


@auth.verify_password
def verify_password(username, password):
    """Use light Enigma-style encryption to check password."""

    e = EnigmaOperator(os.path.join(app.instance_path, 'gelheim.key'))
    plaintext = e.decrypt(password)

    if (not username == app.config['USERNAME'] or
       not plaintext == app.config['PASSWORD']):
       return False
    return True

