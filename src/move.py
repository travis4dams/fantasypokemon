# corresponds with pkpywrapper.py extensively

# ----- IMPORTED PACKAGES -----

# project packages
from helper_functions import *
from pglobals import *
from pkpywrapper import *
import pokemon
#from pokemon import is_legal_type_name

import beckett.exceptions
import sys

class Move:

	# attributes

	# NOTE: see Pokemon for suggestions on how to add new attributes in accordance with this project's OOP design

	"""
	self.id = -1
	self.name = None
	self.type_str = None
	self.is_banned = False
	"""

	# min/max values for id
	min_move_id = 1
	max_move_id = 251

	# use an intenger move id to index into this list for the move object associated with it
	# used by __init__ to save loading time if we already initialized this move later
	# this solution relies on the assumption that any two moves of the same id will be equal, and don't differ in runtime properties
	move_cache = [None]*251
	move_cache_hits = 0

	# __init__ takes int move_id and str name from __new__
	# input is checked via __new__
	def __init__(self, move_id):

		funct_name = "move __init__"

		start_timer(funct_name)

		#print("in init")

		# fetch related pokepy_move_obj
		pokepy_move_obj = get_pkpy_move(move_id)

		# we reference ruleset object to determine if this is banned
		global rs

		# fetch attrs
		#move_id = int(pokepy_move_obj.id)
		name = pokepy_move_obj.name.title().replace('-', ' ')

		# manual exception handling
		# manually referenced hyphenated_moves in pglobals.py for this... perhaps these should be synchronized
		manual_exceptions = ["Double Edge", "Mud Slap", "Lock On", "Mud Slap", "Self Destruct", "Soft Boiled"]
		if name in manual_exceptions:
			name = name.replace(' ','-')

		type_str = get_pokepy_move_type_name(pokepy_move_obj)
		
		# ensure attrs from pokepy_move_obj are correct
		# is_legal_move_id check is technically a redundant that of __new__
		assertd(is_legal_move_id(move_id))
		assertd(is_legal_move_name(name))
		assertd(pokemon.is_legal_type_name(type_str))

		# set attrs
		self.id = move_id
		self.name = name
		self.type_str = type_str
		self.banned = move_id in rs.banned_moves_dict # fetch banned attr after checking that move_id attr is legit

		# add to cache
		Move.move_cache[move_id-1] = self

		end_timer(funct_name)

	# return a cached instance instead of a new instance when possible
	def __new__(cls, move_identifier):

		funct_name = "move __new__"

		start_timer(funct_name)

		#printd("in new")

		# input check
		input_is_valid_int = False
		input_is_valid_str = False
		if is_int(move_identifier):
			input_is_valid_int = is_legal_move_id(move_identifier)
		elif is_str(move_identifier):
			input_is_valid_str = is_legal_move_name(move_identifier)
		else: 
			raise ValueError("Improper type to move.__new__(): " + str(type(move_identifier) + " " + str(move_identifier)))		
		assertd(input_is_valid_int or input_is_valid_str)

		# setup move_id and name based on input
		# is_legal_move_name and is_legal_move_id checks that move_identifier is valid, so accessing pkpywrapper dict is fine
		if input_is_valid_int:
			move_id = move_identifier
			#name = move_id_to_name_dict[move_identifier]
		else:			
			move_id = move_name_to_id_dict[move_identifier]
			name = move_identifier

		# attempt a cache load if possible
		if Move.move_cache[move_id-1] != None:
			# hit/success
			#printd("move cache hit: " + str(move_id-1))			
			instance = Move.move_cache[move_id-1]			
			Move.move_cache_hits += 1
			end_timer(funct_name)
			return instance

		# cache fail - just init a new object
		# https://howto.lintel.in/python-__new__-magic-method-explained/
		#printd("move cache fail: " + str(move_id-1))
		instance = super(Move, cls).__new__(cls)
		instance.__init__(move_id)		 

		end_timer(funct_name)

		return instance 

	# turns this Move into a human readable string
	def __str__(self):
		return self.name + " [" + str(self.id) + "] (" + str(self.type_str) + ")"

	# two moves are equal if they share same id
	def __eq__(self, other):

		# check same type
		if not is_same_type(self, other):
			return False

		return self.id == other.id

		"""
		# check same set of attributes (attributes of all objects can be added dynamically in python)
		self_attr_names = dir(self)
		other_attr_names = dir(other)
		if set(self_attr_names) != set(other_attr_names):
			return False


		# check same attribute values
		try:

			for attr_name in self_attr_names:

				#printd(attr_name)

				# overlook these values otherwise we get a recursion error
				if attr_name.startswith("__") and attr_name.endswith("__"):
					continue

				x = getattr(self, attr_name)
				y = getattr(other, attr_name)

				if callable(x) or callable(y):
					continue

				if x != y:
					return False

		except RuntimeError:
			printd(attr_name)
			printd("RuntimeError, likely due to stack recursion depth being exceeded.")
			sys.exit()
		"""

		# passed
		return True

	def __hash__(self):
		return hash(self.id)

	def get_id(self):
		return self.id

	def get_name(self):
		return self.name

	def get_type_str(self):
		return self.type_str

	def is_banned(self):
		return self.banned

# ----- MOVE LIBRARY BASE FUNCTIONS -----
# akin to class/static level functions

# we can assume 
# should we perhaps change this to check each attribute, in case they've been changed to an illegal value during runtime?
def is_legal_move(m):
	return isinstance(m, Move)

# TODO: double check cases using is_legal_move_id are just handling move_id... if they have a move_obj they should use is_legal_move
def is_legal_move_id(m_id):
	return is_int(m_id) and m_id >= Move.min_move_id and m_id <= Move.max_move_id

# TODO: implement better way to check than fetching pokepy_move_obj (i.e. check if mn actual set of gen 2 names)... 
# 		tho actually this current implement may be faster despite being a "less elegant" solution
def is_legal_move_name(mn):
	return mn in move_name_to_id_dict
	"""
	result = mn in move_name_to_id_dict
	if not result:
		printd(move_name_to_id_dict)
		printd(mn)
		printd(type(mn))
	return result
	"""
	"""
	try:
		pokepy_move_obj = get_pkpy_move(mn)
	except beckett.exceptions.InvalidStatusCodeError as ex:
		return False
	if pokepy_move_obj == None: #TODO: check that this is a pokepy move obj, instead of just seeing that it isn't None
		return False
	return True
	"""
