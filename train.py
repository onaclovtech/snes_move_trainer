
import pygame
import threading
import socket
import struct
import time
import datetime
import json
import os
print ("input finished")
import sys

def normalize_data(data):
    for i in range(len(data)):
        data[i] = round(data[i])
    return data
class joystickEventSender(threading.Thread):
    controllers = []
    running = 1
    JoystickData = []
    def __init__(self):
        pygame.init()
        pygame.joystick.init()
        for x in range(pygame.joystick.get_count()):
            pygame.joystick.Joystick(x).init()
            if(pygame.joystick.Joystick(x).get_numbuttons() == 15):
                self.controllers.append(1)
            else:
                self.controllers.append(0)
            self.JoystickData.append([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
       	threading.Thread.__init__(self)
    def run(self):
        if os.path.exists('trainer_tracking.json'):
            tracking = json.load(open('trainer_tracking.json', 'r'))
        else:
            tracking = {}
        #while self.running:
        x = 0
        presses = ["Horizontal","Vertical", "Start/Select", "B", "X", "A", "Y", "L", "R"]
        timer = [0.0, # Left / Right (-1,1)
                 0.0, # Up, Down (-1,1)
                 0.0, # Start, Select
                 0.0, # B
                 0.0, # X
                 0.0, # A
                 0.0, # Y 
                 0.0, # L bumper
                 0.0 # R bumper
                 ]
        goal_time = [0.0, # Left / Right (-1,1)
                 0.0, # Up, Down (-1,1)
                 0.0, # Start, Select
                 0.0, # B
                 0.0, # X
                 0.03, # A
                 0.0, # Y 
                 0.0, # L bumper
                 0.0 # R bumper
                 ]
        self.PriorData = [0.0, # Left / Right (-1,1)
                 0.0, # Up, Down (-1,1)
                 0, # Start, Select
                 0, # B
                 0, # X
                 0, # A
                 0, # Y 
                 0, # L bumper
                 0 # R bumper
                 ]

         # Goal Sequence of States
         # This can be loaded from a file probably
        index_move = {"Left": 0, "Right" : 0, "Up" : 1, "Down" : 1, "Start" : 2, "Select" : 2, "B" : 3, "X": 4, "A" : 5, "Y" : 6, "L" : 7, "R" :8}
        goal_states = []
        sequence = [["B", "Right"],
                  ["B","Right", "A"], # Duration, Min, Max
                  ["B", "Right"], # Duration, Min, Max
                  ["B", "Right", "A"], # Duration, Min, Max
                  ["B", "A"], # Duration, Min, Max
                  ["B", "Down", "A"], # Duration, Min, Max
                  ["B", "A"], # Duration, Min, Max
                  ["B", "Down", "A"], # Duration, Min, Max
                  ["B", "A"], # Duration, Min, Max
                  ["B", "Right", "A"]]
        for i in sequence: # Duration, Min, Max
            goal_states.append([0.0, 0.0, 0, 0, 0, 0, 0, 0, 0])
            for j in i:
                if j == "Right" or j == "Start" or j == "Down":
                    goal_states[-1][index_move[j]] = 1.0
                elif j == "Left" or j == "Select" or j == "Up":
                    goal_states[-1][index_move[j]] = -1.0
                else:
                    goal_states[-1][index_move[j]] = 1

        start_time = time.clock()
        time_index = str(datetime.datetime.now())
        # Add tracking of what sequence of buttons were pressed
        if time_index not in tracking:
            tracking[time_index] = {"actual_sequence" : [], "step_time" : [], "count" : 0, "sequence_time" : 0, "total_time" : 0}
        idx = 0
        print ("First Sequence", sequence[idx])
        sequence_incomplete = True
        time.sleep(.03)
        pygame.event.pump()
        step_timer = time.clock()
        sequence_timer = time.clock()

        while sequence_incomplete:

            self.JoystickData = normalize_data([pygame.joystick.Joystick(x).get_axis(0), # Left / Right (-1,1)
                    pygame.joystick.Joystick(x).get_axis(1), # Up, Down (-1,1)
                    pygame.joystick.Joystick(x).get_button(6) - pygame.joystick.Joystick(x).get_button(7), # Start, Select
                    pygame.joystick.Joystick(x).get_button(1), # B
                    pygame.joystick.Joystick(x).get_button(2), # X
                    pygame.joystick.Joystick(x).get_button(0), # A
                    pygame.joystick.Joystick(x).get_button(3), # Y 
                    pygame.joystick.Joystick(x).get_button(4), # L bumper
                    pygame.joystick.Joystick(x).get_button(5), # R bumper
                    ])
            
            tracking[time_index]["actual_sequence"].append(goal_states[idx])
            
            # Check to see if we matched the goal state
            if self.JoystickData == goal_states[idx]:
                #print ("Sequence", idx, "Complete")
                tracking[time_index]["step_time"].append(time.clock() - step_timer)
                idx += 1
                step_timer = time.clock()
                if len(goal_states) <= idx:
#                    print ("It took you ", time.clock() - start_time, "seconds from the start to end of the move doing it correctly.")
                    tracking[time_index]["sequence_time"] = time.clock() - sequence_timer
                    tracking[time_index]["total_time"] = time.clock() - start_time
                    sequence_incomplete = False
                    print (tracking)
                    f = open("trainer_tracking.json", "w")
                    f.write(json.dumps(tracking, sort_keys = True, indent = 2))
                    f.close()
                    
                    for i in tracking[time_index]:
                        print (i, tracking[time_index][i])
                    break
                print ("Next Sequence", sequence[idx])
            else:
                if idx > 0:
                    if self.JoystickData == goal_states[idx-1]:
                        pass
                    else:
                        # I think this means we pressed a different key?
                        print ("You pressed an incorrect key sequence Restarting!")
                        idx = 0
                        tracking[time_index]["count"] += 1
                        print ("First Sequence", sequence[idx])
                        step_timer = time.clock()
                        sequence_timer = time.clock()
            time.sleep(.03)
            pygame.event.pump()
                
thread = joystickEventSender()
thread.start()


