import json
from setuptools import setup

with open('requirements.txt') as f:
    requirements = list(filter(lambda x: not not x, map(lambda x: x.strip(), f.readlines())))

with open('info.json') as f:
    info = json.load(f)

setup(
    name='volcano-mbsrv',
    version=info['version'],
    description='Modbus server satellite for Volcano',
    author='Vinogradov D',
    author_email='dgrapes@gmail.com',
    license='MIT',
    packages=['volcano.mbsrv'],
    install_requires=requirements,
    zip_safe=False
)
