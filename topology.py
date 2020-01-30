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
from mininet.log import setLogLevel, info
from emuvim.dcemulator.net import DCNetwork
from emuvim.api.rest.rest_api_endpoint import RestApiEndpoint
from emuvim.api.openstack.openstack_api_endpoint import OpenstackApiEndpoint

import time

logging.basicConfig(level=logging.INFO)
setLogLevel('info')  # set Mininet loglevel
#logging.getLogger('werkzeug').setLevel(logging.DEBUG)
#logging.getLogger('api.openstack.base').setLevel(logging.DEBUG)
#logging.getLogger('api.openstack.compute').setLevel(logging.DEBUG)
#logging.getLogger('api.openstack.keystone').setLevel(logging.DEBUG)
#logging.getLogger('api.openstack.nova').setLevel(logging.DEBUG)
#logging.getLogger('api.openstack.neutron').setLevel(logging.DEBUG)
#logging.getLogger('api.openstack.heat').setLevel(logging.DEBUG)
#logging.getLogger('api.openstack.heat.parser').setLevel(logging.DEBUG)
#logging.getLogger('api.openstack.glance').setLevel(logging.DEBUG)
#logging.getLogger('api.openstack.helper').setLevel(logging.DEBUG)


def create_topology():
    net = DCNetwork(monitor=False, enable_learning=True)

    info('*** Adding datacenters\n')
    dc1 = net.addDatacenter("dc1")
    dc2 = net.addDatacenter("dc2")
    # add OpenStack-like APIs to the emulated DC
    api1 = OpenstackApiEndpoint("0.0.0.0", 6001)
    api1.connect_datacenter(dc1)
    api1.connect_datacenter(dc2)
    api1.start()
    api1.connect_dc_network(net)
    # add the command line interface endpoint to the emulated DC (REST API)
    rapi1 = RestApiEndpoint("0.0.0.0", 5001)
    rapi1.connectDCNetwork(net)
    rapi1.connectDatacenter(dc1)
    rapi1.connectDatacenter(dc2)
    rapi1.start()


    # params
    SRV_PORT = 8080


    info('*** Adding switches\n')
    sw1 = net.addSwitch('sw1')
    sw2 = net.addSwitch('sw2')

    info('*** Adding docker containers\n')

    server = net.addDocker('server', ip='10.100.0.10', dimage="alpine:4", dcmd="node ./server.js --local_ip '127.0.0.1' --local_port 8080 --local_name 'srv' &")

    GW = net.addDocker('GW', ip='10.100.0.4', dimage="alpine:4")

    GF1 = net.addDocker('GF1', ip='10.100.0.1', dimage="alpine:4")

    GF2 = net.addDocker('GF2', ip='10.100.0.2', dimage="alpine:4")
    GF3 = net.addDocker('GF3', ip='10.100.0.3', dimage="alpine:4")

    net.addLink(server, sw1)
    net.addLink(GW, sw1)
    net.addLink(sw1, sw2)
    net.addLink(GF1, sw2)
    net.addLink(GF2, sw2)
    net.addLink(GF3, sw2)

  


    info('*** Starting network\n')
    net.start()


    time.sleep(5)

    # launch gateway GW
    info("//// Starting GW gateway\n")
    GW.cmd("node ./gateway.js --local_ip '127.0.0.1' --local_port 9000 --local_name 'GW' --remote_ip '10.100.0.10' --remote_port 8080 --remote_name 'srv' &")
    info('//// started !\n')

    time.sleep(5)


    # launch gateways GFs

    info("//// Starting GF1 gateway\n")
    GF1.cmd("node ./gateway.js --local_ip '127.0.0.1' --local_port 5000 --local_name 'GF1' --remote_ip '10.100.0.4' --remote_port 9000 --remote_name 'GW' &")
    info('//// started !\n')

    info("//// Starting GF2 gateway\n")
    GF2.cmd("node ./gateway.js --local_ip '127.0.0.1' --local_port 5000 --local_name 'GF2' --remote_ip '10.100.0.4' --remote_port 9000 --remote_name 'GW' &")
    info('//// started !\n')

    info("//// Starting GF3 gateway\n")
    GF3.cmd("node ./gateway.js --local_ip '127.0.0.1' --local_port 5000 --local_name 'GF3' --remote_ip '10.100.0.4' --remote_port 9000 --remote_name 'GW' &")
    info('//// started !\n')


    # launch devices

    info("//// Starting devices on GF1\n")
    GF1.cmd("node ./device.js --local_ip '127.0.0.1' --local_port 5001 --local_name 'device-1' --remote_ip '127.0.0.1' --remote_port 5000 --remote_name 'GF1' --send_period 3 &")
    info('//// started !\n')


    info('*** Testing connectivity\n')
    net.ping([GW, GF1])
    info('*** Running CLI\n')
    net.CLI()
    info('*** Stopping network\n')
    net.stop()
def main():
    create_topology()


if __name__ == '__main__':
    main()
