
# Import Distutils
from distutils.core import setup

setup(
    name='py_wapp',
    version='2.0.7',
    license='MIT',
    description='HTTP Rest API for Whatsapp Bot',
    author='anthony',
    url='https://github.com/anthony-freitas/py-wapp',
    packages=[
        'py_wapp',
        'py_wapp/modules'
    ],
    install_requires=[
        'py_misc @ git+https://github.com/anthony-freitas/py-misc#egg=py-misc',
        'unidecode',
        'requests'
    ]
)