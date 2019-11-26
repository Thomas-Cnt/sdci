# parent image
FROM node:latest

# install needed packages
RUN apt-get update && apt-get install -y \
    net-tools \
    iputils-ping \
    iproute2 \
    telnet telnetd \
    iperf
   && npm install express request systeminformation yargs
   && curl -X GET http://homepages.laas.fr/smedjiah/tmp/gateway.js >> gateway.js
   && curl -X GET http://homepages.laas.fr/smedjiah/tmp/device.js >> device.js

# set entry point for emulator gatekeeper
ENV VIM_EMU_CMD "iperf -s -D"
ENV VIM_EMU_CMD_STOP "echo 'Stop iperf_server'"

# run bash interpreter
CMD node gateway.js --local_ip "127.0.0.1" --local_port 8282 --local_name "gwf1" --remote_ip "127.0.0.1" --remote_port 8181 --remote_name "gwi" 
&& node device.js --local_ip "127.0.0.1" --local_port 9001 --local_name "dev1" --remote_ip "127.0.0.1" --remote_port 8282 --remote_name "gwf1" --send_period 3000 
&& node device.js --local_ip "127.0.0.1" --local_port 9001 --local_name "dev1" --remote_ip "127.0.0.1" --remote_port 8282 --remote_name "gwf1" --send_period 3000
