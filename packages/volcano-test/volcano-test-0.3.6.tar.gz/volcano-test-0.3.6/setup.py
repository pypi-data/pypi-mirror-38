from setuptools import setup

import json

with open('info.json') as f:
    info = json.load(f)

setup(
    name='volcano-test',
    version=info['version'],
    description='Volcano test kit',
    author='Vinogradov D',
    author_email='dgrapes@gmail.com',
    license='MIT',
    packages=['volcano.test'],
    zip_safe=False,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)
