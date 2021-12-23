#!/usr/bin/python

'''
Module name: My_topology.py
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
        
        #global host_list
        
        #Add Agents
        ag1 = self.addHost('ag1', ip = '10.0.0.100')

        # Add hosts and switches
        s1 = self.addSwitch('s1')
        #s2 = self.addSwitch('s2')
        #s3 = self.addSwitch('s3')
        
        for i in range(1, 21):
            self.addHost('h%s'%i)
            #host_list.append('h%s'%i)
            self.addLink('h%s'%i, s1)
            #self.addLink('h%s'%i, ag1)

        '''            
        for i in range(21,41):
            self.addHost('h%s'%i)
            self.addLink('h%s'%i, s2)
        
        for i in range(41,61):
            self.addHost('h%s'%i)
            self.addLink('h%s'%i, s3)
        '''
        self.addLink(ag1, s1)
        #Add link between switches
        #self.addLink(s1, s2)
        #self.addLink(s2, s3)

def ping():
    for i in range(1,3):
        h1 = net.get('h%s'%i)
        print(h1.cmd('ifconfig'))
    #net.pingPair()
    #net.pingAll()
def attack():
    for i in range(1,9):
        h1 = net.get('h%s'%i)
        h1.cmd('sudo python /home/bob/pox/ext/My_SYNflood_attack.py 10.0.0.%s 10.0.0.10'%i )
    #h1 = net.get('h1')
    #h1.cmd('sudo python /home/bob/pox/ext/My_SYNflood_attack.py 10.0.0.2 10.0.0.4' )
    
def RTT():
    global host_list
    print(time.time())
    ag1 = net.get('ag1')
    w = open('/home/bob/pox/ext/rtt.txt', 'w')
    for i in range(2, 20):
        #w = open('/home/bob/pox/ext/rtt.txt', 'w')
        w.write(str(ag1.cmd('ping -c2 10.0.0.%s'%i)))
    w.close()
    print(time.time())
'''
def Agent_Process():
    ag1 = net.get('ag1')
    ag1.cmd('sudo python /home/bob/pox/ext/Agent_Analyze.py')
'''


setLogLevel('info')
topo = MyTopo()
net = Mininet(topo, controller=lambda name: RemoteController(name,
                  ip= '127.0.0.1', protocol= 'tcp', port= 6633), autoSetMacs= True)
net.start()
#x = True
#T = time.time()
#print('Start of algorithm:', T)
'''while x == True:
    if time.time() == T + 10:
        print(time.time())
        attack()
        x = False'''


#ping()
#attack()
#RTT()
#t = Timer(20.0, attack)
#t.start()
CLI(net)
net.stop()