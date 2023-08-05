import os
import re
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()


def get_packages(package):
    """
    Return root package and all sub-packages.
    """
    return [dirpath for dirpath, dirnames, filenames in os.walk(package) if os.path.exists(os.path.join(dirpath, '__init__.py'))]


version = '1.13.0'

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-apollo-forms',
    version=version,
    url='https://morgan-and-morgan.github.io/apollo/',
    packages=get_packages('apollo'),
    include_package_data=True,
    license='BSD License',
    description='Simple CMS for forms',
    long_description=README,
    install_requires=[
        'djangorestframework>=3.7,<4',
        'django-filter>=1,<2',
        'django-rest-swagger>=2,<3'
    ],
    author='Morgan & Morgan Developers',
    author_email='developers@forthepeople.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.9',
        'Framework :: Django :: 1.10',
        'Framework :: Django :: 1.11',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',  # example license
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)