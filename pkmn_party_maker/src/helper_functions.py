# external libs
import math
import os
import random
import pyperclip
import pokepy
from datetime import datetime #https://www.programiz.com/python-programming/datetime/timestamp-datetime
import inspect
import time
import colorama
import traceback
import operator

# project libs
from pglobals import DEBUG
from timing import *

input_wait_identifier = "USER INPUT DELAY"

# returns the lesser of a and b
def lesser(a,b):
	return a if a < b else b

# returns the greater of a and b
def greater(a,b):
	return a if a > b else b

# prints to console if DEBUG is True
# this seems to accept multiple inputs correctly
# print("hello","bye") --> hello bye
# printd("hello","bye") --> hello bye
# TODO: test with print("this is an int: %d", digit) kinda stuff
def printd(*args):
	if(DEBUG): 
		print("("  + get_parent_file_name() + " " + str(get_parent_line_number()) + " " + get_parent_funct_name() + "()) ", end="")
		print(*args)

# a wrapper for assert that only executes if DEBUG is True
def assertd(condition, message = None):
	if(DEBUG): assert condition, message 

# returns True if i is an int
# according to https://www.tutorialspoint.com/python3/python_numbers.htm "long" is no longer a type in Py3
def is_int(i):
	return isinstance(i, int)

# returns True if f is a float
def is_float(f):
	return isinstance(f, float)

# returns True if s is a string
def is_str(s):
	return isinstance(s, str)

# returns True if l is a list
def is_list(l):
	return isinstance(l, list)

# returns True if d is a dict
def is_dict(d):
	return isinstance(d, dict)

# returns True if o is a Pokepy Pokemon object
def is_pokepy_pkmn(o):
	return isinstance(o,pokepy.resources_v2.PokemonResource)

# returns True if o is a Pokepy Move object
def is_pokepy_move(o):
	return isinstance(o,pokepy.resources_v2.PokemonMoveSubResource)

# returns true if i is a positive integer
def is_positive_int(i):
	return is_int(i) and i > 0

# returns T if a is an rgb tuple in the form (0-255, 0-255, 0-255)
def is_rgb(a):
	rgb_val_check = lambda x: 0 <= x and x <= 255
	return len(a) == 3 and get_class_name(a) == "tuple" and False not in [rgb_val_check(x) for x in a]

# return the class name of object o 
# this simply reformats the ouput of type() 
# type(o) --> "<class 'foo'>" 
# get_class_name(o) --> "foo"
# "type(x).__name__" might also work: https://stackoverflow.com/questions/510972/getting-the-class-name-of-an-instance 
def get_class_name(o):
	"""
	y = str(type(o))
	x = y.split(' ')[1]
	x = x.replace('<', '')
	x = x.replace('>', '')
	x = x.replace('\'', '')
	return x
	"""
	return type(o).__name__

# prints each element of list l, one line at a time
def print_list(l):
	assertd(is_list(l),"Argument to print_list() is not a list. Type: " + get_class_name(l))
	for e in l:
		print(e)

# prints each k,v pair of dict d, one line at a time
def print_dict(d):
	assertd(is_dict(d),"Argument to print_dict() is not a dict. Type: " + get_class_name(d))
	for k in d:
		print(k)

# prints all the attributes of the given object o, one line at a time
# source: https://stackoverflow.com/questions/2675028/list-attributes-of-an-object
def print_attributes(o):
	#print(o.__dict__)
	assertd(o!=None,"Bad input to print_attributes(): " + str(o))
	print("\nAttributes of " + get_class_name(o) + ":")
	attribs = vars(o)
	for attrib in attribs:
		print(attrib)
	print("\n")

# prints all the callable functions of the given object o, one line at a time
# source: https://stackoverflow.com/questions/34439/finding-what-methods-a-python-object-has
def print_functions(o):
	assertd(o!=None,"Bad input to print_functions(): " + str(o))
	object_methods = [method_name for method_name in dir(o) if callable(getattr(o, method_name))]
	for method in object_methods:
		print(method)

# list all the files in path
def list_files(path):
	assertd(path != None and is_str(path) and path.strip() != "","Invalid argument to list_files(): " + str(path))
	return [f for f in listdir(path) if isfile(join(path, f))]

# input: len(str(number)) <= num_digits
# output: string that is num_digits long with 0's in front of number
# i.e. format_digits(1,3) --> 001
# i.e. format_digits(10,3) --> 010
# i.e. format_digits(100,3) --> 100 
# i.e. format_digits(100,5) --> 00100
def format_digits(number, num_digits):
	# input check
	assertd(is_int(number),"Invalid number argument to format_digits(): " + str(number))
	assertd(is_int(num_digits) and num_digits > 1,"Invalid number argument to format_digits(): " + str(number))
	
	number_str_len = len(str(number))
	assertd(number_str_len <= num_digits,
		"Invalid input to format_digits(): number " + str(number) + " is already longer than " + str(num_digits) + " digits long.")

	# form output
	sign_str = ""
	if(number < 0):
		sign_str = "-"
	diff = greater(0,num_digits - number_str_len)
	return sign_str + "0"*diff + str(abs(number))

# prints the items in l1 but not l2, then vice versa
def list_compare(l1,l2):
	start_timer()
	assertd(is_list(l1),"Bad input to list_compare(): l1 is not a list, it is of type: " + get_class_name(l1))
	assertd(is_list(l2),"Bad input to list_compare(): l2 is not a list, it is of type: " + get_class_name(l2))
	for x in l1:
		if x not in l2:
			print(str(x) + " is in l1 but not l2")
	for y in l2:
		if y not in l1:
			print(str(y) + " is in l2 but not l1")
	end_timer()

# generates a text file containing #s 1-251
def write_dexnumbers():
	start_timer()
	f = open("dexnums.txt","w+")
	for i in range(1,252):
		if(i!=251):
			f.write(format_digits(i,3) + "\n")
		else:
			f.write(format_digits(i,3))
	f.close()
	end_timer()

# input: min_num < max_num
# output: a random integer between min_num and max_num (inclusive)
# originally borrowed as js code from H:\cloud\Dropbox\ucla\experiments\group_dm\static\js	
#TODO: test this and get the expected statistical distributions
# NOTE: get_random_int(a,a) (where min_num == max_num) is allowed
def get_random_int(min_num, max_num):

	start_timer()

	# check inputs
	assertd(is_int(min_num), "min to get_random_int() is not an integer. min: " + str(min_num))
	assertd(is_int(max_num), "max to get_random_int() is not an integer. max: " + str(max_num))
	assertd(min_num <= max_num, "min_num > max_num in get_random_int() min: " + str(min_num) + " max: " + str(max_num))

	# optional code as opposed to is_int() asserts that converts float arguments into ints. 
	# if code is reinstated, the following comments could be added to the function defintion:
	# if min_num is a float, it will have ceil() applied to it (only ints ABOVE that float are allowed)
	# if max_num is a float, it will have floor() applied to it (only ints BELOW that float are allowed)
	"""
	if is_float(min_num):
		min_num = math.ceil(min_num)
	if is_float(max_num):
		max_num = math.floor(max_num)
	"""

	# RNG
	result = random.randint(min_num,max_num)
	#result = round(math.floor(math.random() * (max_num - min_num + 1)) + min_num)

	# check output
	assertd(result >= min_num, "bad result from get_random_int: result is < min. min: " + str(min_num) + " result: " + str(result))
	assertd(result <= max_num, "bad result from get_random_int: result is > max. max: " + str(max_num) + " result: " + str(result))

	end_timer()

	return result

# copies the string s to the OS (Windows only??) copy-paste clipboard (available to paste by Ctrl+V or right click -> paste)
# taken from https://stackoverflow.com/questions/11063458/python-script-to-copy-text-to-clipboard
def copy_str_to_clipboard(s):
	start_timer()
	assertd(s!=None,"Bad input to copy_str_to_clipboard(): " + str(s))
	pyperclip.copy(s)
	end_timer()

# returns an int representing the number of bytes the object o requires
# taken from https://stackoverflow.com/questions/449560/how-do-i-determine-the-size-of-an-object-in-python
def get_size(o):
	assertd(o!=None,"Bad input to get_size(): " + str(o))
	return sys.getsizeof(o)

# returns True if n is an int is a legitiamte Gen2 Pokedex #, aka (1-251) inclusive
def is_gen2_dexnum(n):
	return is_int(n) and n > 0 and n < 252

def get_timestamp_str():
	start_timer()
	result = str(datetime.fromtimestamp(datetime.timestamp(datetime.now()))).split('.')[0].replace(':','.').replace(' ','_')
	end_timer()
	return result

# returns the string name of the calling function
# useful for debugging purposes (i.e. timing and perhaps assertd statements)
# source: https://stackoverflow.com/questions/900392/getting-the-caller-function-name-inside-another-function-in-python
# for "get THIS function name":
# https://stackoverflow.com/questions/33162319/how-can-get-current-function-name-inside-that-function-in-python/33162432
def get_fname():
	#start_timer()
	result = inspect.stack()[1][3]
	#end_timer()
	return 

# returns the string name of the parent function of the function that called get_parent_funct_name
# NOTE: do not time this function, as start_timer/end_timer calls this... so timing this causes a recursive stack overflow
# i.e. f() -> g() -> get_parent_funct_name() returns "f"
# used by timing scripts
# inferred stack()[i] i should be 2 from 
# https://stackoverflow.com/questions/900392/getting-the-caller-function-name-inside-another-function-in-python
def get_parent_funct_name():
	#start_timer()
	stack = inspect.stack()
	assertd(len(stack) >= 3)
	# i dont know exactly what stack_i2 or the stack list represents, just following above stackoverflow post and adding sanity checks
	stack_i2 = stack[2]
	assertd(len(stack_i2) >= 4)
	parent_fname = stack_i2[3]
	assertd(is_str(parent_fname) and parent_fname.strip() != '')
	#end_timer()
	return parent_fname

# https://stackoverflow.com/questions/3711184/how-to-use-inspect-to-get-the-callers-info-from-callee-in-python
def get_parent_line_number():
	#start_timer()
	prev_frame = inspect.currentframe().f_back.f_back
	(filename, line_number, function_name, lines, index) = inspect.getframeinfo(prev_frame)
	#end_timer()
	return line_number

def get_parent_file_name():
	#start_timer()
	prev_frame = inspect.currentframe().f_back.f_back
	(filename, line_number, function_name, lines, index) = inspect.getframeinfo(prev_frame)
	#end_timer()
	return str(filename).split(filename[2])[-1]

def print_stack_trace():
	#start_timer()
	for line in traceback.format_stack():
		print(line.strip())
	#end_timer()

def is_same_type(o1, o2):
	return type(o1) is type(o2)

# gets current timestamp
# NOTE: if timing accuracy is very crucial, you may want to import and directly call timer() in the parent function instead, 
#		since get_time() inherently has some overhead
# source: https://stackoverflow.com/questions/7370801/measure-time-elapsed-in-python
def get_time():
	return time.time()

# loads each string line in the file named fname into load_enum
# if the input file is detected to be a dict, load_enum will be setup as a dict
# note that this will only have lists of strings or dicts with strings mapped to strings
# i.e. strings that actually encode lists/ints are left to be decoded by the calling function
# TODO: better is_dict detection... perhaps have output files just flag this
# TODO: detect types (i.e. lists, dicts, ints)... but thats a lot more complicated and not always guarenteed based solely on file text?
def load_input_file(fname):
	start_timer()
	f = open(fname,"r+")
	setup = False
	#input_is_dict = is_dict(load_enum)
	#printd(load_enum)
	list_result = []
	dict_result = {}
	for line in f:
		split_line = line.split(": ")
		line_is_dict = len(split_line) == 2
		if line_is_dict:
			dict_result[split_line[0]] = split_line[1]
		else:
			list_result.append(line)

		"""
		
		if file_is_dict:
			if not setup:
				result = {}
				setup = True
			else:
				assertd(is_dict(result))
			load_enum[split_line[0]] = load_enum[1]
		else:
			if not setup:
				result = []
				setup = True
			else:
				assertd(is_list(result))
		"""
			
	f.close()
	end_timer()
	if(line_is_dict):
		return dict_result
	else:
		return list_result

# outputs the enumerable object (i.e. list/dict), each entry line by line, to the output file (with path) specified by fname
# prefix/postfix get prepended/appended respectively to the lines in out_enum
# NOTE: if you want "\n"s between entries of out_enum, set postfix = "\n"
def output_enum(out_enum, fname, prefix = None, postfix = None):

	start_timer()

	#printd(os.path.dirname(os.path.realpath(__file__)))
	#printd(os.getcwd())

	#fname_new = fname.replace('/','\\')

	f = open(fname,"w+")
	input_is_dict = False
	if(is_dict(out_enum)):
		input_is_dict = True
	for entry in out_enum:
		if(input_is_dict):
			line = str(entry) + ": " + str(out_enum[entry])
		else:
			line = str(entry)
		# rather than check the existence of prefix/postfix and add them to out_str individually, 
		# build out_str all at once rather than twice to save some time
		if(prefix != None):
			if(postfix != None): # prefix and postfix exist
				out_str = prefix + line + postfix
			else: # prefix exists but postfix doesn't
				out_str = prefix + line
		elif(postfix != None): # prefix doesn't exist but postfix does
			out_str = line + postfix
		else: # neither prefix nor postfix exist
			out_str = line
		f.write(out_str)
	f.close()

	end_timer()

# returns a list of strings that is a tab_formatted version of this one
# tab_format() assumes each str should be appended by tab at least once
# TODO: does print("%s %d" % (strx, inty)) render this kind of stuff pointless? solutions might exist with that built in function
def tab_format(inlist):

	start_timer()

	# using the actual "\t" character seems less consistent than an arbitrary number of spaces
	tab_postfix = " "

	max_len = 0
	for instr in inlist:
		assertd(is_str(instr))
		#printd(instr)
		instr_len = len(instr+tab_postfix)
		if instr_len > max_len:
			max_len = instr_len

	for i in range(len(inlist)):
		format_template = '{:<' + str(max_len) + 's}' + tab_postfix
		inlist[i] = format_template.format(inlist[i])

	end_timer()	

# https://algocoding.wordpress.com/2015/04/14/how-to-sort-a-list-of-tuples-in-python-3-4/
def sort_list_of_tuples(tlist, tindex, reverse = False):
	start_timer()
	assertd(is_list(tlist))
	assertd(is_int(tindex))
	tlist.sort(key = operator.itemgetter(tindex), reverse = reverse)
	end_timer()

# wrapper function for input() and times it, and records that as "user input delay" in timing.py stats
def input_and_time(*args):
	global input_wait_identifier
	start_timer(input_wait_identifier)
	result = input(*args)
	end_timer(input_wait_identifier)
	return result

# ----- COLOR METHODS -----
# https://pypi.org/project/colorama/
# https://www.devdungeon.com/content/colorize-terminal-output-python

# returns the colorama foreground constant associated with a string color_str
def get_color(color_str):
	start_timer()
	assertd(is_str(color_str))
	color_str_formatted = color_str.strip().lower()
	assertd(color_str_formatted != '')
	if color_str_formatted == 'black':
		return colorama.Fore.BLACK
	elif color_str_formatted == 'red':
		return colorama.Fore.RED
	elif color_str_formatted == 'green':
		return colorama.Fore.GREEN
	elif color_str_formatted == 'yellow':
		return colorama.Fore.YELLOW
	elif color_str_formatted == 'blue':
		return colorama.Fore.BLUE
	elif color_str_formatted == 'magenta':
		return colorama.Fore.MAGENTA
	elif color_str_formatted == 'cyan':
		return colorama.Fore.CYAN
	elif color_str_formatted == 'white':
		return colorama.Fore.WHITE
	elif color_str_formatted == 'reset':
		return colorama.Fore.RESET
	else:
		printd("unrecognized color string to get_color(): " + color_str)
		return None
	end_timer()

# sets the terminal foreground color to the given color
# TODO if not str, check in_color is within colorama colors
def set_color(in_color):
	start_timer()
	assertd(in_color != None)
	if is_str(in_color):
		in_color = get_color(in_color)
	print(in_color)
	end_timer()

def reset_color():
	return set_color("reset")

# returns the colorama constant associated with a string bg_color_str
def get_bg_color(bg_color_str):
	start_timer()
	assertd(is_str(bg_color_str))
	bg_color_str_formatted = bg_color_str.strip().lower()
	assertd(bg_color_str_formatted != '')
	if bg_color_str_formatted == 'black':
		return colorama.Back.BLACK
	elif bg_color_str_formatted == 'red':
		return colorama.Back.RED
	elif bg_color_str_formatted == 'green':
		return colorama.Back.GREEN
	elif bg_color_str_formatted == 'yellow':
		return colorama.Back.YELLOW
	elif bg_color_str_formatted == 'blue':
		return colorama.Back.BLUE
	elif bg_color_str_formatted == 'magenta':
		return colorama.Back.MAGENTA
	elif bg_color_str_formatted == 'cyan':
		return colorama.Back.CYAN
	elif bg_color_str_formatted == 'white':
		return colorama.Back.WHITE
	elif bg_color_str_formatted == 'reset':
		return colorama.Back.RESET
	else:
		printd("unrecognized color string to get_bg_color(): " + bg_color_str)
		return None
	end_timer()

# sets the terminal background color to the given color
# TODO if not str, check bg_in_color is within colorama bg colors
def set_bg_color(bg_in_color):
	start_timer()
	assertd(bg_in_color != None)
	if is_str(bg_in_color):
		bg_in_color = get_color(bg_in_color)
	print(bg_in_color)
	end_timer()

def reset_bg_color():
	return set_bg_color("reset")

def get_style(style_str):
	start_timer()
	assertd(is_str(style_str))
	style_str_formatted = style_str.strip().lower()
	assertd(style_str_formatted != '')
	if style_str_formatted == 'dim':
		return colorama.Style.DIM
	elif style_str_formatted == 'normal':
		return colorama.Style.NORMAL
	elif style_str_formatted == 'bright':
		return colorama.Style.BRIGHT
	elif style_str_formatted == 'reset':
		return colorama.Style.RESET_ALL
	else:
		printd("unrecognized style string to get_style(): " + style_str)
		return None
	end_timer()

# TODO if not str, check in_style (lol @ "in style") is within colorama styles
def set_style(in_style):
	start_timer()
	assertd(in_style != None)
	if is_str(in_style):
		in_style = get_color(in_style)
	print(in_style)
	end_timer()

def reset_style():
	print(colorama.Style.RESET_ALL)

def get_all_resets(): 
	start_timer()
	result = get_color("reset") + get_bg_color("reset") + get_style("reset")
	end_timer()
	return result

def reset_all():
	print(get_all_resets())

"""
def color_str(s,c):
	return get_color(c) + s + get_all_resets()
"""

"""

# ----- UNUSED -----

# ??
def is_within_range(value, range_tuple):
	return range_tuple[0] <= value and value <= range_tuple[1]

# js code from dropbox ucla group_dm static js folder
# forgot python has native assert lol
# assert is a special function that throws an error if condition is not true
# this is used for parameter checking
# does not run if DEBUG is disabled
def assert(condition, message):
	if(DEBUG && !condition):
		if(message != undefined)
			message = "Assertion failed: " + message;
		else
			message = "Assertion failed.";
		throw new Error(message);
"""
