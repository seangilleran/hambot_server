import os
import uuid

import flask

from hambot_server.views import views


def create_app(*args, **kwargs):
    """Create a server instance."""

    app = flask.Flask(
        __name__,
        instance_relative_config=True,
        template_folder='',
        *args, **kwargs)

    app.config.update(
        SECRET_KEY=str(uuid.uuid4()),
        KEY_SHEET='keys.key',
        TIME_STR='%m/%d/%Y %H:%M:%S',
        LOG_FILE=os.path.join(app.instance_path, 'temp.log'),
        UPLOAD_PATH=os.path.join(app.instance_path, 'uploads'),
        USERNAME='USER',
        PASSWORD='PASS'
    )

    app.register_blueprint(views)

    return app

