# ----- created by Nathan Giles 6/30/19 -----
# NOTE: this entire project currently (as of 7.2.19 1:45 AM) is only intended for gen 2 functionality... 
# no pkmn or functionality or attributes beyond gen 2 were included here

import pokepy
from helper_functions import *
#import re
#from webrequest import main_request
import sys


#TODO: random nickanmes drawn from like list of popular fictional characters... having a random omanyte named thanos xD
#TODO: could randomly generate pkmn then use pkhex's suggested moveset
#TODO: pull travis's type_advantages.csv from https://github.com/travis4dams/fantasypokemon
#TODO: ***** folder import for batch editor on PkHex *****
#TODO: ensure no two pokemon from the same line i.e. no abra and kadabra
#TODO: rules enforced by ruleset luke/ciaran/logan and i established - i.e. max evolution in chain, use best move, ensure at least one damaging move, no N/A moves like sleep talk w/o rest, etc
#TODO: type balancing i.e. no type repeated more than once or smt
#TODO: pkmn edit allows editing any property like introducing an attr into pkmn's dict
#TODO: print cmd from pkmn dict function should iterate through ALL dict entries even those unrecognized
#TODO: efficiency, caching, test cases, etc
#TODO: enter trainer name
#TODO: save output files
#TODO: search all todo's and pull to top of file anything thats impt
#TODO: test gc on windows programs incl n64 emulator
#TODO: order more usb n64 controllers
#TODO: when picking highest evolution, if it branches off (i.e. eevee or slowpoke), they get to pick... eevee makes a cool wild card 
#		in that case kinda... tyrogue and other baby pkmn not banned picks in that case. ID "choices" by "evolution_tree" branches off 
# 		instead of just going up 1 level or w/e.
#TODO: det/ask who goes first among teams
#TODO: asserts, incl those in helper_functions... also test cases again :) 
#TODO: ensure any "artifacts" from stuff after gen 2 (i.e. fairy type) arent in data
#TODO: jigglypuff typing (normal-normal instead of normal) and other strange corner cases you think might arise
#TODO: focus on the set of attributes actually needed for PkmnStad2 battles... then make sure all of that is tested properly
#TODO: pp ups seemed to be assumed
#TODO: test move set - seemed to be a lot of flagged moves. double checking this w/ serebii would be good... see chrome history for stuff about html request... i believe there was a builtin py3 lib
#TODO: double check values like stats and such w/ an outside source for additional confidence/validity
#TODO: design - how to generate more balanced movesets/types... ideas travis had about prebuilt movesets... 
#TODO: command prompt interface to include some of that
#TODO: calling team_make() more than once should append more teams not overwrite... is all that working properly?
#TODO: timing functions to narrow optimization... compare import times (import less libs?) to main algorithms
#TODO: revisit algorithms... consider, is there a faster way to get this? esp if we cache/store some stuff? am i recalc'ing smt repeatedly?
#TODO: revisit "low level" functions i.e. fetching the name from a pkmn obj... even getting that to be faster could streamline some stuff



# ----- GLOBAL VARIABLES -----

# main pokepy client
client = pokepy.V2Client()

# list of acceptable input commands
cmd_list = ['help','quit','ruleset','teammake','teamedit','teamprint']

# dict mapping acceptable input commands to their help descriptions
# this is used for "help" output
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
type_names = ['Bug', 'Dark', 'Dragon', 'Electric', 'Fighting', 'Fire', 'Flying', 'Ghost', 'Grass', 'Ground', 'Ice', 'Normal', 
'Poison', 'Psychic', 'Rock', 'Steel', 'Water']

# ideally write this out to a file somewhere or cache it or smt
file_list = []

# list of banned dexNums
banned_dexnums_list = [10, 11, 13, 14, 129, 132, 150, 151, 172, 173, 174, 175, 201, 235, 236, 238, 239, 240, 249, 250, 251]

# dict of banned dexNums mapped to a tuple containing (name, ban_reason)
banned_dexnums_dict = 
{
10:("Caterpie","Less than four learnable moves"),
11:("Metapod","Less than four learnable moves"), 
13:("Weedle","Less than four learnable moves"), 
14:("Kakuna","Less than four learnable moves"), 
129:("Magikarp","Less than four learnable moves"), 
132:("Ditto","Less than four learnable moves"), 
150:("Mewtwo","Legendary and outside stadium rentals"), 
151:("Mew","Legendary and outside stadium rentals"),
172:("Pichu","Baby Pokemon"), 
173:("Cleffa","Baby Pokemon"), 
174:("Igglybuff","Baby Pokemon"), 
175:("Togepi","Baby Pokemon"), 
201:("Unown","Less than four learnable moves"), 
235:("Smeargle","Less than four learnable moves"),
236:("Tyrogue","Baby Pokemon"), 
238:("Smoochum","Baby Pokemon"), 
239:("Elekid","Baby Pokemon"), 
240:("Magby","Baby Pokemon"), 
249:("Lugia","Legendary and outside stadium rentals"), 
250:("Ho-oh","Legendary and outside stadium rentals"), 
251:("Celebi","Legendary and outside stadium rentals")
}

# list of genderless dexNums
# inferred from https://bulbapedia.bulbagarden.net/wiki/List_of_Pok%C3%A9mon_by_gender_ratio
genderless_dexnums = [81, 82, 100, 101, 120, 121, 137, 233, 132, 144, 145, 146, 150, 151, 201, 243, 244, 245, 249, 250, 251]

# list of moves with hyphens in the names all in lower case
hyphenated_moves = ["lock-on", "mud-slap", "double-edge", "self-destruct", "soft-boiled"]

# number of pokemon on a given team, usually 6
ruleset_team_size = 6

ev_iv_labels = ['ATK','DEF','HP','SPA','SPD','SPE']


# ----- FUNCTIONS -----


# main function beginning script
def main():

	print("\nStart of script.\n")

	#write_dex_numbers()

	dex_num = 1

	input_loop()

	script_quit()

# input loop that continuously interprets user commands until they quit
def input_loop():

	# welcome/introduction
	print("Welcome to Pokemon Team Maker!")

	# input instructions
	print("\nThe possible commands are:")
	print_list(cmd_list)
	print()

	# accept input
	cmd = input("Please input a command:\n").lower()
	while(cmd != None and cmd != "" and cmd != "quit"):
		interpret_cmd(cmd)
		cmd = input("Please input a command:\n").lower()

# parses string cmd and calls appropriate functions
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

# help function - called to list and desctibe commands
def help():
	print("\nList of commands:")
	for cmd in cmd_list:
		print("\n" + cmd)
		print(help_instructions[cmd] + "\n")
	print()

# quit function - called to close everything out
# quit() is a reserved python function 
def script_quit():
	print("\nEnd of script.\n")
	sys.exit("Script ended by script_quit() call.")

	# should not be reached
	print("\nThe script did not quit successfully.")
	return

# see "readme.txt" and randomize_PKMN() comments for more info on defining ruleset(s)
def ruleset():
	print("\nruleset not yet implemented.\n")

# creates all the teams
# OR 
# rerandom a team
def team_make(replace_team_num = None):
	# build all teams
	if(replace_team_num == None):
		print("Beginning to build a total of " + str(default_num_teams) + " teams.")
		for team_num in range(default_num_teams):
			print("Building team " + str(team_num))
			team = []
			while len(team) < ruleset_team_size:
				pkmn = randomize_PKMN()
				team.append(pkmn)
			teams.append(team)
		#print(teams)
		assert(len(teams) == default_num_teams)
		print("Done building " + str(len(teams)) + " teams.")
		#print(teams)

	# replace a specific team
	"""
	else:
		team = []
		while len(team) < ruleset_team_size:
			pkmn = randomize_PKMN()
			team.append(pkmn)
		teams[replace_team_num] = team
		print("Done replacing team " + replace_team_num + " with a new team.")
	"""

# rerandom a specific pokemon on a specific team
def team_edit(team_num, slot_num):
	print("\nteam_edit not yet implemented.\n")

	"""
	loose algorithm pseudocode:
	pkmn = teams[team_num][slot_num]
	new_pkmn = randomize_PKMN()
	teams[team_num][slot_num] = new_pkmn
	print("Done replacing the Pokemon in slot " + str(slot_num) + " of team " + str(team_num) + " with a new Pokemon.")
	"""

# output the teams to console, copy to clipboard, and output to file(s)
def team_print(team_num = None):

	# generate console output
	out_strs = []
	if(team_num != None):
		pass
		#print only that team
	for team in teams:
		team_str = ""
		for pkmn in team:
			team_str += "\n" + PKMN_dict_to_str(pkmn) + "\n"
		out_strs.append(team_str)
	print_result = ""
	for out_str in out_strs:
		print_result += out_str
	print(print_result)

	# generate PkHex commands to clipboard
	cmd_strs = []
	for team in teams:
		for pkmn_num in range(len(team)):
			pkmn = team[pkmn_num]
			# whitespace is handled by batch handler yes?
			cmd_str = PKMN_dict_to_cmd(pkmn,pkmn_num+1)
			print("This is the current PkHex command for team " + str(team_num) + ":")
			print(cmd_str.split('\n')[2])
			print("Would you like to proceed? (y/n)")
			proceed = input().replace(" ","").lower()
			if(proceed != "y"):
				print("Quitting teamprint.")
				return
			print("Copied command to keyboard.\n")
			cmd_strs.append(cmd_str)
			copy_str_to_clipboard(cmd_str)
		#continue

	# generate output file(s)
	# request team name(s)
	# ensure positions in each list here align, i.e. index 0 is referencing team 1 across all these lists
	"""
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

	#print("\nteam_print not yet implemented.\n")

# ensures that proper input is given to main command functions
# TODO: check is_int here and elsewhere
def team_cmd_input_handling(cmd_list):

	cmd = cmd_list[0]

	subcmd = None

	if cmd == 'teamprint':
		if len(cmd_list) > 1:
			subcmd = cmd_list[1]
		if(subcmd != None):
			if(subcmd == '' or subcmd < 0):
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
		
	print("Subcmd from input handling: " + str(subcmd))
	return subcmd

# generate one random pokemon
# try to use strings (variables/values) congruent w/ PkHex
#TODO: prevent rerandoming same pkmn
def randomize_PKMN():
	pkmn = {}	
	dexnum = get_random_int(1,251)
	while(dexnum in banned_dexnums_list): 
		print("Generated a banned Pokemon: " + banned_dexnums_dict[dexnum][0] + "(" + str(dexnum) + "). Reason for ban: " + banned_dexnums_dict[dexnum][1])
		dexnum = get_random_int(1,251)
	pkmn['dexnum'] = dexnum
	init_static_pkmn_vars(pkmn)
	init_dynamic_pkmn_vars(pkmn)
	return pkmn
	
# stats that are standardized:
# level (100)
# xp (??)
# EVs
# IVs (or if Hidden Power given, randomize HP type but max IVs... user knows HP type???)
# friendship
# held item
# OT (trainer name) and TID (trainer ID)
# PP ups for moves (+3 i believe)
def init_static_pkmn_vars(pkmn):
	pkmn['CurrentLevel'] = 100
	for label in ev_iv_labels:
		pkmn['EV_' + label] = 65535
		pkmn['IV_' + label] = 15
	pkmn['CurrentFriendship'] = 0
	pkmn['HeldItem'] = 0
	#TODO: random TIDs
	pkmn['TID'] = 48011
	#TODO: current player name
	pkmn['OT_Name'] = "Nate"
	#TODO: pp ups


# stats that are randomized:
# dex_number (already given)
# moves
# gender (if that pkmn is not genderless)
# (for fun) - "garble" up the nickname
# (for fun) - isShiny
def init_dynamic_pkmn_vars(pkmn):
	# build moves
	dexnum = pkmn['dexnum']
	pkmn_obj = get_PKMN(dexnum)
	pkmn_name = get_PKMN_name(dexnum)
	print(pkmn_name)
	pkmn_types = pkmn_obj.types
	pkmn_type1 = pkmn_types[0]
	pkmn_type_names = []
	if(len(pkmn_types) > 1):
		pkmn_type2 = pkmn_types[1]
	else:
		pkmn_type2 = None
	pkmn_type1_name = pkmn_type1.type.name.strip().lower()
	if(pkmn_type1_name == "fairy"):
		pkmn_type1_name = "normal"
	pkmn_type_names.append(pkmn_type1_name)
	if(pkmn_type2 != None):
		pkmn_type2_name = pkmn_type2.type.name.strip().lower()
		if(pkmn_type2_name == "fairy"):
			pkmn_type2_name = "normal"
		if(pkmn_type2_name not in pkmn_type_names):
			pkmn_type_names.append(pkmn_type2_name)
		else:
			pkmn_type_names.append("None")
	else:
		pkmn_type_names.append("None")
	print("type 1: " + str(pkmn_type_names[0]))
	print("type 2: " + str(pkmn_type_names[1]))
	moves = get_moves(get_PKMN(dexnum),2,True)
	if(len(moves) < 4):
		#print("init_dynamic_pkmn_vars() failed, not enough moves")
		return
	move_ids = []
	#TODO: prevent dupes here
	for i in range(len(moves)):
		move_id = get_move_id(moves[i])
		move_ids.append(move_id)
	move_names = []
	for i in range(len(moves)):
		move_names.append(get_move_name(moves[i]))
	#print("The pokemon " + str(dexnum) + " can learn the following moves:")
	#print(move_names)
	#print(move_ids)
	#x = input()
	random_indices = []
	i = 0
	used_type_name = ""
	used_move_names = []
	while(len(random_indices) < 4):
		#print(i)
		#print(random_indices)
		random_index = get_random_int(0,len(moves)-1)
		if(random_index in random_indices):
			continue
		move = moves[random_index]
		move_id = get_move_id(move)
		move_obj = client.get_move(move_id)
		move_name = move_obj.name
		if(move_name in used_move_names):
			continue
		move_type_name = move_obj.type.name.strip().lower()
		x = list(vars(move_obj))
		#print(move_name)
		#print(move_type_name)
		# y = input()
		#move_type = moves[random_index].move.type.strip().lower()
		if(i==0 and move_type_name in pkmn_type_names):
			random_indices.append(random_index)
			used_move_names.append(move_name)
			used_type_name = move_type_name
			i += 1
		elif(i==1):
			if(pkmn_type_names[1] != "None"):
				if(move_type_name != used_type_name and move_type_name in pkmn_type_names):
					random_indices.append(random_index)
					used_move_names.append(move_name)
					i += 1
				else:
					pass
			else:
				random_indices.append(random_index)
				used_move_names.append(move_name)
				i += 1
		elif(i>1):
			random_indices.append(random_index)
			used_move_names.append(move_name)
			i += 1

	for i in range(len(random_indices)):
		random_index = random_indices[i]
		move_str = 'Move' + str(i+1)
		pkmn[move_str] = move_ids[random_index]
		print(move_str + ": " + used_move_names[i])
		#pkmn['Move' + str(i+1)] = moves[random_index].move.name
	# select gender
	if(pkmn['dexnum'] in genderless_dexnums):
		pkmn['Gender'] = 2
	else:
		gender_num = get_random_int(0,1)
		# default in case bad random num.. seem to be getting bad output from above line
		if(gender_num != 0 and gender_num != 1):
			pkmn['Gender'] = 1
		# use actual random #
		else:
			pkmn['Gender'] = gender_num
		

# takes the pokemon dict output by randomize_PKMN and turns it into a readable human string
def PKMN_dict_to_str(pd):
	out_str = ""
	dex_num = pd['dexnum']
	pkmn_name = get_PKMN_name(dex_num)
	#nickname = pkmn_name
	out_str += "\n" + pkmn_name + "(#" + str(dex_num) + ") - Lv. " + str(pd['CurrentLevel'])
	for stat in ev_iv_labels:
		out_str += "\n--- EV_" + stat + ": " + str(pd['EV_'+stat])
	for stat in ev_iv_labels:
		out_str += "\n--- IV_" + stat + ": " + str(pd['IV_'+stat])
	out_str += "\n--- CurrentFriendship: " + str(pd['CurrentFriendship'])
	out_str += "\n--- HeldItem: " + str(pd['HeldItem'])
	out_str += "\n--- TID: " + str(pd['TID'])
	out_str += "\n--- OT_Name: " + pd['OT_Name']
	for i in range(1,5):
		move_str = "Move" + str(i)
		out_str += "\n--- " + move_str + ":" + pd[move_str]
	out_str += "\n--- Gender:" + str(pd['Gender'])
	return out_str
	#TODO: ppups and any other additions to props in pkmn dicts from static/dynamic var init functs or elsewhere

# takes the pokemon dict output by randomize_PKMN and turns it into an exeuctable PkHex cmd
def PKMN_dict_to_cmd(pd,slot_num):
	dex_num = pd['dexnum']
	pkmn_name = get_PKMN_name(dex_num)
	out_str = "=Box=1"
	out_str += "\n=Slot="+str(slot_num)
	out_str += "\n.Species=" + str(pd['dexnum'])
	out_str += "\n.Nickname=" + pkmn_name.capitalize()
	#pkmn_name = get_PKMN_name(dex_num)
	out_str += "\n.CurrentLevel=" + str(pd['CurrentLevel'])
	for stat in ev_iv_labels:
		out_str += "\n.EV_" + stat + "=" + str(pd['EV_'+stat])
	for stat in ev_iv_labels:
		out_str += "\n.IV_" + stat + "=" + str(pd['IV_'+stat])
	out_str += "\n.CurrentFriendship=" + str(pd['CurrentFriendship'])
	out_str += "\n.HeldItem=" + str(pd['HeldItem'])
	out_str += "\n.TID=" + str(pd['TID'])
	out_str += "\n.OT_Name=" + pd['OT_Name']
	for i in range(1,5):
		move_str = "Move" + str(i)
		out_str += "\n." + move_str + "=" + pd[move_str]
	out_str += "\n.Gender=" + str(pd['Gender'])
	return out_str
	#TODO: ppups and any other additions to props in pkmn dicts from static/dynamic var init functs or elsewhere

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

	#print("in get_moves()")

	moves = []
	for move in p.moves:
		#print_attributes(move)
		#x = input()
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

def get_move_id(m):
	m_id = m.move.url.split('/')[-2]
	return m_id

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