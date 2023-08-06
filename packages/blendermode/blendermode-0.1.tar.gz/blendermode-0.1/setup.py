#!/usr/bin/env python
from distutils.core import setup

setup(
    name = 'blendermode',
    packages = [
        'blendermode'],
    version = '0.1',
    description = 'Automatic keyboard shortcut remapping when working in Blender',
    author = 'Contracode',
    author_email = 'contracode@protonmail.com',
    url = 'https://gitlab.com/contracode/blendermode',
    install_requires=[],
    entry_points={
        'console_scripts': [
            'blendermode = blendermode.main:main',
        ]
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: Unix',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
    ],
)

