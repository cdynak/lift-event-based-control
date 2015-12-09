var net = require('net');

Array.prototype.max = function() {
  return Math.max.apply(null, this);
};
Array.prototype.min = function() {
  return Math.min.apply(null, this);
};

var lista_pieter = []
if(process.argv[2]) {
  lista_pieter = JSON.parse(process.argv[2]);
} else {
  lista_pieter = [10, 10, 10, 10, 10, 10, 10, 10, 10, 7, 8, 20];
}
console.log("floor list: " + lista_pieter);
console.log("max floor: " + lista_pieter.max());

var P = [];
var Q = [];
for(var i=0; i<lista_pieter.max(); i++) {
  P[i] = new Array(2);
}
for(var i=0; i<lista_pieter.length; i++) {
  Q[i] = new Array(lista_pieter[i]);
}

console.log(P);
console.log(Q);

var sender = new net.Socket();
sender.connect('8089', 'localhost', function(){
  sender.write("1:1");
});

var listener = new net.Socket();
listener.on('data', function(data) {
  console.log(data.toString());
});
listener.connect('8090', 'localhost');
