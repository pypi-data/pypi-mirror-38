import sys

from setuptools import setup

if sys.version_info < (3, 6):
    raise ImportError('cryptology-ws-client-python only supports python3.6 and newer')

setup(
    name='cryptology-ws-client',
    version='1.1.1',
    description='Cryptology webscoket client',
    author='Cryptology',
    author_email='s.prikazchikov@cryptology.com',
    packages=['cryptology'],
    python_requires='>= 3.6',
    install_requires=[
        'aiodns',
        'aiohttp >= 2.3.6',
        'cchardet',
    ],
    extras_require={
        'devel': ['pytz',
                  'pytest-aiohttp'
                  ]
    },
    url='https://github.com/CryptologyExchange/cryptology-ws-client-python',
)
