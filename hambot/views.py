import os
import logging

import flask
from flask import current_app as app
from flask_classy import FlaskView, route

from hambot.auth import auth
from hambot.models import Temperature, Image
import hambot.utils as u


class TemperatureLogView(FlaskView):

    route_prefix = '/api/'

    @route('/')
    @route('/max=<int:max_count>')
    def index(self, max_count=None):
        data = Temperature.get_all(max_count)
        if not data:
            return ('', 204)
        rv = [t.to_dict() for t in data]
        return flask.jsonify(rv)

    @route('/chart/')
    @route('/chart/max=<int:max_count>')
    def get_chart(self, max_count=None):
        from pygal import Line

        data = Temperature.get_all(max_count)
        data = [t.to_dict() for t in data]
        chart = Line(x_label_rotation=75)
        chart.x_labels = [t['timestamp'] for t in data]
        chart.add('°C', [float(t['reading']) for t in data])
        return chart.render(is_unicode=True)

    def before_post(self):
        logging.info('Request: POST TemperatureLog')
        for h in flask.request.headers:
            logging.info('  {h}'.format(h=h))
        logging.info('  {d}'.format(d=flask.request.get_json() or 'No data'))

    @auth.login_required
    def post(self):
        data = flask.request.get_json()
        if not data or not data.get('reading'):
            flask.abort(415)
        t = Temperature(
            data['reading'],
            timestamp=u.isostrptime(data.get('timestamp',
                                    u.dtz_now().isoformat())))
        t.save()
        res = flask.make_response('', 201)
        res.headers['Location'] = flask.url_for(
            'TemperatureLogView:index_1', _external=True)
        return res


class ImagesView(FlaskView):

    route_prefix = '/api/'

    @route('/')
    @route('/max=<int:max_count>')
    def index(self, max_count=None):
        data = Image.get_all(max_count)
        if not data:
            return ('', 204)
        rv = [i.to_dict() for i in data]
        return flask.jsonify(rv)

    def get(self, filename):
        return flask.send_from_directory(
            app.config['IMAGE_UPLOAD_PATH'], filename)

    def before_post(self):
        logging.info('Request: POST Image')
        for h in flask.request.headers:
            logging.info('  {h}'.format(h=h))
        logging.info('  {d}'.format(d=flask.request.get_json() or 'No data'))

    @auth.login_required
    def post(self):
        f = flask.request.files.get('file')
        if not f or not f.filename:
            flask.abort(415)
        ext = os.path.splitext(f.filename)[1]
        if not ext == app.config['IMAGE_UPLOAD_EXT']:
            flask.abort(415)
        i = Image.save_from_upload(f)
        res = flask.make_response('', 201)
        res.headers['Location'] = i.url
        return res
