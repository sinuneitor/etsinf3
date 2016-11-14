var zmq = require('zmq');
var frontend = zmq.socket('router');
var backend  = zmq.socket('router');
var workers = {}, queue = [];

if (process.argv.length < 4 || process.argv.length > 5) {
    console.log('Usage: node broker port1 port2 [-v]');
    process.exit(-1);
}

var frontport = process.argv[2];
var backport  = process.argv[3];
var debug = function() {};
if (process.argv.length == 5 && process.argv[4] == '-v') {
    debug = console.log;
}
debug('Arguments are correct!');

frontend.bindSync('tcp://*:' + frontport);
backend.bindSync('tcp://*:' + backport);

debug('Frontend ready at port ' + frontport);
debug('Backend  ready at port ' + backport);

frontend.on('message', function() {
    var msg = Array.apply(null, arguments);
    debug('Received message');
    for (k in msg)
        debug('\tPart ', k, ': ', msg[k].toString());
    msg.unshift('');
    sendWork(msg);
});

backend.on('message', function() {
    var msg = Array.apply(null, arguments);
    var newOrReady = true;
    if (msg.length == 4) {
        // Register message
        if (workers[msg[0]] != undefined && workers[msg[0]].ready) newOrReady = false;
        workers[msg[0]] = {'ready':true,'load':parseInt(msg[2]),'port':parseInt(msg[3])};
        debug('Worker ', msg[0].toString(), ' registered.');
    } else {
        // Response message
        debug('Response from worker ', msg[0].toString());
        for (k in msg)
            debug('\tPart ', k, ': ', msg[k].toString());
        workers[msg[0]].ready = true;
        msg.splice(0,2);
        frontend.send(msg);
    }
    if (newOrReady && queue.length > 0) sendWork(queue.shift());
});

setInterval(function() {
    for (w in workers) {
        checkStatus(w);
    }
}, 20000);

function sendWork(msg) {
    var minLoad = Number.MAX_VALUE;
    var minId   = undefined;
    for (w in workers) {
        if (workers[w].ready && workers[w].load < minLoad) {
            minLoad = workers[w].load;
            minId   = w;
        }
    }
    if (minId != undefined) {
        msg.unshift(minId);
        backend.send(msg);
        workers[minId].ready = false;
        debug('Sent message to ' + minId);
        for (k in msg)
            debug('\tPart ' + k + ': ' + msg[k].toString());
    } else {
        queue.push(msg);
    }
}

function checkStatus(id) {
    var req = zmq.socket('req');
    var responded = false;
    var t1, t2;
    setTimeout(function() {
        if (!responded) {
            req.on('message', function(){});
            debug('Worker ', id, ' unavailable.');
            workers[id].load = Number.NaN;
        }
    }, 1000);
    req.connect('tcp://localhost:' + workers[id].port);
    req.on('message', function(msg) {
        responded = true;
        debug('Worker ' + id + ' available with load ' + msg.toString() + '.');
        if (workers[id].load == Number.NaN && workers[id].ready && queue.length > 0)
            sendWork(queue.shift());
        workers[id].load = parseInt(msg);
        req.close();
    });
    req.send('ping');
}
