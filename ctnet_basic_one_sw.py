#!/usr/bin/python
'''
Modification de containernet_example.py pour creer le reseau du projet SDCI
'''
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
Serv=net.addDocker('S', ip='10.0.0.251', dimage="test:noel",dcmd="sh ./server.sh")
GI = net.addDocker('GI', ip='10.0.0.252', dimage="test:noel",dcmd="sh ./gi.sh")
GF1 = net.addDocker('GF1', ip='10.0.0.253', dimage="test:noel",dcmd="sh ./gf1.sh")
GF2 = net.addDocker('GF2', ip='10.0.0.254', dimage="test:noel",dcmd="sh ./gf2.sh")
GF3 = net.addDocker('GF3', ip='10.0.0.255', dimage="test:noel",dcmd="sh ./gf3.sh")
info('*** Adding switches\n')
s1 = net.addSwitch('s1')
info('*** Creating links\n')
net.addLink(GF1, s1)
net.addLink(GF2, s1)
net.addLink(GF3, s1)
net.addLink(GI, s1)
net.addLink(Serv, s1)
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
