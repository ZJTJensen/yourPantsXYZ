var http = require('http').createServer().listen(4000);
var io = require('socket.io').listen(http);



// when a connection happens (client enters on the website)
io.on('connection', function(socket) {
    
    socket.on('message', function(data) {
       
        // emits the  to the client
        // socket.emit(data);
        io.emit('working', data);

    });

});