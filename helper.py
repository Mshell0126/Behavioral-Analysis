import database
import os

#db = database.eat_database("200_database.pickle")

"""
lists the sessions in the database on screen.
"""
def list_sessions():
	for p in db:
		for g in db[p]:
			for b in db[p][g]:
				print("Phase %s, Group %s, Bird %s:" % (p, g, b))
				print("Sessions included: ")
				for s in db[p][g][b]:
					print(db[p][g][b][s]['session_no'])
					
#this has been run so the session names should be correct
def set_session_names():
	for p in db:
		for g in db[p]:
			for b in db[p][g]:
				print("Phase %s, Group %s, Bird %s:" % (p, g, b))
				for s in db[p][g][b]:
					name = int(db[p][g][b][s]['name'][5:7])
					if s is not (name):
						print(s)
						print(name)
						name += 99
					db[p][g][b][s]['session_no'] = name						

"""
This method allows you to perform the same action on every element of a large group.
"""
def for_all_do(db, do_this, args):
	for p in db:
		for g in db[p]:
			for b in db[p][g]:
				PGB = db[p][g][b]
				
				do_this(PGB, *args)
	
	
"""
similar to the for_all_do method.
"""
def for_selected_do(db, include, do_this, args):
	for i in include:
		P = i[0]
		G = i[1]
		for B in db[P][G]:
			#PGB = db[P][G][B]
			if ['static'] == args:
				do_this(db[P][G][B])
			else:
				do_this(db[P][G][B], *args)
		

"""
This routine is used for adding and changing labels of existing database elements
"""		
		
def set_PGB_labels(PGB, p, g, b):
		PGB['Phase_Name'] = p
		PGB['Group_Name'] = g
		PGB['Bird_Name'] = b
		print p, g, b
		return PGB
		

		
"""
#delete selected files manually

for p in db:
	for g in db[p]:
		for b in db[p][g]:
			key = 'key'
			while (key is not 'q'):
				print("now in phase %s, group %s, bird %s..." % (p, g, b))
				try:
					ds = raw_input("\n Enter session number to delete: ")
					del db[p][g][b][int(ds)]
					print("done")
				except:
					print("session doesn't exist? key error?")
				key = raw_input("continue?(enter 'q' to quit)")

database.pickle_database("200", db)
"""