from distutils.core import setup
from setuptools import find_packages

setup(
    name='kiprotect',
    version='0.1',
    author='KIProtect GbR',
    author_email='pypi@kiprotect.com',
    license='BSD-3',
    url='https://github.com/KIProtect/kiprotect-python',
    packages=find_packages(),
    package_data={'': ['*.ini']},
    include_package_data=True,
    install_requires=['six'],
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'kiprotect = kiprotect.commands:kiprotect'
        ]
    },
    description='Python bindings to the KIProtect API.',
    long_description="""KIProtect is an API for secure, privacy-preserving data science and machine learning.

It provides state-of-the-art methods for protecting data via anonymization and pseudonymization.
"""
)
