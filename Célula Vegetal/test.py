import cv2
import numpy as np

# Cargar el video
vidcap = cv2.VideoCapture("video.mp4")

while True:
    # Leer un fotograma del video
    ret,image = vidcap.read()
    frame = cv2.resize(image, (270,480))

    if ret:
        # Convertir el fotograma a escala de grises
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Aplicar el algoritmo de detección de bordes Canny
        edges = cv2.Canny(gray, 50, 150, apertureSize=3)

        # Encontrar los contornos de la imagen
        contours, hierarchy = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        if contours:
            # Seleccionar el contorno más grande (el del documento)
            largest_contour = max(contours, key=cv2.contourArea)

            # Calcular la envolvente convexa del contorno
            hull = cv2.convexHull(largest_contour)

            # Calcular la transformación de perspectiva
            epsilon = 0.02 * cv2.arcLength(hull, True)
            approx = cv2.approxPolyDP(hull, epsilon, True)
            w, h = 800, 1000
            dst = np.float32([[0, 0], [w, 0], [w, h], [0, h]])
            approx = np.float32(approx)
            dst = np.float32(dst)
            M = cv2.getPerspectiveTransform(approx, dst)

            # Aplicar la transformación de perspectiva al fotograma
            warped = cv2.warpPerspective(frame, M, (w, h))

            # Recortar el documento del fotograma
            x, y, w, h = cv2.boundingRect(largest_contour)
            cropped = warped[y:y+h, x:x+w]

            # Mostrar el resultado
            cv2.imshow('Recorte', cropped)

        else:
            # No se encontró ningún contorno
            cv2.imshow('Recorte', frame)

    else:
        # No se pudo leer un fotograma del video
        break

    # Esperar la tecla 'q' para salir
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

#
