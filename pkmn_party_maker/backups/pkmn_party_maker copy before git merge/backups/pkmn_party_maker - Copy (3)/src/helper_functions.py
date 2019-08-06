import math
from os import listdir
from os.path import isfile, join
import random
import pyperclip

from pglobals import *


# returns the lesser of a and b
def lesser(a,b):
	if (a > b):
		return b
	return a

# returns the greater of a and b
def greater(a,b):
	if (a > b):
		return a
	return b

def is_within_range(value, range_tuple):
	return range_tuple[0] <= value and value <= range_tuple[1]

#TODO: check is_int
def is_positive_integer(a):
	return a > 0

# returns T/F if a is an rgb value in the form (0-255, 0-255, 0-255)
def is_rgb(a):
	rgb_val_check = lambda x:  0 <= x and x <= 255
	return len(a) == 3 and strip_class_name(a) == "tuple" and False not in [rgb_val_check(x) for x in a]

# a is an object such that type(a) yields a string "<class 'foo'>"
# this simple function strips the class name from that string and returns it (i.e. "foo")
def strip_class_name(a):
	y = str(type(a))
	x = y.split(' ')[1]
	x = x.replace('<', '')
	x = x.replace('>', '')
	x = x.replace('\'', '')
	return x

# prints all the attributes of the given object x
# source: https://stackoverflow.com/questions/2675028/list-attributes-of-an-object
def print_attributes(x):
	#print(x.__dict__)
	print("\nAttributes of " + strip_class_name(x) + ":")
	attribs = vars(x)
	for attrib in attribs:
		print(attrib)
	print("\n")

# prints all the callable functions of the given object x
# source: https://stackoverflow.com/questions/34439/finding-what-methods-a-python-object-has
def print_functions(x):
	object_methods = [method_name for method_name in dir(object) 
		if callable(getattr(object, method_name))]
	for method in object_methods:
		print(method)

# prints each element of list l one line at a time
def print_list(l):
	for x in l:
		print(x)

# prints each k,v pair of dict d one line at a time
def print_dict(d):
	for k in d:
		print(k)

def list_files(path):
	return [f for f in listdir(path) if isfile(join(path, f))]

# displays the number with leading 0's up to num_digits
# i.e. format_digits(1,3) --> 001
# i.e. format_digits(10,3) --> 010
# i.e. format_digits(100,3) --> 100
def format_digits(number, num_digits):
	diff = greater(0,num_digits - len(str(number)))
	return "0"*diff + str(number)

# prints the items in l1 but not l2, then vice versa
def list_compare(l1,l2):
	for x in l1:
		if x not in l2:
			print(str(x) + " is in l1 but not l2")
	for y in l2:
		if y not in l1:
			print(str(y) + " is in l2 but not l1")

# generates a text file containing #s 1-251
def write_dex_numbers():
	f = open("dex_nums.txt","w+")
	for i in range(1,252):
		if(i!=251):
			f.write(format_digits(i,3) + "\n")
		else:
			f.write(format_digits(i,3))
	f.close()

# js code from H:\cloud\Dropbox\ucla\experiments\group_dm\static\js	
# forgot python has native assert lol
"""
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

# returns true if i is an int
#TODO: should this include long or not?
def is_int(i):
	return isinstance(i, int)
	#return isinstance(i, (int,long))

# returns true if f is a float
def is_float(f):
	return isinstance(f, float)

# originally borrowed as js code from H:\cloud\Dropbox\ucla\experiments\group_dm\static\js	
# returns a random integer between min_num and max_num, INCLUSIVE
# if min_num is not an int, it will have ceil() applied to it (only ints ABOVE that float are allowed)
# if max_num is not an int, it will have floor() applied to it (only ints BELOW that float are allowed)
def get_random_int(min_num, max_num):
	# handle inputs
	#assert(is_int(min_num), "min to get_random_int() is not an integer. min: " + min_num)
	#assert(is_int(max_num), "max to get_random_int() is not an integer. max: " + max_num)
	#if(is_float(min_num)) { min_num = math.ceil(min_num) }
	#if(is_float(max_num)) { max_num = math.floor(max_num) }
	#result = round(math.floor(math.random() * (max_num - min_num + 1)) + min_num)
	result = random.randint(min_num-1,max_num)
	#assert(result >= min_num, "bad result from get_random_int: result is < min. min: " + min_num + " result: " + result)
	#assert(result <= max_num, "bad result from get_random_int: result is > max. max: " + max_num + " result: " + result)
	return result

# copies the string s to the OS (Windows only??) copy-paste clipboard (available to paste by Ctrl+V or right click -> paste)
def copy_str_to_clipboard(s):
	pyperclip.copy(s)
	spam = pyperclip.paste()
