var zmq = require('zmq');
var req = zmq.socket('req');

if (process.argv.lenght < 4) {
    console.log('Usage: node config url distribution(equitable|lowerLoad) [...]');
    process.exit(-1);
}

var url = process.argv[2];

var obj = {};
switch (process.argv[3]) {
    case 'equitable':
        obj.distribution = process.argv[3];
        if (process.argv.length < 5) {
            console.log('Usage: node config url equitable adjustFactor');
            process.exit(-2);
        }
        obj.adjustFactor = parseInt(process.argv[4]);
        break;
    case 'lowerLoad':
        distribution = process.argv[3];
        if (process.argv.length < 6) {
            console.log('Usage: node config url lowerLoad period lowLoadWorkers');
            process.exit(-2);
        }
        obj.periodicity = parseInt(process.argv[4]);
        obj.lowLoadWorkers = parseInt(process.argv[5]);
        break;
    default:
        console.log('Invalid distribution');
        process.exit(-1);
        break;
}

req.connect(url);

req.on('message', function() {
    console.log('Response received');
    req.close();
    process.exit(0);
});

req.send(JSON.stringify(obj));
