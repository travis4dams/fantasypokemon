# ----- CREATED BY Nathan Giles 6/30/19 -----
# NOTE: this entire project currently (as of 7.2.19 1:45 AM) is only intended for gen 2 functionality... 
# no pkmn or functionality or attributes beyond gen 2 were included here


# ----- GENERAL TODO LIST ITEMS -----
# see todo.txt


# ----- IMPORTED PACKAGES -----

# project packages
from helper_functions import *
from pglobals import *
from pkmnwrapper import *

# external packages
import sys

# previously used packages (kept for reference's sake)
#import re
#from webrequest import main_request


# ----- FUNCTIONS -----

# entry point of script
def main():
	print("\nStart of script.\n")
	init_vars()
	intf.input_loop()
	script_quit()

# initializes unitialized variables in pglobals, including interface
def init_vars():
	intf = Interface()

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
	if replace_team_num == None:
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
	if team_num != None:
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
			if proceed != "y":
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
		if subcmd != None:
			if(subcmd == '' or subcmd < 0):
				print("Unrecognized input to teamprint: " + str(subcmd))
				return
			if(subcmd > len(teams)):
				print("Team number to teamprint out of range: " + str(subcmd) + ". There are currently only " + len(teams) + "teams.")
				return

	elif cmd == 'teammake':
		if len(cmd_list) > 1:
			subcmd = cmd_list[1]
		if subcmd == '' or subcmd == None or subcmd < 0:
			print("Unrecognized input to teammake: " + str(subcmd))
			return
		if subcmd > len(teams):
			print("Team number to teammake out of range: " + str(subcmd) + ". There are currently only " + len(teams) + "teams.")
			return

	elif cmd == 'teamedit':
		if len(cmd_list) < 3:
			print("Not enough inputs to teamedit: Got " + len(cmd_list) + ", expected 3.")
		# check team_num
		team_num = cmd_list[1]
		if team_num == '' or team_num == None or team_num < 0:
			print("Unrecognized first input to teamedit: " + str(team_num))
			return
		if team_num > len(teams):
			print("Team number to teamedit out of range: " + str(team_num) + ". There are currently only " + len(teams) + "teams.")
			return
		# check slot_num
		team = teams[team_num]
		slot_num = cmd_list[2]
		if slot_num == '' or slot_num == None or slot_num < 0:
			print("Unrecognized second input to teamedit: " + str(slot_num))
			return
		if slot_num > len(team):
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
	while dexnum in banned_dexnums_list: 
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
	if len(pkmn_types) > 1:
		pkmn_type2 = pkmn_types[1]
	else:
		pkmn_type2 = None
	pkmn_type1_name = pkmn_type1.type.name.strip().lower()
	if pkmn_type1_name == "fairy":
		pkmn_type1_name = "normal"
	pkmn_type_names.append(pkmn_type1_name)
	if pkmn_type2 != None:
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
	#TODO: ensure this correctly interacts w/ banned moves and wont cause an infinite loop later
	if len(moves) < 4:
		print("init_dynamic_pkmn_vars() failed, not enough moves")
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
	while len(random_indices) < 4:
		#print(i)
		#print(random_indices)
		random_index = get_random_int(0,len(moves)-1)
		if random_index in random_indices:
			continue
		move = moves[random_index]
		move_id = get_move_id(move)
		move_obj = client.get_move(move_id)
		move_name = move_obj.name
		if move_name in used_move_names:
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