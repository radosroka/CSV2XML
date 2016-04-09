#!/usr/bin/python3

import sys
import argparse

input_data = ""
		

parser = parser = argparse.ArgumentParser(description='CSV2XML', add_help=False)
parser.add_argument("--help", action="store_true", dest="help",
				  default=False, help="Show this help message and exit")
parser.add_argument("--input",
				  dest="input_file", help="Input CSV file",
				  metavar="filename", default=sys.stdin)
parser.add_argument("--output",
                  dest="output_file", help="Output XML file",
                  metavar="filename", default=sys.stdout)
parser.add_argument("-n", action="store_true", dest="n",
				  default=False, help="Doesn't generate XML header")
parser.add_argument("-r",
                  dest="root-element", help="Set root element",
                  metavar="root_element", default="no")
parser.add_argument("-s",
                  dest="separator", help="Set separator",
                  metavar="separator", default=",")
parser.add_argument("-h",
                  dest="subst", help="Set substitution",
                  metavar="subst", default="-", nargs="?")
parser.add_argument("-c",
                  dest="column-element", help="Set column-element",
                  metavar="column_element", default="col")
parser.add_argument("-l",
                  dest="line-element", help="Set line-element",
                  metavar="line_element", default="row")
parser.add_argument("-i", action="store_true", dest="i",
				  default=False, help="Insert index into line-element")
parser.add_argument("--start",
                  dest="start", help="Start index",
                  metavar="N", default=1, type=int)
parser.add_argument("-e", "--error-recovery",
                  dest="error_recovery", help="Self recovery",
                  action="store_true", default=False)
parser.add_argument("--missing-field",
                  dest="missing_field", help="Insert val into empty missing cell",
                  metavar="val", default="")
parser.add_argument("--all-columns",
                  dest="all_columns", help="All columns will be recovered",
                  action="store_true", default=False)

options = parser.parse_args()
print (options)
print (sys.argv)

if options.help:
	if len(sys.argv) != 2:
		parser.error("Parameter --help needs to be alone")
	parser.print_help()

if options.i and "-l" not in sys.argv:
	parser.error("Parameter -i cannot be without -l")

if "--start" in sys.argv and "-i" not in sys.argv:
	parser.error("Parameter --start cannot be without -i and -l")

if options.missing_field and not options.error_recovery:
	parser.error("Parameter --missing-field cannot be without --error-recovery")

if options.all_columns and not options.error_recovery:
	parser.error("Parameter --all-columns. cannot be without --error-recovery")

try:
	if type(options.input_file) == str:
		f = open(options.input_file, "r")
		input_data = f.read();
		f.close();
	else:
		input_data = options.input_file.read()
except OSError as err:
	print("OS error: {0}".format(err), file=sys.stderr)
	exit(2)

print (input_data)