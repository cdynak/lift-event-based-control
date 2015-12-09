var net = require('net');

var sender = new net.Socket();
sender.connect('8089', 'localhost', function(){
  sender.write("1:1");
});

var listener = new net.Socket();
listener.on('data', function(data) {
  console.log(data.toString());
});
listener.connect('8090', 'localhost');
