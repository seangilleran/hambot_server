import flask

import hambot.utils as u


class Temperature():

    def __init__(
          self, reading, id=u.id(), timestamp=u.now(),
          file_path=flask.current_app.config['TEMPERATURE_LOG_PATH']):
        self.id = id
        self.timestamp = timestamp
        self.reading = reading

    @classmethod
    def from_str(cls, string):
        data = string.strip().split(' ')
        return cls(
            id=data[0],
            timestamp=u.isostrptime(data[1]),
            reading=float(data[2])
        )

    @classmethod
    def get_all(cls):
        rv = []
        with open(self.file_path) as f:
            lines = f.readlines()
        for line in lines:
            rv.append(cls.from_str(line))
        return rv or None

    def to_dict(self):
        return dict(
            id=self.id,
            timestamp=self.timestamp,
            reading=self.reading,
            uri=self.get_uri()
        )

    def get_uri(self):
        return flask.url_for(
            'TemperatureLogView:get', id=self.id, _external=True)

    def save(self):
        with open(self.file_path, 'a') as f:
            f.write(str(self) + os.linesep)

    def __str__(self):
        return '{id} {timestamp} {reading}\n'.format(
            id=self.id, timestamp=self.timestamp.isoformat(),
            reading=str(self.reading)
        )

    def __repr__(self):
        return '<Temperature {id}>'.format(id=self.id)


class Image(db.Model):

    def __init__(
          self, filename,
          upload_path=flask.current_app.config['IMAGE_UPLOAD_PATH'],
          ext=flask.current_app.config['IMAGE_UPLOAD_EXT']):
        name, ext = os.path.splitext(filename)
        self.filename = filename
        self.url = flask.send_from_directory(
            os.path.join(upload_path, filename))
        self.timestamp = u.fromtimestamp(os.path.getmtime(path))

    @classmethod
    def save_from_upload(cls, f):
        filename = u.id() + self.ext
        f.save(os.path.join(self.upload_path, filename))
        return cls(filename)

    @classmethod
    def get_all(cls):
        rv = []
        for f in os.listdir(upload_path):
            name, ext = os.splitext(f)
            if ext == self.ext:
                rv.append(cls(f))
        return rv or None

    def to_dict(self):
        return dict(
            image_url=self.url, timestamp=self.timestamp,
            uri=self.get_uri()
        )

    def get_uri(self):
        return flask.url_for(
            'ImagesView:get', filename=self.filename, _external=True)

    def __repr__(self):
        return '<Image {path}>'.format(
            path=os.path.join(self.upload_path, self.filename))
