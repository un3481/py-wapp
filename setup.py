
# Import Distutils
from distutils.core import setup

setup(
    name='py_wapp',
    version='2.1.0',
    license='MIT',
    description='HTTP Rest API for Whatsapp Bot',
    author='anthony',
    url='https://github.com/melon-yellow/py-wapp',
    packages=[
        'py_wapp'
    ],
    install_requires=[
        'requests',
        'unidecode',
        'py_misc @ git+https://github.com/un3481/py-misc#egg=py-misc' 
    ]
)
