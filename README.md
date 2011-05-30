netifaces_ya (netifaces, yet another)
====

Provides network interface information by simple methods.
Network interface name, 'activated' interface`s IP address, netmask, MAC address and broadcast IP are provided. 

This pure python module is for providing network interface information instantly.
Basically, similar to [netifaces](http://pypi.python.org/pypi/netifaces) .


Supports Mac OS X and Windows.
(Tested on Mac OS X 10.6.7 and Windows 2003/2008, python 2.6/2.7)


Usage:

    # 'xxx_first_xxx' method is returning only one item, as following
    print netifaces_ya.get_active_first_IP()

    # Be able to get only 'activated'(in other words, 'connected') item
    print netifaces_ya.get_active_IPs()     # returns list
 
    # get every network interface information
    interfaces = netifaces_ya.get_interfaces()
    for interface_name in interfaces:
        print interface_name
        print netifaces_ya.get_interface_info(interface_name)


Reporting Issues
--------

If you have bugs or other issues, file them [here][issues].


