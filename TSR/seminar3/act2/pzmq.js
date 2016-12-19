var zmq = require('zmq');

exports.socket = function(type) {
    if (type == 'req') {
        var req = zmq.socket('req');
        req.request = function() {
            var array = Array.apply(null, arguments);
            return new Promise(function (resolve, reject) {
                req.on('message', function () {
                    var msg = Array.apply(null, arguments);
                    resolve(msg);
                });
                req.on('error', function(err) {
                    reject(err);
                });
                req.send(array);
            });
        };
        return req;
    } else {
        return zmq.socket(type);
    }
}
