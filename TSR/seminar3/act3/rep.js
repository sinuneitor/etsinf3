var zmq = require('./pzmq');
var rep = zmq.socket('rep');

rep.bind('tcp://127.0.0.1:8888', function(err) {
    if (err) throw err;
});

var i = 0;

rep.on('message', function(msg) {
    console.log('Request: ' + msg);
    rep.send('World');
    i++;
    if (i == 10) {
        process.exit(0);
    }
})
