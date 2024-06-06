
# Proyeto Final

Este proyecto consiste en dos servidores que se comunican entre sí para la captura de imágenes de una cámara y el intercambio de mensajes. Uno de los servidores captura la imagen de la cámara y envía tanto las imágenes como algunos mensajes al otro servidor. El otro servidor recibe los mensajes y permite a los clientes consultar el último mensaje recibido.

## Servidor de Recepción de Mensajes

Este servidor está diseñado para recibir mensajes y permitir a los clientes consultar el último mensaje recibido.

### Tecnologías Utilizadas:
- Python
- Flask

### Configuración del Servidor:
1. Instalar las dependencias del proyecto:
    ```bash
    pip install Flask
    ```

2. Ejecutar el servidor:
    ```bash
    python server_receive_messages.py
    ```

### Rutas Disponibles:
- `/receive_message` (POST): Esta ruta recibe mensajes en formato JSON. El cuerpo del mensaje debe contener una clave `"message"` con el contenido del mensaje.
- `/get_last_message` (GET): Esta ruta devuelve el último mensaje recibido en formato JSON.

## Servidor de Captura de Imágenes y Envío de Mensajes

Este servidor captura imágenes de una cámara y envía mensajes basados en la detección de landmarks faciales.

### Tecnologías Utilizadas:
- Python
- Flask
- OpenCV
- MediaPipe

### Configuración del Servidor:
1. Instalar las dependencias del proyecto:
    ```bash
    pip install Flask Flask-SocketIO opencv-python-headless mediapipe requests
    ```

2. Ejecutar el servidor:
    ```bash
    python server_capture_images.py
    ```

### Funcionamiento:
Este servidor captura imágenes de la cámara en tiempo real y utiliza MediaPipe para detectar landmarks faciales. Basándose en la posición de estos landmarks, se generan mensajes que son enviados al otro servidor a través de una solicitud POST.

## Cliente

Se proporciona un cliente básico implementado en HTML, CSS y JavaScript para visualizar las imágenes de la cámara y consultar el último mensaje recibido.

### Tecnologías Utilizadas:
- HTML
- CSS
- JavaScript

### Ejecución:
1. La persona que iniciara la camara debe ejecutar el archivo camara.py:
   
  ```bash
    cd camara
    python camara.py
  ```
2. La persona que recibira las imagenes y vera la conversacion ejecutara el servidor.py:
```bash
    cd api
    python servidor.py
```

---


