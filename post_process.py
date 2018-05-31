'''This will parse the original gcode file from slic3r and adapt parameters for use with LENS'''

#TODO: Add arg parsing for settings like print parameters and parsing rules
#TODO: Add analytics (number of lines omitted, other changes)
#TODO: Add option to write to different file

import sys
import os
import argparse



supported_types=[".gcode",".txt"]

omit_line_rules=["G92", #extruder offset command
					"M1", #all M1** codes
					#"G1 E" ,#extruder specific commands
					"M82", 
					]


def omit(line):
	return ';Line omitted in post-process\n'
rules = {
	'G92' : omit,
	'M1' : omit,
	'M82' : omit,
}
					
def check_omit_line(line):
	'''Checks to see if line contains bad codes according to omit_line_rules,
	will return true if line should be omitted'''
	for code in omit_line_rules:
		if code in line:
			return True
			
	else: return False

def parse_file(in_file,out_file):
	'''Parse an input file line-by-line and change codes in file according to specified rule modifiers'''

	if os.path.isfile(out_file):
		print('File already exists...')

		ans = input('Would you like to overwrite it? (y/n)')
		if ans in ['y','Y','Yes','yes']:
			pass
		else: 
			print('No edits will be made. Specify output filename if desired.')
			return None

	# A counter for the nubmer of lines changed in the script
	lines_changed=0;

	# Open the input file
	with open(in_file) as i_f:

		# Store its contents
		lines=i_f.readlines()

		#Open and/or create the output file
		with open(out_file, 'w') as o_f:

			# For each line in the input file, apply the appropriate changes and write them to the output file
			for line in lines:
				was_changed, line = check_rules(line)
				
				# Track the number of changes made
				if was_changed :
					lines_changed += 1
				o_f.write(line)

	# Return the lines changed to an output statistic
	return lines_changed

def check_rules(in_line):
	''' Checks to see which rule modifiers apply to a line of text and modifies them according to the fucntion specified in the dict'''

	was_changed = False
	out_line = in_line
	for rule in rules:
		# print(rule)
		if rule in in_line:
			was_changed = True
			out_line = rules[rule](in_line)
	# print(out_line)
	return was_changed, out_line
	

if __name__=="__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument('input_file', help = 'the path to the input file', type=str)
	parser.add_argument('output_file', help = 'the path to the output file', type=str, default = None, nargs='?')

	args = parser.parse_args()

	input_file=args.input_file
	filename_, filetype =os.path.splitext(input_file)

	if filetype not in supported_types:
		print("Unrecognized filetype")
		print("Please use the following types:")
		print(*supported_types, sep=',')
		sys.exit()

	output_file=args.output_file

	if output_file is None:
		output_file = input_file.split('.')
		output_file = output_file[0]+'-LENS.'+output_file[1]
		
	print("Processing {}....".format(input_file))

	lines_changed = parse_file(input_file,output_file)
	
	if lines_changed is not None:

		print("Finished")
		print("Number of lines changed: {}".format(lines_changed))

	
		