# corresponds with team_make(), randomize_pkmn(), create_pkmn(), init_static_pkmn_vars(), init_dynamic_pkmn_vars() and any similar functions
# corresponds with pkpywrapper.py extensively

#TODO: perhaps a "Pokemon_Species" class should be created, which contains info about a Pokemon's species, contrasted with an individual's info
#		but i worry we are just reinventing the pokepy API too much... but it might be useful to have our own functionality and such.

# ----- IMPORTED PACKAGES -----

# project packages
from helper_functions import *
from pglobals import *
from pkpywrapper import *
import move as move_class
from timing import *
#from move import Move, is_legal_move_id

secondary_characters = ["-","?","!","/",".",",","(",")",":","[", " "]

class Pokemon:

	# attributes

	# NOTE: WHEN ADDING A NEW ATTRIBUTE, implement the following (some optional):
	# 		1 - set/init_<attr> methods - use and check any appropriate parameters (i.e. set_iv(stat_label, val)). 
	#									  also consider if it should be initialized along w/ dexnum	
	#		2 - get_<attr> methods - use and check any appropriate parameters (i.e. get_iv(stat_label)) 
	#		3 - is_legal_<attr> methods 					
	# 		4 - add appropriate check to is_initialized  			
	#		5 - (optional for ints) - add max value				
	#		6 - (optional) - add to __str__()				
	#		7 - (?? later) - add to to_cmd() or w/e will be implemented	
	#		8 - (necessary for some attrs) - add to __eq__()

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
	self.OT_id = 48011
	self.OT_name = "Nate"
	self.gender_id = 0
	self.move1 = None
	self.move2 = None
	self.move3 = None
	self.move4 = None
	"""
	# max values of int attributes, used by is_legal_<stat>() functions
	# minimum values are assumed to be 0 or 1, see is_legal_<stat>() functions
	max_dexnum = 251
	max_level = 100
	max_ev = 65535
	max_iv = 15
	max_fv = 255
	max_OT_id = 65535
	max_hi_id = 254
	max_gender_id = 2
	max_nickname_length = 10 # this is generation dependent

	# __init__ does nothing
	#TODO: 	as noted in has_dexnum, consider init requiring dexnum... but that'd be inconsistent w/ other stats. 
	#		... but it is also necessary is setting up a pokemon, and determines many things (movesets, evolutions, stats, etc)
	def __init__(self):
		pass		

	# turns this Pokemon into a human readable string
	# this is used in the command line and in output files
	# TODO: ppups and any other additions to props in pkmn dicts from static/dynamic var init functs or elsewhere
	# TODO: i think this function would do well to work w/ the to_cmd() method for a Pokemon object
	#		some of this functionality seems shared so it'd probably be best to standardize it in one place
	def __str__(self):

		timer_function_name = "Pokemon __str__"

		start_timer(timer_function_name)

		assertd(self.is_initialized())

		out_str = ""

		dexnum = self.dexnum
		nickname = self.nickname
		species_name = self.species_name
		type_names = self.type_names

		# type_str describes this Pokemon's types, and includes ()'s 
		# it is formatted like:
		#		"(Type1)" 	or 	"(Type1, Type2)"
		# i.e. 	"(Water)"	or 	"(Rock, Ground)"
		if(len(type_names) < 2):
			type_str = "(" + type_names[0].capitalize() + ")"
		else:
			type_str = "(" + type_names[0].capitalize() + ", " + type_names[1].capitalize() + ")"
	
		# add everything to out_str so far
		out_str += species_name.title() + " \"" + str(nickname) + "\" [#" + str(dexnum) + "]\t" + type_str + " {"

		# add moves to out_str
		# TODO: perhaps this should use self.get_moves() ??
		for i in range(1,5):
			move_prefix = "Move" + str(i)
			m = self.get_move(i)
			move_name = m.get_name()
			move_name_formatted = move_name.replace("-"," ").title()
			if i != 4:
				out_str += move_name_formatted + ", "
			else:
				out_str += move_name_formatted + "}"

		end_timer(timer_function_name)

		return out_str

	# https://stackoverflow.com/questions/30682791/python-asking-if-two-objects-are-the-same-class
	# https://stackoverflow.com/questions/2559083/python-check-if-object-is-in-list-of-objects
	# https://stackoverflow.com/questions/11637293/iterate-over-object-attributes-in-python
	# https://stackoverflow.com/questions/9623114/check-if-two-unordered-lists-are-equal
	# https://stackoverflow.com/questions/9089400/set-in-operator-uses-equality-or-identity
	# a seemingly universal function to check if two objects have the same class, attributes and values
	def __eq__(self, other):

		timer_function_name = "Pokemon __eq__"

		start_timer(timer_function_name)

		# check same type
		if not type(self) is type(other):
			return False

		# check same set of attributes (attributes of all objects can be added dynamically in python)
		self_attr_names = dir(self)
		other_attr_names = dir(other)
		if set(self_attr_names) != set(other_attr_names):
			return False

		# check same attribute values
		try:

			for attr_name in self_attr_names:

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

		end_timer(timer_function_name)

		# passed
		return True

	# takes the pokemon dict output by randomize_PKMN and turns it into an exeuctable PkHex cmd
	# TODO: i think this function would do well to work w/ the str() method for a Pokemon object
	#		some of this functionality seems shared so it'd probably be best to standardize it in one place
	def to_cmd(self, slot_num):
		start_timer()
		dexnum = self.get_dexnum()
		species_name = self.get_species_name()
		nickname = self.get_nickname()
		out_str = "=Box=1"
		out_str += "\n=Slot=" + str(slot_num)
		out_str += "\n.Species=" + str(dexnum)
		out_str += "\n.Nickname=" + str(nickname)
		out_str += "\n.CurrentLevel=" + str(self.get_level())
		for stat in stat_labels:
			out_str += "\n.EV_" + stat + "=" + str(self.get_ev(stat))
		for stat in stat_labels:
			out_str += "\n.IV_" + stat + "=" + str(self.get_iv(stat))
		out_str += "\n.CurrentFriendship=" + str(self.get_friendship())
		out_str += "\n.HeldItem=" + str(self.get_held_item_id())
		out_str += "\n.TID=" + str(self.get_OT_id())
		out_str += "\n.OT_Name=" + str(self.get_OT_name()) # it should already be a string but oh well
		for i in range(1,5):
			move_prefix = "Move" + str(i)
			out_str += "\n." + move_prefix + "=" + str(self.get_move(i).get_id())
		out_str += "\n.Gender=" + str(self.get_gender_id())
		end_timer()
		return out_str
		#TODO: ppups and any other additions to props in pkmn dicts from static/dynamic var init functs or elsewhere

	# returns True if this Pokemon object has been fully initialized
	# functions that initialize a Pokemon should use this to check that the object is complete before passing the object to other code
	# an alternative to this design is to force these in __init__()... but I see that possibly involving too many parameters for __init__()
	def is_initialized(self):
		start_timer()
		if not self.has_dexnum():
			assertd(False,"dexnum caused pokemon is_initialized() to fail.")
			return False
		if not hasattr(self, "type_names") or not is_legal_type_names(self.type_names):
			assertd(False,"type_names caused pokemon is_initialized() to fail.")
			return False
		if not hasattr(self, "level") or not is_legal_level(self.level):
			assertd(False,"level caused pokemon is_initialized() to fail.")
			return False
		if not hasattr(self, "EV_ATK") or not is_legal_ev(self.EV_ATK):
			assertd(False,"EV_ATK caused pokemon is_initialized() to fail.")
			return False
		if not hasattr(self, "EV_DEF") or not is_legal_ev(self.EV_DEF):
			assertd(False,"EV_DEF caused pokemon is_initialized() to fail.")
			return False
		if not hasattr(self, "EV_HP") or not is_legal_ev(self.EV_HP):
			assertd(False,"EV_HP caused pokemon is_initialized() to fail.")
			return False
		if not hasattr(self, "EV_SPA") or not is_legal_ev(self.EV_SPA):
			assertd(False,"EV_SPA caused pokemon is_initialized() to fail.")
			return False
		if not hasattr(self, "EV_SPD") or not is_legal_ev(self.EV_SPD):
			assertd(False,"EV_SPD caused pokemon is_initialized() to fail.")
			return False
		if not hasattr(self, "EV_SPE") or not is_legal_ev(self.EV_SPE):
			assertd(False,"EV_SPE caused pokemon is_initialized() to fail.")
			return False
		if not hasattr(self, "IV_ATK") or not is_legal_iv(self.IV_ATK):
			assertd(False,"IV_ATK caused pokemon is_initialized() to fail.")
			return False
		if not hasattr(self, "IV_DEF") or not is_legal_iv(self.IV_DEF):
			assertd(False,"IV_DEF caused pokemon is_initialized() to fail.")
			return False
		if not hasattr(self, "IV_HP") or not is_legal_iv(self.IV_HP):
			assertd(False,"IV_HP caused pokemon is_initialized() to fail.")
			return False
		if not hasattr(self, "IV_SPA") or not is_legal_iv(self.IV_SPA):
			assertd(False,"IV_SPA caused pokemon is_initialized() to fail.")
			return False
		if not hasattr(self, "IV_SPD") or not is_legal_iv(self.IV_SPD):
			assertd(False,"IV_SPD caused pokemon is_initialized() to fail.")
			return False
		if not hasattr(self, "IV_SPE") or not is_legal_iv(self.IV_SPE):
			assertd(False,"IV_SPE caused pokemon is_initialized() to fail.")
			return False
		if not hasattr(self, "friendship") or not is_legal_friendship(self.friendship):
			assertd(False,"friendship caused pokemon is_initialized() to fail.")
			return False
		if not hasattr(self, "held_item_id") or not is_legal_held_item_id(self.held_item_id):
			assertd(False,"held_item_id caused pokemon is_initialized() to fail.")
			return False
		if not hasattr(self, "OT_id") or not is_legal_OT_id(self.OT_id):
			assertd(False,"OT_id caused pokemon is_initialized() to fail.")
			return False
		if not hasattr(self, "OT_name") or not is_legal_OT_name(self.OT_name):
			assertd(False,"OT_name caused pokemon is_initialized() to fail.")
			return False
		if not hasattr(self, "gender_id") or not is_legal_gender_id(self.gender_id):
			assertd(False,"gender_id caused pokemon is_initialized() to fail.")
			return False
		if not hasattr(self, "move1") or not move_class.is_legal_move(self.move1):
			assertd(False,"move1 caused pokemon is_initialized() to fail.")
			return False
		if not hasattr(self, "move2") or not move_class.is_legal_move(self.move2):
			assertd(False,"move2 caused pokemon is_initialized() to fail.")
			return False
		if not hasattr(self, "move3") or not move_class.is_legal_move(self.move3):
			assertd(False,"move3 caused pokemon is_initialized() to fail.")
			return False
		if not hasattr(self, "move4") or not move_class.is_legal_move(self.move4):
			assertd(False,"move4 caused pokemon is_initialized() to fail.")
			return False
		if not hasattr(self, "nickname") or not is_legal_nickname(self.nickname):
			assertd(False,"nickname caused pokemon is_initialized() to fail.")
			return False
		end_timer()
		return True

	# sets the dexnum for this pokemon
	# since dexnum is 1:1 with species name and type_names, setting dexnum determines species_name and type_names
	# thus when setting dexnum, we assertd species_name and type_names are both uninitialized
	def set_dexnum(self, dexnum):
		start_timer()
		assertd(is_legal_dexnum(dexnum),str(dexnum))
		assertd(not hasattr(self, "species_name"))
		assertd(not hasattr(self, "type_names"))
		self.dexnum = dexnum
		self.species_name = get_PKMN_name(dexnum).title()
		self.set_nickname(self.species_name) # initially set nickname to default value (species name), though it may be overriden later
		self.init_type_names()
		end_timer()

	# returns True if dexnum has been properly initialized for this object
	#TODO: as noted in init, perhaps just requiring this in init would be best, but that is inconsistent w/ other parameters at the moment
	def has_dexnum(self):
		start_timer()
		if not hasattr(self, "dexnum"):
			return False
		dexnum = self.dexnum
		if not is_legal_dexnum(dexnum):
			return False
		end_timer()	
		return True

	# this considered an "init" method not a "set" method because this is not given arguments
	#TODO: use type objects instead of building a list of two strings
	def init_type_names(self):
		start_timer()
		assertd(self.has_dexnum())
		dexnum = self.dexnum
		pkmnpy_obj = get_PKMN(dexnum)
		result = extract_type_names(pkmnpy_obj)	
		assertd(is_legal_type_names(result))
		self.type_names = result
		end_timer()

	def set_level(self, l):
		start_timer()
		assertd(is_legal_level(l))
		self.level = l
		end_timer()

	def set_ev(self, stat_str, ev):
		start_timer()
		assertd(is_legal_ev(ev))
		assertd(is_str(stat_str))
		stat_str_formatted = format_stat_str(stat_str)
		assertd(is_legal_stat_str(stat_str_formatted))
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
		end_timer()

	def set_iv(self, stat_str, iv):
		start_timer()
		assertd(is_legal_iv(iv))
		assertd(is_str(stat_str))
		stat_str_formatted = format_stat_str(stat_str)
		assertd(is_legal_stat_str(stat_str_formatted))
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
		end_timer()

	def set_friendship(self, fv):
		assertd(is_legal_friendship(fv))
		self.friendship = fv

	def set_held_item_id(self, hi_id):
		assertd(is_legal_held_item_id(hi_id))
		self.held_item_id = hi_id

	def set_OT_id(self, OT_id):
		assertd(is_legal_OT_id(OT_id))
		self.OT_id = OT_id

	def set_OT_name(self, tn):
		assertd(is_legal_OT_name(tn))
		self.OT_name = tn

	def set_gender_id(self, g_id):
		assertd(is_legal_gender_id(g_id))
		self.gender_id = g_id

	def set_move(self, slot_num, m):
		start_timer()
		assertd(move_class.is_legal_move(m))
		assertd(is_positive_int(slot_num) and slot_num >= 1 and slot_num <= 4)
		if slot_num == 1:
			self.move1 = m
		elif slot_num == 2:
			self.move2 = m
		elif slot_num == 3:
			self.move3 = m
		elif slot_num == 4:
			self.move4 = m
		else:
			assertd(False,"unreached case")
		end_timer()

	# NOTE: allow this function to override an existing nickname... in other words dont assume nickname is uninitialized when this is called
	def set_nickname(self, nickname):
		assertd(is_legal_nickname(nickname))
		self.nickname = nickname

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
		stat_str_formatted = format_stat_str(stat_str)
		assertd(is_legal_stat_str(stat_str_formatted))
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
		stat_str_formatted = format_stat_str(stat_str)
		assertd(is_legal_stat_str(stat_str_formatted))
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

	def get_OT_name(self):
		return self.OT_name

	def get_gender_id(self):
		return self.gender_id

	def get_move(self, slot_num):
		assertd(is_int(slot_num) and slot_num >= 1 and slot_num <= 4)
		if slot_num == 1:
			return self.move1
		elif slot_num == 2:
			return self.move2
		elif slot_num == 3:
			return self.move3
		elif slot_num == 4:
			return self.move4

	def get_moves(self):
		return [self.move1, self.move2, self.move3, self.move4]

	def get_nickname(self):
		return self.nickname

	# input:
	# include_prior_evos - a boolean indicating whether 
	# output:
	# a tuple containing four lists:
	# 1 - "learnable moves" 
	# 			a list of move objects learnable by this pkmn
	# 2 - "legal moves" 
	# 			a list of move objects learnable by this pkmn and are ruleset compliant
	# 3 - "legal type 1 moves" 
	# 			a list of move objects learnable by this pkmn and are ruleset compliant and are of the pokemon's first type
	# 4 - "legal type 2 moves" 
	# 			a list of move objects learnable by this pkmn and are ruleset compliant and are of the pokemon's second type (list is empty if monotype)
	#TODO: proper input handling
	#TODO: which moves SHOULD be allowed for a pokemon? i.e. there are some moves a pkmn can only learn from gen 1, BUT there are also egg moves... cant have both right?
	#	   .... what about event moves? serebii does not list these.
	#TODO: rename to "get_learnable_moves" or stadium moves or smt
	#TODO: some bug in here related to mantine and not having any moves when output from get_learnable_moves
	def get_learnable_moves(self, include_prior_evos = True, ignore_set = set()):

		start_timer()

		pokepy_obj = get_PKMN(self.dexnum)

		global rs
		
		assertd(include_prior_evos == None or isinstance(include_prior_evos, bool),
			"Bad input to get_learnable_moves(); include_prior_evos is not a bool. Type: " + get_class_name(include_prior_evos) + " str: " + str(include_prior_evos))

		# (not implemented) - load from move cache
		# move cache is handled by get_move_id in pkpywrapper.py
		"""
		dexnum = self.dexnum
		if(dexnum in pkmn_move_cache):
			printd("move cache hit")
			result = pkmn_move_cache[dexnum][1]
			end_timer()
			return result
		"""

		# types of this pokemon, i.e. ["Water"] or ["Rock", "Ground"]
		pkmn_type_names = self.get_type_names()
		is_monotype = len(pkmn_type_names) == 1

		# return values
		# we initialize the lists to a size of 251 items so we can index into it directly by move_id
		# that way we dont have to use "if m in list", we can do "if learnable_moves[i] ! = None", making that search O(1) instead of O(N)
		# make sure to use move_id-1 to index into list; move_ids go from 1 to 251, indices from 0 to 250
		learnable_moves = set()
		legal_moves = set()
		legal_type1_moves = set()
		legal_type2_moves = set()
		"""
		learnable_moves = [None]*move_class.Move.max_move_id
		legal_moves = [None]*move_class.Move.max_move_id
		legal_type1_moves = [None]*move_class.Move.max_move_id
		legal_type2_moves = [None]*move_class.Move.max_move_id
		"""

		# fetch moves from pokepy pokemon's moves attributes
		for pokepy_move in pokepy_obj.moves:

			assertd(is_pokepy_move(pokepy_move),
				"Bad move in pkmn moves in get_learnable_moves(); move isn't a move object. Type: " + get_class_name(pokepy_move) + " str: " + str(pokepy_move))

			# TODO: we need to check not only that the move was ADDED in gen 1 or gen 2 (i.e. 1 <= move_id <= 251)
			#		you also need to check if this pokemon could learn this move DURING gen 1 or gen 2
			#		for example marowak got an ice form in like gen 7 or w/e, so even though blizzard EXISTED in gen 1 (id < 251),
			#		marowak couldn't learn it
			#		so i need to use my old code logic of checking "user version" here

			# only accept moves that were learnable in gen 1 or gen 2
			move_id = int(get_move_id(pokepy_move))
			if not move_class.is_legal_move_id(move_id):
				continue
		
			# replace move_id with the id of a superior move, if one exists
			if move_id in rs.inferior_moves_dict:
				superior_move_id = int(rs.inferior_moves_dict[move_id][1])
				assertd(move_class.is_legal_move_id(superior_move_id))
				move_id = superior_move_id

			# reject Fairy type moves
			move_type = get_pokepy_move_type_name(pokepy_move)
			if move_type == 'fairy':
				continue

			# create move_obj
			m = move_class.Move(move_id)

			# used so that recursive calls to this function don't waste time generating moves its parent pokemon already knows
			"""
			if m in ignore_set:
				continue
			"""

			# add move to the respective sets
			
			# we dont NEED to check if the move is excluded from the set before adding it,
			# BUT doing so may save us some calculation
			# we assume being in learnable_moves means it has been checked in the other sets too
			# ... as it is currently implemented, learnable_moves is a set, so adding it will do nothing if already present
			# ... so we don't need this check
			"""
			if m in learnable_moves:
				continue
			"""

			# add to learnable moves regardless of "legality"
			learnable_moves.add(m)

			# moves that are banned are obviously "illegal"
			if(m.is_banned()):
				continue

			# the move is legal - add to legal_moves and type moves
			legal_moves.add(m)

			# update learnable type1/type2 move sets if the move type matches one of pokemon's type
			mtype_name = m.get_type_str()
			if mtype_name == pkmn_type_names[0]:
				legal_type1_moves.add(m)
			elif not is_monotype and mtype_name == pkmn_type_names[1]:
				legal_type2_moves.add(m)

		# if include_prior_evos, then also include moves learnable by pokemon earlier up in the evolution path by a recursive call
		#TODO: does this cause a pokemon to add its own learnable moves?
		if include_prior_evos == True:

			evo_path = self.get_evolution_path()

			for evo_pkmn in evo_path:	

				# exit condition - no further evolutions (??)
				if(evo_pkmn == None):
					continue	

				# recursive call
				# note that evo_pkmn is a Pokemon object that is not fully initialized (only has a set dexnum)				
				# pass learnable_moves as ignore_set to get_learnable_moves if desired
				(evo_learnable_moves, evo_legal_moves, evo_legal_type1_moves, 
					evo_legal_type2_moves) = evo_pkmn.get_learnable_moves(False)


				# at this point, any moves in ANY of these sets should be those not already learnable by this pokemon
				# (through its own learnset, or from already processed prior evolutions)

				# all moves learnable by prior evolutions are learnable by this pokemon
				for move in evo_learnable_moves:

					# as it is currently implemented, ignore_set will only be a non-empty set when include_prior_evos == False
					# so this case shouldnt be reached
					"""
					if move in ignore_set:
						continue
					"""

					learnable_moves.add(move)

				# all legal learnable moves from prior evolutions are learnable by this pokemon
				for move in evo_legal_moves:
					legal_moves.add(move)

				# update type1 move set
				for move in evo_legal_type1_moves:
					mtype_name = m.get_type_str()
					if mtype_name == pkmn_type_names[0]:
						legal_type1_moves.add(m)
					elif not is_monotype and mtype_name == pkmn_type_names[1]:
						legal_type2_moves.add(m)

				# update type2 move set
				for move in evo_legal_type2_moves:
					mtype_name = m.get_type_str()
					if mtype_name == pkmn_type_names[0]:
						legal_type1_moves.add(m)
					elif not is_monotype and mtype_name == pkmn_type_names[1]:
						legal_type2_moves.add(m)					

		"""
		new_learnable_moves = []
		new_legal_moves = []
		new_legal_type1_moves = []
		new_legal_type2_moves = []
		# TODO: assert list lengths the same... perhaps can assert things like, if we got a type move at this position,
		# 		there should also be one in learnable moves... etc
		# trim the output lists by deleting default (0) move ids
		for i in range(len(learnable_moves)):
			if learnable_moves[i] != None:
				new_learnable_moves.append(learnable_moves[i])
			if legal_moves[i] != None:
				new_legal_moves.append(legal_moves[i])
			if legal_type1_moves[i] != None:
				new_legal_type1_moves.append(legal_type1_moves[i])
			if legal_type2_moves[i] != None:
				new_legal_type2_moves.append(legal_type2_moves[i])
		learnable_moves = new_learnable_moves
		legal_moves = new_legal_moves
		legal_type1_moves = new_legal_type1_moves
		legal_type2_moves = new_legal_type2_moves
		"""

		#TODO: we dont want this assert here b/c with gen restrictions a pokemon may have no learnable moves 
		# 	   (i.e. retrieving wobbuffets moveset retrieves wynauts which has only gen 3 moves or smt)
		#TODO: perhaps do something if gen excludes that pkmn dont fetch its moves or smt idk
		"""
		assertd(is_list(moves) and len(moves)>0,
			"Bad output from get_learnable_moves. Type: " + get_class_name(moves) + " str: " + str(moves) + " len: " + str(len(moves)))
		"""

		end_timer()

		return (learnable_moves, legal_moves, legal_type1_moves, legal_type2_moves)

	# get_legal_learnable_moves is like get_learnable_moves(), except that it essentially removes illegal moves...
	# does not allow duplicates

	# .................................................................................................................
	#  this function really needs to be redesigned. get_legal_moves above checks the ruleset, is that not what "legal" means?
	#  it feels redundnat with get_learnable_moves. this and presumably several other functions should be more compactly organized in OOP design.
	#  i believe this function may also be trying to give THE 4 selected moves, rather than what the name implies: all legal and learnable moves.
	# .................................................................................................................

	#TODO: we may just want to wrap the "legality" checks into get_learnable_moves()
	#	   unless there is some point we want even those learnable moves which don't comply with the rulesets
	# TODO: enforce_ruleset not working. 
	# 		currently we ALWAYS attempt to make their first move a type 1 move (if they can), 
	#		and we ALWAYS attempt to make their second move a type 2 move (if they can)
	def get_random_moveset(self, enforce_ruleset = True):

		start_timer()

		# retrieve ALL possible learnable moves, including those from prior evolutions hence True parameter
		(learnable_moves, legal_moves, legal_type1_moves, legal_type2_moves) = self.get_learnable_moves(True)

		# move_type_names is a list (effectively functions as set tho) of types that have at least 1 move associated with them in this moveset
		# note that len of move_type_names doesnt need to be the same as other lists, since it is just the set of types used across all moves, not a type for each move
		# this is used to check whether or not the Pokemon can meet the type restriction
		#TODO: this would more properly be a set i believe
		#TODO: could potentailly quit a little earleir if you have like 3 moves generated and you need fire and flying moves but none of your moves are fire/flying you might as well restart the moveset
		#TODO: rename to learnable_move_type_names
		move_type_names = []

		# types of this pokemon, i.e. ["Water"] or ["Rock", "Ground"]
		pkmn_type_names = self.get_type_names()
		is_monotype = len(pkmn_type_names) == 1

		# ruleset
		global rs
		
		#TODO: should "get_move_names()" be called here instead?

		# ensure we have enough moves to work with before continuing
		if len(legal_moves) < 4:
			print("get_legal_learnable_moves() failed, not enough moves")
			return

		# if we don't need to enforce the type restriction, add what we've got and move on
		if(not enforce_ruleset):
			# enforce default case of generate_moves by giving no type list, so they just generate random moves
			# TODO: once "ruleset" is more properly defined in OOP, this should be much cleaner
			generated_moves = self.generate_moves(legal_moves, [], [])
			for i in range(len(generated_moves)):
				self.set_move(i+1, generated_moves[i])
			return
		
		# beyond this point, enforce_ruleset == True, so enforce the type restriction

		# check that our ruleset condition of "have at least one move of each of its types" is even feasible for this pokemon
		# if not, enforce no type restrictions on the moveset (banned moves and other restrictions (such as...??) may still apply)
		# NOTE: we want to make this type restriction check AFTER the learnable moveset has been filtered down to the pool of moves we actually use
		# we wouldn't want to check this before removing banned moves, pass the check and assume its feasible, then its not after banned removals...
		#TODO: change it to requiring as many types as it CAN satisfy (<-- ... I think this comment is no longer applicable...?)
		#TODO: change "moves" and similar lists to learnable moves ... rename vars
		"""
		if len(legal_type1_moves) == 0 or len(legal_type2_moves):
			type_restriction = False
		else: 
			type_restriction = True
		"""

		# successful_moves tracks whether our current moveset meets ruleset requirements 
		successful_moves = False

		# number of times we've attempted to generate a moveset for this pokemon (used for debugging)
		moveset_attempts = 0

		generated_moves = self.generate_moves(legal_moves, legal_type1_moves, legal_type2_moves)

		"""
		# build and keep rerandoming a moveset until it meets ruleset requirements
		while not successful_moves:

			# attempt to generate some moves
			#TODO: should this first paramter be "illegal" (disallowed) rather than legal_moves...? 
			generated_moves = self.generate_moves(legal_learnable_moves, type1_moves, type2_moves)

			# check that at least 1 move from each of the pokemon's types are here
			#TODO: have generate_moves return list of type names instead of essentially rebuilding it here
			generated_move_type_names = []
			for i in range(len(generated_moves)):
				generated_move = generated_moves[i]
				move_type_name = generated_move.get_type_str()
				generated_move_type_names.append(move_type_name)
			
			# check types
			if type_restriction:
				if pkmn_type_names[0] in generated_move_type_names and (is_monotype or pkmn_type_names[1] in generated_move_type_names):
					successful_moves = True
			else:
				successful_moves = True

			moveset_attempts += 1
		"""

		end_timer()

		return generated_moves

	# helper function to generate a set of 4 moves
	# allowed_move_set - set of moves that we select from
	# type1_moves - set of moves that are of the pokemon's first type (length may be 0)
	# type2_moves - set of moves that are of the pokemon's second type (length may be 0)
	# this may be called repeatedly (outside this function, not recursively) until the move set meets the ruleset requirements
	def generate_moves(self, allowed_move_set, type1_moves, type2_moves):

		start_timer()

		# generated_move represents the moves we have currently generated
		# names contains string names, ids contains ids (as with move lists above)
		generated_moves = []

		# move_slot represents the index into generated_moves we are CURRENTLY trying to build
		# thus, it also represents the # of successfully generated moves
		move_slot = 0

		# convert sets into lists so we can index into them
		allowed_move_list = list(allowed_move_set) 
		type1_moves_list = list(type1_moves)
		type2_moves_list = list(type2_moves)

		#TODO: this algorithm sucks... could check that the type requirement is even "meetable" in this area, i had that on todo list
		#TODO: could update the moves set so the RNG gets an updated length and cant generate bad #s? idk
		while len(generated_moves) < 4:

			#TODO: if we tried generating a move on THiS "i", store it in attempted_move_names
			#NOTE: the copy call is important, or else changes to attempted_move_names will be made to used_move_names and vice versa (pointers!)

			# attempted_moves contains the moves we have attempted for THIS slot
			# if we have tried the move for an earlier slot though (thus in generated_moves), we shouldn't attempt it again
			attempted_moves = generated_moves.copy()

			# select first move among learnable type1 moves (if any)
			if move_slot == 0 and len(type1_moves) != 0:
				random_index = get_random_int(0,len(type1_moves_list)-1)
				move = type1_moves_list[random_index]

			# select second move among learnable type2 moves (if any)
			elif move_slot == 1 and len(type2_moves) != 0:
				random_index = get_random_int(0,len(type2_moves_list)-1)
				move = type2_moves_list[random_index]

			# default case
			else:
				random_index = get_random_int(0,len(allowed_move_list)-1)
				move = allowed_move_list[random_index]
				
			# skip moves we've already tried
			if(move in generated_moves):
				continue

			# only use allowed moves
			# NOTE: instead of this check, we assume the moves in allowed_move_list, type1_moves, and type2_moves are acceptable
			"""
			if(not move in allowed_move_list):
				continue
			"""

			# successful move for this slot
			generated_moves.append(move)
			move_slot += 1

		assertd(len(generated_moves) == 4)

		#printd("generate_moves() had " + str(iterations) + " iterations before returning an attempted moveset.")

		end_timer()

		return generated_moves

	# returns evolution chain object associated with this pokemon
	def get_evolution_chain(self):
		start_timer()
		assertd(self.has_dexnum())
		#printd(self.dexnum)
		species = client.get_pokemon_species(self.dexnum)
		evolution_chain_url = species.evolution_chain.url
		evolution_chain_id = evolution_chain_url.split('/')[-2]
		evolution_chain = client.get_evolution_chain(evolution_chain_id)
		end_timer()
		return evolution_chain

	# returns list of UNINITIALIZED Pokemon objects that lead up to this pokemon in evolution
	# a pokemon that is unevolved will return an empty list
	#TODO: not working properly (i.e. Eevee, Bellosom cases)
	def get_evolution_path(self):
		start_timer()
		assertd(self.has_dexnum())

		result = []

		pkmn_name = self.species_name

		evo_chain = self.get_evolution_chain()
		chain = evo_chain.chain

		species = chain.species
		evo_chain_name = species.name

		# this pokemon has no evolutions leading up to it: return an empty list
		if(evo_chain_name == pkmn_name):
			return result

		pkmn_obj = Pokemon()
		species_url = species.url
		dexnum = int(species_url.split('/')[-2])

		# don't bother looking into branches beyond second gen
		if not is_gen2_dexnum(dexnum):
			return []

		pkmn_obj.set_dexnum(dexnum)
		result.append(pkmn_obj)
		
		evolution_links = chain.evolves_to

		# a pokemon could evolve into more than one pokemon (i.e. eevee, slowpoke), so we need a for loop here instead of just going to "next up" in the chain
		# if there are no evolutions in the entire chain (i.e. aerodactyl and other legendaries), evolution_links will be an empty list
		# note that is also not safe to assume that a lower dexnum means it comes earlier tin the chain... i.e. pichu is later in the dex than pikachu but earlier in evo chain
		while(len(evolution_links)!=0):
			chain_link = evolution_links[0]
			link_species = chain_link.species
			link_name = link_species.name

			# once we reach the input pokemon, we've fetched all the pokemon leading up to the input, so return the list of those up to the input
			if(link_name == pkmn_name):
				return result

			pkmn_obj = Pokemon()
			species_url = link_species.url
			dexnum = int(species_url.split('/')[-2])

			# skip pokemon that were added beyond gen 2
			# otherwise pkmn_obj.set_dexnum(dexnum) below will cause is_legal_dexnum to throw an exception
			if not is_gen2_dexnum(dexnum):
				del evolution_links[0]
				continue

			pkmn_obj.set_dexnum(dexnum)
			result.append(pkmn_obj)	

			if(hasattr(chain_link, 'evolves_to')):
				link_evolves = chain_link.evolves_to
				for link in link_evolves:
					evolution_links.append(link)
			del evolution_links[0]

		end_timer()

		return result

	# print evolution path received from get_evolution_path()
	def print_evolution_path(self):
		start_timer()
		assertd(self.has_dexnum())
		ep = self.get_evolution_path()
		pkmn_name = self.species_name
		index = 0
		evo_str = ""
		for pkmn in ep:
			evo_str += pkmn.name
			if(index != len(ep)-1):
				evo_str += " -> "
			index += 1
		print("\nThe evolution path to " + pkmn_name + " is:\n" + evo_str + "\n")
		end_timer()

	# prints all pokemon that are possible from the base evolution chain
	# i believe this is currently unused
	def print_evolution_tree(self, ec):

		start_timer()

		result_chain = []

		chain = ec.chain
		#print_attributes(chain)

		species = chain.species
		result_chain.append(species.name)
		print(species)

		evolution_links = chain.evolves_to
		print(evolution_links)

		# a pokemon could evolve into more than one pokemon (i.e. eevee, slowpoke), so we need a for loop here instead of just going to "next up" in the chain
		# if there are no evolutions in the entire chain (i.e. aerodactyl and other legendaries), evolution_links will be an empty list
		# note that is also not safe to assume that a lower dexnum means it comes earlier tin the chain... i.e. pichu is later in the dex than pikachu but earlier in evo chain
		while(len(evolution_links)!=0):
			chain_link = evolution_links[0]
			link_species = chain_link.species
			link_name = link_species.name
			result_chain.append(link_name)
			link_evolves = chain_link.evolves_to
			for link in link_evolves:
				evolution_links.append(link)
			del evolution_links[0]

		print(result_chain)

		end_timer()

# ----- POKEMON LIBRARY BASE FUNCTIONS -----
# akin to class/static level functions

def is_pokemon(p):
	return isinstance(p, Pokemon)

# TODO: perhaps these could be renamed to "is_<thing>" instead of "is_legal_<thing>"?
def is_legal_dexnum(dexnum):
	return is_positive_int(dexnum) and is_gen2_dexnum(dexnum)

def is_gen2_dexnum(dexnum):
	return is_positive_int(dexnum) and dexnum <= Pokemon.max_dexnum

# (UNUSED)
def is_legal_species_name(sname):
	return is_str(sname) and sname.strip() != ""

def is_legal_type_names(type_names):
	if not is_list(type_names) or len(type_names) < 1:
		printd("bad type_names")
		return False
	type_name1 = type_names[0]
	has_two_names = len(type_names) > 1
	if has_two_names:
		type_name2 = type_names[1]
	return is_legal_type_name(type_name1) and (not has_two_names or is_legal_type_name(type_name2))

def is_legal_type_name(tn):
	if not is_str(tn):
		printd("is_legal_type_name(): bad type_name case 1 " + str(tn))
		return False
	#tn_formatted = tn.strip()
	if tn == "" or not tn in all_type_names:
		printd("is_legal_type_name(): bad type_name case 2 " + str(tn) + " --- " + str(tn))
		return False
	return True

def is_legal_level(l):
	return is_positive_int(l) and l <= Pokemon.max_level

def is_legal_ev(ev):
	return is_int(ev) and ev >= 0 and ev <= Pokemon.max_ev

def is_legal_iv(iv):
	return is_int(iv) and iv >= 0 and iv <= Pokemon.max_iv

# attempts to format a stat string
def format_stat_str(stat_str):
	return stat_str.replace(' ','').upper()

def is_legal_stat_str(stat_str):
	if not is_str(stat_str):
		return False
	stat_str_formatted = format_stat_str(stat_str)
	if not stat_str_formatted in stat_labels:
		return False
	return True

# lol @ this method name... "does my friendship hold up in court"
# could rename "friendship" to "fv" for friendship value
def is_legal_friendship(fv):
	return is_int(fv) and fv >= 0 and fv <= Pokemon.max_fv

# TODO: implement max range
def is_legal_held_item_id(hi_id):
	return is_positive_int(hi_id) and hi_id <= Pokemon.max_hi_id

def is_legal_OT_id(OT_id):
	return is_int(OT_id) and OT_id >= 0 and OT_id <= Pokemon.max_OT_id

# TODO: ... what other requirements might there be on a trainer name?
def is_legal_OT_name(tn):
	return is_str(tn)

def is_legal_gender_id(g_id):
	return is_int(g_id) and g_id >= 0 and g_id <= Pokemon.max_gender_id

def is_legal_nickname(nickname):
	if not is_str(nickname):
		return False
	nickname_formatted = nickname.strip()
	str_len = len(nickname_formatted)
	if str_len < 1 or str_len > Pokemon.max_nickname_length:
		return False
	for c in nickname_formatted:
		if not is_legal_character(c):
			return False
	return True

# returns true if c is a string of length 1 and c is in the list of acceptable characters for this generation 
# https://bulbapedia.bulbagarden.net/wiki/Nickname#Generation_II
# NOTE: this does not handle the multiplication symbol or the "PK" and "MN" symbols
def is_legal_character(c):
	if not is_str(c):
		return False
	if len(c) != 1:
		return False
	if not c.isalpha() and not c.isdigit() and not c in secondary_characters:
		return False
	return True

