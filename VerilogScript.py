from __future__ import print_function
import sys
import re
import getopt
import argparse
import os
from convert import Converter, SyntaxError_
import subprocess

class FileNotFound(Exception):
	def __init__(self, file):
		self.message = "The file '%s' was not found." % file
	def __str__(self):
		return self.message
class WrongFileType(Exception):
	def __init__(self, file):
		self.message = "File '%s' has unrecognized extension." % (file)
	def __str__(self):
		return self.message

def process_options(argv):
	parser = argparse.ArgumentParser(description='VerilogScript processor')
	parser.add_argument('-e', '--execute', help="Command to execute Verilog compiler")
	parser.add_argument('file', nargs='+')
	args = parser.parse_args(argv)
	if args.execute:
		exec_params = args.execute.split()
	else:
		exec_params = [False]
	conv = Converter()
	for file in args.file:
		if not os.path.isfile(file):
			raise FileNotFound(file)
		if file.endswith('.v'):
			exec_params.append(file)
		elif file.endswith('.vs'):
			target_file = file[:-1] #remove ending 's'
			if not os.path.exists(target_file) or \
					os.path.getmtime(target_file) < os.path.getmtime(file):
				conv.convert_vs(file, target_file)
			exec_params.append(target_file)
		else:
			raise WrongFileType(file)
	if exec_params[0]:
		#print("EXEC"," ".join(exec_params))
		p = subprocess.Popen(exec_params, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		#print('out',p.stdout.read())
		for line in p.stdout:
			print(line, end="")
		error = False
		for line in p.stderr:
			error = True
			line = line.rstrip()
			parts = line.split(':',2)
			if len(parts) > 2:
				parts[0], parts[1] = conv.convert_error(parts[0], int(parts[1]))
				print('%s:%d:%s' %(parts[0], parts[1], parts[2]))
			else:
				print(line)
		if error:
			sys.exit(-1)
def main():
	try:
		process_options(sys.argv[1:])
	except SyntaxError_ as e:
		print("Syntax error: %s at line %d" % (e.msg, e.line))
	except (FileNotFound, WrongFileType) as e:
		print("Error: "+str(e))

if __name__ == "__main__":
	main()

