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

    if not os.path.exists(app.instance_path):
    raise RuntimeError(
        'Expected instance folder at {p} but could not find!'.format(
            p=app.instance_path)
    )
    if not os.path.exists(app.static_path):
    raise RuntimeError(
        'Expected static folder at {p} but could not find!'.format(
            p=app.static_path)
    )
    app.config.update(
        SECRET_KEY=str(uuid.uuid4()),
        KEY_SHEET='keys.key',
        TIME_STR='%m/%d/%Y %H:%M:%S',
        LOG_FILE=os.path.join(app.instance_path, 'temp.log'),
        UPLOAD_PATH=os.path.join(app.instance_path, 'uploads'),
        USERNAME='USER',
        PASSWORD='PASS'
    )
    config_path = os.path.join(app.instance_path, 'server.cfg'))
    if not os.path.exists(config_path):
        raise RuntimeWarning('No config file present, reverting to defaults.')
    else:
        app.config.from_pyfile(config_path)
    if not os.path.exists(app.config['UPLOAD_PATH']):
        raise RuntimeError(
            'Expected upload path at {p} but could not find!'.format(
                p=app.config['UPLOAD_PATH'])
        )
    if not os.path.exists(app.config['KEY_SHEET']):
        raise RuntimeError(
            'Expected key sheet at {p} but could not find!'.format(
                p=app.config['KEY_SHEET'])
        )

    app.register_blueprint(views)

    return app

