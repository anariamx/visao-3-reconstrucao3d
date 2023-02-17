# TERCEIRO TRABALHO PARA A DISCIPLINA DE VISÃO COMPUTACIONAL 
# Reconstrução da posição 3D durante o movimento de um robô móvel

# Breno Ferreira e Mariana Godoy

# Para impressão de parâmetros em tela, faça debug = 1
debug = 0

# Bibliotecas usadas
import numpy as np
import json
import cv2
from cv2 import aruco
import matplotlib.pyplot as plt

# Vetor de posições finais 3d
path = []

# Vetores de posições finais 2d (para conferência)
path_2d_0 = []
path_2d_1 = []
path_2d_2 = []
path_2d_3 = []

# ---Funções 

###### read_image:
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
	
	try: 								# Verifica se algum aruco foi detectado, qualquer um:
		len(ids)
	except TypeError:					# Caso nenhum aruco seja detectado, isto impede crash. Retorna NaN
		void = np.zeros((4, 2))
		void[:] = np.NaN
		return void, 0

	# ---Filtro: detecta apenas os arucos com ID igual ao especificado na variável de entrada 'ID'

	ids = np.reshape(ids, len(ids))		# Remodela ids para conformidade com loops
	for i in range(0, len(ids)):		# Verifica o ID de todos os arucos encontrados e retorna apenas o com ID correto
		if ids[i] == ID:
			found = found + 1
			return corners[0][0], found
			
	
	if found == 0:						# Se nenhum aruco com ID válido foi encontrado, retorna NaN:
		void = np.zeros((4, 2))
		void[:] = np.NaN
		return void, 0
	
###### - assemble_matrix:
# Cria a matriz B para cálculo da triangulação, de acordo com os requisitos para aplicação do SVD mais à frente no código
## ENTRADAS
# 	P_raw: Lista (1xn) de matrizes de projeção, onde n é o número de câmeras. Ainda não filtrado
# 	points_raw: lista (1xn) de pontos, onde n é o número de câmeras (um ponto por câmera). Ainda não filtrado
# 	found:  lista True/False (1xn) indicando em quais câmeras foi detectado o aruco correto
## SAÍDAS
# 	B: Matriz resultante B, de dimensões variávei
def assemble_matrix(P_raw, points_raw, found):	
	n_found = np.count_nonzero(found)	 					#Número de empilhamentos, n câmeras detectando aruco com sucesso
	
	# --Montando "coluna" de P's
	P_collumn = P_raw[found]					 			# Usa apenas Matrizes de câmeras que detectaram aruco
	P_collumn = np.concatenate(P_collumn,axis=0) 			# Concatena verticalmente

	# --Montando Matriz de m's
	
	points = points_raw[found].copy()			 			# Usa apenas pontos que foram detectados
	points = np.concatenate([points,
							np.ones((n_found,1))], axis=1)  # Coloca os pontos em coordenadas homogêneas

	# i-> linha, j-> coluna
	for j in range(0, n_found):
																	
		m = np.concatenate([np.zeros((3*j,1)),				# Empilhamos j vetores (3x1) de zeros antes dos pontos, os pontos, e então (n_found-j-1) vetores (3x1) de zeros
			np.reshape(points[j],(3,1)), 
			np.zeros((3*(n_found-j-1),1))], axis=0)
		
		if j == 0:											# Concatena a coluna mais recente com as anteriores, exceto para a coluna inicial
			m_final = m
		else:	
			m_final = np.concatenate([m_final,m],axis=1) 	# Concatenação horizontal
		
	B = np.concatenate([P_collumn,m_final], axis=1)
	return B

def printdb(var):
	if debug:
		print("------------")
		print(var)
	return

def get_center(edges):
	x = np.mean(edges[:,0])
	y = np.mean(edges[:,1])
	center = np.array([x,y])
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

# ATENÇÃO: Parâmetros R0 e T0 convertem da câmera para o mundo:

K0, R0, T0, res0, dis0 = camera_parameters('0.json')
K1, R1, T1, res1, dis1 = camera_parameters('1.json')
K2, R2, T2, res2, dis2 = camera_parameters('2.json')
K3, R3, T3, res3, dis3 = camera_parameters('3.json')

# -----2º: Montar as matrizes de projeção P0,P1,P2 e P3
# Lembre-se de inverter a matriz de transformação geométrica, [R,T]

print("----------------- PARÂMETROS")

print("\n--- Parâmetros da câmera 0")
print('Camera 0\n')
print('Resolucao',res0,'\n')
print('Parametros intrinsecos:\n', K0, '\n')
print('Parametros extrinsecos:\n')
print('R0\n', R0, '\n')
print('T0\n', T0, '\n')
print('Distorcao Radial:\n', dis0)

print("\n--- Parâmetros da câmera 1")
print('Camera 1\n')
print('Resolucao',res1,'\n')
print('Parametros intrinsecos:\n', K1, '\n')
print('Parametros extrinsecos:\n')
print('R1\n', R1, '\n')
print('T1\n', T1, '\n')
print('Distorcao Radial:\n', dis1)

print("\n--- Parâmetros da câmera 2")
print('Camera 2\n')
print('Resolucao',res2,'\n')
print('Parametros intrinsecos:\n', K2, '\n')
print('Parametros extrinsecos:\n')
print('R2\n', R2, '\n')
print('T2\n', T2, '\n')
print('Distorcao Radial:\n', dis2)

print("\n--- Parâmetros da câmera 3")
print('Camera 3\n')
print('Resolucao',res3,'\n')
print('Parametros intrinsecos:\n', K3, '\n')
print('Parametros extrinsecos:\n')
print('R0\n', R3, '\n')
print('T0\n', T3, '\n')
print('Distorcao Radial:\n', dis3)

# DEBUG: Teste das matrizes RT, MT 

# RT = np.concatenate((R0,T0), axis = 1)
# printdb('matriz RT\n', RT)

# MT = np.concatenate((np.concatenate((R0,T0), axis = 1), [[0, 0, 0, 1]]), axis = 0)

# printdb('matriz MT\n', MT)

# MTinv = np.linalg.inv(MT)
# printdb(MTinv)
 
p = np.concatenate((np.eye(3), [[0], [0],[0]] ), axis = 1)	# matriz de projeção
printdb("Matriz de Projeção pi:\n{}".format(p))

# matriz Pi = Ki * p * [R, T]
P0 =(np.dot(K0, np.dot(p, (np.linalg.inv(np.concatenate((np.concatenate((R0,T0), axis = 1), [[0, 0, 0, 1]]), axis = 0))))))
P1 =(np.dot(K1, np.dot(p, (np.linalg.inv(np.concatenate((np.concatenate((R1,T1), axis = 1), [[0, 0, 0, 1]]), axis = 0))))))
P2 =(np.dot(K2, np.dot(p, (np.linalg.inv(np.concatenate((np.concatenate((R2,T2), axis = 1), [[0, 0, 0, 1]]), axis = 0))))))
P3 =(np.dot(K3, np.dot(p, (np.linalg.inv(np.concatenate((np.concatenate((R3,T3), axis = 1), [[0, 0, 0, 1]]), axis = 0))))))

printdb("P0:\n{}".format(P0))
printdb("P1:\n{}".format(P1))
printdb("P2:\n{}".format(P2))
printdb("P3:\n{}".format(P3))

# Lista de matriz de projeção: cada índice é uma câmera
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

count_loop = 0

while True:
	_, img_0 = vid_0.read()
	_, img_1 = vid_1.read()
	_, img_2 = vid_2.read()
	_, img_3 = vid_3.read()

	printdb("------ Iteração: {}".format(count_loop))

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

	# Vetor de pontos 2d para impressão
	path_2d_0.append(np.array(points_0))
	path_2d_1.append(np.array(points_1))
	path_2d_2.append(np.array(points_2))
	path_2d_3.append(np.array(points_3))

	# Coloca pontos (numpy) numa lista
	points = np.array([points_0,points_1,points_2,points_3]) # points[camera][coordenadas do ponto]

	# Cria vetor True/False de "Aruco encontrado nesta câmera"
	found_camera = np.array([bool_found_0,bool_found_1,bool_found_2,bool_found_3])
	found_camera = found_camera > 0
	
	# verifica se é possível realizar a triangulação
	num_found = np.count_nonzero(found_camera)
	if num_found < 2:
		print("---PYTHON: Pulando frame por insuficiência de pontos para triangulação")
	else:
		# -----5º: Monta a matriz final com pontos e Matrizes P (segundo método do slide)
		B = assemble_matrix(P, points, found_camera)
		printdb("B = \n{}".format(B))



	# -----6º: Calcular a posição com base na decomposição por valor singular 
	U, S, V = np.linalg.svd(B) #decompõe A em 3 matrizes: unitária, diagonal e transposta unitária
	M = V[:4,-1]
	printdb("V = \n{}".format(V))
	printdb("M não normalizado: \n{}".format(M))
	M = M[:]/M[3]
	printdb("M normalizado: \n{}".format(M))
	# Colocar a posição calculada num vetor
	path.append(M)

	count_loop += 1


path = np.array(path)

path_2d_0 = np.array(path_2d_0)
path_2d_1 = np.array(path_2d_1)
path_2d_2 = np.array(path_2d_2)
path_2d_3 = np.array(path_2d_3)

printdb("posições 3d:\n{}".format(path))
printdb("path_2d_0: \n{}".format(path_2d_0))
printdb("path_2d_1: \n{}".format(path_2d_1))
printdb("path_2d_2: \n{}".format(path_2d_2))
printdb("path_2d_3: \n{}".format(path_2d_3))

# -----7º: Imprimir vetor de posições num espaço 3D
lim = [-50,50]
fig = plt.figure(figsize=(8,8))
ax = fig.add_subplot(111, projection='3d')
ax.scatter(path[:,0], path[:,1], path[:,2],c=path[:,2], cmap='Blues')
#ax.set_aspect('equal')
ax.set_title("Caminho do robô")
ax.set_xlabel('X Label')
ax.set_ylabel('Y Label')
ax.set_zlabel('Z Label')
ax.set_xlim(lim)
ax.set_ylim(lim)
ax.set_zlim(lim)

# plt.show()

# Imprime figura 2d das trajetórias
# lim_2d = 

fig_2d = plt.figure(figsize=(8,8))
ax_2d = fig_2d.add_subplot(111)
ax_2d.scatter(path_2d_0[:,0], path_2d_0[:,1],c=path_2d_0[:,1], cmap='Blues')
ax_2d.scatter(path_2d_1[:,0], path_2d_1[:,1],c=path_2d_1[:,1], cmap='Greens')
ax_2d.scatter(path_2d_2[:,0], path_2d_2[:,1],c=path_2d_2[:,1], cmap='Reds')
ax_2d.scatter(path_2d_3[:,0], path_2d_3[:,1],c=path_2d_3[:,1], cmap='Purples')

ax_2d.set_title("Caminho do robô nas 4 câmeras")
ax_2d.set_xlabel('X Label')
ax_2d.set_ylabel('Y Label')
# ax_2d.set_xlim(lim_2d)
# ax_2d.set_ylim(lim_2d)

plt.show()

# --FIM
cv2.destroyAllWindows()
