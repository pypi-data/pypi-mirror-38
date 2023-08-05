from setuptools import *

with open('README.md', 'r') as file:
    longDesc = file.read()

setup(name='arithmetic-graphing',
    version='0.0.9',
    description='A small arithmetic module for functions of graphing',
    long_description=longDesc,
    long_description_content_type="text/markdown",
    author='TheOnlyWalrus',
    license='MIT',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Development Status :: 1 - Planning',
        'Topic :: Education',
        'Intended Audience :: Education'
    ],
)