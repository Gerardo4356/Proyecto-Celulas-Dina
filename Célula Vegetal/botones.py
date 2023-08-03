import cv2
import mediapipe as mp
import pygame
import time

# Creación de los objetos necesarios
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

# Lista de los puntos y tiempos
points = []
points_touch_time = [0] * 10
is_audio_playing = [False] * 10

# Función para capturar los clicks del mouse
def capture_click(event, x, y, flags, param):
    global points
    if event == cv2.EVENT_LBUTTONDOWN:
        if len(points) < 10:
            points.append((x, y))
            print(f"Point {len(points)}: ({x}, {y})")
        else:
            print("Todos los puntos han sido establecidos.")

# Inicialización del video
cap = cv2.VideoCapture(0)

# Creación de la ventana y asignación de la función de captura de clicks
cv2.namedWindow("Video")
cv2.setMouseCallback("Video", capture_click)

# Inicialización del modelo de manos y de pygame
with mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.5, min_tracking_confidence=0.5) as hands:
    pygame.mixer.init()
    while cap.isOpened():
        ret, frame = cap.read()

        # Volteamos la imagen para que sea más natural
        frame = cv2.flip(frame, 1)

        # Pasamos la imagen a RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Hacemos la detección de manos
        result = hands.process(rgb_frame)

        # Dibujamos las manos
        if result.multi_hand_landmarks:
            for hand_landmarks in result.multi_hand_landmarks:
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        # Dibujamos los puntos y comprobamos si el índice está sobre el punto
        for i, point in enumerate(points):
            cv2.circle(frame, point, 10, (255, 255, 255), -1)

            if result.multi_hand_landmarks:
                index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
                h, w, _ = frame.shape
                x, y = int(index_tip.x * w), int(index_tip.y * h)
                if abs(x - point[0]) < 20 and abs(y - point[1]) < 20:
                    if i == 9:  # Si es el punto 10, detenemos la música
                        pygame.mixer.music.stop()
                    elif not is_audio_playing[i]:
                        is_audio_playing[i] = True
                        if not pygame.mixer.music.get_busy():
                            pygame.mixer.music.load(f'{i+1}.mp3')
                            pygame.mixer.music.play()
                else:
                    is_audio_playing[i] = False

        # Mostramos el video
        cv2.imshow('Video', frame)

        # Si se presiona la tecla q, salimos del bucle
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# Liberamos los recursos y cerramos las ventanas
cap.release()
cv2.destroyAllWindows()
