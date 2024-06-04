import cv2
import mediapipe as mp
import time
import threading

mp_face_mesh = mp.solutions.face_mesh
mp_drawing = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

landmark_133 = None #ojo izquierdo
landmark_362 = None #ojo derecho

#giro izquierda

landmark_33 = None #parte serca al ojo
landmark_34 = None #parte lejos al ojo

#giro derecha

landmark_263 = None #parte serca al ojo
landmark_264 = None #parte lejos al ojo

def print_landmarks():
    global landmark_133, landmark_362, landmark_33, landmark_34, landmark_263, landmark_264
    while True:
        #si se salen de los limites izquierda y derecha
        if landmark_133 is not None and landmark_362 is not None:
        #     print(f'izquierdo {landmark_133}')
        #     print(f'derecho {landmark_362}')
            if landmark_133 < 3:
                print('fuera de los limites izquierdo')
            elif landmark_362 > 7:
                print('fuera de los limites derecho')
        if landmark_33 is not None and landmark_34 is not None:
            # print(f'lejos al ojo {landmark_34}')
            # print(f'serca al ojo {landmark_33}')
            if(landmark_33 - landmark_34) <=1:
                print('mirando a la izquierda')
        if landmark_263 is not None and landmark_264 is not None:
        #     print(f'serca al ojo {landmark_263}')
        #     print(f'lejos al ojo {landmark_264}')
            if (landmark_264 - landmark_263) <= 1:
                print('viendo a la derecha')
            
        time.sleep(1)

thread = threading.Thread(target=print_landmarks)
thread.daemon = True  # Establece el hilo como daemon
thread.start()

try:
    with mp_face_mesh.FaceMesh(
        static_image_mode=False,
        max_num_faces=1,
        min_detection_confidence=0.5) as face_mesh:

        while True:
            ret, frame = cap.read()
            if ret == False:
                break
            frame = cv2.flip(frame,1)
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = face_mesh.process(frame_rgb)

            if results.multi_face_landmarks is not None:
                for face_landmarks in results.multi_face_landmarks:
                    mp_drawing.draw_landmarks(frame, face_landmarks,
                        mp_face_mesh.FACEMESH_TESSELATION,
                        mp_drawing.DrawingSpec(color=(0, 255, 255), thickness=1, circle_radius=1),
                        mp_drawing.DrawingSpec(color=(255, 0, 255), thickness=1))
                    
                    landmark_133 = face_landmarks.landmark[133].x * 10 #ojo izquierdo
                    landmark_362 = face_landmarks.landmark[362].x * 10 #ojo derecho
                    
                    #giro izquierda
                    landmark_33 = round(face_landmarks.landmark[33].x * 100)
                    landmark_34 = round(face_landmarks.landmark[34].x * 100)

                    #giro derecha
                    landmark_263 = round(face_landmarks.landmark[263].x * 100)
                    landmark_264 = round(face_landmarks.landmark[264].x * 100)
                    

            cv2.imshow("Frame", frame)
            k = cv2.waitKey(1) & 0xFF
            if k == 27:
                break
except KeyboardInterrupt:
    pass
finally:
    cap.release()
    cv2.destroyAllWindows()
