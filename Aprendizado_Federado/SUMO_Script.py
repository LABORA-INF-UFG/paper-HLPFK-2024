from __future__ import absolute_import
from __future__ import print_function

from __future__ import absolute_import
from __future__ import print_function

import os
import sys
import optparse

if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("please declare environment variable 'SUMO_HOME'")
    
import traci  # noqa
from sumolib import checkBinary  # noqa
import randomTrips  # noqa
import time
import csv

def run():
    with open('20_users_1_hour_by_sec.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['id' ,'x' , 'y', 'o'])    
        
        start_time = 0

        while traci.simulation.getMinExpectedNumber() > 0:
            traci.simulationStep()

            lstPeopleId = traci.person.getIDList()

            if(len(lstPeopleId) < 20):                
                continue #Starts to record values when all pedestrians are walking

            if(start_time == 0):
                start_time = traci.simulation.getTime()            

            for personId in lstPeopleId:
                x, y = traci.person.getPosition(personId)

                orientation = traci.person.getAngle(personId)                
                
                person = [personId, x, y, orientation]

                writer.writerow(person)
            
            end_time = traci.simulation.getTime()

            #To get 1 hour (3600 sec) of registers
            if(end_time - start_time >= 3599):
                break

    sys.stdout.flush()
    traci.close()

def get_options():
    """define options for this script and interpret the command line"""
    optParser = optparse.OptionParser()
    optParser.add_option("--nogui", action="store_true",
                         default=False, help="run the commandline version of sumo")
    options, args = optParser.parse_args()
    return options


# this is the main entry point of this script
if __name__ == "__main__":
    # load whether to run with or without GUI
    options = get_options()

    # this script has been called from the command line. It will start sumo as a
    # server, then connect and run
    if options.nogui:
        sumoBinary = checkBinary('sumo')
    else:
        sumoBinary = checkBinary('sumo-gui')

    # generate the pedestrians for this simulation
    randomTrips.main(randomTrips.get_options([
        '--net-file', 'data/osm.net.xml',
        '--route-file', 'osm.pedestrians.rou.xml',
        '--pedestrians',
        '--trip-attributes', 'departPos="random" arrivalPos="random"',
        '--end', '20',
        '--intermediate', '10']))
    
    traci.start([sumoBinary, '-c', os.path.join('data', 'osm.sumocfg'), "--fcd-output", "fcd.xml"])

    run()
