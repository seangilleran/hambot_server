from setuptools import setup


setup(
    name='hambot-server',
    version='0.4',
    license='MIT',
    author='Sean Gilleran',
    author_email='sgilleran@gmail.com',
    url='https://github.com/seangilleran/hambot_server',
    download_url='https://github.com/seangilleran/hambot_server/tarball/0.4',
    packages=['hambot'],
    install_requires=[
        'click>=6.6',
        'Flask>=0.11.1',
        'Flask-Classy>=0.6.10',
        'Flask-HTTPAuth>=3.1.2',
        'itsdangerous>=0.24',
        'Jinja2>=2.8',
        'MarkupSafe>=0.23',
        'py-enigma>=0.1',
        'py-enigma-operator>=0.6',
        'pygal>=2.2.3',
        'pytz>=2016.6',
        'tzlocal>=1.2.2',
        'Werkzeug>=0.11.10'],
    include_package_data=True,
    zip_safe=False
)
