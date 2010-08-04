from __future__ import print_function
import sys
import re
import config
from vsparser import parse_script, SyntaxError_
import getopt
import argparse
import os

class StrException(Exception):
	def __str__(self):
		return self.message
class FileNotFound(StrException):
	def __init__(self, file):
		self.message = "The file '%s' was not found." % file
class FileNewerExists(StrException):
	def __init__(self, file_newer, file_older):
		self.message = "File '%s' is newer than '%s'." % (file_newer, file_older)
class WrongFileType(StrException):
	def __init__(self, file):
		self.message = "File '%s' has unrecognized extension." % (file)

def convert_vs(file, target_file):
	print("convert %s to %s"%(file,target_file))
	#out = parse_script(sys.argv[1], open(sys.argv[1]), config.config)
	#print("\n".join(out))

def process_options(argv):
	parser = argparse.ArgumentParser(description='VerilogScript processor')
	parser.add_argument('-e', '--execute', help="Command to execute Verilog compiler")
	parser.add_argument('file', nargs='+')
	args = parser.parse_args(argv)
	exec_params = []
	for file in args.file:
		if not os.path.isfile(file):
			raise FileNotFound(file)
		if file.endswith('.v'):
			exec_params.append(file)
		elif file.endswith('.vs'):
			target_file = file[:-1] #remove ending 's'
			if os.path.exists(target_file) and \
				os.path.getmtime(target_file) > os.path.getmtime(file):
				raise FileNewerExists(target_file, file)
			convert_vs(file, target_file)
			exec_params.append(target_file)
		else:
			raise WrongFileType(file)

def main():
	try:
		process_options(sys.argv[1:])
	except SyntaxError_, e:
		print("Syntax error: %s at line %d" % (e.msg, e.line))
	except StrException as e:
		print("Error: "+str(e))

if __name__ == "__main__":
	main()

