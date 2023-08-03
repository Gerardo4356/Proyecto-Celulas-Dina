# WARP Perspective
import cv2 #pip install opencv-python

vidcap = cv2.VideoCapture("video.mp4")
success,image = vidcap.read()

while success:
    success,image = vidcap.read()
    frame = cv2.resize(image, (270,480))
    
    # Coordenadas
    tl = (222,222)
    bl = (222,222)
    tr = (222,222)
    br = (222,222)
    
    cv2.circle(frame, tl, 5, (0, 0, 255), -1)
    cv2.circle(frame, bl, 5, (0, 0, 255), -1)
    cv2.circle(frame, tr, 5, (0, 0, 255), -1)
    cv2.circle(frame, br, 5, (0, 0, 255), -1)
    
    
    cv2.imshow('Video', frame)
    
    if cv2.waitKey(1)==27:
        break   