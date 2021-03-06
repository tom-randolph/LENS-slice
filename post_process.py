'''This will parse the original gcode file from slic3r and adapt parameters for use with LENS'''

#TODO: Add arg parsing for settings like print parameters and parsing rules
#TODO: Add analytics (number of lines omitted, other changes)
#TODO: Add option to write to different file

import sys
import os
import fileinput



supported_types=[".gcode",".txt"]

omit_line_rules=["G92", #extruder offset command
					"M1", #all M1** codes
					#"G1 E" ,#extruder specific commands
					"M82", 
					]
lines_changed=0;

postamble="""M5 ;turn off laser
M303 ; turn off powder 1
M305 ;turn off powder 2
G1 Z20 F5000 ;Raise print head
G28 X Y ; home X Y axis"""
					
def check_omit_line(line):
	'''Checks to see if line contains bad codes according to omit_line_rules,
	will return true if line should be omitted'''
	for code in omit_line_rules:
		if code in line:
			return True
			
	else: return False

if __name__=="__main__":

	nargs=len(sys.argv)
	if nargs is not 2:
		print("please provide a file to edit")
		exit()
	filename=sys.argv[1]
	filename_, filetype=os.path.splitext(filename)

	if filetype not in supported_types:
		print("Unrecognized filetype")
		print("Please use the following types:")
		print(*supported_types, sep=',')
		exit()
		
	print("Processing {}....".format(filename))
	
	try:
		#wrapping this operation in a try statement allows for automatic file recovery in case of a fatal error
		with fileinput.FileInput(filename, inplace=True,backup ='.old') as file:
		
			for line in file:
				if check_omit_line(line):
					lines_changed+=1
					continue
				print(line,end='')
		
			
	except:
		#restore the original file from backup
		os.remove(filename)
		os.rename(filename+'.old',filename)
		raise
	#with open(filename,'a') as file:
	#	file.write(postamble)
	print("Finished")
	print("Number of lines change:{}".format(lines_changed))
	#print("Added Postamble:")
	#print(postamble)
	
		