from setuptools import setup

setup(
    name='hambot-server',
    version='0.1',
    license='MIT',
    author='Sean Gilleran',
    author_email='sgilleran@gmail.com',
    url='https://github.com/seangilleran/hambot_server',
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

