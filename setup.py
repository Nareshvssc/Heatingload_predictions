
from setuptools import setup,find_packages
from typing import List

NAME = "HeatingloadsPredictions"
VERSION = '1.0'
DESCRIPTION = 'This is Heating and cooling load prediction project \
               done to complete internship'
AUTHOR = 'NARESH KUMAR SINGH'

REQUIREMENTS_FILE = 'requirements.txt'

def get_packages()-> List[str]:
    with open(REQUIREMENTS_FILE,'r') as file:
        libraries = [x.replace("\n","") for x in file.readlines()]
    if '-e .' in libraries:
        libraries.remove('-e .')
    return libraries

setup(
name= NAME,
version = VERSION,
description=  DESCRIPTION,
author= AUTHOR,
packages = find_packages(),
install_requires = get_packages()
)

if __name__ == '__main__':
    print(get_packages())
