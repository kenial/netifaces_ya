#!/usr/bin/env python
# -*- coding: utf-8 -*-
from distutils.core import setup
 
setup(
    name='netifaces_ya',
    version='0.11',
    description='Provides network interface information by simple methods. Network interface name, activated interface`s IP address, netmask, MAC address and broadcast IP are provided.',
    author='Kenial Lee',
    url='http://github.com/kenial/netifaces_ya',
    package_dir={'': 'src'},
    py_modules=[
        'netifaces_ya',
    ],
)