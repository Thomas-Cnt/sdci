var http = require('http');
var url = require('url');
const forward = require('http-forward')
var index = 1;
console.log("Started LB")
http.createServer(function (req, res) {
        index = 1 - index;
        if (index == 0) {
           req.forward = {target:"http://10.0.0.205:8585/"};
           forward(req, res);
           console.log("Sent a message to Virtual GI\n");
        }
        if (index == 1) {
           req.forward = {target:"http://10.0.0.201:8181/"};
           forward(req, res);
           console.log("Sent a message to real GI\n");
        }
}).listen(8686);
