var zmq = require('zmq');
var req = zmq.socket('req');

req.bind('tcp://127.0.0.1:8888', function(err) {
    if (err) throw err;
});

var i = 0;

setInterval(function() {
    req.send('Hello ' + i++);
}, 1000);

req.on('message', function(msg) {
    console.log('Response: ' + msg);
});
