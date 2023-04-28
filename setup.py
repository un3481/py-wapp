
# Import Distutils
from distutils.core import setup

setup(
    name='py_wapp',
    version='2.4.0',
    license='MIT',
    description='Python client for ts-wapp.js',
    author='anthony',
    url='https://github.com/un3481/py-wapp',
    packages=[
        'py_wapp'
    ],
    install_requires=[
        'requests',
        'unidecode',
        'flask',
        'flask_httpauth'
    ]
)
