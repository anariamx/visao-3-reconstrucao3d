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

# Lê pontos de interesse do arUco de um frame de um vídeo
## ENTRADAS
# 	img: frame obtido do método 'vid.read()', onde vid é o vídeo desejado
# 	ID: ID do aruco a ser detectado
## SAÍDAS
# 	corners: vetor de pontos encontrados.
#			 Os valores são coordenadas dos cantos do aruco detectado.
# 	n_found: Número de arucos com ID correto encontrados no frame

def read_frame(img, ID):
	n_found = 0

	aruco_dict = aruco.Dictionary_get(aruco.DICT_4X4_50)
	parameters =  aruco.DetectorParameters_create()

	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)

	# Filtro: detecta apenas os arucos com ID igual ao especificado na variável de entrada 'ID'
	try:
		corners_filtered = [0 for i in range(len(ids))] 	# Inicializa vetor
	except TypeError:
		# print("Nenhum aruco detectado nesta imagem")
		return 0, 0
	

	for i in range(0, len(ids)):
		# print(i)
		if ids[i] == ID:
			corners_filtered[i] = corners[i]
			# print("ok")
			# print(corners_filtered[i])
			n_found = n_found + 1
		# else:
		# 	print("skip.")
	# print(corners_filtered)


	return corners_filtered, n_found
	




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

# print('Camera 0\n')
# print('Resolucao',res0,'\n')
# print('Parametros intrinsecos:\n', K0, '\n')
# print('Parametros extrinsecos:\n')
# print('R0\n', R0, '\n')
# print('T0\n', T0, '\n')
# print('Distorcao Radial:\n', dis0)

# -----2º: Montar as matrizes de projeção P0,P1,P2 e P3
# Lembre-se de inverter a matriz de transformação geométrica, [R,T]

# P0 = np.linalg.inv(np.dot(K0, np.hstack((R0, T0.reshape(3, 1)))))
# P1 = np.linalg.inv(np.dot(K1, np.hstack((R1, T1.reshape(3, 1)))))
# P2 = np.linalg.inv(np.dot(K2, np.hstack((R2, T2.reshape(3, 1)))))
# P3 = np.linalg.inv(np.dot(K3, np.hstack((R3, T3.reshape(3, 1)))))

#placeholder block
P0 = np.zeros((3,4))
P0[0][0] = 1
P0[1][1] = 1
P0[2][2] = 1
P1 = P0.copy()
P1[0][0] = 2
P2 = P0.copy()
P2[0][0] = 3
P3 = P0.copy()
P3[0][0] = 4
#placeholder block end

P = [P0, P1, P2, P3]
print("P:\n{}".format(P))
# -----3º: Loop de leitura de frames dos vídeos

file_name_0 = "camera-00.mp4"
file_name_1 = "camera-01.mp4"
file_name_2 = "camera-02.mp4"
file_name_3 = "camera-03.mp4"

vid_0 = cv2.VideoCapture(file_name_0)
vid_1 = cv2.VideoCapture(file_name_1)
vid_2 = cv2.VideoCapture(file_name_2)
vid_3 = cv2.VideoCapture(file_name_3)

while True:
	_, img_0 = vid_0.read()
	_, img_1 = vid_1.read()
	_, img_2 = vid_2.read()
	_, img_3 = vid_3.read()

	#Sai do loop no caso de frames vazios em qualquer um dos vídeos (final dos vídeos)
	if img_0 is None:
		print("Empty Frame 0")
		break
	if img_1 is None:
		print("Empty Frame 1")
		break
	if img_2 is None:
		print("Empty Frame 2")
		break
	if img_3 is None:
		print("Empty Frame 3")
		break
	
	# -----4º: Ler pontos da imagem (frame) do vídeo
	# print("----- Video 0")
	points_0, bool_found_0 = read_frame(img_0, 0)
	# print("----- Video 1")
	points_1, bool_found_1 = read_frame(img_1, 0)
	# print("----- Video 2")
	points_2, bool_found_2 = read_frame(img_2, 0)
	# print("----- Video 3")
	points_3, bool_found_3 = read_frame(img_3, 0)
	
	found_camera = [bool_found_0,bool_found_1,bool_found_2,bool_found_3]
	print(found_camera)

	# -----5º: Montar a matriz final com pontos e Matrizes P (segundo método)
	




	# -----6º: Calcular a posição com base na decomposição por valor singular 
	# np.linalg.svd(B)

	# Colocar a posição calculada num vetor


# -----7º: Imprimir vetor de posições num espaço 3D

# --FIM
cv2.destroyAllWindows()
