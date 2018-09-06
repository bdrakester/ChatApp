document.addEventListener("DOMContentLoaded", () => {
  // Connect to websocket
  var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

  //  When connected, configure submit
  socket.on("connect", () => {
    const chatroom = document.querySelector("#send").dataset.room;
    socket.emit("join", {"chatroom": chatroom});
    document.getElementById("send").onclick = () => {
      const message = document.getElementById("message").value;
      //const chatroom = document.querySelector("#send").dataset.room;
      socket.emit("send message", {"message": message, "chatroom": chatroom});
    };
  });

  // When a new message is received, add to list
  socket.on("receive message", data => {
    const li = document.createElement("li");
    li.innerHTML = `${data.time} ${data.username} :  ${data.message}`;
    document.querySelector("#messages").append(li);
    document.querySelector("#message").value = "";
  });
});
