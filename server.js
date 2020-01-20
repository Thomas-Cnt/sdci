/**
 *  Author: Samir MEDJIAH medjiah@laas.fr
 *  File : server.js
 *  Version : 0.1.0
 */


var express = require('express')
var app = express()
app.use(express.json()) 

var argv = require('yargs').argv;
// --local_ip
// --local_port
// --local_name
const si = require('systeminformation');

var LOCAL_ENDPOINT = {IP : argv.local_ip, PORT : argv.local_port, NAME : argv.local_name};

const E_OK              = 200;
const E_CREATED         = 201;
const E_FORBIDDEN       = 403;
const E_NOT_FOUND       = 404;
const E_ALREADY_EXIST   = 500;


var db = {
        devices : new Map(),
        data : new Map(),
        gateways : new Map()
    };

function addNewDevice(dev) {
    var result = -1;
    if (!db.devices.get(dev.Name)) {
        db.devices.set(dev.Name, dev);

        if (db.devices.get(dev.Name))
            db.data.delete(dev.Name);
        db.data.set(dev.Name, []);

        result = 0;
    }
    return result;
}

function addNewGateway(gw) {
    var result = -1;
    if (!db.gateways.get(gw.Name)) {
        db.gateways.set(gw.Name, gw);
        result = 0;
    }
    return result;
}

function removeDevice(dev) {
    if (db.devices.get(dev.Name)) {
        db.devices.delete(dev.Name);
        if (db.devices.get(dev.Name))
            db.data.delete(dev.Name);
    }
}

function removeGateway(gw) {
    if (db.gateways.get(gw.Name))
        db.gateways.delete(gw.Name);
}

function addDeviceData(dev, data) {
    var result = -1;
    var device = db.devices.get(dev);
    if (device) {
        db.data.get(dev).push(data);
        result = 0;
    }
    return result;
}



app.get('/devices', function(req, res) {
    console.log(req.body);
    let resObj = [];
    db.devices.forEach((v,k) => {
        resObj.push(v);
    });
    res.status(E_OK).send(resObj);
});
app.get('/device/:dev', function(req, res) {
    console.log(req.body);
    var dev = req.params.dev;
    var device = db.devices.get(dev);
    if (device)
        res.status(E_OK).send(JSON.stringify(device));
    else
        res.sendStatus(E_NOT_FOUND);
});
app.post('/device/:dev/data', function(req, res) {
    console.log(req.body);
    var dev = req.params.dev;
    var result = addDeviceData(dev, req.body);
    if (result === 0)
        res.sendStatus(E_CREATED);
    else
        res.sendStatus(E_NOT_FOUND);
});
app.get('/device/:dev/data', function(req, res) {
    console.log(req.body);
    var dev = req.params.dev;
    var device = db.devices.get(dev);
    if (device){
        var data = db.data.get(dev);
        if (data) {
            let resObj = [];
            data.forEach((v,k) => {
                resObj.push(v);
            });
            res.status(E_OK).send(JSON.stringify(resObj));
        }
        else
            res.sendStatus(E_NOT_FOUND);
    }
    else
        res.sendStatus(E_NOT_FOUND);
});
app.post('/devices/register', function(req, res) {
    console.log(req.body);
    var result = addNewDevice(req.body);
    if ( result === 0)
        res.sendStatus(E_CREATED);  
    else
        res.sendStatus(E_ALREADY_EXIST);  
});
app.get('/gateways', function(req, res) {
    console.log(req.body);
    let resObj = [];
    db.gateways.forEach((v,k) => {
        resObj.push(v);
    });
    res.send(resObj);
});
app.get('/gateway/:gw', function(req, res) {
    console.log(req.body);
    var gw = req.params.gw;
    var gateway = db.gateways.get(gw);
    if (gateway)
        res.status(E_OK).send(JSON.stringify(gateway));
    else
        res.sendStatus(E_NOT_FOUND);
});
app.post('/gateways/register', function(req, res) {
    console.log(req.body);
    var result = addNewGateway(req.body);
    if ( result === 0)
        res.sendStatus(E_CREATED);  
    else
        res.sendStatus(E_ALREADY_EXIST);  
});

app.get('/ping', function(req, res) {
    console.log(req.body);
    res.status(E_OK).send({pong: Date.now()});
});
app.get('/health', function(req, res) {
    console.log(req.body);
    si.currentLoad((d) => {
        console.log(d);
        res.status(E_OK).send(JSON.stringify(d));
    })
});

app.listen(LOCAL_ENDPOINT.PORT , function () {
    console.log(LOCAL_ENDPOINT.NAME + ' listening on : ' + LOCAL_ENDPOINT.PORT );
});
