var zmq = require('./pzmq');
var req = zmq.socket('req');

req.connect('tcp://127.0.0.1:8888');

var i = 0;

var reply = req.request(3, 'Hello ' + i++);
reply.then(function(msg) {
    console.log('Response: ' + msg);
}, console.err);

setInterval(function() {
    var reply = req.request(3, 'Hello ' + i++);
    reply.then(function(msg) {
        console.log('Message: ', msg);
    }, function(err) {
        if (err === 'TMOUT')
            console.log('Connexion timed out');
        else if (err)
            throw err;
    });
}, 1000);

