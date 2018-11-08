import struct, time

#for debugging import os
import os

class fileHandler:
	"""
		Handles loading of files which are stored in binary
		See: http://www.jsu.edu/depart/psychology/sebac/datafile/data-format.html
		For information about how the file format
	"""
	def __init__(self):
		
		self.birdNo = None
		self.date = None
		self.weight = None
		self.box = None
		self.id = None
		
		self.name = '123AA12.123'
		self.session_no = ''
		
		self.session = {"T": []}
		
	"""
		Private Method, this should never need to be used by external classes
		input 8 bits of data from file
	"""
	@staticmethod
	def get8(fileInput):
		return struct.unpack('B', fileInput.read(1))[0]

	"""
		Private Method, this should never need to be used by external classes
		input 16 bits of data from file (2 bytes)
	"""
	@staticmethod
	def get16(fileInput):
		data = struct.unpack('H',fileInput.read(2))[0]
		return data

	"""
		Private Method, this should never need to be used by external classes
		input 32 bits of data from file (4 bytes)
	"""
	@staticmethod
	def get32(fileInput):
		data = struct.unpack('I',fileInput.read(4))[0]
		return data

	"""
		Returns True on success False on failure
	"""
	def loadFile(self,fileName):
		try:
			f = open(fileName,'rb')
			oldtim = 0;
			self.birdNo = self.get16( f );
			#time might be causing an issue in converting to json file
			self.date = time.localtime(self.get32( f )); #Todo: Set the timezone
			self.weight = self.get16( f );
			self.box = self.get16( f );
			self.id = self.get32( f );
			

			self.name = fileName[-11:]
			self.session_no = self.name[5:7]
			
			readFile = True;
			
			
			line_no = 0
			
			#load header into events table
			#Need to add a header field for session number and adjust it so that phase c sessions get +99 OR do the latter in database
			header = {'bird_no':self.birdNo,"""'date':self.date,""" 'weight':self.weight, 'box':self.box, 'name':self.name, 'contains_error': False}
			for c in header:
				self.session[c] = header[c]
				
				
			while(readFile == True):
				#Read the data from the file
				itype = self.get8( f )
				idata = self.get8( f )
				bird_time = self.get32( f )
				
				#build tables of events
				line = []
				
				line.append(itype)
				line.append(idata)
				line.append(bird_time)
				
				self.session["T"].append(line)
				
				line_no = line_no + 1
				
				
				if(itype == 8):
					self.session['contains_error'] = True
					
					
					
				if(itype != 7):
					oldtim = bird_time;
					if ( itype == 5 ):
						#The end of the file has been reached
						readFile = False
					
				
					
			f.close()
			return True
		except IOError:
			print("Could not open file %s" %fileName)
			return False
			