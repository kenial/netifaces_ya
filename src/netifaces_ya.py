# netifaces_ya (netifaces Yet Another ver.) 0.01
#
# Created on May 28, 2011
# @author: kenial (keniallee-NOSPAM-PLEASE@gmail.com)


#! /usr/bin/env python
#encoding:UTF-8

'''
Provides network interface information by simple methods.
Network interface name, 'activated' interface`s IP address, netmask, MAC address and broadcast IP are provided. 


This module supports IPv4 only.
Tested on Mac OS X 10.6.7 and Windows 2003/2008

Test on other unix-like platforms is needed. Would you give me a hand?


* This module doesn't use C program module, 
  so you can utilize this module by just copy-and-paste.
'''



        
import os
import sys

class netifaces_ya:
    '''netifaces-like module provides network interface information.
This returns interface name, IP, netmask, MAC address, and etc. This module use command line utility like ifconfig and ipconfig rather than native C program module.'''
    
    __interfaces = []
    __interfaces_info = {}
    __host_info = {}
    platform = 0
    
    @staticmethod
    def get_interfaces():
        if(len(netifaces_ya.__interfaces) == 0):
            netifaces_ya.fill_interfaces()
        return netifaces_ya.__interfaces
        
    @staticmethod
    def get_interface_info(ifname):
        if(len(netifaces_ya.__interfaces) == 0):
            netifaces_ya.fill_interfaces()
        return netifaces_ya.__interfaces_info[ifname]        
    
    @staticmethod
    def fill_interfaces():
        # for Mac OS X
        a_interface = None
        interface_name = None
        netifaces_ya.__host_info["platform"] = sys.platform
        netifaces_ya.__host_info["platform"] = 'nt'
        if(netifaces_ya.__host_info["platform"] == 'darwin'):
            # warning : review for another version of Mac OS X needed!
            # if(platform.mac_ver()[0] == "10.6.7"):

            # A interface of information from ifconfig will be displayed throughout many lines,
            # a_interface is processed with vary trying.
            ifconfig_output = os.popen("ifconfig").read()
            for a_line_from_ifconfig in ifconfig_output.split("\n"):
                if(len(a_line_from_ifconfig.strip()) == 0): continue
                
                words = a_line_from_ifconfig.split(' ')
                is_interface_name = (a_line_from_ifconfig[0] != '\t')
                if(is_interface_name):
                    # if an interface to process changed, store it
                    if(a_interface != None):
                        netifaces_ya.__interfaces.append(interface_name)
                        netifaces_ya.__interfaces_info[interface_name] = a_interface
                    interface_name = words[0][0:-1]
                    a_interface = {}

                    i=1
                    while(i<len(words)):
                        if(words[i]):
                            if(words[i].startswith("flags")):    # "flags" just to store
                                a_interface["flags"] = words[i]
                                i -= 1
                            else:
                                a_interface[words[i]] = words[i+1]
                        i += 2
                else:
                    # drop '\t' character
                    words[0] = words[0][1:] 

                    i=0
                    while(i<len(words)):
                        if(words[i]):
                            # drop ':' in the end of word, in case of as 'media:'
                            if(words[i].endswith(':')): words[i]=words[i][0:-1]
                            a_interface[words[i]] = words[i+1]
                        i += 2
                        
            # save last one
            netifaces_ya.__interfaces.append(interface_name)
            netifaces_ya.__interfaces_info[interface_name] = a_interface
        elif(netifaces_ya.__host_info["platform"] == 'nt'):
            # chcp is for non-english system. this command will convert all message to english word.
            ipconfig_output = os.popen("chcp 437 | ipconfig /all").read()

            is_first_item = 0
            is_interface_name = 0
            config_key = None
            config_value = None
            for a_line_from_ipconfig in ipconfig_output.split("\n"):
                if(a_line_from_ipconfig.strip() == ''): continue
                
                is_interface_name = not a_line_from_ipconfig.startswith(' ')
                if(is_interface_name):
                     is_first_item = a_line_from_ipconfig.startswith('Windows IP Configuration')
                
                word_left = a_line_from_ipconfig[:37]   # 37 is ':' character's position
                word_right = a_line_from_ipconfig[38:]
                # drop surplus text thing
                word_left = word_left.replace('. ', '').strip()
                word_right = word_right.replace("(Preferred)", "").strip()
                        
                if(word_left.strip() == ''):
                    config_value = word_right
                else:
                    config_key = word_left
                    config_value = word_right
                    
                # host 관련 정보 저장
                if(is_first_item):
                    if(is_interface_name): continue
                    netifaces_ya.__host_info[config_key] = config_value
                # 인터페이스 정보 저장
                else:
                    if(is_interface_name):
                        if(a_interface != None): # store previous inferface info
                            netifaces_ya.__interfaces.append(interface_name)
                            netifaces_ya.__interfaces_info[interface_name] = a_interface
                        a_interface = {}
                        interface_name = config_key
                    else:
                        # if exists duplicated key, make them as list
                        if(a_interface and a_interface.has_key(config_key)):
                            if(type(a_interface[config_key]) is list):
                                a_interface[config_key].append(config_value)
                            else:
                                a_interface[config_key] = [a_interface[config_key], config_value]
                        else:
                                a_interface[config_key] = config_value
                        
                        
            # save last one
            netifaces_ya.__interfaces.append(interface_name)
            netifaces_ya.__interfaces_info[interface_name] = a_interface
            
    @staticmethod
    def get_active_interfaces():
        result = []
        interfaces = netifaces_ya.get_interfaces()
        if(netifaces_ya.__host_info["platform"] == 'darwin'):
            for interface_name in interfaces:
                if(netifaces_ya.__interfaces_info[interface_name].has_key("status") and
                   netifaces_ya.__interfaces_info[interface_name]["status"] == "active"):
                    result.append(interface_name)
        elif(netifaces_ya.__host_info["platform"] == 'nt'):
            for interface_name in interfaces:
                # considering only in IPv4!
                interface_info = netifaces_ya.__interfaces_info[interface_name]
                if(interface_info.has_key("IPv4 Address") and 
                   len(interface_info["IPv4 Address"]) !=0 and
                   interface_info.has_key("Default Gateway") and 
                   len(interface_info["Default Gateway"]) !=0):
                    result.append(interface_name)
        return result

    @staticmethod
    def get_active_first_interface():
        active_interfaces = netifaces_ya.get_active_interfaces()
        if(len(active_interfaces) == 0):
            return ''
        else:
            return active_interfaces[0]
    
    @staticmethod
    def get_active_IPs():
        active_IPs = []
        active_interfaces = netifaces_ya.get_active_interfaces()
        if(netifaces_ya.__host_info["platform"] == 'darwin'):
            for interface_name in active_interfaces:
                interface_info = netifaces_ya.__interfaces_info[interface_name]
                # pass loopback adpater
                if(interface_info['flags'].find('LOOPBACK') != -1): continue
                if(interface_info.has_key('inet')): 
                    active_IPs.append(interface_info['inet'])
        elif(netifaces_ya.__host_info["platform"] == 'nt'):
            for interface_name in active_interfaces:
                interface_info = netifaces_ya.__interfaces_info[interface_name]
                ip_value = interface_info["IPv4 Address"]
                if(type(ip_value) is list):
                    for ip in ip_value: active_IPs.append(ip)
                else:
                    active_IPs.append(ip_value)
        return active_IPs 

    @staticmethod
    def get_active_first_IP():
        active_IPs = netifaces_ya.get_active_IPs()
        if(len(active_IPs) == 0):
            return ''
        else:
            return active_IPs[0]
    
    # this method is for nt platform
    @staticmethod
    def get_active_netmasks():
        active_netmasks = []
        active_interfaces = netifaces_ya.get_active_interfaces()
        if(netifaces_ya.__host_info["platform"] == 'darwin'):
            pass
        elif(netifaces_ya.__host_info["platform"] == 'nt'):
            for interface_name in active_interfaces:
                interface_info = netifaces_ya.__interfaces_info[interface_name]
                ip_value = interface_info["Subnet Mask"]
                if(type(ip_value) is list):
                    for ip in ip_value: active_netmasks.append(ip)
                else:
                    active_netmasks.append(ip_value)
        return active_netmasks 

    @staticmethod
    def get_active_broadcast_IPs():
        active_broadcast_IPs = []
        active_interfaces = netifaces_ya.get_active_interfaces()
        if(netifaces_ya.__host_info["platform"] == 'darwin'):
            for interface_name in active_interfaces:
                interface_info = netifaces_ya.__interfaces_info[interface_name]
                if(interface_info.has_key('broadcast')):
                    active_broadcast_IPs.append(interface_info['broadcast'])
        elif(netifaces_ya.__host_info["platform"] == 'nt'):
            active_IPs = netifaces_ya.get_active_IPs()
            active_netmasks = netifaces_ya.get_active_netmasks()
            for i in range(0,len(active_IPs)):
                broadcast_IP = ''
                divided_ip = active_IPs[i].split('.')
                divided_broadcast_IP = list(divided_ip)
                divided_netmask = active_netmasks[i].split('.')
                netmask_inversion = list(divided_netmask)
                for j in range(0,4):
                    netmask_inversion[j] = int(netmask_inversion[j]) ^ 255
                    divided_broadcast_IP[j] = str(int(divided_broadcast_IP[j]) | netmask_inversion[j])
                    broadcast_IP = ".".join(divided_broadcast_IP)
                active_broadcast_IPs.append(broadcast_IP) 
        return active_broadcast_IPs

    @staticmethod
    def get_active_first_broadcast_IP():
        active_broadcast_IPs = netifaces_ya.get_active_broadcast_IPs()
        if(len(active_broadcast_IPs) == 0):
            return ''
        else:
            return active_broadcast_IPs[0]

    @staticmethod
    def get_active_mac_addresses(separator = '-'):
        '''MAC address separator in UNIX is ':', while it is '-' in NT. '-' is default separator for this.'''
        active_mac_addresses = []
        if(netifaces_ya.__host_info["platform"] == 'darwin'):
            for interface_name in netifaces_ya.get_active_interfaces():
                interface_info = netifaces_ya.__interfaces_info[interface_name]
                if(interface_info.has_key('ether')):
                    active_mac_addresses.append(interface_info['ether'].replace(':',separator))
        elif(netifaces_ya.__host_info["platform"] == 'nt'):
            for interface_name in netifaces_ya.get_active_interfaces():
                interface_info = netifaces_ya.__interfaces_info[interface_name]
                if(interface_info.has_key('Physical Address')):
                    active_mac_addresses.append(interface_info['Physical Address'].replace('-',separator))
        return active_mac_addresses 

    @staticmethod
    def get_active_first_mac_address(separator = '-'):
        '''MAC address separator in UNIX is ':', while it is '-' in NT. '-' is default separator for this.'''
        active_mac_addresses = netifaces_ya.get_active_mac_addresses(separator)
        if(len(active_mac_addresses) == 0):
            return ''
        else:
            return active_mac_addresses[0]

    # from here, for compatibility with netifcaces
    @staticmethod
    def interfaces():
        return netifaces_ya.get_interfaces()

    @staticmethod
    def ifaddresses(ifname):
        return netifaces_ya.get_interface_info(ifname)




# test code
if __name__ == "__main__":

    # something like netifaces ...
    print netifaces_ya.interfaces()  
#    print netifaces_ya.ifaddresses('en0')  
    
    # Or, on our way!
    # We know that there's plenty of network interface NOT CONNECTED or NOT ACTIVATED.
    # So I just need to take active-things only.
    print netifaces_ya.get_active_interfaces()
    print netifaces_ya.get_active_IPs()
 
    # You wanna 'a piece' of something? Just use 'first_XXX' series functions.
    print netifaces_ya.get_active_first_IP()
    print netifaces_ya.get_active_first_mac_address('')    
    print netifaces_ya.get_active_first_interface()
    print netifaces_ya.get_active_first_broadcast_IP()
    
    # If you want everything, get everything
    interfaces = netifaces_ya.get_interfaces()
    for interface_name in interfaces:
        print interface_name
        print netifaces_ya.get_interface_info(interface_name)
        
    