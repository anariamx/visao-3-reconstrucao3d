# TERCEIRO TRABALHO PARA A DISCIPLINA DE VISÃO COMPUTACIONAL 
# Reconstrução da posição 3D durante o movimento de um robô móvel

# Breno Ferreira e Mariana Godoy
 

# Bibliotecas usadas
#parameters
import numpy as np
import json
#detect_markers
import cv2
from cv2 import aruco
import matplotlib.pyplot as plt
debug = 1
# ---Funções 

# Lê pontos de interesse do arUco de um frame de um vídeo
## ENTRADAS
# 	img: frame obtido do método 'vid.read()', onde vid é o vídeo desejado
# 	ID: ID do aruco a ser detectado
## SAÍDAS
# 	corners: vetor de pontos encontrados em formato (numpy 4x2)
#			 Os valores são coordenadas dos cantos do aruco detectado.
# 			 Caso não seja encontrado aruco, retorna uma matriz com np.NaN
# 	found: 1 caso tenha encontrado, 0 caso não tenha
def read_frame(img, ID):
	found = 0

	aruco_dict = aruco.Dictionary_get(aruco.DICT_4X4_50)
	parameters =  aruco.DetectorParameters_create()

	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)
	
	try: #Verifica se algum aruco foi detectado, qualquer um:
		len(ids)
	except TypeError:
		# Caso nenhum aruco seja detectado, isto impede crash. Retorna NaN
		print("Nenhum Aruco Detectado, retornando nan")
		void = np.zeros((4, 2))
		void[:] = np.NaN
		return void, 0

	# ---Filtro: detecta apenas os arucos com ID igual ao especificado na variável de entrada 'ID'
	
	
	ids = np.reshape(ids, len(ids))		# Remodela ids para conformidade com loops

	
	# Verifica o ID de todos os arucos encontrados e retorna apenas o com ID correto
	for i in range(0, len(ids)):
		if ids[i] == ID:
			found = found + 1
			return corners[0][0], found
			
	# Se nenhum aruco com ID válido foi encontrado, retorna NaN:
	if found == 0:
		#Nenhum aruco com ID apropriado foi encontrado
		void = np.zeros((4, 2))
		void[:] = np.NaN
	else:
		print("--WARNING: Quebra de lógica")
	
# - assemble_matrix:
# Cria a matriz B para cálculo da triangulação
## ENTRADAS
# 	P: Lista (1xn) de matrizes de projeção, onde n é o número de câmeras
# 	points: lista (1xn) de pontos, onde n é o número de câmeras (um ponto por câmera)
# 	found:  lista True/False (1xn) indicando em quais câmeras foi detectado o aruco
## SAÍDAS
# 	B: Matriz resultante B, de dimensões variáveis
#
def assemble_matrix(P_raw, points_raw, found):	
	n_found = np.count_nonzero(found)	 #Número de empilhamentos, n câmeras detectando aruco com sucesso
	
	# Montando "coluna" de P's
	P_collumn = P_raw[found]					 # Usa apenas Matrizes de câmeras que detectaram aruco
	P_collumn = np.concatenate(P_collumn,axis=0) # Concatena verticalmente
	# printdb("P_collum:\n{}".format(P_collumn))


	# Montando Matriz de m's
	
	printdb("Shape points_raw: {}".format(np.shape(points_raw)))
	printdb("points_raw = \n{}".format(points_raw))
	# Usa apenas pontos que foram detectados
	points = points_raw[found].copy()
	# printdb("points_raw = \n{}".format(points_raw))
	printdb("points = \n{}".format(points))

	# Coloca os pontos em coordenadas homogêneas
	points = np.concatenate([points,np.ones((n_found,1))], axis=1)

	# i-> linha, j-> coluna
	for j in range(0, n_found):
		# Empilhamos j vetores (3x1) de zeros antes dos pontos, os pontos, e então (n_found-j-1) vetores (3x1) de zeros
		m = np.concatenate([np.zeros((3*j,1)),np.reshape(points[j],(3,1)), np.zeros((3*(n_found-j-1),1))], axis=0)
		
		if j == 0:					# Concatena a coluna mais recente com as anteriores, exceto para a coluna inicial
			m_final = m
		else:	
			m_final = np.concatenate([m_final,m],axis=1) # Concatenação horizontal
		printdb("m_final:\n{}".format(m_final))

	B = np.concatenate([P_collumn,m_final], axis=1)
	printdb("B = \n{}".format(B))
	return B

def printdb(var):
	if debug:
		print("------------")
		print(var)

def get_center(edges):
	x = np.mean(edges[:,0])
	y = np.mean(edges[:,1])
	center = np.array([x,y])
	printdb(center)
	return center

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

P = np.array([P0, P1, P2, P3])

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
		print("--PYTHON: Empty Frame 0")
		break
	if img_1 is None:
		print("--PYTHON: Empty Frame 1")
		break
	if img_2 is None:
		print("--PYTHON: Empty Frame 2")
		break
	if img_3 is None:
		print("--PYTHON: Empty Frame 3")
		break
	
	# print(img_1)

	# -----4º: Ler pontos da imagem (frame) do vídeo
	points_0_edges, bool_found_0 = read_frame(img_0, 0)
	points_1_edges, bool_found_1 = read_frame(img_1, 0)
	points_2_edges, bool_found_2 = read_frame(img_2, 0)
	points_3_edges, bool_found_3 = read_frame(img_3, 0)

	# Calcula o centro do Aruco de cada imagem
	points_0 = get_center(points_0_edges)
	points_1 = get_center(points_1_edges)
	points_2 = get_center(points_2_edges)
	points_3 = get_center(points_3_edges)

	# Coloca pontos (numpy) numa lista
	points = np.array([points_0,points_1,points_2,points_3]) # [camera][coordenadas do ponto]

	# Cria vetor True/False de "Aruco encontrado nesta câmera"
	found_camera = np.array([bool_found_0,bool_found_1,bool_found_2,bool_found_3])
	found_camera = found_camera > 0
	print("Câmeras aruco detectado: {}".format(found_camera))
	
	# verifica se é possível realizar a triangulação
	num_found = np.count_nonzero(found_camera)
	if num_found < 2:
		print("---PYTHON: Pulando frame por insuficiência de pontos para triangulação")
	else:
		# -----5º: Monta a matriz final com pontos e Matrizes P (segundo método do slide)
		B = assemble_matrix(P, points, found_camera)



	# -----6º: Calcular a posição com base na decomposição por valor singular 
	# np.linalg.svd(B)

	# Colocar a posição calculada num vetor


# -----7º: Imprimir vetor de posições num espaço 3D

# --FIM
cv2.destroyAllWindows()
