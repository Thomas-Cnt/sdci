sleep 5 & node gateway.js --local_ip 10.0.0.202 --local_port 8282 --local_name gf1 --remote_ip 10.0.0.201 --remote_port 8181 --remote_name gwi & sleep 7 & node device.js --local_ip 10.0.0.211 --local_port 9011 --local_name dev11 --remote_ip 10.0.0.202 --remote_port 8282 --remote_name gf1 --send_period 3000 
