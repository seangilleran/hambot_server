import os
import logging

import flask

import hambot.utils as u


def init_app(app):
    Temperature.file_path = app.config['TEMPERATURE_LOG_PATH']
    Image.upload_path = app.config['IMAGE_UPLOAD_PATH']
    Image.ext = app.config['IMAGE_UPLOAD_EXT']


class Temperature():

    file_path = ''

    def __init__(self, reading, timestamp=u.dtz_now()):
        self.timestamp = timestamp
        self.reading = reading

    @classmethod
    def get_all(cls, max_count=None):
        rv = []
        with open(cls.file_path) as f:
            lines = filter(None, (line.rstrip() for line in f.readlines()))
            for line in lines:
                timestamp, reading = line.strip().split(' ')
                rv.append(cls(timestamp=timestamp, reading=reading))
        if max_count:
            del rv[:-max_count]
        logging.debug('Retrieved {n} log entries from {p}'.format(
            n=len(rv), p=cls.file_path))
        return rv or None

    def to_dict(self):
        return dict(
            timestamp=self.timestamp, reading=self.reading)

    def save(self):
        with open(self.file_path, 'a') as f:
            f.write(str(self) + os.linesep)
        logging.info('Saved new temperature log entry to {p}'.format(
            p=self.file_path))

    def __str__(self):
        return '{timestamp} {reading}'.format(
            timestamp=self.timestamp.isoformat(),
            reading=str(self.reading)
        )


class Image():

    upload_path = ''
    ext = ''

    def __init__(self, filename):
        from flask import url_for

        self.filename = filename
        self.url = url_for(
            'ImagesView:get', filename=self.filename, _external=True),
        self.timestamp = u.dtz_from_time(
            os.path.getmtime(os.path.join(self.upload_path, filename)))

    @classmethod
    def save_from_upload(cls, f):
        from werkzeug.utils import secure_filename

        filename = secure_filename(f.filename)
        f.save(os.path.join(self.upload_path, filename))
        logging.info('Saved new image to {p}'.format(
            p=os.path.join(self.upload_path, filename)))
        return cls(filename)

    @classmethod
    def get_all(cls, max_count=None):
        rv = []
        for f in os.listdir(cls.upload_path):
            if os.path.splitext(f)[1] == cls.ext:
                rv.append(cls(f))
        rv.sort(key=lambda i: i.timestamp)
        if max_count:
            del rv[:-max_count]
        logging.debug('Retrieved {n} images from {p}'.format(
            n=len(rv), p=cls.upload_path))
        return rv or None

    def to_dict(self):
        return dict(
            url=self.url,
            timestamp=self.timestamp,
        )

    def __repr__(self):
        return '<Image {path}>'.format(
            path=os.path.join(self.upload_path, self.filename))
