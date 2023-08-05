"""
Flask-sshtunnel
-------------

This package lets you easily integrate the sshtunnel into your app. I find it useful for test-cases against read-only
databases.
"""
from setuptools import setup


setup(
    name='Flask-sshtunnel',
    version='0.1b1',
    url='https://github.com/heyoni/flask-tunnel',
    license='MIT',
    author='Jonathan Revah',
    author_email='jrevah@gmail.com',
    description='sshtunnel extension for flask',
    long_description=__doc__,
    py_modules=['flask_sshtunnel'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        'Flask',
        'sshtunnel'
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Flask',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)