'''This will parse the original gcode file from slic3r and adapt parameters for use with LENS'''

#TODO: Add arg parsing for settings like print parameters and parsing rules
#TODO: Add analytics (number of lines omitted, other changes)
#TODO: Add option to write to different file

import sys
import os
import argparse
import numpy as np



supported_types=[".gcode",".txt"]

laser = True


def laser_on(line=None):
	return 'M3\n'

def laser_off(line=None):
	return 'M5\n'

def laser_toggle(line=None):
	global laser
	laser = not laser
	if laser:
		return laser_on()
	else:
		return laser_off()

def confirm_laser(line):
	global laser
	if 'E' in line:
		if not laser:
			laser = True;
			return 'M3\n' + line
	else:
		return line

def omit(line):
	return ';Line omitted in post-process\n'

def adjust_feed(line, scale=15.5):
	out_line = line.split('F')

	try:
		out_line=out_line[0] + 'F' + str(np.around(float(out_line[-1])/scale,5)) + '\n'
	except ValueError:
		return line
	except:
		raise
		print('Error adjusting feed rate')
		return line
	
	return out_line
rules = {
	# 'G1 X' : confirm_laser,
	'F' : adjust_feed,
	'G1 E' : laser_toggle,
	'G92' : laser_off,
	'M1' : omit,
	'M82' : omit,
	
}
					

def parse_file(in_file,out_file):
	'''Parse an input file line-by-line and change codes in file according to specified rule modifiers'''

	# A counter for the nubmer of lines changed in the script
	lines_changed=0

	# Open the input file
	with open(in_file) as i_f:

		# Store its contents
		lines=i_f.readlines()

		#Open and/or create the output file
		with open(out_file, 'w') as o_f:

			# For each line in the input file, apply the appropriate changes and write them to the output file
			for line in lines:

				was_changed, out_line = check_rules(line)

				# Track the number of changes made
				if was_changed :
					lines_changed += 1
				o_f.write(out_line)

	# Return the lines changed to an output statistic
	return lines_changed

def check_rules(in_line):
	''' Checks to see which rule modifiers apply to a line of text and modifies them according to the fucntion specified in the dict'''

	was_changed = False
	out_line = in_line
	for rule in rules:
		if rule in in_line:
			was_changed = True
			out_line = rules[rule](in_line)
			print('Checked rule')
			print(out_line)
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
		sys.exit(1)

	output_file=args.output_file

	if output_file is None:
		output_file = input_file.split('.')
		output_file = output_file[0]+'-LENS.'+output_file[1]
	
	if os.path.isfile(output_file):
		print('File already exists...')

		ans = input('Would you like to overwrite it? (y/n)')
		if ans in r'^[Yy]$|^Yes$|^yes|':
			pass
		else: 
			print('No edits will be made. Specify output filename if desired.')

			sys.exit(1)
		
	print("Processing {}....".format(input_file))

	lines_changed = parse_file(input_file,output_file)
	
	if lines_changed is not None:

		print("Finished")
		print("Number of lines changed: {}".format(lines_changed))

	
		