import database
import os

db = database.eat_database("200_database.pickle")

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

def iterate_and(db, do_this): #, args):
	for p in db:
		for g in db[p]:
			for b in db[p][g]:
				PGB = db[p][g][b]
				db[p][g][b] = do_this(PGB, p, g, b)
				#do_this(PGB, *args)
	os.system("pause")
	database.pickle_database("200", db)

def set_PGB_labels(PGB, p, g, b):
		PGB['Phase_Name'] = p
		PGB['Group_Name'] = g
		PGB['Bird_Name'] = b
		print p, g, b
		return PGB
		
iterate_and(db, set_PGB_labels)
		
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