import csv_gen
import database
import os

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import NullFormatter, ScalarFormatter

SSN = 01 #starting session number
db_version = "200" #put in the name of the db version
db_name = ("%s_database.pickle" % (db_version))

markers = [((4, 111), (4, 112)), ((4, 113), (4, 114)), ((4, 121), (4, 122)), ((4, 123), (4, 124)), ((4, 131), (4, 132)), ((4, 133), (4, 134))]
start_markers = []
end_markers = []
rein_marker = [(2, 18), (4, 100)]
peck_marker = (3, 2)

error = False
error_log = []

db = None

"""
a couple of convenience routines.
"""
def clear_markers():
	start_markers = []
	end_markers = []
	return

def set_db(d):
	return database.eat_database(d)
	
"""
the goto_marker() function should be essential to future releases.
It requires a tuple or 'marker', a list, and a current line number.
It starts searching the list for a marker matching the one passed 
to it and stops and returns the current line when it gets a match 
returns the an index equivalent to the last line + 1 to terminate
the calling programs loop if it finds one of the 'ending' markers.
"""	
	
def goto_marker(mrkr, data, i):
	e = i
	while(i < len(data)):
		if(mrkr == (data[i][0], data[i][1])):
			return i
		elif(mrkr in end_markers):
			return len(data)
		else:
			i += 1

	print("", mrkr, " marker not found before end of list...", "line: ", e)
	return -7
	
"""
pulse_n_BR() takes as a parameter a dictionary ' Each session contains some meta
info and a list of events that make up the data to be analyzed and plotted.
it also takes an integer indicating the pulse to be analzed and uses that to pull
the markers it needs from a list.
"""
	

def pulse_n_BR(n, session):

	s = session['session_no']
	start_markers = []
	end_markers = []
	start_markers.append(markers[n][0])
	end_markers.append((2, 18))
	end_markers.append(markers[n][1])
	
	pulse_start = markers[n][0]
	pulse_end = markers[n][1]
	rein_start = rein_marker[0]
	rein_end = rein_marker[1]
	
	
	end_markers.append(pulse_end)
	end_markers.append(rein_start)

		
	data = {}
	count = 0
	error = False
	IRI = 0
	pecks = 0
	acc = 0
	count += 1
	if s >= SSN:	
		events = session['T']
		recording = False
		skip = False
		last_type = None
		
		e = goto_marker(pulse_start, events, 0)
		while(e < len(events) and e > -1):
			
			e_type = (events[e][0], events[e][1])
			
			e_data = (events[e][2]) #e_data is the time stamp for most events
			
			if skip:
				IRI = e_data
				skip = False
				skip_to = -1
			
			if not recording:
				if e_type == pulse_start:
					recording = True
					IRI = e_data


			elif recording:				
				if e_type == rein_start:
					recording = False
					acc += e_data - IRI
					e = len(events) + 2
				elif e_type == pulse_end:
					recording = False
					acc += e_data
					e = len(events) + 2
				elif e_type == peck_marker:					
					pecks += 1
					irt = e_data
				else:
					pass

			last_type = e_type
			
			if skip:
				e = skip_to
			else:
				e += 1
		acc += e_data - IRI
		if recording:
			print("recording at end of session...")
			print bird[s]['bird_no']
			print bird[s]['session_no']
			print s
			error = True
			os.system("pause")
		if error:
			excluded += 1
			return 'exclude'
		if not error:
			data = [pecks, acc]
			return data	

"""
This method is the sister to pulse_multi_BR()
and is functionally equivalent. There are some differences in 
the algorithm used depending on whether you track data before 
or after the first reinforcer marker and so two routines are 
used. Future versions will seek to eliminate the need for two 
separate routines by abstracting the problem further and 
implementing a GUI
"""				
			
def pulse_n_AR(n, session):
	s = session['session_no']
	start_markers = []
	end_markers = []
	
	pulse_start = markers[n][0]
	pulse_end = markers[n][1]
	
	rein_start = rein_marker[0]
	rein_end = rein_marker[1]
	
	end_markers.append(pulse_end)

	
	data = []
	count = 0
	excluded = 0
	count += 1
	error =  False
	IRI = 0
	pecks = 0
	acc = 0
	if s >= SSN:	
		events = session['T']
		recording = False
		last_type = None
		IRI = 0
		irt = 0

		e = 0
		rein_1 = False
		#rein_n = False
		start = False
		skip = False
		quit_session = False
		while(e < len(events)):

			if not start:
						
				e = goto_marker(pulse_start, events, e)
				
				if pulse_start == (events[e][0], events[e][1]):
					start = True
				else:
					print("fix goto_marker()")
					os.system("pause")
					e = len(events)
					
			e_type = (events[e][0], events[e][1])
			
			e_data = (events[e][2]) #e_data is time stamp for most events

			if skip:
				IRI = e_data
				irt = e_data
				skip = False
				skip_to = -1
			
			if not recording:
				if start and not rein_1:
					skip_to = goto_marker(rein_start, events, e)

					if skip_to == -7:
						print("line 699")
						error_log.append("session %s, bird %s, no 2, 18 found after line %d" % (session['session_no'], session['bird_no'], e))
						error = True
						

					else: 
						skip_to = goto_marker(rein_end, events, skip_to)
					
						if skip_to == -7:
							print("line 704")
							error_log.append("session %s, bird %s, no 4, 100 found after line %d" % (session['session_no'], session['bird_no'], e))
							error = True
						
					if skip_to == -7:
						e = len(events) +2
						
					else:
						rein_1 = True
						skip = True
					
				elif rein_1 and e_type == rein_end:
					recording = True
					IRI = e_data

			elif recording:				
				if e_type == pulse_end:
					recording = False
					quit_session = True
					acc += e_data - IRI
				
				elif e_type == peck_marker:					
				
					pecks += 1
				
				elif e_type == rein_start:
					acc += e_data - IRI
					skip_to = goto_marker(rein_end, events, e)
					if skip_to == -7:
						print("line 715")
						error_log.append("session %s, bird %s, no 4,100 found after line %d" % (session['session_no'], session['bird_no'], e))
						error = True
					else:
						skip = True
					#this is here as a reminder.
					#a later implementation might count
					#the number of reinforcer markers in the table
					# activate a boolean after so many...
					#rein_n = True
				
				else:
					#print(e_type)
					pass
					
				
			last_type = e_type
			
			if quit_session:
				e = len(events) + 2
			if skip:
				
				e = skip_to
			else:
				e += 1
		acc += e_data - IRI
		
		if error:
			excluded += 1
			return 'exclude'
		if not error:
			data = [pecks, acc]
			return data
	
"""
A simple concatenator for joining two lists together.
"""
	
def join_list(s1, s2):
	temp = s1 + s2
		
	return temp

"""
get_avg() takes a list of pairs. The first element of
each pair is a count of a certain event, in this case 'pecks.'
The second element is the accumulated time counted.
"""
def get_avg(list):
	pecks = 0
	acc = 0
	seconds = 0
	for i in list:
		if i == 'exclude':
			pass
		else:
			pecks += i[0]
			acc += i[1]
	seconds += float(acc/1000)
	try:
		avg = float(pecks)/seconds
	except:
		avg = 'exclude'
	return avg
		
"""
pulse_multi_BR takes a list of pulses to include as well as a dictionary
of sessions. This routine ties everything together and builds a list of
average pecks vs time averages.
"""

def pulse_multi_BR(list, bird):
	data = []
	x = []
	y = []
	sorter = []
	for s in bird:
	
		try:
			session_no = bird[s]['session_no']
		
			temp = []
			for i in list:
				temp.append(pulse_n_BR(i, bird[s]))
			avgFreq = get_avg(temp)
			if avgFreq == 'exclude':
				pass
			else:
				a = session_no
				b = avgFreq
				sorter.append((a, b))
		except:
			if s in ['Phase_Name', 'Group_Name', 'Bird_Name']:
				pass
			else:
				print("Failed to process session %s in pulse_multi_BR" % (s))
	sorter = sorted(sorter, key=lambda item: item[0])
	for element in sorter:
		x.append(element[0])
		y.append(element[1])
	data = [x, y]
	
	return data

"""
This helper method is the sister to pulse_multi_BR()
and is functionally equivalent. There are some differences in 
the algorithm used depending on whether you track data before 
or after the first reinforcer marker and so two routines are 
used. Future versions will seek to eliminate the need for two 
separate routines by abstracting the problem further and 
implementing a GUI
"""	
	
def pulse_multi_AR(list, bird):
	data = []
	x = []
	y = []
	sorter = []
	for s in bird:
	
		try:
			session_no = bird[s]['session_no']

			temp = []
			
			for i in list:
				temp.append(pulse_n_BR(i, bird[s]))
			avgFreq = get_avg(temp)
			
			if avgFreq == 'exclude':
				pass
				
			else:
				a = session_no
				b = avgFreq
				sorter.append((a, b))
		except:
			if s in ['Phase_Name', 'Group_Name', 'Bird_Name']:
				pass
			else:
				print("Failed to process session %s in pulse_multi_BR" % (s))
	sorter = sorted(sorter, key=lambda item: item[0])
	for element in sorter:
		x.append(element[0])
		y.append(element[1])
	data = [x, y]
	
	return data
	

include = [['B', 'A'], ['B', 'B'], ['B', 'C'], ['A', 'D']]

plt.ylabel("pecks/second")
plt.xlabel("session no.")


"""
This is the 'main' of the program
This helper subroutine is called from outside with the desired programs
This subroutine builds the plot using the above methods
"""
def make(PGB, range, BoA):
	
	
	P = PGB['Phase_Name']
	G = PGB['Group_Name']
	B = PGB['Bird_Name']
	plt.title("Dynamic Stability--%sR: %s %s %s" %(BoA, P, G, B))

	
	if(BoA == 'B'):
		data = pulse_multi_BR(range, PGB)
	elif(BoA == 'A'):
		data = pulse_multi_AR(range, PGB)
	else:
		print("Please specify 'Before Reinforcer' or 'After Reinforcer' . ")
		return
	
	
	x = data[0]
	y = data[1]
	
	plt.plot(x, y)

	plt.show()

	