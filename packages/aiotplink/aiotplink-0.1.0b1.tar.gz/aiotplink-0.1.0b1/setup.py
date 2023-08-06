#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import setuptools

version = '0.1.0b1'
package = 'aiotplink'

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(name=package,
    packages=[package],
    version=version,
    author='François Wautier',
    author_email='francois@wautier.eu',
    description='API for local communication with TP-Link Smart Plugs devices over a LAN with asyncio.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='http://github.com/frawau/'+package,
    download_url='https://github.com/frawau/'+package+'/archive/'+version+'.tar.gz',
    keywords = ['TP-Link', 'IoT', 'switch', 'Smart Plug', 'automation'],
    license='MIT',
    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5'
    ])
