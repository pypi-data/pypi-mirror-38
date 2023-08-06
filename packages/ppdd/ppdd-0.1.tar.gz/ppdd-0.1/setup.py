#!/usr/bin/env python3

from setuptools import setup, find_packages


setup(
    name='ppdd',
    version='0.1',
    description='Place pictures to directories based on date',
    long_description='None',
    author='Sakaki Mirai',
    author_email='oisiitakuwan@gmail.com',
    url='https://github.com/Sakaki/ppdd',
    license='Apache License, Version 2.0',
    packages=find_packages(),
    install_requires=[
        'pillow',
        'click'
    ],
    py_modules=['place_pictures'],
    entry_points='''
        [console_scripts]
        ppdd=place_pictures:main
    '''
)
