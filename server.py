import os

import flask
import pygal
from werkzeug.utils import secure_filename

from models import CamPhoto, LogEntry


app = flask.Flask(__name__)
app.config.update(
    TIME_STR="%m/%d/%Y %H:%M:%S",
    UPLOAD_FOLDER=os.path.join(app.instance_path, "uploads"),
    UPLOAD_EXT=set([".jpg", ".jpeg"])
)


@app.route("/")
def index():
    return flask.render_template(
        "index.htm",
        images=CamPhoto.get_all(app.config["UPLOAD_FOLDER"]),
        temp_log=LogEntry.get_all(os.path.join(app.instance_path, "temp.log")),
        time_str=app.config["TIME_STR"]
    )


@app.route("/cam_imgs/", methods=["POST"])
def post_cam_img():
    f = request.files.get("file")
    if (not f or f.filename == "" or
       not os.path.splitext(f.filename)[1] in app.config["UPLOAD_EXT"]):
        flask.abort(400)
    filename = secure_filename(f.filename)
    f.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
    return flask.jsonify(dict(status="success")), 201


@app.route("/cam_imgs/<filename>")
def get_cam_img(filename):
    return flask.send_from_directory(app.config["UPLOAD_FOLDER"], filename)


@app.route("/time_str/")
def get_time_str():
    return flask.jsonify(dict(temp_str=app.config["TIME_STR"]))


@app.route("/temp_logs/")
def get_temp_logs():
    return flask.jsonify([dict(
        timestamp=l.timestamp,
        temp=l.temperature
    ) for l in LogEntry.get_all(os.path.join(app.instance_path, "temp.log"))])


@app.route("/temp_logs/", methods=["POST"])
def post_temp_logs():
    data = flask.request.get_json()
    if (not data.get("time_str") or not data.get("timestamp") or
       not data.get("temp")):
        flask.abort(400)
    LogEntry.add_new(
        os.path.join(app.instance_path, "temp.log"),
        LogEntry.from_dict(data)
    )
    return flask.jsonify(dict(status="success")), 201


@app.route("/temp_logs/chart/")
def get_temp_chart():
    data = LogEntry.get_latest(os.path.join(app.instance_path, "temp.log"))
    chart = pygal.Line(x_label_rotation=75)
    chart.x_labels = map(
        lambda d: d.strftime(app.config["TIME_STR"]),
        [t.timestamp for t in data]
    )
    chart.add("Temperature", [t.temperature for t in data])
    return chart.render(is_unicode=True)


if __name__ == "__main__":
    app.run()
