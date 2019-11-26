# parent image
FROM node:latest

# install needed packages
RUN apt-get update && apt-get install -y \
    net-tools \
    iputils-ping \
    iproute2 \
    telnet telnetd \
    iperf
   && npm install express systeminformation yargs
   && curl -X GET http://homepages.laas.fr/smedjiah/tmp/server.js >> server.js

# set entry point for emulator gatekeeper
ENV VIM_EMU_CMD "iperf -s -D"
ENV VIM_EMU_CMD_STOP "echo 'Stop iperf_server'"

# run bash interpreter
CMD node server.js --local_ip "127.0.0.1" --local_port 8080 --local_name "srv"
