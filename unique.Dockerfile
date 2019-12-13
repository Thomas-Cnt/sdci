# parent image
FROM node:latest

# install needed packages
RUN echo 'nameserver 8.8.8.8' >> /etc/resolve.conf && echo 'nameserver 8.8.4.4' >> /etc/resolve.conf
   && apt-get update && apt-get install -y \
    net-tools \
    iputils-ping \
    iproute2 \
    telnet telnetd \
    iperf
   && npm install express request systeminformation yargs
   && curl -X GET http://homepages.laas.fr/smedjiah/tmp/gateway.js >> gateway.js

# set entry point for emulator gatekeeper
ENV VIM_EMU_CMD "iperf -s -D"
ENV VIM_EMU_CMD_STOP "echo 'Stop iperf_server'"

# run bash interpreter
CMD ["sh"]
