import numpy as np
import json

# Function to read the intrinsic and extrinsic parameters of each camera
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


#Load cameras parameters
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



