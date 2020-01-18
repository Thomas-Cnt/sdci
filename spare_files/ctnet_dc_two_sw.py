# Copyright (c) 2015 SONATA-NFV and Paderborn University
# ALL RIGHTS RESERVED.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Neither the name of the SONATA-NFV, Paderborn University
# nor the names of its contributors may be used to endorse or promote
# products derived from this software without specific prior written
# permission.
#
# This work has been performed in the framework of the SONATA project,
# funded by the European Commission under Grant number 671517 through
# the Horizon 2020 and 5G-PPP programmes. The authors would like to
# acknowledge the contributions of their colleagues of the SONATA
# partner consortium (www.sonata-nfv.eu).
import logging
from mininet.net import Containernet
from mininet.node import Controller
from mininet.cli import CLI
from mininet.link import TCLink
from mininet.log import setLogLevel
from emuvim.dcemulator.net import DCNetwork
from emuvim.api.rest.rest_api_endpoint import RestApiEndpoint
from emuvim.api.openstack.openstack_api_endpoint import OpenstackApiEndpoint

# Tous les ping fonctionnent
# Le serveur connait 2 sur 3 devices 
# MAIS aucune GW n'est connue ni du GI ni du serv

logging.basicConfig(level=logging.INFO)
setLogLevel('info')  # set Mininet loglevel
logging.getLogger('werkzeug').setLevel(logging.DEBUG)
logging.getLogger('api.openstack.base').setLevel(logging.DEBUG)
logging.getLogger('api.openstack.compute').setLevel(logging.DEBUG)
logging.getLogger('api.openstack.keystone').setLevel(logging.DEBUG)
logging.getLogger('api.openstack.nova').setLevel(logging.DEBUG)
logging.getLogger('api.openstack.neutron').setLevel(logging.DEBUG)
logging.getLogger('api.openstack.heat').setLevel(logging.DEBUG)
logging.getLogger('api.openstack.heat.parser').setLevel(logging.DEBUG)
logging.getLogger('api.openstack.glance').setLevel(logging.DEBUG)
logging.getLogger('api.openstack.helper').setLevel(logging.DEBUG)

image="sdci:sdci"

def create_topology():
    net = DCNetwork(monitor=False, enable_learning=True)

    dc1 = net.addDatacenter("dc1")
    # add OpenStack-like APIs to the emulated DC
    api1 = OpenstackApiEndpoint("0.0.0.0", 6001)
    api1.connect_datacenter(dc1)
    api1.start()
    api1.connect_dc_network(net)
    # add the command line interface endpoint to the emulated DC (REST API)
    rapi1 = RestApiEndpoint("0.0.0.0", 5001)
    rapi1.connectDCNetwork(net)
    rapi1.connectDatacenter(dc1)
    rapi1.start()

    Serv=net.addDocker('Serv', ip='10.0.0.200', dimage=image,dcmd="sh ./server.sh")
    GI = net.addDocker('GI', ip='10.0.0.201', dimage=image,dcmd="sh ./gi.sh")
    GF1 = net.addDocker('GF1', ip='10.0.0.202', dimage=image,dcmd="sh ./gf1.sh")
    GF2 = net.addDocker('GF2', ip='10.0.0.203', dimage=image,dcmd="sh ./gf2.sh")
    GF3 = net.addDocker('GF3', ip='10.0.0.204', dimage=image,dcmd="sh ./gf3.sh")

    s1 = net.addSwitch('s1')
    s2 = net.addSwitch('s2')

    net.addLink(Serv, s1)
    net.addLink(GI, s1)
    net.addLink(s1, s2, cls=TCLink, delay='100ms', bw=1)
    net.addLink(GF1, s2)
    net.addLink(GF2, s2)
    net.addLink(GF3, s2)
    net.addLink(dc1, s2)

    net.start()

    net.ping([GF1, GI])
    net.ping([GF2, GI])
    net.ping([GF3, GI])
    net.ping([Serv, GI])

    net.CLI()

    net.stop()


def main():
    create_topology()


if __name__ == '__main__':
    main()
