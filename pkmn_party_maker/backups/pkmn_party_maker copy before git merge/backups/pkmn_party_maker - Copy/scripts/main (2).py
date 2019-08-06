# ----- created by Nathan Giles 6/30/19 -----

import pokepy
from helper_functions import *
import re


#TODO: random nickanmes drawn from like list of popular fictional characters... having a random omanyte named thanos xD
#TODO: could randomly generate pkmn then use pkhex's suggested moveset

# ----- GLOBAL VARIABLES -----

# main pokepy client
client = pokepy.V2Client()

# name of "Pokedex" folder
dex_folder = "../dex_entries/"

type_names = ['Bug', 'Dark', 'Dragon', 'Electric', 'Fighting', 'Fire', 'Flying', 'Ghost', 'Grass', 'Ground', 'Ice', 'Normal', 'Poison', 'Psychic', 'Rock', 'Steel', 'Water']

# cached 
file_list = []

hyphenated_moves = ["lock-on", "mud-slap", "double-edge", "self-destruct", "soft-boiled"]




# ----- FUNCTIONS -----


# main
def main():

	print("\nStart\n")

	write_dex_numbers()

	dex_num = 1

	pkmn = get_PKMN(dex_num)

	# print evolution path for testing
	ep = get_evolution_path(dex_num)
	print_evolution_path(dex_num)


	#print("Moves allowed by " + pkmn.name + " in gen 2: ")
	# want to use len(move_names) instead of len(moves) b/c moves may contain dupes
	moves = get_moves(pkmn, 2, True)
	move_names = get_move_names(moves)
	move_names.sort()
	format_move_list(move_names)
	#print_list(move_names)
	#print(len(move_names))

	file_ml = move_list_from_file(dex_num)
	file_ml.sort()
	format_move_list(file_ml)
	#print_list(file_ml)
	#print(len(file_ml))

	list_compare(move_names, file_ml)

	"""
	for move in moves:
		url = move.move.url.split('/')[-2]
		print("move: " + move.move.name + " id: " + url)
	"""


	"""
	#print(get_PKMN_name(14))
	#print_attributes(kakuna)
	#print(vars(kakuna)['game_indices'])
	
	#kakuna_moves = get_moves(kakuna,2)
	#print_list(get_move_names(kakuna_moves))
	#version_groups = get_version_groups(kakuna_moves[1])
	#print(version_groups)
	#print(str_move_versions(version_groups))
	#version_group_details = vars(kakuna_moves[1])['version_group_details']
	#print(get_move_name(kakuna_moves[0]))
	#print(version_group_details)

	#pichu_chain = vars(client.get_evolution_chain(18))['chain']
	#print(vars(pichu_chain))


	#test_chain = get_evolution_chain(79)
	print_evolution_tree(test_chain)
	#print_attributes(evolution_chain)
	#k_s_vars = vars(kakuna_species)
	#print(k_s_vars)

	#print_list(get_move_names(kakuna))
	moves = get_moves(kakuna)
	print(moves)
	move_names = get_move_names(moves)
	print(move_names)

	#attribs = vars(kakuna)
	#print_dict(attribs)
	#moves = attribs['moves']

		
	#print(client.get_ability("stench"))
	#print_attributes(kakuna)
	#print_functions(kakuna)
	#print(kakuna['moves'])
	#print(kakuna)
	"""

	print("\nEnd\n")


# generate one random pokemon
def randomize_PKMN():

	# stats that are randomized:
	# dex_number
	# moves
	# gender (if that pkmn is not genderless)
	# (for fun) - "garble" up the nickname

	# stats that are standardized:
	# level (100)
	# xp (??)
	# EVs
	# IVs (or if Hidden Power given, randomize HP type but max IVs... user knows HP type???)
	# friendship
	# held item
	# OT (trainer name) and TID (trainer ID)
	# PP ups for moves (+3 i believe)
	x = 5


# returns a pokemon given its int Pokedex number
# TODO: string name input
def get_PKMN(dex_num):
	return client.get_pokemon(dex_num)

# returns the name of the pokemon given its int Pokedex number
def get_PKMN_name(dex_num):
	return client.get_pokemon(dex_num).name

# extracts the name property from the move object
def get_move_name(m):
	return m.move.name
	
# prints the names of the moves in the list
def get_move_names(move_list):
	result = []
	for m in move_list:
		m_name = get_move_name(m)
		if m_name not in result:
			result.append(m_name)
	return result

# returns a list of the moves a pokemon with Pokedex number dex_num can learn
# optional: g is generation number; this function will instead return only the moves learnable by p in this generation
# TODO: proper input handling
# TODO: which moves SHOULD be allowed for a pokemon? i.e. there are some moves a pkmn can only learn from gen 1, BUT there are also egg moves... cant have both right?
# .... what about event moves? serebii does not list these.
def get_moves(p, g = None, include_prior_evos = False):

	moves = []
	for move in p.moves:
		moves.append(move)

	if g == 2:
		new_moves = []
		for move in moves:
			used_versions = set(str_move_versions(get_version_groups(move)))
			if "gold-silver" in used_versions or "crystal" in used_versions or "red-blue" in used_versions or "yellow" in used_versions:
				new_moves.append(move)
		moves = new_moves

	if include_prior_evos == True:
		evo_path = get_evolution_path(p.id)	
		for evo_pkmn in evo_path:		
			pkmn_move_list = get_moves(evo_pkmn,g,False)
			for move in pkmn_move_list:
				#TODO - prevent duplicate moves being added here? currently gives kakuna harden twice, b/c move objects will be diff even if move name is the same
				if move not in moves:
					moves.append(move)

	return moves


# returns a list of the "version_group"s associated with this "pokemon-move" 
# (not sure im using pokepy or whatever restful API's terminology correctly)
def get_version_groups(m):
	return vars(m)['version_group_details']

# converts this move version object into a string
def str_move_version(mv):
	return vars(vars(mv)['version_group'])['name']

# converts a series of move version objects into a list of strings
def str_move_versions(mv_list):
	result = []
	for mv in mv_list:
		result.append(str_move_version(mv))
	return result

# returns evolution chain object associated with this dex_num
def get_evolution_chain(dex_num):
	species = client.get_pokemon_species(dex_num)
	evolution_chain_url = vars(vars(species)['evolution_chain'])['url']
	evolution_chain_id = evolution_chain_url.split('/')[-2]
	evolution_chain = client.get_evolution_chain(evolution_chain_id)
	return evolution_chain

# returns list of species names leading up to this pokemon
def get_evolution_path(dex_num):
	result = []

	pkmn_name = get_PKMN_name(dex_num)

	ec = get_evolution_chain(dex_num)
	chain = vars(ec)['chain']
	#print_attributes(chain)

	species = vars(chain)['species']
	#print(species)
	ec_name = vars(species)['name']
	result.append(client.get_pokemon(ec_name))
	if(ec_name == pkmn_name):
		return result

	evolution_links = vars(chain)['evolves_to']
	#print(evolution_links)

	# a pokemon could evolve into more than one pokemon (i.e. eevee, slowpoke), so we need a for loop here instead of just going to "next up" in the chain
	# if there are no evolutions in the entire chain (i.e. aerodactyl and other legendaries), evolution_links will be an empty list
	# note that is also not safe to assume that a lower dexnum means it comes earlier tin the chain... i.e. pichu is later in the dex than pikachu but earlier in evo chain
	while(len(evolution_links)!=0):
		chain_link = evolution_links[0]
		chain_link_vars = vars(chain_link)
		link_species = chain_link_vars['species']
		link_name = vars(link_species)['name']
		result.append(client.get_pokemon(link_name))
		if(link_name == pkmn_name):
			return result
		link_evolves = chain_link_vars['evolves_to']
		for link in link_evolves:
			evolution_links.append(link)
		del evolution_links[0]

	return result

def print_evolution_path(dex_num):
	ep = get_evolution_path(dex_num)
	pkmn_name = get_PKMN_name(dex_num)
	index = 0
	evo_str = ""
	for pkmn in ep:
		evo_str += pkmn.name
		if(index != len(ep)-1):
			evo_str += " -> "
		index += 1
	print("\nThe evolution path to " + pkmn_name + " is:\n" + evo_str + "\n")

# prints all pokemon that are possible from the base evolution chain
def print_evolution_tree(ec):

	result_chain = []

	chain = vars(ec)['chain']
	#print_attributes(chain)

	species = vars(chain)['species']
	result_chain.append(vars(species)['name'])
	print(species)

	evolution_links = vars(chain)['evolves_to']
	print(evolution_links)

	# a pokemon could evolve into more than one pokemon (i.e. eevee, slowpoke), so we need a for loop here instead of just going to "next up" in the chain
	# if there are no evolutions in the entire chain (i.e. aerodactyl and other legendaries), evolution_links will be an empty list
	# note that is also not safe to assume that a lower dexnum means it comes earlier tin the chain... i.e. pichu is later in the dex than pikachu but earlier in evo chain
	while(len(evolution_links)!=0):
		chain_link = evolution_links[0]
		chain_link_vars = vars(chain_link)
		link_species = chain_link_vars['species']
		link_name = vars(link_species)['name']
		result_chain.append(link_name)
		link_evolves = chain_link_vars['evolves_to']
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
def move_list_from_file(dex_num):
	move_list = []
	digits = format_digits(dex_num,3)
	#prefix = "Serebii.net Pokédex - #"
	prefix = "view-source_https___www.serebii.net_pokedex-gs_"
	species_name = get_PKMN_name(dex_num).capitalize()
	postfix = ".shtml"
	#fname = dex_folder + prefix + digits + " - " + species_name + postfix
	fname = dex_folder + prefix + digits + postfix
	print(fname)
	fname2 = dex_folder + "view-source_https___www.serebii.net_pokedex-gs_001" + postfix
	print(fname == fname2)
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
			if(l.capitalize() not in type_names and l!=""):
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


# ----- END -----

if __name__ == "__main__":
	main()
