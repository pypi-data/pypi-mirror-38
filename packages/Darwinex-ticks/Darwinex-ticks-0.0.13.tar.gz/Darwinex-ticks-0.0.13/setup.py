import os
from setuptools import setup, find_packages

DESCRIPTION = 'Darwinex tick data downloader Python API'
# ere = os.path.abspath(os.path.dirname(__file__))

try:
    with open('README.md') as f:
        long_description = f.read()
except FileNotFoundError:
    long_description = DESCRIPTION

setup(
    name='Darwinex-ticks',
    version='0.0.13',
    packages=find_packages(),
    url='https://github.com/paduel/darwinex_ticks',
    license='MIT',
    author='Paduel',
    author_email='paduel@gmail.com',
    install_requires=['pandas'],
    description=DESCRIPTION,
    # long_description='Visit [GitHub repo]('
    #                  'https://github.com/paduel/Darwinex-ticks) for more '
    #                  'information',
    long_description=long_description,
    long_description_content_type='text/markdown',
)
