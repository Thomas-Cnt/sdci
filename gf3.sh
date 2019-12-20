node gateway.js --local_ip 10.0.0.255 --local_port 8484 --local_name gf3 --remote_ip 10.0.0.252 --remote_port 8181 --remote_name gwi 
node device.js --local_ip 10.0.0.255 --local_port 9001 --local_name dev1 --remote_ip 10.0.0.255 --remote_port 8484 --remote_name gf3
