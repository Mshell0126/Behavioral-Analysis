import csv_gen
import database
import os

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import NullFormatter

SSN = 30 #starting session number

"""
db_version = "200" #put in the name of the db version
db_name = ("%s_database.pickle" % (db_version))
"""

start_markers = []
end_markers = []
rein_marker = [(2, 18), (4, 100)]

peck_marker = (3, 2)

end_file = (4, 151)

rein_start = rein_marker[0]
rein_end = rein_marker[1]

error_log = []



#db = database.eat_database(db_name)
#for phase A static, groups a, b, c

"""
skips ahead to the desired marker or stops and returns an out of range line number
if an ending marker has been found.
"""

def goto_marker(mrkr, data, i):

	while i < len(data):
		try:
			event = (data[i][0], data[i][1])
			
			if (event) == (5, 0):
				return i
			elif event == mrkr:
				return i
			else:
				i = i + 1				
		except:
			print("marker ", mrkr, "not found after line ", i)
			return i
	
	print("marker ", mrkr, "not found after line ", i)
	return i
	
	
"""
special case of goto_marker()
"""	
def skip_rein(data, e):

	e = goto_marker(rein_end, data, e)
	return e
	

	
"""
this method ties everything together and builds the data for plotting
"""
def static_dot_plot(bird):

	recording = False
		
	IRIs = []
	IRTs = []
	
	for s in bird:
		if s in ['Phase_Name', 'Group_Name', 'Bird_Name']:
			pass
		elif s >= SSN:
			events = bird[s]['T']
			skip = False
			skip_to = -1
			last_type = None
			
			IRI = 0
			irt = 0
			recording = False
			e = 0
			while(e < len(events)):
				
				try:
					e_type = (events[e][0], events[e][1])
					e_data = (events[e][2])
				except:
				
					print ("event type or data unable to be stored for line: %d" % (e))
					os.system("pause")
					
					e_type = (0, 0)
					e_data = 0
					
				if skip:
					IRI = e_data
					irt = e_data
					skip = False
					skip_to = -1
				
				if recording:
					if e_type == end_file:
						e = len(events) + 2
				
					if e_type == rein_start:
						skip_to = skip_rein(events, e)
						skip = True
				
					if e_type == peck_marker:
						IRIs.append(e_data - IRI)
						IRTs.append(e_data - irt)
						
						irt = e_data
					
					
				if not recording:
	
					if not (e_type == (1, 18)):
						
						skip_to = goto_marker((1, 18), events, e)
						
						skip = True
					recording = True
				last_type = e_type
				if skip:
					e = skip_to
				else:
					e += 1
	data = [IRIs, IRTs]
	return data

		
		
"""make() does the actual plotting and calls other functions to get what it needs."""		
		
		# run should take a list such as the one below for deciding which birds to run.
		# include will be passed as it is for a default value
		# include = [['A', 'A'], ['A', 'B'], ['A', 'C'], ['B', 'D']]
		
def make(PGB):#, include=[['A', 'A'], ['A', 'B'], ['A', 'C'], ['B', 'D']])

	#try:
	
	#manual input that takes phase ('A' or 'B') group ('A', 'B', 'C', OR 'D') and bird number as a string i.e. ('034')
	#P, G, B = [raw_input("Phase: "), raw_input("Group: "), raw_input("Bird: ")]
	
	plt.close('all')
	
	P = PGB['Phase_Name']
	G = PGB['Group_Name']
	B = PGB['Bird_Name']	
	plt.figure("Static IRI vs IRT--%s %s %s" %(P, G, B))

	
	
	#the plotting instructions below are adapted from an example on the matplotlib website
	# https://matplotlib.org/examples/pylab_examples/scatter_hist.html
	nullfmt = NullFormatter()         # no labels

	# definitions for the axes
	left, width = 0.1, 0.65
	bottom, height = 0.1, 0.65
	bottom_h = left_h = bottom + height + 0.04

	rect_scatter = [left, bottom, width, height]
	rect_histx = [left, bottom_h, width, 0.2]
	rect_histy = [left_h, bottom, 0.15, height]

	# start with a rectangular Figure
	plt.figure(1, figsize=(12, 8))

	axHistx = plt.axes(rect_histx)
	axHisty = plt.axes(rect_histy)
	axScatter = plt.axes(rect_scatter, sharex = axHistx, sharey = axHisty)

	# the scatter plot:
	table = static_dot_plot(PGB)

	db = None
	x = table[0]
	y = table[1]
	table = None
	axScatter.scatter(x, y, 0.1, 'black', alpha = 1)

	# now determine nice limits by hand:
	binwidth = 50
	xymax = np.max([np.max(np.fabs(x)), np.max(np.fabs(y))])
	lim = (int(xymax/binwidth) + 1) * binwidth

	axScatter.set_xlim((0, lim))
	axScatter.set_ylim((0, 3000))

	bins = np.arange(0, lim + binwidth, binwidth)
	ybins = np.arange(0, 3000 + 50, 50)
	axHistx.hist(x, bins=bins, color = 'black')
	axHisty.hist(y, bins=ybins, orientation='horizontal', color = 'black')

	axHistx.set_xlim(axScatter.get_xlim())
	axHisty.set_ylim(axScatter.get_ylim())

	plt.show()
	plt.gcf().clear()
				
