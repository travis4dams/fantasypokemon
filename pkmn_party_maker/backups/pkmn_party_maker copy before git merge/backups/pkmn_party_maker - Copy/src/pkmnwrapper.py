# ----- INFORMATION -----

# pkmnwrapper.py mainly serves as a wrapper of the pokepy API to streamline its use
# put another way, pkmnwrapper.py serves to set up data/objects related to Pokemon 

# ----- IMPORTED PACKAGES -----

# project packages
from pglobals import *
from helper_functions import *

# external packages
import pokepy
import beckett.exceptions

# previouslly used packages
#from main import squit

# ----- PKMNWRAPPER VARIABLES -----

# maps pkmn dexnums to pokemon objs that have already been loaded
#TODO: not sure this actually works with global variables correctly
pkmn_obj_cache = {}

# maps pkmn dexNum to a tuple of (<pkmn_name>,<learnable_move_obj_list>)
# used by get_moves to save loading time if we already determined the moves learnable by a pokemon
pkmn_move_cache = {}

# ----- PKMNWRAPPER FUNCTIONS -----

# attempt to fetch pokemon object from Pokepy client and handle any errors
def client_pkmn_request(dexnum):

	# check input
	assertd(is_int(dexnum),"Bad input to client_pkmn_request(): " + str(dexnum) + " is not an int.")
	assertd(is_gen2_dexnum(dexnum),"dexnum to client_pkmn_request() is out of range: " + str(dexnum))

	# client request
	try:
		return client.get_pokemon(dexnum)
	except beckett.exceptions.InvalidStatusCodeError:
		raise ValueError("Bad input to client.get_pokemon() in get_PKMN() wrapper: " + str(dexnum))
	
	# generic catch... but commented out because why not just pass the original error for more info about the error?
	"""
	except:
		raise Exception("Unknown error in get_PKMN() fetching dexnum " + str(dexnum))
		#squit()
	"""

# input: 1 <= dexnum <= 251
# output: Pokepy Pokemon object given an int Pokedex number
# NOTE: only Gen2 dexnum's are allowed (1-251 inclusive)
# TODO: string name input
def get_PKMN(dexnum):
	# check input
	assertd(is_int(dexnum),"Bad input to get_PKMN(): " + str(dexnum) + " is not an int.")

	# check if pkmn obj is cached
	if(dexnum in pkmn_obj_cache):
		return pkmn_obj_cache[dexnum]

	# get output, check it, and return if acceptable
	result = client_pkmn_request(dexnum)	
	assertd(result != None and isinstance(result,pokepy.resources_v2.PokemonResource),
		"Bad result from client_pkmn_request() in get_PKMN(). Type: " + get_class_name(result) + " str: " + str(result))
	return result

# returns the name of the pokemon given an int Pokedex number
def get_PKMN_name(dexnum):
	# check input
	assertd(is_int(dexnum),"Bad input to get_PKMN_name(): " + str(dexnum) + " is not an int.")
	assertd(is_gen2_dexnum(dexnum),"dexnum to get_PKMN_name() is out of range: " + str(dexnum))

	# attempt to get pokemon object and its name
	result_pkmn = get_PKMN(dexnum)
	assertd(result_pkmn != None and is_pokepy_pkmn(result_pkmn),
		"Bad result from get_PKMN() in get_PKMN_name(). Type: " + get_class_name(result_pkmn) + " str: " + str(result_pkmn))
	result_name = result_pkmn.name
	assertd(is_str(result_name) and result_name!="",
		"Bad retrieved name in get_PKMN_name(). Type: " + get_class_name(result_name) + " str: " + str(result_name))
	return result_name

# fetches the move name given a move ID OR extracts the name property from a move object 
def get_move_name(o):
	a = is_int(o)
	b = is_pokepy_move(o)
	assertd(a or b,
		"Bad input to get_move_name(); it is neither an int nor a Pokemon move. Type: " + get_class_name(o) + " str: " + str(o))
	if(a):
		return client.get_move(o).name
	else:
		return o.move.name
	
# returns a list of the names associated with the move objects/id#s in request_list
def get_move_names(request_list):
	assertd(is_list(request_list),"Argument to get_move_names() is not a list. Type: " + get_class_name(request_list))
	result = []
	for o in request_list:
		assertd(is_int(o) or is_pokepy_move(o),
			"Bad element in request_list to get_move_names(); it is neither an int nor a Pokemon move. " + 
			"Type: " + get_class_name(o) + " str: " + str(o))
		m_name = get_move_name(o)\
		#if m_name not in result:
		result.append(m_name)
	return result

# input:
# p - a pokemon object
# g - an int representing generation number, assumed to be 2 throughout this script. 
# 		if g is provided, this function will instead return only the moves learnable by p in this generation
#		defaults to gen 2
# include_prior_evos - a boolean indicating whether 
# output:
# a list of pokepy move objects that are learnable by that Pokemon
# TODO: proper input handling
# TODO: which moves SHOULD be allowed for a pokemon? i.e. there are some moves a pkmn can only learn from gen 1, BUT there are also egg moves... cant have both right?
# .... what about event moves? serebii does not list these.
#TODO: rename to "get_learnable_moves" or stadium moves or smt
#TODO: some bug in here related to mantine and not having any moves when output from get_moves
def get_moves(p, g = 2, include_prior_evos = True):

	global rs

	#print("in get_moves()")

	assertd(is_pokepy_pkmn(p),
		"Bad input to get_moves(); p is not a pokepy Pokemon object. Type: " + get_class_name(p) + " str: " + str(p))	
	
	assertd(g == None or (g > 0 and g < 8),
		"Bad input to get_moves(); g is bad type or out of range. Type: " + get_class_name(g) + " str: " + str(g))	

	assertd(include_prior_evos == None or isinstance(include_prior_evos, bool),
		"Bad input to get_moves(); include_prior_evos is not a bool. Type: " + get_class_name(include_prior_evos) + " str: " + str(include_prior_evos))

	if(g != 2):
		print("get_moves() failed: g = " + str(g) + " but only Gen 2 is currently supported.")
		return None

	dexnum = p.id
	if(dexnum in pkmn_move_cache):
		printd("move cache hit")
		result = pkmn_move_cache[dexnum][1]
		return result

	# fetch moves from pokemon's moves attribute
	moves = []
	for move in p.moves:
		assertd(is_pokepy_move(move),
			"Bad move in pkmn moves in get_moves(); move isn't a move object. Type: " + get_class_name(move) + " str: " + str(move))	
		moves.append(move)

	# replace moves with a new list that contains only the gen2 moves from moves list
	# (only supported case atm)
	if g == 2:
		new_moves = []
		for move in moves:
			used_versions = set(str_move_versions(get_version_groups(move)))
			if "gold-silver" in used_versions or "crystal" in used_versions or "red-blue" in used_versions or "yellow" in used_versions:
				new_moves.append(move)
		moves = new_moves

	#print("weqeq")
	#print(len(moves))

	# if(include_prior_evos), then fetch moves from pokemon earlier up in the evolution path and consider them learnable by this pokemon
	if include_prior_evos == True:
		evo_path = get_evolution_path(p.id)	
		#print(evo_path)
		for evo_pkmn in evo_path:	
			if(evo_pkmn == None):
				continue	
			pkmn_move_list = get_moves(evo_pkmn,g,False)
			for move in pkmn_move_list:
				#TODO - prevent duplicate moves being added here? currently gives kakuna harden twice, b/c move objects will be diff even if move name is the same
				if move not in moves:
					moves.append(move)

	# remove any "inferior" moves from the moves list by skipping over them when we copy moves into moves_result
	move_ids = []
	for move in moves:
		move_ids.append(get_move_id(move))

	moves_result = []
	for move in moves:
		move_id = get_move_id(move)
		if move_id in rs.inferior_moves_dict:
			superior_move_id = rs.inferior_moves_dict[move_id][1]
			if not superior_move_id in move_ids:
				moves_result.append(move)
			"""
			else:
				inf_mname = rs.inferior_moves_dict[move_id][0]
				sup_mname = rs.inferior_moves_dict[move_id][2]
				printd("Detected inferior move for " + get_PKMN_name(dexnum).capitalize() + ": " + inf_mname + " to " + sup_mname)
			"""
		else:
			moves_result.append(move)

	#TODO: we dont want this assert here b/c with gen restrictions a pokemon may have no lkearnable moves (i.e. retrieving wobbuffets moveset retrieves wynauts which has only gen 3 moves or smt)
	#TODO: perhaps do something if gen excludes that pkmn dont fetch its moves or smt idk
	"""
	assertd(is_list(moves) and len(moves)>0,
		"Bad output from get_moves. Type: " + get_class_name(moves) + " str: " + str(moves) + " len: " + str(len(moves)))
	"""
	return moves_result

# returns int move id associated with move object m
def get_move_id(m):
	assertd(is_pokepy_move(m),
		"Bad input to get_move_id(); it is not a Pokemon move. Type: " + get_class_name(m) + " str: " + str(m))
	m_id = int(m.move.url.split('/')[-2])
	# 743 is the max pokemon id # according to https://bulbapedia.bulbagarden.net/wiki/List_of_moves
	assertd(is_positive_int(m_id) and m_id < 743,
		"Bad output from get_move_id() move_id bad type or out of range. Type: " + get_class_name(m_id) + " str: " + str(m_id))
	return m_id

# returns the move object associated with the name name
# pokepy API seems to have moves in the form "word1-word2", i.e. lower case and separated by -'s
def get_move_by_name(name):
	assertd(is_str(name),
		"Bad input to get_move_by_name(); it is not a Pokemon move. Type: " + get_class_name(name) + " str: " + str(name))
	name = name.strip()
	assertd(name!="",
		"Bad input to get_move_by_name(). Type: " + get_class_name(name) + " str: " + str(name) + " len: " + str(len(name)))
	name = name.lower().replace(' ','-')
	move = client.get_move(name) 
	#assertd(is_pokepy_move(move),
	#	"Bad output from get_move_by_name(). Type: " + get_class_name(move) + " str: " + str(move))
	return move

# returns a list of move objects associated with each name in name_list
# pokepy API seems to have moves in the form "word1-word2", i.e. lower case and separated by -'s
def get_moves_by_name(name_list):
	move_objs = []
	for name in name_list:
		move_objs.append(get_move_by_name(name))
	return move_objs

# returns a list of the "version_group"s associated with this "pokemon-move" 
# (not sure im using pokepy or whatever restful API's terminology correctly)
def get_version_groups(m):
	assertd(is_pokepy_move(m),
		"Bad input to get_version_groups(); it is not a Pokemon move. Type: " + get_class_name(m) + " str: " + str(m))
	result = m.version_group_details
	assertd(is_list(result),
		"Bad output get_version_groups(); it is not a list. Type: " + get_class_name(result) + " str: " + str(result))
	assertd(len(result)>0,
		"Bad output get_version_groups(); it is an empty list. Type: " + get_class_name(result) + " str: " + str(result) + " len: " + str(len(result)))
	return result

# converts a move version object into a string
def str_move_version(mv):
	assertd(isinstance(mv,pokepy.resources_v2.PokemonMoveVersionSubResource),
		"Bad input to get_version_groups(); it is not a Pokemon move version. Type: " + get_class_name(mv) + " str: " + str(mv))
	result = mv.version_group.name
	assertd(is_str(result),
		"Bad output str_move_version(); it is not a string. Type: " + get_class_name(result) + " str: " + str(result))
	return result

# converts a series of move version objects into a list of strings
def str_move_versions(mv_list):
	assertd(is_list(mv_list),
		"Bad input to str_move_versions(); it is not a list. Type: " + get_class_name(mv_list) + " str: " + str(mv_list))
	assertd(len(mv_list)>0,
		"Bad input to str_move_versions(); it is an empty list. Type: " + get_class_name(mv_list) + " str: " + str(mv_list) + " len: " + str(len(mv_list)))
	result = []
	for mv in mv_list:
		assertd(isinstance(mv,pokepy.resources_v2.PokemonMoveVersionSubResource),
			"Bad mv in mv_list in str_move_versions(); it is not a Pokemon move version. Type: " + get_class_name(mv) + " str: " + str(mv))
		result.append(str_move_version(mv))
	assertd(is_list(result),
		"Bad output str_move_versions(); it is not a list. Type: " + get_class_name(result) + " str: " + str(result))
	assertd(len(result)>0,
		"Bad output str_move_versions(); it is an empty list. Type: " + get_class_name(result) + " str: " + str(result) + " len: " + str(len(result)))
	return result

# returns evolution chain object associated with this dexnum
def get_evolution_chain(dexnum):
	assertd(is_int(dexnum),
		"Bad input to get_evolution_chain(); dexnum is not a list. Type: " + get_class_name(dexnum) + " str: " + str(dexnum))
	species = client.get_pokemon_species(dexnum)
	evolution_chain_url = species.evolution_chain.url
	evolution_chain_id = evolution_chain_url.split('/')[-2]
	evolution_chain = client.get_evolution_chain(evolution_chain_id)
	return evolution_chain

# returns list of species names leading up to this pokemon
# a pokemon that is unevolved will return an empty list
def get_evolution_path(dexnum):
	result = []

	pkmn_name = get_PKMN_name(dexnum)

	ec = get_evolution_chain(dexnum)
	chain = ec.chain
	#print_attributes(chain)

	species = chain.species
	#print(species)
	ec_name = species.name

	# this pokemon has no evolutions leading up to it: return an empty list
	if(ec_name == pkmn_name):
		return result

	result.append(client.get_pokemon(ec_name))
	evolution_links = chain.evolves_to
	#print(evolution_links)

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
		result.append(client.get_pokemon(link_name))	
		if(hasattr(chain_link, 'evolves_to')):
			link_evolves = chain_link.evolves_to
			for link in link_evolves:
				evolution_links.append(link)
		del evolution_links[0]

	return result

# print evolution path received from get_evolution_path()
def print_evolution_path(dexnum):
	ep = get_evolution_path(dexnum)
	pkmn_name = get_PKMN_name(dexnum)
	index = 0
	evo_str = ""
	for pkmn in ep:
		evo_str += pkmn.name
		if(index != len(ep)-1):
			evo_str += " -> "
		index += 1
	print("\nThe evolution path to " + pkmn_name + " is:\n" + evo_str + "\n")

# prints all pokemon that are possible from the base evolution chain
# i believe this is currently unused
def print_evolution_tree(ec):

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

# capitalizes the names of moves and such in move list
def format_move_list(l):

	for i in range(len(l)):
		l[i] = l[i].replace('-','')

	"""
	for i in range(len(l)):
		move = l[i].replace('-',' ').title()
		if move == "Solarbeam":
			move = "Solar Beam"
		elif move == "Poisonpowder":
			move = "Poison Powder"
		l[i] = move

		mname = l[i]
		if(mname not in hyphenated_moves):
			mname = mname.replace('-',' ').title()
		else:
			j = mname.index('-')
			mname.replace(j+1,mname[j+1].upper())
		l[i] = mname
	"""


# attempts to build a learnable move list from the serebii page
def move_list_from_file(dexnum):
	move_list = []
	digits = format_digits(dexnum,3)
	#prefix = "Serebii.net Pokédex - #"
	prefix = "view-source_https___www.serebii.net_pokedex-gs_"
	species_name = get_PKMN_name(dexnum).capitalize()
	postfix = ".shtml"
	#fname = dex_folder + prefix + digits + " - " + species_name + postfix
	fname = dex_folder + prefix + digits + postfix
	printd(fname) 
	fname2 = dex_folder + "view-source_https___www.serebii.net_pokedex-gs_001" + postfix
	printd(fname == fname2)
	fp = open(fname,'r')
	line = fp.readline()
	while line!="":
		#line = line.strip()
		#attackdex_positions = [m.start() for m in re.finditer('attackdex', line)]
		#shtml_positions = [m.start() for m in re.finditer('.shtml', line)]
		if("attackdex" in line and ".shtml" in line):
		#if(len(attackdex_positions)!=0 and len(shtml_positions)!=0):
			#if("sword" in line or "charm" in line):
				#print(line[attackdex_positions[0]:attackdex_positions[1]])
			i = line.index("attackdex")
			j = line.index(".shtml", i)
			k = line[i:j]
			l = k.split('/')[-1]
			if(l == 'psychict'):
				l = "psychic"
			if(l.capitalize() not in all_type_names and l!=""):
				#print(l)
				move_list.append(l)

			"""
			attackdex_i = line.index("https://www.serebii.net/attackdex")
			a_index = line.index("</a>",attackdex_i)
			i = a_index
			while(i >= 0):
				if(line[i] == ">"):
					break
				i -= 1
			if(i >= 0):
				move_line = line[i+1:a_index]
				if(move_line!="" and "Gen" not in move_line and move_line not in move_list):
					move_list.append(move_line)
			"""

		line = fp.readline()
	return move_list
	fp.close()

def organize_move_list(l):
	return "blah"

def pkmn_to_str(name, dexnum):
	return name.title() + " (" + str(dexnum) + ")"

# returns a list of the strings of the types associated with this pokepy pokemon p
# if they have no second type, output[1] == "None"
def get_type_names(p):
	pkmn_types = p.types
	pkmn_type1 = pkmn_types[0]
	pkmn_type1_name = pkmn_type1.type.name.strip().lower()
	pkmn_type_names = []
	# pkmn_type2 is None if the pokemon is single typed
	if len(pkmn_types) > 1:
		pkmn_type2 = pkmn_types[1]
	else:
		pkmn_type2 = None
	# override fairy type with normal type
	#TODO: ensure this works correctly with the movesets of normal type pokemon and checking condition below for move type
	if pkmn_type1_name == "fairy":
		pkmn_type1_name = "normal"
	pkmn_type_names.append(pkmn_type1_name)
	# pokemon has a second type
	if pkmn_type2 != None:
		pkmn_type2_name = pkmn_type2.type.name.strip().lower()
		# replace fairy with normal
		if(pkmn_type2_name == "fairy"):
			pkmn_type2_name = "normal"
		# if the change from fairy to normal (or something else) causes this pokemon to have the same type twice, instead say second type is None
		if(pkmn_type2_name not in pkmn_type_names):
			pkmn_type_names.append(pkmn_type2_name)
		else:
			pkmn_type_names.append("None")
	# pokemon has no second type: add None
	else:
		pkmn_type_names.append("None")
	return pkmn_type_names

# checks that the nickname n is a string and between 1 and 10 characters inclusive
#TODO: note that this increased to max of 12 charactrers after gen 5 apparently?
def is_legal_nickname(n):
	if not is_str(n):
		return False
	l = len(n)
	return l > 1 and l < 11

# TODO: global variable type_names probably redundant w/ local variables in other functions 
def get_type_color(type_name):
	assertd(is_str(type_name))
	type_name_formatted = type_name.strip().capitalize()
	assertd(type_name_formatted in type_names)
	if type_name_formatted == 'Bug':
		return get_color("green") + get_style("dim")
	elif type_name_formatted == 'Dark':
		return get_color("black") + get_style("bright")	
	elif type_name_formatted == 'Dragon':
		return get_color("blue") + get_style("dim")
	elif type_name_formatted == 'Electric':
		return get_color("yellow") + get_style("bright")
	elif type_name_formatted == 'Fighting':
		return get_color("red") + get_style("normal")
	elif type_name_formatted == 'Fire':
		return get_color("red") + get_style("bright")
	elif type_name_formatted == 'Flying':
		return get_color("cyan") + get_style("normal")
	elif type_name_formatted == 'Ghost':
		return get_color("magenta") + get_style("dim")
	elif type_name_formatted == 'Grass':
		return get_color("green") + get_style("bright")
	elif type_name_formatted == 'Ground':
		return get_color("yellow") + get_style("dim")
	elif type_name_formatted == 'Ice':
		return get_color("cyan") + get_style("bright")
	elif type_name_formatted == 'Normal':
		return get_color("white") + get_style("bright")
	elif type_name_formatted == 'Poison':
		return get_color("magenta") + get_style("normal")
	elif type_name_formatted == 'Psychic':
		return get_color("magenta") + get_style("bright")
	elif type_name_formatted == 'Rock':
		return get_color("red") + get_style("dim")
	elif type_name_formatted == 'Steel':
		return get_color("white") + get_style("dim")
	elif type_name_formatted == 'Water':
		return get_color("blue") + get_style("bright")
	else:
		printd("unrecognized type name to get_type_color(): " + str(type_name))