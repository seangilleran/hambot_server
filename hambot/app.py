import os
import uuid
import logging

import flask
from enigma_operator import EnigmaOperator

from hambot.auth import auth
import hambot.models as models
import hambot.views as views


def create_app(*args, **kwargs):
    """Create a server instance."""

    app = flask.Flask(
        __name__,
        instance_relative_config=True,
        static_url_path='',
        *args, **kwargs)
    if not os.path.exists(app.instance_path):
        os.makedirs(app.instance_path)
    app.config.update(
        DEBUG=True,
        SERVER_LOG_PATH=os.path.join(app.instance_path, 'server.log'),
        SECRET_KEY=str(uuid.uuid4()),
        TEMPERATURE_LOG_PATH=os.path.join(app.instance_path, 'temp.log'),
        IMAGE_UPLOAD_PATH=os.path.join(app.instance_path, 'uploads'),
        IMAGE_UPLOAD_EXT='.jpg',
        AUTH_KEY_PATH=os.path.join(app.instance_path, 'enigma.key'),
        AUTH_TOKEN='ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    )
    config_path = os.path.join(app.instance_path, 'server.cfg')
    if not os.path.exists(config_path):
        raise RuntimeError(
            'Expected config file at {p} but could not find!'.format(
                p=config_path))
    app.config.from_pyfile(config_path)
    if not os.path.exists(app.config['IMAGE_UPLOAD_PATH']):
        os.makedirs(app.config['IMAGE_UPLOAD_PATH'])
    if not os.path.exists(app.config['TEMPERATURE_LOG_PATH']):
        with open(app.config['TEMPERATURE_LOG_PATH'], 'a+') as f:
            f.close()

    logging.basicConfig(
        level=logging.DEBUG if app.debug else logging.INFO,
        format='%(asctime)s %(levelname)s %(message)s',
        filename=app.config['SERVER_LOG_PATH'],
        filemode='a+')
    logging.getLogger('').addHandler(logging.StreamHandler())

    models.init_app(app)

    @auth.verify_token
    def verify_token(token):
        from string import ascii_uppercase
        from re import sub

        # Override encryption for debug mode.
        if app.debug and token == app.config['AUTH_TOKEN']:
            return True

        e = EnigmaOperator(app.config['AUTH_KEY_PATH'], int(token[:2]))
        ciphertext = sub('[^A-Z]', '', token[2:].strip())
        if not ciphertext:
            return False
        plaintext = e.decrypt(ciphertext)
        if ciphertext == app.config['AUTH_TOKEN']:
            return True
        return False

    views.TemperatureLogView.register(app)
    views.ImagesView.register(app)

    return app
