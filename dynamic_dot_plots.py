import csv_gen
import database
import os

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import NullFormatter, ScalarFormatter
nullfmt = NullFormatter()

SSN = 30 #starting session number
db_version = "200" #put in the name of the db version
db_name = ("%s_database.pickle" % (db_version))

markers = [((4, 111), (4, 112)), ((4, 113), (4, 114)), ((4, 121), (4, 122)), ((4, 123), (4, 124)), ((4, 131), (4, 132)), ((4, 133), (4, 134))]

end_markers = []

rein_marker = [(2, 18), (4, 100)]
peck_marker = (3, 2)

error = False
error_log = []



db = None


#takes the name of the file where the database is stored as a string. should be a .pickle file
#this is currently done by passing db_name which is preset to the current database version
#this is also now just for convenience in debugging.
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
	
	# -7 used as a special debugging value
	return -7

"""
pulse_n_BR() takes as a parameter a dictionary with some meta elements and a 
group of elements called 'sessions.' Each session contains a 
list of events that make up the data to be analyzed and plotted.
it also takes an integer indicating the pulse to be analzed and uses that to pull
the markers it needs from a list.
"""

def pulse_n_BR(n, bird):

	
	pulse_start = markers[n][0]
	pulse_end = markers[n][1]
	
	end_markers = []
	end_markers.append(pulse_end)
	
	rein_start = rein_marker[0]
	rein_end = rein_marker[1]


		
	IRIs = []
	IRTs = []
	count = 0
	excluded = 0
	
	for s in bird:
		error = False
		iris = []
		irts = []
		count += 1
		
		if s in ['Phase_Name', 'Bird_Name', 'Group_Name']:
			pass
		
		elif s >= SSN:	
			events = bird[s]['T']
			recording = False
			skip = False
			last_type = None
			
			IRI = 0
			irt = 0
			e = goto_marker(pulse_start, events, 0)
			while(e < len(events) and e > -1):
			#for e in events:
				
				e_type = (events[e][0], events[e][1])
				
				e_data = (events[e][2]) #e_data is time stamp for most events
				
				if skip:
					IRI = e_data
					irt = e_data
					skip = False
					skip_to = -1
				
				if not recording:
					if e_type == pulse_start:
						recording = True
						IRI = e_data
						irt = e_data
	
				elif recording:				
					if e_type == rein_start:
						recording = False
						e = len(events) + 2
						
					elif e_type == pulse_end:
						recording = False
						e = len(events) + 2
						
					elif e_type == peck_marker:					
						iris.append(e_data - IRI)
						irts.append(e_data - irt)
					
						irt = e_data
						
					else:
						pass

				last_type = e_type
				
				if skip:
					e = skip_to
				else:
					e += 1
			if recording:
				print("recording at end of session...")
				print bird[s]['bird_no']
				print bird[s]['session_no']
				print s
				error = True
				#os.system("pause")
		if error:
			excluded += 1
		if not error:
			IRIs = IRIs + iris
			IRTs = IRTs + irts
	print "excluded %d out of %d sessions." % (excluded, count)
	#os.system("pause")
	
	data = [IRIs, IRTs]
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
	
def pulse_n_AR(n, bird):
	
	#start_markers = []
	
	pulse_start = markers[n][0]
	pulse_end = markers[n][1]

	end_markers = []
	end_markers.append(pulse_end)
	
	rein_start = rein_marker[0]
	rein_end = rein_marker[1]
	

	
	IRIs = []
	IRTs = []
	count = 0
	excluded = 0	
	
	for s in bird:
		count += 1
		error =  False
		iris = []
		irts = []
		
		if s in ['Phase_Name', 'Bird_Name', 'Group_Name']:
			pass		
		
		elif s >= SSN:	
			events = bird[s]['T']
			recording = False
			last_type = None
			IRI = 0
			irt = 0

			e = 0
			rein_1 = False
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
							error_log.append("session %s, bird %s, no 2, 18 found after line %d" % (bird[s]['session_no'], bird[s]['bird_no'], e))
							error = True

						else: 
							skip_to = goto_marker(rein_end, events, skip_to)
						
							if skip_to == -7:
								print("line 704")
								error_log.append("session %s, bird %s, no 4, 100 found after line %d" % (bird[s]['session_no'], bird[s]['bird_no'], e))
								error = True
							
						if skip_to == -7:
							e = len(events) +2
							
						else:
							rein_1 = True
							skip = True
						
					elif rein_1 and e_type == rein_end:
						recording = True
						IRI = e_data
						irt = e_data
	
				elif recording:				
					if e_type == pulse_end:
						recording = False
						quit_session = True
					
					elif e_type == peck_marker:					
						iris.append(e_data - IRI)
						irts.append(e_data - irt)
					
						irt = e_data
						
					
					elif e_type == rein_start:
						skip_to = goto_marker(rein_end, events, e)
						if skip_to == -7:
							print("line 715")
							error_log.append("session %s, bird %s, no 4,100 found after line %d" % (bird[s]['session_no'], bird[s]['bird_no'], e))
							error = True
						else:
							skip = True
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
		if error:
			excluded += 1
		if not error:
			IRIs = IRIs + iris
			IRTs = IRTs + irts
	data = [IRIs, IRTs]
	print "excluded %d out of %d sessions." % (excluded, count)
	

	return data
	
"""
join_pulse() is a simple list concatenator.
it takes two lists and joins them in order.
"""	
	
def join_pulse(p1, p2):
	temp = p1 + p2
	return temp

	
#experimental -- not in use	
"""
def pulse_n(n, bird, BR = False, AR = False):
	if((BR and AR) or (not BR and not AR)):
		print("full pulse not yet programmed, returning to caller...")
	start_markers = []
	end_markers = []
	listen_markers = []
	sleep_markers = []
	
	listen_markers.append(markers[n][0])
	sleep_markers.append(markers[n][1])
	
	start_markers.append(markers[n][0])
	end_markers.append(markers[n][1])
	#start_markers.append((2, 18))	
	
	#print start_markers
	#print end_markers
	#os.system("pause")
		#end_markers.append([t][1])
		
	IRIs = []
	IRTs = []
	for s in bird:
		if s >= SSN:	
			events = bird[s]['T']
			recording = False
			last_type = None
			#IRI = 0
			#irt = 0
			e = 0
			rein_1 = False
			rein_n = False
			start = True
			while(e < len(events)):
			#for e in events:
				skip = False
				skip_to = -1
				
				e_type = (events[e][0], events[e][1])
				
				e_data = (events[e][2]) #e_data is time stamp for most events
				
				if not recording:
					if e_type in start_markers:
						#skip = True
						#skip_to = events.index(goto_marker(rein_marker[1], events, e)
						start = True
						
					elif start:
						if e_type == (2, 18):
							rein_1 = True
							start = False
					elif e_type == (4, 100):
						if rein_1:						
							recording = True
							rein_1 = False
							IRI = e_data
							irt = e_data
	
				elif recording:				
					if e_type in end_markers:
						recording = False
					
					elif e_type == (3, 2):					
						IRIs.append(e_data - IRI)
						IRTs.append(e_data - irt)
					
						irt = e_data
						
					
					elif e_type == (2, 18):
						#skip_to = events.index(goto_marker(rein_marker[1], events[e:]))
						#skip = True
						rein_n = True
						
						
					elif e_type == (4, 100):
						if rein_n:
							rein_n = False
							IRI = e_data
							irt = e_data
					
				last_type = e_type
				
				if skip:
					e = skip_to
				else:
					e += 1

	data = [IRIs, IRTs]
	return data
"""



"""
These two methods build the data needed to create the desired graphs
"""

def pulse_multi_BR(list, bird):
	data = []
	for i in list:
		p = pulse_n_BR(i, bird)
		data = join_pulse(data, p)
	return data

def pulse_multi_AR(list, bird):
	data = []
	for i in list:
		p = pulse_n_AR(i, bird)
		data = join_pulse(data, p)
	return data	
	
	
#db = set_db(db_name)

"""
This subroutine needs a PGB and a range of pulses. 
It also requires a command to run BR or AR
This is the 'Main' routine and puts all the parts 
together based on the parameters given to it.
"""

#todo --  rename variable 'range', it's misleading
def make(PGB, range, BoA, title, topBins = 50, sideBins = 50, dotSize = 0.1):
	plt.close('all')
	#plt.cla()
	
	pulsesToString = ''
	for i in range:
		pulsesToString = pulsesToString + str(i) +'_' 
		
	P = PGB['Phase_Name']
	G = PGB['Group_Name']
	B = PGB['Bird_Name']

	# definitions for the axes
	left, width = 0.1, 0.65
	bottom, height = 0.1, 0.65
	bottom_h = left_h = bottom + height + 0.04

	rect_scatter = [left, bottom, width, height]
	rect_histx = [left, bottom_h, width, 0.2]
	rect_histy = [left_h, bottom, 0.15, height]

	

	
	plt.figure("DotPlot_%sR_%s%s%s_pulses_%s" %(BoA, P, G, B, pulsesToString), figsize=(12, 8))
	#plt.title("Dynamic IRI vs. IRT--%sR: %s %s %s--pulses: %s" %(BoA, P, G, B, str(range)), loc = 'right')
	
	axHistx = plt.axes(rect_histx)#, sharex = axScatter)
	axHisty = plt.axes(rect_histy)#, sharey = axScatter)
	axScatter = plt.axes(rect_scatter, sharex = axHistx, sharey = axHisty)

	
	#axHistx.xaxis.set_major_formatter(nullfmt)
	#axHisty.yaxis.set_major_formatter(nullfmt)

	# the scatter plot:
	if(BoA == 'B'):
		table = pulse_multi_BR(range, PGB)
	elif(BoA == 'A'):
		table = pulse_multi_AR(range, PGB)
	else:
		print("Please specify 'Before Reinforcer' or 'After Reinforcer' . ")
		return
	
	db = None
	x = table[0]
	y = table[1]
	table = None
	axScatter.scatter(x, y, 0.1, 'black', alpha = 1)



	binwidth = topBins
	#xymax = np.max([np.max(np.fabs(x)), np.max(np.fabs(y))])
	h_lim = (int(np.max(x)/binwidth) + 1) * binwidth
	v_lim = (int(np.max(y)/binwidth) + 1) * binwidth

	#axScatter.set_xlim((0, np.max(x)))	
	#axScatter.set_xlim((0, h_lim))
	axScatter.set_xlim((0, 80000))
	axScatter.set_ylim((0, 3000))
	#axScatter.set_ylim((0, v_lim))

	bins = np.arange(0, h_lim + binwidth, binwidth)
	ybins = np.arange(0, v_lim + binwidth, binwidth) #try a *3 multiplier here on binwidth
	axHistx.hist(x, bins=bins, color = 'black')
	axHisty.hist(y, bins=ybins, orientation='horizontal', color = 'black')

	axHistx.set_xlim(axScatter.get_xlim())
	axHisty.set_ylim(axScatter.get_ylim())

	plt.show()
	plt.cla()
	plt.close()

