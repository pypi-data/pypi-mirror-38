import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as rf:
    README = rf.read()

os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-inbox',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    license='MIT',
    description=['A not live messaging system that simulates an email inbox'],
    long_description=README,
    url='https://gitlab.com/polrodoreda/django-inbox',
    author='Pol Rodoreda Valeri',
    author_email='pol_rodoreda@hotmail.com',
    install_requires=[
        'Django>=2.0'
    ]
)
