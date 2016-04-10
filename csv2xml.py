#!/usr/bin/python3

import sys
import argparse
import re
from lxml import etree
import xml.dom.minidom
import sys
sys.path.append(sys.path.pop(0))
import csv

def meta_conv(cell):
	cell = cell.replace("\"", "???")
	return cell

def conv_meta(match):
	return chr(int(match.group(2)))

def substitution(rows):
	if len(rows[0]) < 1: return
	chars = (' ', ',', '\n', '\r')
	for i in range(0, len(rows[0])):
		for c in chars:
			rows[0][i] = rows[0][i].replace(c, options.subst)

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
# print (options)
# print (sys.argv)

if options.help:
	if len(sys.argv) != 2:
		parser.error("Parameter --help needs to be alone")
	parser.print_help()

if options.i and not options.line_element:
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

rows = list()
try:
	if type(options.input_file) == str:
		with open(options.input_file, "r", encoding="UTF-8", newline="") as f:
			csv_iter = csv.reader(f, delimiter=options.separator, quotechar="\"")
			for row in csv_iter:
				rows.append("?????".join(row))
	else:
		csv_iter = csv.reader(options.input_file, delimiter=options.separator, quotechar="\"")
		for row in csv_iter:
			rows.append("?????".join(row))
except OSError as err:
	print("OS error: {0}".format(err), file=sys.stderr)
	exit(2)


for i in range(0, len(rows)):
	rows[i] = rows[i].split("?????")

# print (rows)
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

# building xml

indent = "  "
ind_num = 2
if options.root_element:
	ind_num += 1

try:
	output_data = ""
	root = None
	if options.root_element:
		root = etree.Element(options.root_element)
	
	if options.subst is None:
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
				cell.text = "\n" + ind_num*indent + meta_conv(col) + "\n" + (ind_num-1)*indent
				counter += 1
			if not options.root_element:
				output_data += (etree.tostring(r, pretty_print=True).decode("UTF-8"))
		if options.root_element:
			output_data = etree.tostring(root, pretty_print=True).decode("UTF-8")

	else:
		substitution(rows)
		for j in range(0, len(rows)):
			if j == 0 and len(rows) > 1: continue
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
			for i in range(0, len(rows[j])):
			
				if i >= len(rows[0]) and options.all_columns: cell = etree.SubElement(r, options.column_element + str(i+1))
				elif i < len(rows[0]): cell = etree.SubElement(r, rows[0][i])
				else: continue

				if len(rows) != 1: cell.text = "\n" + ind_num*indent + meta_conv(rows[j][i]) + "\n" + (ind_num-1)*indent
			
			if not options.root_element:
				output_data += (etree.tostring(r, pretty_print=True).decode("UTF-8"))
		if options.root_element:
			output_data = etree.tostring(root, pretty_print=True).decode("UTF-8")

except ValueError as err:
	print("Invalid tag name", file=sys.stderr)
	exit(30)



if not options.n:
	output_data = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n" + output_data;

#print output

output_data = re.sub(r"(&#(\d{3});)", conv_meta, output_data)
output_data = re.sub(r"\?\?\?", "&quot;", output_data)
output_data = re.sub(r"\ \ ", 2*indent, output_data)

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