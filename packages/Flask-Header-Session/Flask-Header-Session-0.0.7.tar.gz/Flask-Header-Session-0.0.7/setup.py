"""
Flask-Session
-------------

Flask-Session is an extension for Flask that adds support for 
Server-side Session to your application.

This variation uses a header instead of cookie as message vehicle.

So that you can tell the client to set session on headers, and later 
verify the header value to identify different users.

"""
from setuptools import setup


setup(
    name='Flask-Header-Session',
    version='0.0.7',
    url='https://github.com/laalaguer/flask-session',
    license='BSD',
    author='Xiqing Chu',
    author_email='laalaguer@gmail.com',
    description='Flask server side session via HTTP header',
    long_description=__doc__,
    packages=['flask_header_session'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        'Flask>=0.8'
    ],
    test_suite='test_session',
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
