var zmq = require('./pzmq');

var req = zmq.socket('req');
var rep = zmq.socket('rep');

rep.bind('tcp://127.0.0.1:8000');
req.connect('tcp://127.0.0.1:8000');

rep.on('message', function(request) {
    console.log('Request: ' + request);
    rep.send('Response!');
});

var reply = req.request('request this');
reply.then(function(msg) {
    var k;
    for (k in msg)
        console.log("Message part ", k, ": ", msg[k].toString());
    process.exit(0);
}, console.error);
