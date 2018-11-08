import fileHandler
import time
#import analysis

#import file management libraries/tools
import json
import os
import shutil

#pickling experiment
import pickle

handler = fileHandler.fileHandler()

#error counters
error_PA = 0
error_PB = 0
error_PC = 0

error_GA = 0
error_GB = 0
error_GC = 0
error_GD = 0

ephase = {}
ephase['A'] = error_PA
ephase['B'] = error_PB
ephase['C'] = error_PC

egroup = {}
egroup['A'] = error_GA
egroup['B'] = error_GB
egroup['C'] = error_GC
egroup['D'] = error_GD

#returns a simplified table of events
def make_database(folder, template):#, tmp):
	

	database = template
	unknown_birds = {}
	#wrong_group_log = open("wrong_group_log.txt", 'wb')
	
	#counters for file inclusion reports
	f_included = 0    # counts files included
	f_w_errors = 0    # counts files with some error
	f_unreadable = 0  # counts files that were unreadable inside fileHandler
	f_total = 0       # counts all files processed
	f_o_exception = 0 # counts files with some other exception
	f_u_exception = 0 # counts files that really should have been included. 
					      # ^ This is a final catch-all for files that are to be excluded
	
	# an empty list for checking/comparing table values for accuracy
	check = []
	
	for filename in os.listdir(folder):
		
		#This counts the total number of files processed.
		f_total = f_total +1
		
		#this is defaulted to false until file is verified/evaluated
		storing = False
		file = folder + "\%s" % (filename)
		
		try:
			
			handler = fileHandler.fileHandler()
			handler.loadFile(file)
			print("successfully loaded " + filename + ".")
			
			#debug marker
			dcounter = 1
			
			#This section prevents tables containing an error from being stored in the database.
			if (handler.session["contains_error"]):
				print ("file %s contains at least one error code," % (filename))
				print ("%s not included in database" % (filename))
				
				#counter block
				phz = filename[4]
				grp = filename[3]
				
				dcounter = 2
				
				ephase[phz] = ephase[phz] + 1				
				egroup[grp] = egroup[grp] + 1
				
				dcounter = 3
				
				f_w_errors = f_w_errors + 1
				#/end counter block
				
				dcounter = 4
				
			else:
				storing = True
		
		except:
			print("error loading or reading file %s." % (filename))
			
			#reports which section of try block failed
			print dcounter
			
			#counts the number of unreadable files, most likely they are corrupted
			f_unreadable = f_unreadable + 1
		
		if (storing):
		
		#  naming convention:
		#  123|A|A|12|.|123  --> Format
		#  012|3|4|56|7|8910 --> String Indices
		#  exp|g|p|sn|.|brd  --> Key -- experiment | group | phase | session | . | bird 
	
			name = handler.name
			phase = name[4]
			group = name[3]
			bird = name[-3:]
			session = int(name[5:7])
			print name
			
			#Phase C is an extension of phase B
			#adjust session numbers to continue from 99.
			if phase == 'C':
				phase = 'B'
				session = session + 99	
				#TODO update the session's name as well, so handler.name  == ("%d" % (session))
				
			try:				
				#event-table database with line numbers for keys
				database[phase][group][bird][session] = handler.session
				
				
				print("successfully loaded and read file '%s.'" % filename)
				
				#Counts the number of files stored in the database
				f_included = f_included + 1
				
			except:
				
				#Counts the files that cause an (key?) error upon adding them to the database
				f_o_exception = f_o_exception +  1
				
				print("could not store %s in database" % (name))
				print(" Phase: %s\n Group: %s\n Bird: %s\n Session: %s" % (phase, group, bird, session))
				if phase not in database:
					print("need handling for phase %s..." % phase)
					os.system("pause")
					
					
				elif(bird not in (database[phase][group])):
					if bird not in birdlist:
						if bird not in unknown_birds:
							unknown_birds[bird] = [bird]
						unknown_birds[bird].append(filename)
							
					else:	
						#wrong_group_log.write('\n Bird %s in Group %s.\n\n' % (bird, group))
						print("bird '%s' not found in group '%s' (according to database)." % (name[-3:], name[4]))
						os.system("pause")
				else:
					print("not sure why this file isn't included...")
					f_u_exception = f_u_exception + 1
			
		
			#TODO need to figure out how to move and copy files to new folders
			
		handler = fileHandler.fileHandler()
	
	#summary
	print("\n\n")
	print("processed all files in " + folder + ".")
	print("Total in folder: %d" % (f_total))
	print("Included  files: %d" % (f_included))
	print("Files corrupted: %d (?)" % (f_unreadable))
	print("Files w/ errors: %d" % (f_w_errors))
	print("Other files n/i: %d" % (f_o_exception))
	
	
	print("Unknown file ex: %d" % (f_u_exception))
	percent_included = float(f_included) / float(f_total) * 100
	percent_included = ('%.2f'%percent_included)
	print("Percent success: %s" % (percent_included))	
	print("\n\n")

	
	'''
	# this prints all the unknown birds
	for b in unknown_birds:
		for item in unknown_birds[b]:
			print item
	'''		
	
	return database
	
	
"""
	This method saves a database as a .json file in the current working directory.
	This method requires a string for the file name and should be the experiment number
	 preceded by a capital "E."
"""	
def save_database(experiment, database):	
	#Dump database into a .json file. 
	print("saving database...")
	with open('%s_database.json' % (experiment), 'w') as output_file:
		json.dump(database, output_file)
		output_file.close()
	print("done.")
	
"""
	This method loads a database from a .json file and returns it to the caller.
	This method requires the path to the desired .json file as a parameter.
"""
def load_database(database_name):
#todo: adapt this method to only require the experiment number as input.
	print("loading database from .json file...")
	with open(database_name, 'r') as database_in:
		database_json = json.load(database_in)
		database_in.close()
	print("done.")
	return database_json

"""
	This method saves a database as a .pickle file in the current working directory.
	This method requires a string for the file name and should be the experiment number
	 preceded by a capital "E."
"""		
def pickle_database(experiment, database):
	print("pickling database...")
	with open("%s_database.pickle" % (experiment), "wb") as output_file:
		pickle.dump(database, output_file, protocol = pickle.HIGHEST_PROTOCOL)
		output_file.close
	print("done.")

"""
	This method loads a database from a .pickle file and returns it to the caller.
	This method requires the path to the desired .pickle file as a parameter.
"""
def eat_database(database_name):
#todo: adapt this method to only require the experiment number as input.
	print("absorbing pickled database...")
	with open(database_name, 'rb') as database_in:
		database = pickle.load(database_in)
		database_in.close()
	print("done.")
	return database
		
def get_blank():
	return
	# TO DO
	#get user input to instantiate database.



#MAIN

#E200 hardcode
#TO DO: make a gui or console application to load user selected values and ranges into  lists
#use get_blank() for this?
#the populating of mesa below should probably be in get_blank.

"""
phases = "AB"
groups  = 'ABCD' 
birds = {'A':['031', '075', '495', '994'], 'B':['077', '437', '038', '546'], 'C':['079', '091', '538', '998'], 'D':['034', '045', '061', '985']}
birdlist = []
for b in birds:
 for n in birds[b]:
	birdlist.append(n)
mesa = {}
box = "E:\JSU\Behavior Analysis\E200"
for p in phases:
	mesa[p] = {}
	for g in groups:
		mesa[p][g] = {}
		for n in birds[g]:
			mesa[p][g][n] = {}
"""


#instantiation of test session
'''
db = get_db()
pickle_database("E200", db)
save_database("E200", db)

mesa = make_database(box, mesa)
'''

#pickles database and then loads database from pickle
#and checks that they are equal
"""
pickle_database("E200", mesa)

db_p = eat_database("E200_database.pickle")

print "db_p is equal to mesa: ", mesa == db_p
"""

#saves database to .json, loads from json 
#and compares to see they are equal.
"""
save_database("E200", mesa)

db_json = load_database("E200_database.json")

#this will be false unless you set the default table to be all strings
print "db_json is equal to mesa: ", mesa == db_json
"""

