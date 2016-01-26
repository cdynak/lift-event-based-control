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

var W = []; // Lift states
var P = []; // External buttons state
var Q = []; // Internal buttons state
for(var i=0; i<lista_pieter.length; i++) {
  W[i] = Array.apply(null, Array(3)).map(Number.prototype.valueOf,0);
}
for(var i=0; i<lista_pieter.max(); i++) {
  P[i] = Array.apply(null, Array(2)).map(Number.prototype.valueOf,0);
}
for(var i=0; i<lista_pieter.length; i++) {
  Q[i] = Array.apply(null, Array(lista_pieter[i])).map(Number.prototype.valueOf,0);
}

console.log("W = ");
console.log(W);
console.log("P = ");
console.log(P);
console.log("Q = ");
console.log(Q);

var sender = new net.Socket();
sender.connect('8089', 'localhost', function(){
//  sender.write("1:1");
});

var listener = new net.Socket();
listener.on('data', function(data) {
  var x = data.toString();
  console.log('listener: ' + x);
  var m = ["",""];
  if(m = x.match(/(\d+):([u|d])/)) {
    if ((m[1] < lista_pieter.max()) && (m[1] >= 0)) {
      switch (m[2]) {
        case "u":
          P[m[1]][1] = 1;
          break;
        case "d":
          P[m[1]][0] = 1;
          break;
      }
    }

    console.log("P = ");
    console.log(P);
  } else if(m = x.match(/(\d+):(\d+)/)){
    var dir = m[2]-W[m[1]][2];
    console.log('dir: '+dir);
    if(dir > 0) {
      var y=m[1]+':'+(parseInt(W[m[1]][2])+1);
      sender.write(y,function(){
        console.log('sender: '+y);
        Q[m[1]][m[2]] = 1;
        W[m[1]][2]++;
      });
    } else if (dir < 0) {
      var y=m[1]+':'+(parseInt(W[m[1]][2])-1);
      sender.write(y,function(){
        console.log('sender: '+y);
        Q[m[1]][m[2]] = 1;
        W[m[1]][2]++;
      });
    } else {
      Q[m[1]][m[2]] = 0;
    }

    console.log("Q = ");
    console.log(Q);
  } else if(m = x.match(/(\d+):a/)){
    var war = 0;
    var par = 0;
    for(var i = W[m[1]][2]+1; war==0 && i<lista_pieter[m[1]]; i++) {
      if(Q[m[1]][i]==1) {
        war = 1;
        par = i;
      }
    }
    if(war==1) {
      var y=m[1]+':'+par;
      sender.write(y);
      console.log('sender: '+y);
    }

    console.log("W = ");
    console.log(W);
  } else {
    console.log("bad m syntax");
  }
});
listener.connect('8090', 'localhost');
