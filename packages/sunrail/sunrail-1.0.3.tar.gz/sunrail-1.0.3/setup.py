"""Setup."""

from setuptools import find_packages, setup

setup(
    name='sunrail',
    version='1.0.3',
    description='Provides API wrapper to sunrail.com.',
    url='https://github.com/jcconnell/python-sunrail',
    license='MIT',
    author='jcconnell',
    author_email='jamescarltonconnell@gmail.com',
    packages=find_packages(),
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        ]
)
