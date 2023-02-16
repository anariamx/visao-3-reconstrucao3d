import cv2
import numpy as np
from cv2 import aruco
import matplotlib.pyplot as plt
import sys

# Esse exemplo foi adulterado e não imprime mais os arucos no vídeo...mas faz o que tem que fazer >:)


file_name = "video01.mkv" 
aruco_dict = aruco.Dictionary_get(aruco.DICT_4X4_50)
parameters =  aruco.DetectorParameters_create()
vid = cv2.VideoCapture(file_name)

i = 0

while True:
    i = i+1
    _, img = vid.read()
    if img is None:
        print("Empty Frame")
        break

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)
    
    # Filtro: detecta apenas os arucos com ID 1
    filter_index = ids == 1
    filter_index = np.reshape(filter_index, len(ids)) # Transforma vetor filter_index de formato (n,1) para (n)                           
    for i in range(0, len(corners)):                  # Reescreve o vetor de corners mantendo apenas os arucos com ID == 1
        if filter_index[i]:
            corners = corners[i]

    # frame_markers = aruco.drawDetectedMarkers(img.copy(), corners, ids)
    # cv2.imshow('output', frame_markers)
    print("corner[{}]:\n{}\nID:\n{}\nRejected:\n{}".format(i, corners, ids, rejectedImgPoints))

    if cv2.waitKey(1) == ord('q'):
        break

cv2.destroyAllWindows()

