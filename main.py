# TERCEIRO TRABALHO PARA A DISCIPLINA DE VISÃO COMPUTACIONAL 
# Reconstrução da posição 3D durante o movimento de um robô móvel

# Breno Ferreira e Mariana Godoy
 

# Bibliotecas usadas
#parameters
import numpy as np
import json
#detect_markers
import numpy as np
import cv2
from cv2 import aruco
import matplotlib.pyplot as plt

# Funções 

# # Lê pontos de interesse do arUco de um frame de um vídeo
# def read_frame(file_name):
# 	aruco_dict = aruco.Dictionary_get(aruco.DICT_4X4_50)
# 	parameters =  aruco.DetectorParameters_create()
# 	vid = cv2.VideoCapture(file_name)




# 	return 0 #placeholder

# Função que obtém parâmetros intrínsecos e extrínsecos de uma câmera
def camera_parameters(file):
    camera_data = json.load(open(file))
    K = np.array(camera_data['intrinsic']['doubles']).reshape(3, 3)
    res = [camera_data['resolution']['width'],
           camera_data['resolution']['height']]
    tf = np.array(camera_data['extrinsic']['tf']['doubles']).reshape(4, 4)
    R = tf[:3, :3]
    T = tf[:3, 3].reshape(3, 1)
    dis = np.array(camera_data['distortion']['doubles'])
    return K, R, T, res, dis


# ------- MAIN -------

# -----1º: Obtenção das matrizes e parâmetros das câmeras

# ATENÇÃO: Parâmetros que convertem da câmera para o mundo:
K0, R0, T0, res0, dis0 = camera_parameters('0.json')
K1, R1, T1, res1, dis1 = camera_parameters('1.json')
K2, R2, T2, res2, dis2 = camera_parameters('2.json')
K3, R3, T3, res3, dis3 = camera_parameters('3.json')

print('Camera 0\n')
print('Resolucao',res0,'\n')
print('Parametros intrinsecos:\n', K0, '\n')
print('Parametros extrinsecos:\n')
print('R0\n', R0, '\n')
print('T0\n', T0, '\n')
print('Distorcao Radial:\n', dis0)

# -----2º: Montar as matrizes de projeção P0,P1,P2 e P3
# Lembre-se de inverter a matriz de transformação geométrica, [R,T]

P0 = np.linalg.inv(np.dot(K0, np.hstack((R0, T0.reshape(3, 1)))))
P1 = np.linalg.inv(np.dot(K1, np.hstack((R1, T1.reshape(3, 1)))))
P2 = np.linalg.inv(np.dot(K2, np.hstack((R2, T2.reshape(3, 1)))))
P3 = np.linalg.inv(np.dot(K3, np.hstack((R3, T3.reshape(3, 1)))))

# -----3º: Loop de leitura de frames dos vídeos

file_name_0 = "video01.mkv" #placeholder
file_name_1 = "video01.mkv" #placeholder
file_name_2 = "video01.mkv" #placeholder
file_name_3 = "video01.mkv" #placeholder

aruco_dict = aruco.Dictionary_get(aruco.DICT_4X4_50)
parameters =  aruco.DetectorParameters_create()
vid_0 = cv2.VideoCapture(file_name_0)
vid_1 = cv2.VideoCapture(file_name_1)
vid_2 = cv2.VideoCapture(file_name_2)
vid_3 = cv2.VideoCapture(file_name_3)

while True:
	_, img_0 = vid.read()
	_, img_1 = vid.read()
	_, img_2 = vid.read()
	_, img_3 = vid.read()

	#Sai do loop no caso de frames vazios
	if img_0 is None:
		print("Empty Frame")
		break
	if img_1 is None:
		print("Empty Frame")
		break
	if img_2 is None:
		print("Empty Frame")
		break
	if img_3 is None:
		print("Empty Frame")
		break
	
	# -----4º: Ler pontos do frame
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)
	#lembrete: Colocar filtro de ID igual a zero

	# -----5º: Montar a matriz final com pontos e Matrizes P
	
	
	# Colocar a posição calculada num vetor


# Imprimir vetor de posições num espaço 3D

# --FIM
cv2.destroyAllWindows()
