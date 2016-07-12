from setuptools import setup

setup(
    name='hambot-server',
    version='0.2',
    license='MIT',
    author='Sean Gilleran',
    author_email='sgilleran@gmail.com',
    url='https://github.com/seangilleran/hambot_server',
    download_url='https://github.com/seangilleran/hambot_server/tarball/0.6',
    packages=['hambot_server'],
    install_requires=[
        'Flask>=0.11',
        'Flask-HTTPAuth',
        'hashids',
        'pygal',
        'py-enigma-operator'],
    include_package_data=True,
    zip_safe=False
)

