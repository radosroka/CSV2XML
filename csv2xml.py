#!/usr/bin/python3

import sys
import argparse
import re
from lxml import etree

def meta_conv(string):
	string = string.replace("<", "&lt;")
	string = string.replace("&", "&amp;")
	string = string.replace('\r', '')
	string = string.replace(">", "&gt;")
	string = string.replace('\"', "&quot;")	
	return string

def check_root_tag(string):
	if  None != re.match('^[^\w:_].*$', string)  or None != re.match('^[0-9].*$', string) or None != re.match('[^\w:_\.\-]', string):
		print ("Invalid root tag", file=sys.stderr)
		exit(30)
	return
	
def check_line_tag(string):
	if  None != re.match('^[^\w:_].*$',string) or None != re.match('^[0-9].*$', string) or None != re.match('[^\w:_\.\-]', string):
		print ("Invalid line tag", file=sys.stderr)
		exit(30)
	return

def check_col_tag(string):
	if  None != re.match('^[^\w:_].*$',string) or None != re.match('^[0-9].*$', string) or None != re.match('[^\w:_\.\-]', string):
		print ("Invalid col tag", file=sys.stderr)
		exit(30)
	return

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
	  dest="root_element", help="Set root element",
	  metavar="root_element")
parser.add_argument("-s",
	  dest="separator", help="Set separator",
	  metavar="separator", default=",")
parser.add_argument("-h",
	  dest="subst", help="Set substitution",
	  metavar="subst", nargs="?")
parser.add_argument("-c",
	  dest="column_element", help="Set column-element",
	  metavar="column_element", default="col")
parser.add_argument("-l",
	  dest="line_element", help="Set line-element",
	  metavar="line_element", default="row")
parser.add_argument("-i", 
	  action="store_true", dest="i",
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
# print (sys.argv)

if options.help:
	if len(sys.argv) != 2:
		parser.error("Parameter --help needs to be alone")
	parser.print_help()

if options.i and "-l" not in sys.argv:
	parser.error("Parameter -i cannot be without -l")

if "-h" in sys.argv and options.subst == None:
	options.subst = "-"

if "--start" in sys.argv and "-i" not in sys.argv:
	parser.error("Parameter --start cannot be without -i and -l")

if options.missing_field and not options.error_recovery:
	parser.error("Parameter --missing-field cannot be without --error-recovery")

if options.all_columns and not options.error_recovery:
	parser.error("Parameter --all-columns. cannot be without --error-recovery")

if options.separator == "TAB":
	options.separator = "\t"

if options.start <= 0:
	parser.error("--start must be greater than zero")

if options.root_element != None:
	check_root_tag(options.root_element)
check_line_tag(options.line_element)
check_col_tag(options.column_element)

input_data = ""
try:
	if type(options.input_file) == str:
		f = open(options.input_file, "r", encoding="UTF-8")
		input_data = f.read()
		f.close()
	else:
		input_data = options.input_file.read()
except OSError as err:
	print("OS error: {0}".format(err), file=sys.stderr)
	exit(2)

#print (input_data)
rows = input_data.split("\n")
for i in range(0, len(rows)):
	rows[i] = rows[i].split(options.separator)

right_count = len(rows[0])


if not options.error_recovery:
	for row in rows:
		if len(row) != right_count:
			print ("Bad number of columns", file=sys.stderr)
			exit(32)
else:
	for row in rows:
		while len(row) < right_count: row.append(options.missing_field)
		if not options.all_columns:
			while len(row) > right_count: row.pop()



# print (rows)

#building xml

output_data = ""
root = None
if options.root_element:
	root = etree.Element(options.root_element)
for row in rows:
	r = None
	if options.i:
		if options.root_element:
			r = etree.SubElement(root, options.line_element, index=str(options.start))
		else:
			r = etree.Element(options.line_element, index=str(options.start))
		options.start += 1
	else:
		if options.root_element:
			r = etree.SubElement(root, options.line_element)
		else:
			r = etree.Element(options.line_element)
	counter = 1
	for col in row:
		cell = etree.SubElement(r, options.column_element + str(counter))
		cell.text = col
		counter += 1
	if not options.root_element:
		output_data += (etree.tostring(r, pretty_print=True).decode("UTF-8"))
if options.root_element:
	output_data = etree.tostring(root, pretty_print=True).decode("UTF-8")

if not options.n:
	output_data = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n" + output_data;

#print output
try:
	if type(options.output_file) == str:
		f = open(options.output_file, "w", newline='', encoding="UTF-8")
		f.write(output_data)
		f.close();
	else:
		options.output_file.write(output_data)
except OSError as err:
	print("OS error: {0}".format(err), file=sys.stderr)
	exit(2)