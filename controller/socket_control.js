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

var P = []; // External buttons state
var Q = []; // Internal buttons state
for(var i=0; i<lista_pieter.max(); i++) {
  P[i] = Array.apply(null, Array(2)).map(Number.prototype.valueOf,0);
}
for(var i=0; i<lista_pieter.length; i++) {
  Q[i] = Array.apply(null, Array(lista_pieter[i])).map(Number.prototype.valueOf,0);
}

console.log(P);
console.log(Q);

/*var sender = new net.Socket();
sender.connect('8089', 'localhost', function(){
  sender.write("1:1");
}); */

var listener = new net.Socket();
listener.on('data', function(data) {
	var x = data.toString();
	var externalBtn = x.match(/(\d+):([u|d])/);
	if ((externalBtn[1] < lista_pieter.max()) && (externalBtn[1] >= 0)) {
			switch (externalBtn[2]) {
				case "u":
					P[externalBtn[1]][1] = 1;
					break;
				case "d":
					P[externalBtn[1]][0] = 1;
					break;
			}
  	console.log(P);
	}
});
listener.connect('8090', 'localhost');
