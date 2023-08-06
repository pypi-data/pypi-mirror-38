import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-chatter',
    version='0.0.4',
    packages=find_packages(),
    include_package_data=True,
    license='BSD License',
    description='A responsive Chat web app package for Django 2.0+',
    long_description=README,
    url='https://github.com/dibs-devs/chatter',
    author='Ahmed Ishtiaque',
    author_email='ahmedishti27@gmail.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 2.0',  # replace "X.Y" as appropriate
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',  # example license
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    install_requires=[
        'django>=2.0.5',
        'channels',
        'shortuuid',
        'bleach',
        'channels_redis',
        'django-notifications-hq',

    ],
)
