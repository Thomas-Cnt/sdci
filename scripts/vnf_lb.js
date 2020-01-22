var http = require('http');
var url = require('url');
const forward = require('http-forward')

const PORT = 8888;
var index = 1;
console.log("Started LB on port " + PORT)
http.createServer(function (req, res) {
        index = 1 - index;
        if (index == 0) {
           req.forward = {target:"http://10.0.0.100:8585/"};
           forward(req, res);
           console.log("Forward to VNF GI\n");
        }
        if (index == 1) {
           req.forward = {target:"http://10.0.0.4:8181/"};
           forward(req, res);
           console.log("Forward to GI\n");
        }
}).listen(PORT);
