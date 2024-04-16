import json
from classes.BIP import BIP
from classes.Config import Config
from classes.Users import Users
from classes.BaseStation import BaseStation
import sys

users_file = 'users.json'
bs_file = 'base_stations.json'

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


def calculate_BIP(mode):
    dictionary_of_BIPs = {}
    
    bip = BIP()

    users = load_users()
    bs = load_base_stations()
    
    i = [(u, b, t) for u in users for b in bs for t in range(1, config.ti+1)]
    
    for t in range(1, config.ti+1):
        print(t)
        for it1 in i:
            for it2 in i:
                if it1[0] == it2[0] and it1[2] == it2[2] and t == it1[2]:
                    dictionary_of_BIPs['t' + str(t) + '_u' + str(it1[0]) + '_bsUL' + str(it1[1]) + '_bsDL' + str(it2[1])] = \
                        bip.calculateBipTotal(users[it1[0]], bs[it1[1]], bs[it2[1]], it1[2], users)                
    
    with open('BIP_for_all_combinations_' + mode + '.json', 'w') as json_file:
        json.dump(dictionary_of_BIPs, json_file, indent=4)
    
    
if __name__ == '__main__':
    mode = sys.argv[1]
    calculate_BIP(mode)