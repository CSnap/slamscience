# python program for Triple Helix "Science of the Slam" photogate workshop
# by Dylan Rees

import serial #PySerial library for interfacing with the Arduino
import time
import matplotlib #for plotting
import numpy as np #for plotting
import matplotlib.pyplot as plt #for plotting
import matplotlib.patches as mpatches #used for drawing the legend on the graphs

#starting a serial connection with the arduino
arduino = serial.Serial('/dev/ttyACM0', 9600)

data = [] #will hold all arduino data points
airtime = 0 #variable that stores the jump time
jumpup = 0 #variable that stores the last time "jumping" became true
jumpdown = 0 #variable that stores the last time "jumping" became false
jumping = False #boolean variable that stores whether or not somebody is jumping
timekeeper = 0 #timekeeping variable.
jumpheight = 0 #variable to store calculated jump height

#variable for keeping track of how fast measurements can come in
oldtime = 0.0

#y'know
lastgraph = 0.0

#initialize plot and plot for the first time
plt.ion()
plt.plot(data)
plt.axis([0, 20, 0, 5])
plt.ylabel('Photogate Voltage')
plt.legend(['Airtime: '+str(round(airtime,3))+'s\n Jump Height:'+str(round(jumpheight,3))+'m'])

#plotting loop
while True:
	print(arduino.readline())
	try:
		state = float(arduino.readline())/205 #division by 205 should convert arduino analog reading into units of volts
		if state>3 and jumping == False:
			jumping = True
			jumpup = time.time()
		if state<=3 and jumping == True:
			jumping = False
			jumpdown = time.time()
			airtime = jumpdown - jumpup
			jumpheight = 9.81*airtime*airtime/8 #use kinematics formula to calculate jump height based on airtime
		data.append(state)
	except:
		pass
		print("DATA ACQUISITION FAIL!")
	if len(data)>20:
		# route to scroll the graph by discarding the oldest data point before redrawing
		data.pop(0)
		#plt.clf()
		#plt.axis([0, 20, 0, 5])
		#plt.ylabel('Jump Plates')
		#plt.plot(data)
		#plt.legend(['Airtime: '+str(round(airtime,3))+'s\n Jump Height:'+str(round(jumpheight,3))+'m'])
	else:
		plt.plot(data)
	#plt.draw()
	print state
	if time.time()-lastgraph > 0.15:
		plt.clf()
		plt.axis([0, 20, 0, 5])
		plt.ylabel('Jump Plates')
		plt.plot(data)
		plt.legend(['Airtime: '+str(round(airtime,3))+'s\n Jump Height:'+str(round(jumpheight,3))+'m'])
		lastgraph = time.time()
		plt.draw()
	print("Time since last data point: "+str(time.time()-oldtime))
	oldtime = time.time()
