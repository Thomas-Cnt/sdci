node gateway.js --local_ip 10.0.0.254 --local_port 8383 --local_name gf2 --remote_ip 10.0.0.252 --remote_port 8181 --remote_name gwi &
node device.js --local_ip 10.0.0.254 --local_port 9001 --local_name dev1 --remote_ip 10.0.0.254 --remote_port 8383 --remote_name gf2 &
