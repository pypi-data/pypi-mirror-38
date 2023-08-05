from setuptools import find_packages, setup

import os

HERE = os.path.abspath(os.path.dirname(__file__))
README_PATH = os.path.join(HERE, 'README.md')
try:
    with open(README_PATH) as fd:
        README = fd.read()
except IOError:
    README = ''


setup(
    name='aioexponent',
    version='0.3.0',
    description='Expo Server SDK for Python Asyncio',
    long_description=README,
    url='https://github.com/Chefclub/exponent-server-sdk-asyncio',
    author='Expo Team',
    author_email='exponent.team@gmail.com',
    license='MIT',
    install_requires=[
        'aiohttp',
    ],
    packages=find_packages(),
    zip_safe=True
)
