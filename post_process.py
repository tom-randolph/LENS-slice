'''This will parse the original gcode file from slic3r and adapt parameters for use with LENS'''

#TODO: Add arg parsing for settings like print parameters and parsing rules
#TODO: add analytics (number of lines omitted, other changes)

import sys
import os
import fileinput



supported_types=[".gcode",".txt"]

omit_line_rules=["G92", #extruder offset command
					"M" #all M codes
					]
lines_changed=0;
					
def check_omit_line(line):
	omit=False
	for code in omit_line_rules:
		if code in line:
			omit=True
			break
	return omit

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
				print(line)
			
	except:
		#restore the original file from backup
		os.remove(filename)
		os.rename(filename+'.old',filename)
		raise
	print("Finished")
	print("Number of lines change:{}".format(lines_changed))
	
		