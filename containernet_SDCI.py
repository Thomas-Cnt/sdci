#!/usr/bin/python
"""
Modification de containernet_example.py pour créer le réseau du projet SDCI
"""
from mininet.net import Containernet
from mininet.node import Controller
from mininet.cli import CLI
from mininet.link import TCLink
from mininet.log import info, setLogLevel
setLogLevel('info')

net = Containernet(controller=Controller)
info('*** Adding controller\n')
net.addController('c0')
info('*** Adding docker containers\n')
GF1 = net.addDocker('GF1', ip='10.0.0.251', dimage="imageGF1")
GF2 = net.addDocker('GF2', ip='10.0.0.252', dimage="imageGF2")
GF3 = net.addDocker('GF3', ip='10.0.0.253', dimage="imageGF3")
GI = net.addDocker('GF4', ip='10.0.0.254', dimage="imageGI")
Serv=net.addDocker('S', ip='10.0.0.255', dimage="imageServ")
info('*** Adding switches\n')
s1 = net.addSwitch('s1')
s2 = net.addSwitch('s2')
s3 = net.addSwitch('s3')
s4 = net.addSwitch('s4')
info('*** Creating links\n')
net.addLink(GF1, s1)
net.addLink(GF2, s1)
net.addLink(GF3, s2)
net.addLink(GI, s3)
net.addLink(s1, s2, cls=TCLink, delay='100ms', bw=1)
net.addLink(s1, s3, cls=TCLink, delay='100ms', bw=1)
net.addLink(s3, s2, cls=TCLink, delay='100ms', bw=1)
net.addLink(s3, s4, cls=TCLink, delay='100ms', bw=1)
net.addLink(Serv, s4)
info('*** Starting network\n')
net.start()
info('*** Testing connectivity\n')
net.ping([GF1, GI])
net.ping([GF2, GI])
net.ping([GF3, GI])
net.ping([Serv, GI])
info('*** Running CLI\n')
CLI(net)
info('*** Stopping network')
net.stop()

