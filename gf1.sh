node gateway.js --local_ip 10.0.0.253 --local_port 8282 --local_name gf1 --remote_ip 10.0.0.252 --remote_port 8181 --remote_name gwi &
ode device.js --local_ip 10.0.0.253 --local_port 9001 --local_name dev1 --remote_ip 10.0.0.253 --remote_port 8282 --remote_name gf1 &