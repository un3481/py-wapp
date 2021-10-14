
# Import Distutils
from distutils.core import setup

setup(
    name='py_wapp',
    version='1.0.7',
    license='MIT',
    description='Python Miscellaneous Library',
    author='anthony',
    url='https://github.com/anthony-freitas/py-misc',
    packages=[
        'py_misc',
        'py_misc/_call',
        'py_misc/_threading',
        'py_misc/_time'
    ]
)