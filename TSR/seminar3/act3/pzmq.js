var zmq = require('zmq');

exports.socket = function(type) {
    if (type == 'req') {
        var req = zmq.socket('req');
        req.request = function() {
            var array = Array.apply(null, arguments);
            var timeout = array.splice(0, 1)[0];
            return new Promise(function (resolve, reject) {
                req.on('message', function () {
                    var msg = Array.apply(null, arguments);
                    resolve(msg);
                });
                req.on('error', function(err) {
                    reject(err);
                });
                req.send(array);
                if (timeout == 0) return;
                setTimeout(function() {
                    req.on('message', function(){});
                    req.on('error', function(){});
                    req.reconnect();
                    reject("TMOUT");
                }, timeout * 1000);
            });
        };
        return req;
    } else {
        return zmq.socket(type);
    }
}
