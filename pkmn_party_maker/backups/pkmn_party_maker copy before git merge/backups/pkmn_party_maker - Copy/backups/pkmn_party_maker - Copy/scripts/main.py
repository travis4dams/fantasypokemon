# ----- created by Nathan Giles 6/30/19 -----

import pokepy
from helper_functions import *
#import re
#from webrequest import main_request
import sys


#TODO: random nickanmes drawn from like list of popular fictional characters... having a random omanyte named thanos xD
#TODO: could randomly generate pkmn then use pkhex's suggested moveset
#TODO: pull travis's type_advantages.csv from https://github.com/travis4dams/fantasypokemon



# ----- GLOBAL VARIABLES -----

# main pokepy client
client = pokepy.V2Client()

# list of acceptable input commands and their help descriptions
cmd_list = ['help','quit','ruleset','teammake','teamedit','teamprint']
help_instructions = {'help':'Displays a list of acceptable commands.', 
			'quit':'Terminates the script.', 
			'ruleset':'Describes the current ruleset. Typing \"ruleset edit <rule_number> <value>\" will edit that rule to that value if permissible.', 
			'teammake':'Creates the number of teams according the ruleset. Entering \"teammake <team_number>\" will replace that team with a new team.', 
			'teamedit':'Edits a specific Pokemon. Type \"teamedit <team_number> <slot_number>\" to reselect that pokemon.', 
			'teamprint':'Prints the current teams in PkHex format to console, copies it to clipboard, and creates the appropriate output file(s). Typing \"teamprint <team_number>\" will do this for only that team.'}

# main list of teams used by players
teams = []

# number of teams to build per instance of "teammake" run
default_num_teams = 2

# name of "Pokedex" folder
dex_folder = "../dex_entries/"

# list of string pokemon types
type_names = ['Bug', 'Dark', 'Dragon', 'Electric', 'Fighting', 'Fire', 'Flying', 'Ghost', 'Grass', 'Ground', 'Ice', 'Normal', 'Poison', 'Psychic', 'Rock', 'Steel', 'Water']

# ideally write this out to a file somewhere or cache it or smt
file_list = []

# list of moves with hyphens in the names all in lower case
hyphenated_moves = ["lock-on", "mud-slap", "double-edge", "self-destruct", "soft-boiled"]

# number of pokemon on a given team, usually 6
ruleset_team_size = 6



# ----- FUNCTIONS -----


# main
def main():

	print("\nStart of script.\n")

	#write_dex_numbers()

	dex_num = 1

	input_loop()

	script_quit()

def input_loop():

	# welcome/introduction
	print("Welcome to Pokemon team maker!")

	# input instructions
	print("\nThe possible commands are:")
	print_list(cmd_list)
	print()

	# accept input
	cmd = input("Please input a command:\n").lower()
	while(cmd != None and cmd != "" and cmd != "quit"):
		interpret_cmd(cmd)
		cmd = input("Please input a command:\n").lower()

def interpret_cmd(cmd):
	cmd_list = cmd.lower().split(' ')
	cmd = cmd_list[0]
	if cmd == 'help':
		help()
	elif cmd == 'quit': # while loop condition should handle this but eh just incase
		script_quit()
	elif cmd == 'ruleset':
		ruleset()
	elif cmd == 'teamprint':
		subcmd = team_cmd_input_handling(cmd_list)
		team_print(subcmd)
	elif cmd == 'teammake':
		subcmd = team_cmd_input_handling(cmd_list)
		team_make(subcmd)
	elif cmd == 'teamedit':
		subcmd = team_cmd_input_handling(cmd_list)
		if(subcmd!=None):
			team_edit(subcmd[0], subcmd[1])
		else:
			team_edit(subcmd)
	else:
		print("Unrecognized command: " + cmd)
	return


def help():
	print("\nList of commands:")
	for cmd in cmd_list:
		print("\n" + cmd)
		print(help_instructions[cmd] + "\n")
	print()

# called to close anything out
def script_quit():
	print("\nEnd of script.\n")
	sys.exit("Script ended by script_quit() call.")

	#should not be reached
	print("\nThe script did not quit successfully.")
	return

# see "readme.txt" and randomize_PKMN() comments for more info on defining ruleset(s)
def ruleset():
	print("\nruleset not yet implemented.\n")

def team_make(replace_team_num = None):
	print("\nteam_make not yet implemented.\n")

	"""
	loose algorithm pseudocode:

	# build all teams
	if(replace_team_num == None):
		for team_num in range(default_num_teams):
			team = []
			while len(team) < ruleset_team_size:
				pkmn = randomize_pkmn()
				team.append(pkmn)
			teams.append(team)

	# replace a specific team
	else:
		team = []
		while len(team) < ruleset_team_size:
				pkmn = randomize_pkmn()
				team.append(pkmn)
	"""

def team_edit(team_num, slot_num):
	print("\nteam_edit not yet implemented.\n")

	"""
	loose algorithm pseudocode:
	pkmn = teams[team_num][slot_num]
	"""

def team_print(team_num = None):

	"""
	loose algorithm pseudocode:
	# generate console output
	out_strs = []
	if(team_num != None):
		print only that team
	for team in teams:
		team_str = ""
		for pkmn in team:
			team_str += "\n" + PKMN_dict_to_str(pkmn) + "\n"
		out_strs.append(team_str)
	print_result = ""
	for out_str in out_strs:
		print_result += out_str

	# generate PkHex commands to clipboard
	cmd_strs = []
	for team in teams:
		cmd_str = ""
		for pkmn in team:
			# whitespace is handled by batch handler yes?
			cmd_str += "\n" + PKMN_dict_to_cmd(pkmn) + "\n"
		print("This is the current PkHex command for team " + team_num + ":")
		print(cmd_str)
		print("Would you like to proceed? (y/n)")
		proceed = input().replace(" ","").lower()
		if(proceed != "y"):
			print("Quitting teamprint.")
			return
		cmd_strs.append(cmd_str)
		copy command to clipboard
		wait for user to indicate continue
		continue loop


	# generate output file(s)
	# request team name(s)
	# ensure positions in each list here align, i.e. index 0 is referencing team 1 across all these lists
	assert(len(cmd_strs) == len(teams))
	generate folder based on this time stamp
	for team in teams:
		generate file name based on team number
		cmd_file = ...
		readable_file = ...
		for cmd in cmd_strs:
			cmd_file.write(cmd)
		readable_file.write(print_result)
		close files
	"""

	print("\nteam_print not yet implemented.\n")

# todo: check is_int here and elsewhere
def team_cmd_input_handling(cmd_list):

	cmd = cmd_list[0]

	subcmd = None

	if cmd == 'teamprint':
		if len(cmd_list) > 1:
			subcmd = cmd_list[1]
		if(subcmd == '' or subcmd == None or subcmd < 0):
			print("Unrecognized input to teamprint: " + str(subcmd))
			return
		if(subcmd > len(teams)):
			print("Team number to teamprint out of range: " + str(subcmd) + ". There are currently only " + len(teams) + "teams.")
			return

	elif cmd == 'teammake':
		if len(cmd_list) > 1:
			subcmd = cmd_list[1]
		if(subcmd == '' or subcmd == None or subcmd < 0):
			print("Unrecognized input to teammake: " + str(subcmd))
			return
		if(subcmd > len(teams)):
			print("Team number to teammake out of range: " + str(subcmd) + ". There are currently only " + len(teams) + "teams.")
			return

	elif cmd == 'teamedit':
		if len(cmd_list) < 3:
			print("Not enough inputs to teamedit: Got " + len(cmd_list) + ", expected 3.")
		# check team_num
		team_num = cmd_list[1]
		if(team_num == '' or team_num == None or team_num < 0):
			print("Unrecognized first input to teamedit: " + str(team_num))
			return
		if(team_num > len(teams)):
			print("Team number to teamedit out of range: " + str(team_num) + ". There are currently only " + len(teams) + "teams.")
			return
		# check slot_num
		team = teams[team_num]
		slot_num = cmd_list[2]
		if(slot_num == '' or slot_num == None or slot_num < 0):
			print("Unrecognized second input to teamedit: " + str(slot_num))
			return
		if(slot_num > len(team)):
			print("Team number to teamedit out of range: " + str(slot_num) + ". There are currently only " + len(teams) + "teams.")
			return
		subcmd = (cmd_list[1], cmd_list[2])

	# shouldn't be reached based on structure of interpret_cmd()'s if-else structure
	else:
		print("Unrecognized command to team_cmd_input_handling().")
		
	return subcmd

# generate one random pokemon
# try to use strings (variables/values) congruent w/ PkHex
def randomize_PKMN():

	pkmn = {}

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

	"""
	pseudocode

	dexnum = randomint(1,252)
	if banned pokemon: continue
	setup_static_vars
	setup_dynamic_vars

	"""

# takes the pokemon dict output by randomize_pkmn and turns it into a readable human string
def PKMN_dict_to_str(pd):
	pass


# takes the pokemon dict output by randomize_pkmn and turns it into an exeuctable PkHex cmd
def PKMN_dict_to_cmd(pd):
	pass

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








# ----- DUMP -----

"""
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