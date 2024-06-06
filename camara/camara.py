from flask import Flask, Response
from flask_socketio import SocketIO, emit
import cv2
import threading
import mediapipe as mp
import time
import requests

app = Flask(__name__)
socketio = SocketIO(app)

# Configuración de MediaPipe
mp_face_mesh = mp.solutions.face_mesh
mp_drawing = mp.solutions.drawing_utils

# Variables globales para los landmarks
landmark_133, landmark_362, landmark_33, landmark_34, landmark_263, landmark_264 = [None] * 6

# Captura de video
cap = cv2.VideoCapture(0)

def print_landmarks():
    global landmark_133, landmark_362, landmark_33, landmark_34, landmark_263, landmark_264
    while True:
        message = ""
        if landmark_133 is not None and landmark_362 is not None:
            if landmark_133 < 3:
                message = 'Fuera de los límites izquierdo'
                print('Fuera de los límites izquierdo')
            elif landmark_362 > 7:
                message = 'Fuera de los límites derecho'
                print('Fuera de los límites derecho')
        if landmark_33 is not None and landmark_34 is not None:
            if (landmark_33 - landmark_34) <= 1:
                message = 'Mirando a la izquierda'
                print('Mirando a la izquierda')
        if landmark_263 is not None and landmark_264 is not None:
            if (landmark_264 - landmark_263) <= 1:
                message = 'Viendo a la derecha'
                print('Viendo a la derecha')

        if message:
            url = 'http://127.0.0.1:8080/receive_message'
            data = {'message': message}
            requests.post(url, json=data)

        time.sleep(1)

def gen_frames():
    global landmark_133, landmark_362, landmark_33, landmark_34, landmark_263, landmark_264
    with mp_face_mesh.FaceMesh(
        static_image_mode=False,
        max_num_faces=1,
        min_detection_confidence=0.5) as face_mesh:

        while True:
            ret, frame = cap.read()
            if not ret:
                break
            frame = cv2.flip(frame, 1)
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = face_mesh.process(frame_rgb)

            if results.multi_face_landmarks is not None:
                for face_landmarks in results.multi_face_landmarks:
                    mp_drawing.draw_landmarks(frame, face_landmarks,
                                              mp_face_mesh.FACEMESH_TESSELATION,
                                              mp_drawing.DrawingSpec(color=(0, 255, 255), thickness=1, circle_radius=1),
                                              mp_drawing.DrawingSpec(color=(255, 0, 255), thickness=1))

                    landmark_133 = face_landmarks.landmark[133].x * 10  # ojo izquierdo
                    landmark_362 = face_landmarks.landmark[362].x * 10  # ojo derecho
                    landmark_33 = round(face_landmarks.landmark[33].x * 100)  # giro izquierda
                    landmark_34 = round(face_landmarks.landmark[34].x * 100)
                    landmark_263 = round(face_landmarks.landmark[263].x * 100)  # giro derecha
                    landmark_264 = round(face_landmarks.landmark[264].x * 100)

            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    thread = threading.Thread(target=print_landmarks)
    thread.daemon = True  # Establece el hilo como daemon
    thread.start()
    socketio.run(app, host='0.0.0.0', port=5000)

# Liberar recursos al finalizar
cap.release()
cv2.destroyAllWindows()
