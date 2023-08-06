from setuptools import setup, find_packages
from setuptools.command.develop import develop
from setuptools.command.install import install
from subprocess import check_call

import os

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))


class PostDevelopCommand(develop):
    def run(self):
        with open(os.devnull, "w") as f:
            check_call('{}'.format(os.path.join(PROJECT_DIR, 'postinstall.sh')), stdout=f, stderr=f)
        develop.run(self)


class PostInstallCommand(install):
    def run(self):
        with open(os.devnull, "w") as f:
            check_call('{}'.format(os.path.join(PROJECT_DIR, 'postinstall.sh')), stdout=f, stderr=f)
        install.run(self)


with open('README.md', "r") as readme:
    long_description = readme.read()

setup(
    name="py-img-editor",
    version="0.0.2",
    author="Kimball Leavitt",
    author_email="kimballleavitt@gmail.com",
    description="Image editor using Python, uWSGI, and Pillow",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kimballo/py-img-editor",
    package_data={'': ['uwsgi.ini', 'postinstall.sh', 'index.py']},
    packages=find_packages(),
    include_package_data=True,
    cmdclass={
        'develop': PostDevelopCommand,
        'install': PostInstallCommand,
    },
    entry_points={
        'console_scripts': [
            'py-img-editor = py_img_editor:main',
        ],
    },
    install_requires=[
       'Pillow==5.3.0'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)
