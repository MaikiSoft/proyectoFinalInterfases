// Conexión WebSocket
const socket = new WebSocket('ws://192.168.101.11:5000'); // Reemplaza la URL y el puerto con tu configuración

// Evento de apertura de la conexión WebSocket
socket.onopen = function(event) {
    console.log('Conexión establecida');
};

// Evento de recepción de mensaje desde el servidor
socket.onmessage = function(event) {
    const mensaje = event.data; // Mensaje recibido del servidor
    actualizarChat(mensaje);
};

// Función para agregar un mensaje al chat
function actualizarChat(mensaje) {
    const chat = document.getElementById("comentarios");
    const nuevoMensaje = document.createElement("div");
    nuevoMensaje.textContent = mensaje;
    chat.appendChild(nuevoMensaje);
    chat.scrollTop = chat.scrollHeight; // Desplazar el chat hasta el final para mostrar el nuevo mensaje
}
