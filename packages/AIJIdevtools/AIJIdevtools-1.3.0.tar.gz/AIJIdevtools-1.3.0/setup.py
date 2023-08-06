#!/bin/python3
from setuptools import setup
from setuptools import find_packages

NAME = "devtools"
PACKAGES = [NAME] + ["%s.%s" % (NAME, i) for i in find_packages(NAME)]
# print(PACKAGES)

setup(
    name='AIJIdevtools',
    version='1.3.0',
    author='AIJI',
    author_email='thecrazyaiji@gmail.com',
    description='Some useful helper-funcs for devpers',
    packages=PACKAGES,
    install_requires=[
        'sh',
        'sqlparse',
        'termcolor',
    ],
    url='https://github.com/AIJIJI/devtools',
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Development Status :: 1 - Planning"
    ]
)
