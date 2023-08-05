import os
from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    README = f.read()

setup(
    name='django-graphql-framework',
    version='0.1.1',
    packages=['graphql_framework'],
    description='A simple, plug-and-play GraphQL library for Django',
    long_description=README,
    author='Jayden Windle',
    author_email='jaydenwindle@gmail.com',
    url='https://github.com/jaydenwindle/django-graphql-framework/',
    license='MIT',
    install_requires=[
        'Django>=1.11',
    ]
)