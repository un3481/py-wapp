
# Import Distutils
from distutils.core import setup

setup(
    name='py_misc',
    version='1.3.1',
    license='MIT',
    description='Miscellaneous Library to Simplify Python Code',
    author='anthony',
    url='https://github.com/anthony-freitas/py-misc',
    packages=[
        'py_misc',
        'py_misc/_call',
        'py_misc/_threading',
        'py_misc/_time'
    ]
)