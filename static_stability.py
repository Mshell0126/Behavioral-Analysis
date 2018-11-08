import database
import os
import numpy as np
import matplotlib.pyplot as plt

#import dot_plot_values

#db = database.eat_database("200_database.pickle")
x = []
y = []

#for phase A static, groups a, b, c

#include = [['A', 'A'], ['A', 'B'], ['A', 'C'], ['B', 'D']]


"""
takes a lits of sessions and turns it into an ordered list of
pecks/second frequencies.
"""
def get_Avg_Freq(session, x, y):
	
	pecks = 0
	t_sum = 0
	t_marker = 0
	table = session['T']
	record = False

	for i in range(len(table)):
		include = True
		line = table[i]
		event = line[0]
		type = line[1]
		data = line[2]
		

		if(event == 4 and type == 151):

			break
		elif(record):
			if(event == 4 and type == 100):
				print("start interval marker during interval")
				print("session ", session['name'][5:7])
				print("line: ", i)

				include = False
				os.system("pause")
			
			elif(event == 3 and type == 2):
				pecks += 1
			
			elif(event == 2 and type == 18):
				record = False
				t_sum += data - t_marker
				
		else:
			if(event == 2 and type == 18):
				print("end interval marker outside of interval")
				print("session ", session['name'][5:7])
				print("line: ", i)
				include = False
				os.system("pause")
			elif(event == 4 and type == 100):
				record = True
				t_marker = data

	if(record):
		print("still recording pecks at end of event list.")
		print("last interval may not have closed...")
	
	if(include):

		
		t_sum_seconds = float(t_sum / 1000)

		
		print("session number @ line 73", session['name'][5:7])
		avgFreq = float(pecks)/(t_sum_seconds)

		print("session :", session['name'][5:7])
		x.append((session['session_no']))
		y.append(avgFreq)

		
"""
This is the 'main' method used to keep things organized. 
It takes a dictionary and iterates through it's 'sessions'
and records the data in a list for plotting. 
"""
def make(PGB):#, include=['A', 'A'], ['A', 'B'], ['A', 'C'], ['B', 'D']]
	plt.ylabel("pecks/second")
	plt.xlabel("session no.")

	P = PGB['Phase_Name']
	G = PGB['Group_Name']
	B = PGB['Bird_Name']	
	plt.title("Static Stability: %s %s %s" %(P, G, B))
	#PGB = db[P][G][B]
	#y = []
	#x = []
	counter = 0
	x = []
	y = []
	for s in PGB:
		try:
			
			data = get_Avg_Freq(PGB[s], x, y)
		except:
			if s in [P, G, B]:
				pass
			else:
				print("Failed to process session %s in pulse_multi_BR" % (s))

	plt.plot(x, y)

	plt.show()
		