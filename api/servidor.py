from flask import Flask, jsonify, render_template,request

app = Flask(__name__)

# Lista global para almacenar los mensajes recibidos
last_received_message = None

@app.route('/receive_message', methods=['POST'])
def receive_message():
    global last_received_message
    # Obtener datos del cuerpo de la solicitud
    data = request.get_json()
    if data:  
        message = data.get('message')
        last_received_message = message  # Actualizar el último mensaje recibido
        print("Mensaje recibido:", message)
        return '', 204  # Devuelve una respuesta vacía con el código de estado 204 (No Content)
    else:
        return 'Bad request - Data is not in JSON format', 400  # Devuelve un código de estado 400 si no se proporcionaron datos en formato JSON

@app.route('/get_last_message')
def get_last_message():
    global last_received_message
    # Devolver el último mensaje almacenado en formato JSON
    return jsonify({'last_message': last_received_message})

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, port=8080)
