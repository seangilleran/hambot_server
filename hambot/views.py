import flask
from flask import current_app as app
from flask_classy import FlaskView

from hambot.models import Temperature, Image
import hambot.utils as u


class TemperatureLogView(FlaskView):

    def index(self):
        rv = Temperature.get_all()
        if not rv:
            return ('', 204)
        return flask.jsonify(rv)

    def get(self, id):
        rv = None
        for t in Temperature.get_all():
            if t.id == id:
                rv = t
                break
        if not rv:
            flask.abort(404)
        return flask.jsonify(rv.to_dict())

    def post(self):
        data = flask.get_json()
        if not data.get('reading'):
            flask.abort(415)
        t = Temperature(
            data['reading'],
            timestamp=u.isostrptime(data.get('timestamp',
                                    u.now().isoformat()))
        )
        t.save()
        res = flask.make_response('', 201)
        res.headers['Location'] = t.get_uri()
        return res


class ImagesView(FlaskView):

    def index():
        rv = Images.get_all()
        if not rv:
            return ('', 204)
        return flask.jsonify(rv)

    def get(self, filename):
        rv = None
        for i in Images.get_all():
            if i.filename == filename:
                rv = i
                break
        if not rv:
            flask.abort(404)
        return flask.jsonify(rv.to_dict())

    def post(self):
        f = flask.request.files.get('file')
        ext = os.path.splitext(f.filename)[1]
        if not f or not ext == app.config[IMAGE_UPLOAD_EXT]:
            flask.abort(415)
        i = Image.save_from_upload(f)
        res = flask.make_response('', 201)
        res.headers['Location'] = i.get_uri()
        return res
