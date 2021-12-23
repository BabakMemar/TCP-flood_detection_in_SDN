#!/usr/bin/python

'''
Module name: Topology.py
Author: Babak Memar
Contact: babak.memar.it@gmail.com
Desc: In this module I try to create a custom topology for mininet with 3 OF_switches
which connected to each other linearly plus 20 hosts for each ones.
'''
import logging
import os
import sys
import random
import time

from mininet.topo import Topo
from mininet.node import Node
from mininet.net import Mininet
from mininet.cli import CLI
from mininet.node import RemoteController
from mininet.log import setLogLevel
from scapy.all import *
from threading import Timer



#logging.getLogger().setLevel(logging.INFO)
host_list =[] #to keep list of created nodes

class MyTopo (Topo):

    def __init__(self, ipBase='10.0.0.0/8'):
        Topo.__init__(self)

        # Add switches
        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')
        s3 = self.addSwitch('s3')
        
        #Add hosts
        for i in range(1, 21):
            self.addHost('h%s'%i)
            #host_list.append('h%s'%i)
            self.addLink('h%s'%i, s1)
           
        for i in range(21,41):
            self.addHost('h%s'%i)
            self.addLink('h%s'%i, s2)
        
        for i in range(41,61):
            self.addHost('h%s'%i)
            self.addLink('h%s'%i, s3)
        
        #Add link between switches
        self.addLink(s1, s2)
        self.addLink(s2, s3)
    

setLogLevel('info')
topo = MyTopo()
net = Mininet(topo, controller=lambda name: RemoteController(name,
                  ip= '127.0.0.1', protocol= 'tcp', port= 6633), autoSetMacs= True)
net.start()
CLI(net)
net.stop()
