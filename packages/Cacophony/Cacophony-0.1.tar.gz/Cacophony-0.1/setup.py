"""
Cacophony
-------------

Framework for handling events from Slack/Discord/etc
"""
from setuptools import setup


setup(
    name='Cacophony',
    version='0.1',
    url='https://gitlab.com/deepy/cacophony',
    license='BSD',
    author='Alex Nordlund',
    author_email='deep.alexander@gmail.com',
    description='Framework for handling events from Slack/Discord/etc',
    long_description=__doc__,
    packages=['flask_cacophony'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        'Flask'
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)