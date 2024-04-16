import json
from classes.BIP import BIP
from classes.Config import Config
from classes.Users import Users
from classes.BaseStation import BaseStation
from classes.Objects import Objects
import math
import numpy as np

users_file = 'users.json'
bs_file = 'base_stations.json'
obj_file = 'objects.json'

config = Config()

def load_users():
    users = {}
    with open(users_file) as json_file:
        data = json.load(json_file)
        data = data['users']
        
        for i in range(0, config.us):
            x = {}
            y = {}
            height = {}
            orientation = {}
            ang_azim = {}
            for j in range(0, config.ti):
                x[j+1] = data[i]['coordinates_by_time'][j]['x']
                y[j+1] = data[i]['coordinates_by_time'][j]['y']
                height[j+1] = data[i]['coordinates_by_time'][j]['height_cm']
                orientation[j+1] = data[i]['coordinates_by_time'][j]['orientation']
                ang_azim[j+1] = data[i]['coordinates_by_time'][j]['ang_azim']
            
            users[i + 1] = Users(data[i]['id'], x, y, height, orientation, ang_azim)
            
        return users
    
def load_base_stations():
    base_stations = {}
    with open(bs_file) as json_file:
        data = json.load(json_file)
        data = data['bs']
        
        for i in range(1, config.bs+1):
            base_stations[i] = BaseStation(data[str(i)]['id'],
                                           data[str(i)]['x'],
                                           data[str(i)]['y'],
                                           data[str(i)]['height_cm'])
            
        return base_stations
    
    
def load_objects():
    objects = {}
    with open(obj_file) as json_file:
        data = json.load(json_file)
        data = data['obj']
        
        for i in range(1, config.obj+1):
            objects[i] = Objects(data[str(i)]['id'],
                                           data[str(i)]['x'],
                                           data[str(i)]['y'],
                                           data[str(i)]['height_cm'])
            
        return objects

    
    
    
#A função busca o ângulo de chegada do sinal (Fase do sinal de chegada no usuário em relação à BS 
#Ângulo que chega no ponto B vindo de A
def getAoA(user, bs, t):
    az = math.atan2(bs.y-user.y[t],bs.x-user.x[t])
    el = math.asin((bs.height-user.height[t])/np.linalg.norm(np.array([user.x[t], user.y[t], user.height[t]])-np.array([bs.x, bs.y, bs.height])))
    aoa = [az,el]
    aoa = np.rad2deg(aoa)
    return aoa


#A função busca o angulo de partida do sinal (Fase do sinal saindo da BS na direção do usuário)
#Ângulo que sai do ponto A em dieração ao ponto B
def getAoD(user, bs, t):
    az=math.atan2(user.y[t]-bs.y,user.x[t]-bs.x)
    el=math.asin((user.height[t]-bs.height)/np.linalg.norm(np.array([user.x[t], user.y[t], user.height[t]])-np.array([bs.x, bs.y, bs.height])))
    aod=[az,el]
    aod=np.rad2deg(aod)
    return aod


#Verifica auto bloqueio
def autoBlockage(user, t, aoa):
    dif=abs(aoa[0]-user.ang_azim[t]); #Verifica a diferenca entre o angulo de chegada e a oritação
    #limite=2; #phi - limite definido no artigo 2 graus
    
    #print('autoB', aoa[0], dif, config.v)
    AutoBloqueio=dif>config.v #Analisa se há autobloqueio

    return AutoBloqueio

def objectBlockage(user, bs, obj, t, aod):
    UT_dis=np.linalg.norm(np.array([bs.x, bs.y, bs.height])-np.array([user.x[t], user.y[t], user.height[t]]));
    #Objetos no ambiente - só um para teste
    ObjBlockage=0 #Assume que não há objetos bloqueando
    #OB.pos=[25;-50; 5]; #Objeto qualquer no cenário (isso deve ser randomizado)
    az=np.rad2deg(math.atan2(obj[1]-bs.y, obj[0]-bs.x)) #Determina o azimute da bs em relação ao objeto
    #Determina a elevação da bs em relação ao objeto
    el=np.rad2deg(math.asin((obj[2]-bs.height)/np.linalg.norm(np.array([bs.x, bs.y, bs.height])-np.array([obj[0], obj[1], obj[2]])))) 
    dis=np.linalg.norm(np.array([bs.x, bs.y, bs.height])-np.array([obj[0], obj[1], obj[2]]))
    #Verifica se está no mesmo alinhamento, com maior altura e entre a BS e UT
    if (abs(aod[0]-az)<2 and aod[1]<=el and dis < UT_dis):
        ObjBlockage=1

    return ObjBlockage
    
def numberBlockages(user, bs, objects, users, t, aod):
    numBl = 0
    for obj in objects:
        numBl = numBl + objectBlockage(user, bs, [objects[obj].x, objects[obj].y, objects[obj].height], t, aod)
        
    for user2 in users:
        if(user.id_, users[user2].id_):
            continue
        numBl = numBl + objectBlockage(user, bs, [users[user2].x[t], users[user2].y[t], users[user2].height[t]], t, aod)
        
    return numBl
        

def LoS_or_NLoS(user, bs, objects, users, t):
    aoa = getAoA(user, bs, 1)
    aod = getAoD(user, bs, 1)
    #print('AoA', aoa)
    #print('AoD', aod)
    
    auto_B = autoBlockage(user, t, aoa)
    
    numb_B = numberBlockages(user, bs, objects, users, t, aod)
    
    if auto_B == False and numb_B == 0:
        return {'visibility':'LoS', 'auto_blockage':str(auto_B), 'object_blockage':numb_B}
    else:
        return {'visibility':'NLoS', 'auto_blockage':str(auto_B), 'object_blockage':numb_B}

if __name__ == '__main__':

    users = load_users()
    base_stations = load_base_stations()
    objects = load_objects()
    
    los_or_nlos = {}
    
    for t in range(1, config.ti + 1):
        for user in users:
            for bs in base_stations:
                los_nlos = LoS_or_NLoS(users[user], base_stations[bs], objects, users, t)
                los_or_nlos['t' + str(t) + '_u' + str(user) + '_bs' + str(bs)] = los_nlos
    
    with open('los_or_nlos.json', 'w') as json_file:
        json.dump(los_or_nlos, json_file, indent=4)
            
    #aod = getAoA(users[1], bs[1], 1)
    #print(numberBlockages(users[1], bs[1], obj, users, 1, aod))
    #print(users[1].y)
