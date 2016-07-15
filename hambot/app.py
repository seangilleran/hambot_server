import os
import uuid

import flask

import hambot.views as views


def create_app(*args, **kwargs):
    """Create a server instance."""

    app = flask.Flask(
        __name__,
        instance_relative_config=True,
        *args, **kwargs)
    app.config.update(
        SECRET_KEY=str(uuid.uuid4()),
        TEMPERATURE_LOG_PATH=os.path.join(app.instance_path, 'temp.log'),
        IMAGE_UPLOAD_PATH=os.path.join(app.instance_path, 'uploads'),
        IMAGE_UPLOAD_EXT='.jpg')

    if not os.path.exists(app.instance_path):
        os.makedirs(app.instance_path)
    if not os.path.exists(app.config['IMAGE_UPLOAD_PATH']):
        os.makedirs(app.config['IMAGE_UPLOAD_PATH'])
    if not os.path.exists(app.config['TEMPERATURE_LOG_PATH']):
        with open(app.config['TEMPERATURE_LOG_PATH'], 'a+') as f:
            f.close()

    views.TemperatureLogView.register(app)
    views.ImagesView.register(app)

    return app
