
import pygame
import threading
import socket
import struct
import time
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
        idx = 0
        print ("First Sequence", sequence[idx])
        sequence_incomplete = True
        while sequence_incomplete:
            time.sleep(.03)
            pygame.event.pump()

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

            if self.JoystickData == goal_states[idx]:
                #print ("Sequence", idx, "Complete")
                idx += 1
                if len(goal_states) <= idx:
                    print ("It took you ", time.clock() - start_time, "seconds from the start to end of the move doing it correctly.")
                    sequence_incomplete = False
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
                        print ("First Sequence", sequence[idx])
                        start_time = time.clock()
            #else:
                #print (self.JoystickData, goal_states[idx])
            if False:
                #print (self.JoystickData)
                for i in range(len(self.JoystickData)):
                    if abs(self.JoystickData[i] - self.PriorData[i]) > .001:
                        if abs(self.PriorData[i]) > 0.01:
                            #timer[i] = time.start
                            duration = time.clock() - timer[i]
                            print (presses[i], duration)
                            if abs(goal_time[i] - duration) < .001:
                                print ("Achieved!")
                        else:
                            timer[i] = time.clock()
                        self.PriorData[i] = self.JoystickData[i]
                
                

    
    
    
	

thread = joystickEventSender()
thread.start()
