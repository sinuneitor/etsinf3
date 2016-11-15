var zmq = require('zmq');
var aux = require('./auxfunctions.js');
var frontend = zmq.socket('router');
var backend  = zmq.socket('router');
var config   = zmq.socket('rep');
var ready = [], workers = {}, queue = [];
var policy = {'distribution':'equitable','adjustFactor':1};
var statusTimer;

if (process.argv.length < 5 || process.argv.length > 6) {
    console.log('Usage: node broker frontEndPort backEndPort configPort [-v]');
    process.exit(-1);
}

var frontport = process.argv[2];
var backport  = process.argv[3];
var configPort = process.argv[4];
var debug = function() {};
if (process.argv.length == 6 && process.argv[5] == '-v') {
    debug = console.log;
}
debug('Arguments are correct!');

frontend.bindSync('tcp://*:' + frontport);
backend.bindSync('tcp://*:' + backport);
config.bindSync('tcp://*:' + configPort);

debug('Policy is ' + policy);
debug('Frontend ready at port ' + frontport);
debug('Backend  ready at port ' + backport);
debug('Config   ready at port ' + configPort);

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
        ready.push({'id':msg[0],'load':parseInt(msg[2]),'port':parseInt(msg[3]),'jobs':0})
        debug('Worker ', msg[0].toString(), ' registered.');
    } else {
        // Response message
        debug('Response from worker ', msg[0].toString());
        for (k in msg)
            debug('\tPart ', k, ': ', msg[k].toString());
        workers[msg[0]].jobs++;
        ready.push(workers[msg[0]]);
        msg.splice(0,2);
        frontend.send(msg);
    }
    if (newOrReady && queue.length > 0) sendWork(queue.shift());
});

config.on('message', function(msg){
    var policy = JSON.parse(msg);
    if (statusTimer != undefined)
        statusTimer.cancelInterval();
    if (policy.distribution == 'lowerLoad') {
        statusTimer = setInterval(checkAll, policy.secs * 1000);
    } else {
        statusTimer = undefined;
    }
    debug('Policy has been updated to ' + policy);
});


function checkAll() {
    for (w in workers) {
        checkStatus(workers[w]);
    }
}

function sendWork(msg) {
    var minId  = undefined;
    var minPos = undefined;
    if (policy.distribution == 'equitable') {
        var minJobs = Number.MAX_VALUE;
        for (w in ready) {
            if (ready[w].jobs < minLoad) {
                minJobs = ready[w].jobs;
                minId   = ready[w].id;
                minPos  = w;
            }
        }
    } else if (policy.distribution == 'lowerLoad') {
        if (policy.lowLoadWorkers == 1) {
            var minLoad = Number.MAX_VALUE;
            for (w in ready) {
                if (ready[w].load < minLoad) {
                    minLoad = ready[w].load;
                    minId   = ready[w].id;
                    minPos  = w;
                }
            }
        } else {
            sortLoad(ready);
            minPos = aux.randNumber(policy.lowLoadWorkers);
            minId = ready[minPos];
        }
    }
    if (minId != undefined) {
        msg.unshift(minId);
        backend.send(msg);
        ready.splice(minPos, 1);
        debug('Sent message to ' + minId);
        for (k in msg)
            debug('\tPart ' + k + ': ' + msg[k].toString());
    } else {
        queue.push(msg);
    }
}

function checkStatus(worker) { // change everything from id to worker
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
    req.send('Status ping');
}
