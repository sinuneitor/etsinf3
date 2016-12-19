var zmq = require('zmq');
var req = zmq.socket('req');
var rep = zmq.socket('rep');


rep.bind('tcp://*:8000');
req.connect('tcp://localhost:8000');

console.log(rep, '\n\n\n', req);
