# corresponds with team_make(), randomize_pkmn(), create_pkmn(), init_static_pkmn_vars(), init_dynamic_pkmn_vars() and any similar functions
# corresponds with pkmnwrapper.py extensively

# ----- IMPORTED PACKAGES -----

# project packages
from helper_functions import *
from pglobals import *
from pkmnwrapper import *

class Pokemon:

	# attributes

	# NOTE: WHEN ADDING A NEW ATTRIBUTE, simply implement the following:
	# 		1 - set/init_<attr> methods - use and check any appropriate parameters (i.e. set_iv(stat_label, val))
	#		2 - get_<attr> methods - use and check any appropriate parameters (i.e. get_iv(stat_label))
	# 		3 - add appropriate check to is_initialized  
	#		4 - (optional for ints) - add max value
	#		4 - (optional) - add to __str()__
	#		5 - (?? later) - add to to_cmd() or w/e will be implemented

	"""
	self.dexnum = dexnum
	self.species_name = ""
	self.nickname = ""
	self.type_names = []
	self.level = level
	self.EV_ATK = 0
	self.EV_DEF = 0
	self.EV_HP = 0
	self.EV_SPA = 0
	self.EV_SPD = 0
	self.EV_SPE = 0
	self.IV_ATK = 0
	self.IV_DEF = 0
	self.IV_HP = 0
	self.IV_SPA = 0
	self.IV_SPD = 0
	self.IV_SPE = 0
	self.friendship = 0
	self.held_item_id = 0
	self.original_trainer_id = 48011
	self.original_trainer_name = "Nate"
	self.gender_id = 0
	self.move1_id = 0
	self.move2_id = 0
	self.move3_id = 0
	self.move4_id = 0
	"""
	# max values of int attributes, used by is_legal_<stat>() functions
	# minimum values are assumed to be 0 or 1, see is_legal_<stat>() functions
	max_dexnum = 251
	max_level = 100
	max_ev = 65535
	max_iv = 15
	max_fv = 255
	max_OT_id = 65535
	max_gender_id = 2
	max_move_id = 251

	# __init__ does nothing
	#TODO: 	as noted in has_dexnum, consider init requiring dexnum... but that'd be inconsistent w/ other stats. 
	#		... but it is also necessary is setting up a pokemon, and determines many things (movesets, evolutions, stats, etc)
	def __init__(self):
		pass		

	# turns this Pokemon into a human readable string
	# this is used in the command line and in output files
	#TODO: ppups and any other additions to props in pkmn dicts from static/dynamic var init functs or elsewhere
	def __str__(self):

		assertd(is_initialized(self))

		out_str = ""

		dexnum = self.dexnum
		pkmn_name = self.species_name
		type_names = self.type_names

		# type_str describes this Pokemon's types, and includes ()'s 
		# it is formatted like:
		#		"(Type1)" 	or 	"(Type1, Type2)"
		# i.e. 	"(Water)"	or 	"(Rock, Ground)"
		if(type_names[1] == "None"):
			type_str = "(" + type_names[0].capitalize() + ")"
		else:
			type_str = "(" + type_names[0].capitalize() + ", " + type_names[1].capitalize() + ")"
	
		# add everything to out_str so far
		out_str += pkmn_name.title() + " [#" + str(dexnum) + "]\t" + type_str + " {"

		# add moves to out_str
		for i in range(1,5):
			move_prefix = "Move" + str(i)
			move_name = pd[move_prefix][1].replace("-"," ").title()
			if i != 4:
				out_str += move_name + ", "
			else:
				out_str += move_name + "}"

		return out_str
	
	# this considered an "init" method not a "set" method because this is not given arguments
	#TODO: use type objects instead of building a list of two strings
	def init_type_names(self):
		assertd(self.has_dexnum())
		dexnum = self.dexnum
		pkmnpy_obj = get_PKMN(dexnum)
		result = get_type_names(pkmnpy_obj)	
		assertd(is_legal_type_names(result))
		self.type_names = result

	# returns True if dexnum has been properly initialized for this object
	#TODO: as noted in init, perhaps just requiring this in init would be best, but that is inconsistent w/ other parameters at the moment
	def has_dexnum(self):
		if not hasattr(self, "dexnum"):
			return False
		dexnum = self.dexnum
		if not is_legal_dexnum(dexnum):
			return False
		return True

	# returns True if this Pokemon object has been fully initialized
	# functions that initialize a Pokemon should use this to check that the object is complete before passing the object to other code
	# an alternative to this design is to force these in __init__()... but I see that possibly involving too many parameters for __init__()
	def is_initialized(self):
		if not self.has_dexnum():
			printd("dexnum caused pokemon is_initialized() to fail.")
			return False
		if not hasattr(self, "type_names") or not is_legal_type_names(self.type_names):
			printd("type_names caused pokemon is_initialized() to fail. " + str(hasattr(self, "type_names")) + " " + str(is_legal_type_names(self.type_names)))
			return False
		if not hasattr(self, "level") or not is_legal_level(self.level):
			printd("level caused pokemon is_initialized() to fail. " + str(hasattr(self, "level")) + " " + str(is_legal_level(self.level)))
			return False
		if not hasattr(self, "EV_ATK") or not is_legal_ev(self.EV_ATK):
			printd("EV_ATK caused pokemon is_initialized() to fail. " + str(hasattr(self, "EV_ATK")) + " " + str(is_legal_ev(self.EV_ATK)))
			return False
		if not hasattr(self, "EV_DEF") or not is_legal_ev(self.EV_DEF):
			printd("EV_DEF caused pokemon is_initialized() to fail. " + str(hasattr(self, "EV_DEF")) + " " + str(is_legal_ev(self.EV_DEF)))
			return False
		if not hasattr(self, "EV_HP") or not is_legal_ev(self.EV_HP):
			printd("EV_HP caused pokemon is_initialized() to fail. " + str(hasattr(self, "EV_HP")) + " " + str(is_legal_ev(self.EV_HP)))
			return False
		if not hasattr(self, "EV_SPA") or not is_legal_ev(self.EV_SPA):
			printd("EV_SPA caused pokemon is_initialized() to fail. " + str(hasattr(self, "EV_SPA")) + " " + str(is_legal_ev(self.EV_SPA)))
			return False
		if not hasattr(self, "EV_SPD") or not is_legal_ev(self.EV_SPD):
			printd("EV_SPD caused pokemon is_initialized() to fail. " + str(hasattr(self, "EV_SPD")) + " " + str(is_legal_ev(self.EV_SPD)))
			return False
		if not hasattr(self, "EV_SPE") or not is_legal_ev(self.EV_SPE):
			printd("EV_SPE caused pokemon is_initialized() to fail. " + str(hasattr(self, "EV_SPE")) + " " + str(is_legal_ev(self.EV_SPE)))
			return False
		if not hasattr(self, "IV_ATK") or not is_legal_iv(self.IV_ATK):
			printd("IV_ATK caused pokemon is_initialized() to fail. " + str(hasattr(self, "IV_ATK")) + " " + str(is_legal_iv(self.IV_ATK)))
			return False
		if not hasattr(self, "IV_DEF") or not is_legal_iv(self.IV_DEF):
			printd("IV_DEF caused pokemon is_initialized() to fail. " + str(hasattr(self, "IV_DEF")) + " " + str(is_legal_iv(self.IV_DEF)))
			return False
		if not hasattr(self, "IV_HP") or not is_legal_iv(self.IV_HP):
			printd("IV_HP caused pokemon is_initialized() to fail. " + str(hasattr(self, "IV_HP")) + " " + str(is_legal_iv(self.IV_HP)))
			return False
		if not hasattr(self, "IV_SPA") or not is_legal_iv(self.IV_SPA):
			printd("IV_SPA caused pokemon is_initialized() to fail. " + str(hasattr(self, "IV_SPA")) + " " + str(is_legal_iv(self.IV_SPA)))
			return False
		if not hasattr(self, "IV_SPD") or not is_legal_iv(self.IV_SPD):
			printd("IV_SPD caused pokemon is_initialized() to fail. " + str(hasattr(self, "IV_SPD")) + " " + str(is_legal_iv(self.IV_SPD)))
			return False
		if not hasattr(self, "IV_SPE") or not is_legal_iv(self.IV_SPE):
			printd("IV_SPE caused pokemon is_initialized() to fail. " + str(hasattr(self, "IV_SPE")) + " " + str(is_legal_iv(self.IV_SPE)))
			return False
		if not hasattr(self, "friendship") or not is_legal_friendship(self.friendship):
			printd("friendship caused pokemon is_initialized() to fail. " + str(hasattr(self, "friendship")) + " " + str(is_legal_friendship(self.friendship)))
			return False
		if not hasattr(self, "held_item_id") or not is_legal_held_item_id(self.held_item_id):
			printd("held_item_id caused pokemon is_initialized() to fail. " + str(hasattr(self, "held_item_id")) + " " + str(is_legal_held_item_id(self.held_item_id)))
			return False
		if not hasattr(self, "original_trainer_id") or not is_legal_OT_id(self.original_trainer_id):
			printd("original_trainer_id caused pokemon is_initialized() to fail. " + str(hasattr(self, "original_trainer_id")) + " " + str(is_legal_OT_id(self.original_trainer_id)))
			return False
		if not hasattr(self, "original_trainer_name") or not is_legal_trainer_name(self.original_trainer_name):
			printd("original_trainer_name caused pokemon is_initialized() to fail. " + str(hasattr(self, "original_trainer_name")) + " " + str(is_legal_trainer_name(self.original_trainer_name)))
			return False
		if not hasattr(self, "gender_id") or not is_legal_gender_id(self.gender_id):
			printd("gender_id caused pokemon is_initialized() to fail. " + str(hasattr(self, "gender_id")) + " " + str(is_legal_gender_id(self.gender_id)))
			return False
		if not hasattr(self, "move1_id") or not is_legal_move_id(self.move1_id):
			printd("move1_id caused pokemon is_initialized() to fail. " + str(hasattr(self, "move1_id")) + " " + str(is_legal_move_id(self.move1_id)))
			return False
		if not hasattr(self, "move2_id") or not is_legal_move_id(self.move2_id):
			printd("move2_id caused pokemon is_initialized() to fail. " + str(hasattr(self, "move2_id")) + " " + str(is_legal_move_id(self.move2_id)))
			return False
		if not hasattr(self, "move3_id") or not is_legal_move_id(self.move3_id):
			printd("move3_id caused pokemon is_initialized() to fail. " + str(hasattr(self, "move3_id")) + " " + str(is_legal_move_id(self.move3_id)))
			return False
		if not hasattr(self, "move4_id") or not is_legal_move_id(self.move4_id):
			printd("move4_id caused pokemon is_initialized() to fail. " + str(hasattr(self, "move4_id")) + " " + str(is_legal_move_id(self.move4_id)))
			return False
		return True

	# sets the dexnum for this pokemon
	# since dexnum is 1:1 with species name and type_names, setting dexnum determines species_name and type_names
	# thus when setting dexnum, we assertd species_name and type_names are both uninitialized
	def set_dexnum(self, dexnum):
		assertd(is_legal_dexnum(dexnum))
		assertd(not hasattr(self, "species_name"))
		assertd(not hasattr(self, "type_names"))
		self.dexnum = dexnum
		self.species_name = get_PKMN_name(dexnum)
		self.init_type_names()

	def set_level(self, l):
		assertd(is_legal_level(l))
		self.level = l

	def set_ev(self, stat_str, ev):
		assertd(is_legal_ev(ev))
		assertd(is_str(stat_str))
		stat_str_formatted = stat_str.replace(' ','').upper()
		assertd(stat_str_formatted != '')
		assertd(stat_str_formatted in stat_labels)
		if stat_str_formatted == 'ATK':
			self.EV_ATK = ev
		elif stat_str_formatted == 'DEF':
			self.EV_DEF = ev
		elif stat_str_formatted == 'HP':
			self.EV_HP = ev
		elif stat_str_formatted == 'SPA':
			self.EV_SPA = ev
		elif stat_str_formatted == 'SPD':
			self.EV_SPD = ev
		elif stat_str_formatted == 'SPE':
			self.EV_SPE = ev
		else:
			assertd(False,"Bad stat_str_formatted to set_ev")

	def set_iv(self, stat_str, iv):
		assertd(is_legal_iv(iv))
		assertd(is_str(stat_str))
		stat_str_formatted = stat_str.replace(' ','').upper()
		assertd(stat_str_formatted != '')
		assertd(stat_str_formatted in stat_labels)
		if stat_str_formatted == 'ATK':
			self.IV_ATK = iv
		elif stat_str_formatted == 'DEF':
			self.IV_DEF = iv
		elif stat_str_formatted == 'HP':
			self.IV_HP = iv
		elif stat_str_formatted == 'SPA':
			self.IV_SPA = iv
		elif stat_str_formatted == 'SPD':
			self.IV_SPD = iv
		elif stat_str_formatted == 'SPE':
			self.IV_SPE = iv
		else:
			assertd(False,"Bad stat_str_formatted to set_iv")

	def set_friendship(self, fv):
		assertd(is_legal_friendship(fv))
		self.friendship = fv

	def set_held_item_id(self, hi_id):
		assertd(is_legal_held_item_id(hi_id))
		self.held_item_id = hi_id

	def set_OT_id(self, OT_id):
		assertd(is_legal_OT_id(OT_id))
		self.original_trainer_id = OT_id

	def set_trainer_name(self, tn):
		assertd(is_legal_trainer_name(tn))
		self.original_trainer_name = tn

	def set_gender_id(self, g_id):
		assertd(is_legal_gender_id(g_id))
		self.gender_id = g_id

	def set_move_id(self, slot_num, m_id):
		assertd(is_legal_move_id(m_id))
		assertd(is_positive_int(slot_num) and slot_num >= 1 and slot_num <= 4)
		if slot_num == 1:
			self.move1_id = m_id
		elif slot_num == 2:
			self.move2_id = m_id
		elif slot_num == 3:
			self.move3_id = m_id
		elif slot_num == 4:
			self.move4_id = m_id
		else:
			assertd(False,"unreached case")

	def get_dexnum(self):
		return self.dexnum

	def get_species_name(self):
		return self.species_name

	def get_type_names(self):
		return self.type_names

	def get_level(self):
		return self.level

	def get_ev(self, stat_str):
		assertd(is_str(stat_str))
		stat_str_formatted = stat_str.replace(' ','').upper()
		assertd(stat_str_formatted != '')
		assertd(stat_str_formatted in stat_labels)
		if stat_str_formatted == 'ATK':
			return self.EV_ATK
		elif stat_str_formatted == 'DEF':
			return self.EV_DEF
		elif stat_str_formatted == 'HP':
			return self.EV_HP
		elif stat_str_formatted == 'SPA':
			return self.EV_SPA
		elif stat_str_formatted == 'SPD':
			return self.EV_SPD
		elif stat_str_formatted == 'SPE':
			return self.EV_SPE
		else:
			assertd(False,"Bad stat_str_formatted to get_ev")

	def get_iv(self, stat_str):
		assertd(is_str(stat_str))
		stat_str_formatted = stat_str.replace(' ','').upper()
		assertd(stat_str_formatted != '')
		assertd(stat_str_formatted in stat_labels)
		if stat_str_formatted == 'ATK':
			return self.IV_ATK
		elif stat_str_formatted == 'DEF':
			return self.IV_DEF
		elif stat_str_formatted == 'HP':
			return self.IV_HP
		elif stat_str_formatted == 'SPA':
			return self.IV_SPA
		elif stat_str_formatted == 'SPD':
			return self.IV_SPD
		elif stat_str_formatted == 'SPE':
			return self.IV_SPE
		else:
			assertd(False,"Bad stat_str_formatted to get_iv")

	def get_friendship(self):
		return self.friendship

	def get_held_item_id(self):
		return self.held_item_id

	def get_OT_id(self):
		return self.OT_id

	def get_trainer_name(self):
		return self.trainer_name

	def get_gender_id(self):
		return self.gender_id

	def get_move_id(self, slot_num):
		assertd(is_int(slot_num) and slot_num >= 1 and slot_num <= 4)
		if slot_num == 1:
			return self.move1_id
		elif slot_num == 2:
			return self.move2_id
		elif slot_num == 3:
			return self.move3_id
		elif slot_num == 4:
			return self.move4_id

# ----- POKEMON LIBRARY BASE FUNCTIONS -----
# akin to class/static level functions

# TODO: perhaps these could be renamed to "is_<thing>" instead of "is_legal_<thing>"?
def is_legal_dexnum(dexnum):
	return is_positive_int(dexnum) and dexnum <= Pokemon.max_dexnum

# (UNUSED)
def is_legal_species_name(sname):
	return is_str(sname) and sname.strip() != ""

def is_legal_type_names(type_names):
	if not is_list(type_names) or len(type_names) != 2:
		return False
	type_name1 = type_names[0]
	type_name2 = type_names[1]
	if not is_str(type_name1):
		return False
	if not is_str(type_name2):
		return False
	type_name1 = type_name1.strip().title()
	type_name2 = type_name2.strip().title()
	if type_name1 == "" or not type_name1 in all_type_names:
		return False
	if type_name2 != "None" and (type_name2 == "" or not type_name2 in all_type_names):
		return False
	return True

def is_legal_level(l):
	return is_positive_int(l) and l <= Pokemon.max_level

def is_legal_ev(ev):
	return is_int(ev) and ev >= 0 and ev <= Pokemon.max_ev

def is_legal_iv(iv):
	return is_int(iv) and iv >= 0 and iv <= Pokemon.max_iv

# lol @ this method name... "does my friendship hold up in court"
# could rename "friendship" to "fv" for friendship value
def is_legal_friendship(fv):
	return is_int(fv) and fv >= 0 and fv <= Pokemon.max_fv

# TODO: implement max range
def is_legal_held_item_id(hi_id):
	return is_int(hi_id) and hi_id >= 0

def is_legal_OT_id(OT_id):
	return is_int(OT_id) and OT_id >= 0 and OT_id <= Pokemon.max_OT_id

# TODO: ... what other requirements might there be on a trainer name?
def is_legal_trainer_name(tn):
	return is_str(tn)

def is_legal_gender_id(g_id):
	return is_int(g_id) and g_id >= 0 and g_id <= Pokemon.max_gender_id

def is_legal_move_id(m_id):
	return is_positive_int(m_id) and m_id <= Pokemon.max_move_id

