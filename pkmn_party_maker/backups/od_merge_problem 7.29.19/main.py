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
import cmd_interface
from pokedb import *
import ruleset

# external packages
import sys
import colorama
import random

# previously used packages (kept for reference's sake)
#import re
#from webrequest import main_request

# ----- MAIN VARIABLES -----

# team output file variables
out_dir = "teams/" 			# location of
out_prefix = "pkmnteam_"	# filename prefix for all team output files
out_extension = ".txt"		# file type of team output files

# initialize color manager and associated variables
colorama.init()
colors = list(vars(colorama.Fore).values())
CLEAR_SCREEN = '\033[2J'

# team_strs stores 4 strings representing the nicknames of players (aka "trainers") and teams
# team_strs[0] = nickname of player 1
# team_strs[1] = nickname of team 1
# team_strs[2] = nickname of player 2
# team_strs[3] = nickname of team 2
# team_strs initializes to default generic values which may or may not be replaced by user inputs
team_strs = ["Player 1", "Team1", "Player 2", "Team2"]

default_fname1 = "pkmnteam_1_2019-07-17_22.48.59"

default_fname2 = "pkmnteam_2_2019-07-17_22.48.59"

# ----- FUNCTIONS -----

# entry point of program
#TODO: context handling for commands... i.e. teamshow w/ no made teams
#TODO: simplify global variable and initialization design
def main():

	# reset command prompt colors
	reset_style()
	reset_color()

	# generic init message before more "colorful" introduction by cmdintf
	print("\nStart of program.\n")

	# initialize command line interface
	init_vars()
	cmdintf = cmd_interface.CmdInterface() # main interface object (see interface.py)

	# "colorful" welcome message to user
	cmdintf.welcome_message()

	# main input loop
	cmdintf.input_loop()

	# (should not be reached - cmdintf.input_loop should handle quit command)
	print("\nEnd of program by main().\n")
	assertd(False,"Should not be reached")
	squit()

# setups any relevantvariables from pglobals
# ... I originally tried to have some of the asserts in pglobals.py but that was causing recursive import problems I think
# init_vars() could be split into check_vars() which would only be called if(DEBUG)
#TODO: 	this is not interacting with global variables as expected. 
# 		instead it seems simpler to just initialize global variables in the global namespace (i.e. above "main variables" area)
def init_vars():

	# setup and check ruleset
	global rs
	rs = ruleset.Ruleset()
	assertd(num_required_legendaries <= ruleset_team_size and num_required_legendaries <= 6)

	# check Pokepy client
	assertd(client != None and isinstance(client, pokepy.api.V2Client),"PokePy client did not initialize correctly.")
	
	#TODO: 	check other vars from pglobals.py, so if something is changed there to a bad value, this will catch it 
	# 		rather than not being noticed or being hidden amongst some other error
	#load_full_moves()

# generates a quick randomly generated team with  for testing purposes
def get_test_teams():
	printd("Generating test teams...")
	global teams
	for team_num in range(2):
		team = []
		for slot_num in range(6):
			team.append(randomize_PKMN([],False,False))
		teams.append(team)
	printd("Done generating test teams.")

# help function - called to list and desctibe commands
def help(cmdintf):
	print("\nList of commands:")
	for cmd in cmdintf.base_cmd_list:
		print("\n" + cmd)
		print(cmdintf.help_instructions[cmd] + "\n")
	print()

# "script quit" function - called to close everything out
# quit() is a reserved python function 
def squit(quit_msg = None):

	# quit by sys.exit and display quit_msg if any
	if(quit_msg != None and is_str(quit_msg)):
		sys.exit(quit_msg)
	else:
		sys.exit("Script ended by squit() call.")

	# should not be reached
	print("\nThe script did not quit successfully.")
	assertd(False,"Should not be reached")
	return

# ruleset function - used to describe/edit rulesets
# see "readme.txt" and randomize_PKMN() comments for more info on defining ruleset(s)
def ruleset_cmd():
	print("\nruleset not yet implemented.\n")

"""
# TODO: workaround function for proper OOP around rulesets and global variables
def get_ruleset():
	global rs
	return rs
"""

# teammake function - use to either creates all the teams OR rerandom a given team
def team_make(replace_team_num = None):

	# global variables - not sure this is necessary?
	global teams
	global rs
	global num_required_legendaries

	# check parameter(s)
	assertd(replace_team_num == None or 
		( is_int(replace_team_num) and replace_team_num >= 0 and replace_team_num < len(teams)), 
		"Bad input to team_make(): " + str(replace_team_num))

	# build all teams
	if replace_team_num == None:
		print("Beginning to build a total of " + str(default_num_teams) + " teams...")

		start = get_time()

		# build each team
		for team_num in range(default_num_teams):
			print("Building team " + str(team_num+1) + "...")
			team = []
			team_ids = []

			# build team until team size requirement met
			while len(team) < ruleset_team_size:
				#printd("loop start")
				# random a pkmn and add it to team
				if len(team) < num_required_legendaries:
					# force rolling a legendary until we satisfy legendary requirement (if any)
					pkmn = randomize_PKMN(team_ids, True)
				else:
					pkmn = randomize_PKMN(team_ids, False)
				team.append(pkmn)
				team_ids.append(pkmn.get_dexnum())

				assertd(len(team) <= ruleset_team_size)
				assertd(len(team_ids) <= ruleset_team_size)

				# if the team is built (about to exit loop), check that it meets the type requirement (no more than 2 pkmn share a type)
				# if yes, continue
				# if no, randomly choose a pkmn among those of the type with too many pokemon, and rerandom that pokemon
				# TODO: we may wanna check any rules that just deal with dex_nums before calculating movesets, 
				# so we arent wasting time building moves just to be rerandomed
				if len(team) == ruleset_team_size:
					team = check_and_update_team(team)

				#printd("loop end")

			teams.append(team)

		# check and return output
		assertd(len(teams) == default_num_teams, 
			"team_make assumes it completed successfuly but did not create the correct number of teams.")

		end = get_time()
		elapsed_time = round(end - start)

		print("\nteammake done building " + str(len(teams)) + " teams after " + str(elapsed_time) + " seconds.\n")

		#TODO: consistent use of player/trainer var name
		player1_name_input = input("Who is player 1?:\n")
		player1_name_input_formatted = player1_name_input.strip()
		if player1_name_input_formatted != "":
			team1_name_input = input(player1_name_input_formatted + ", do you have a name for your team?:\n")
		else:
			team1_name_input = input("Do you have a name for team 1?:\n")

		player2_name_input = input("Who is player 2?:\n")
		player2_name_input_formatted = player2_name_input.strip()
		if player2_name_input_formatted != "":
			team2_name_input = input(player2_name_input_formatted + ", do you have a name for your team?:\n")
		else:
			team2_name_input = input("Do you have a name for team 2?:\n")

		global team_strs
		team_strs = [player1_name_input_formatted, team1_name_input.strip(), player2_name_input_formatted, team2_name_input.strip()]

		# save and show after building a team
		team_save()
		team_show()

	#printd("team_make end")

	#TODO: replace a specific team
	"""
	else:
		team = []
		while len(team) < ruleset_team_size:
			pkmn = randomize_PKMN()
			team.append(pkmn)
		teams[replace_team_num] = team
		print("Done replacing team " + replace_team_num + " with a new team.")
	"""

#TODO: fix this lol
def check_and_update_team(team):
	return team

	"""
	# type_name_stats maps a type name (i.e. "Fire") to the a list with [<count>, <indices_list>]
	# where count is the number of pokemon in the team that have that type
	# and indices_list is a list of the indices where that type occurs in the team
	#TODO: it might be easier to just track the positions within team for the pkmn of that type... count is redundant w/ len of that list
	type_name_stats = {}

	#printd(team)

	#input()

	for i in range(len(team)):
		pkmn = team[i]
		dex_num = pkmn['dexnum']
		pkmn_obj = get_PKMN(dex_num)
		type_names = get_type_names(pkmn_obj)
		type_name1 = type_names[0]
		type_name2 = type_names[1]
		#TODO: assert=d is a type string, len != 0, etc
		assertd(is_str(type_name1) and type_name1 != "None")
		assertd(is_str(type_name2))
		if(not type_name1 in type_name_stats):
			type_name_stats[type_name1] = [1,[dex_num]]
		else:
			type_count = type_name_stats[type_name1][0]
			existing_ids = type_name_stats[type_name1][1]
			type_name_stats[type_name1][0] = type_count+1
			existing_ids.append(dex_num)
		if type_name2 != "None":
			if not type_name2 in type_name_stats:
				type_name_stats[type_name2] = [1,[dex_num]]
			else:
				type_count = type_name_stats[type_name2][0]
				existing_ids = type_name_stats[type_name2][1]
				type_name_stats[type_name2][0] = type_count+1
				existing_ids.append(dex_num)

	#printd(type_name_stats)

	#input()

	# go through all the types that we have, if we have one more than twice, randomly reselect one of the "offenders"
	# this "reslect" occurs by replacing team with a new list that excludes these pokemon, then repeats the loop
	# rerandom_ids contains the dex_nums of the pokemon to exclude from the new list
	rerandom_ids = []
	for type_name in type_name_stats:
		# count is the number of times this stat has occured in the team
		count = type_name_stats[type_name][0]
		if(is_positive_int(ruleset_repeated_types) and count > ruleset_repeated_types):
			type_ids = type_name_stats[type_name][1]
			# i.e. if we have 4 fire types but are allowed no more than 2 of a type, excess_count = 2
			# i.e. if we have 3 fire types but are allowed no more than 1 of a type, excess_count = 2
			excess_count = count - ruleset_repeated_types
			for rerandom_count in range(excess_count-1):
				i = get_random_int(0,len(type_ids)-1)
				rerandom_id = type_ids[i]
				if not rerandom_id in rerandom_ids:
					rerandom_ids.append(rerandom_id)
				del type_ids[i]

	if(len(rerandom_ids) == 0):
		return team

	#printd(rerandom_ids)

	#input()

	team_update = []
	for pkmn in team:
		dex_num = pkmn['dexnum']
		if not dex_num in rerandom_ids:
			team_update.append(pkmn)
		#else:
			#printd("dex_num " + str(dex_num) + " is getting rerolled.")

	return team_update

	printd(team_copy)

	input()
	"""

# rerandom a specific pokemon on a specific team
def team_edit(team_num, slot_num, is_legendary = False):
	global teams
	assertd(is_int(team_num) and team_num >= 0 and team_num < len(teams))
	assertd(is_int(slot_num))

	teams_len = len(teams)
	assertd(team_num < teams_len)

	team = teams[team_num]
	assertd(is_list(team))
	team_len = len(teams)
	assertd(slot_num < team_len)

	print("Replacing the Pokemon in slot " + str(slot_num) + " of team " + str(team_num) + " with a new Pokemon...")

	replaced_pkmn = teams[team_num][slot_num]
	team_ids = []
	# this assumes you CAN rerandom the same pokemon with team_edit
	for i in range(len(team)):
		if i != slot_num:
			team_ids.append(team[i]['dexnum'])
	teams[team_num][slot_num] = randomize_PKMN(team_ids, is_legendary)

	print("Done replacing.")

	"""
	loose algorithm pseudocode:
	pkmn = teams[team_num][slot_num]
	new_pkmn = randomize_PKMN()
	teams[team_num][slot_num] = new_pkmn
	
	"""

# output the teams to console
# TODO: rather than using a global var for team_strs, change team_show and team_make so it handles inputs w/ cmdintf correctly... 
# TODO: ... also input handling and debugging asserts etc on team_strs here and elsewhere
def team_show(team_num = None):

	# load and check teams list
	global teams
	printd(teams)
	"""
	if(len(teams)==0):
		print("\nThere are no teams to print.\n")
		return
	"""

	global team_strs
	parse_team_strs_list = len(team_strs) == 4
	#printd(team_strs)
	#printd(parse_team_strs_list)

	# generate console output
	#out_strs = []
	if team_num != None:
		return
		#print only that team
	
	# build output string
	out_str = ""
	for i in range(len(teams)):
		team = teams[i]

		# parse trainer name if any
		trainer_name = ""
		trainer_name_postfix = ""
		# trainer name is specified
		if parse_team_strs_list and team_strs[(i*2)+1] != "":
			trainer_name = team_strs[(i*2)+1]
			trainer_name_postfix = "\'s "

		# parse team name if any
		team_name = ""
		# team name is specified
		if parse_team_strs_list and team_strs[i*2] != "":
			team_name = "\"" + team_strs[i*2] + "\""
		# team name is not specified, but trainer name is
		elif trainer_name != "":
			team_name = "team"
		# team and trainer names are not specified - give a generic name for the team
		else:
			team_name = "Team " + str(i+1)
		out_str += "\n\n" + team_name + ":"

		#printd(trainer_name)
		#printd(team_name)
		#printd(out_str)

		pkmn_names = []
		pkmn_types = []
		pkmn_moves = []
		for j in range(len(team)):
			pkmn = team[j]
			pkmn_str = PKMN_dict_to_str(pkmn)
			pid = pkmn.get_dexnum()
			#pkmn_name = get_PKMN_name(pid)
			pkmn_name = get_PKMN_name(pid) + " [#" + str(team[j]['dexnum']) + "]"
			pkmn_names.append(pkmn_name)		
			pkmn_type_name = pkmn_str[pkmn_str.index('('):pkmn_str.index(')')+1]
			"""
			pkmn_type_name_split = pkmn_type_name.replace(' ','').split(',')
			if len(pkmn_type_name_split) == 2:
				first_type_name = pkmn_type_name_split[0]
				second_type_name = pkmn_type_name_split[1]
				pkmn_type_name_new = get_type_color(first_type_name) + first_type_name + get_all_resets() + ", " + get_type_color(second_type_name) + second_type_name + get_all_resets()
			else:
				first_type_name = pkmn_type_name_split[0]
				pkmn_type_name_new = get_type_color(first_type_name) + first_type_name + get_all_resets()
			pkmn_type_name_final = "(" + pkmn_type_name_new + ")"
			"""
			pkmn_types.append(pkmn_type_name)
			#printd(pkmn_type_name)
			pkmn_move_strs = pkmn_str[pkmn_str.index('{')+1:pkmn_str.index('}')].split(', ')
			for pkmn_move_str in pkmn_move_strs:
				pkmn_moves.append(pkmn_move_str.lower())
			"""
			pkmn_move_strs = pkmn_str[pkmn_str.index('{'):pkmn_str.index('}')+1].split(', ')
			for pkmn_move_str in pkmn_move_strs:
				pkmn_moves.append(pkmn_move_str)
			"""
			printd(pkmn_move_strs)
			printd(pkmn_moves)
			input()
			for k in range(len(pkmn_moves)):
				pkmn_move_name = pkmn_moves[k]
				#out_str = ""
				#if k == 0:
				#	out_str += "{"
				m = get_move_by_name(pkmn_move_name)
				#printd(m)
				mtypename = m.type.name # name of the move's type, i.e. m == Fire Blast --> mtypename == "Fire"
				#printd(mtypename)
				type_color_str = get_type_color(mtypename)
				#printd(type_color_str)
				colored_str = type_color_str + pkmn_move_name + get_all_resets()
				#if k == len(pkmn_move_strs)-1:
				#	out_str += "}"
				pkmn_moves[k] = colored_str

		#printd(pkmn_names)
		#printd(pkmn_types)
		#printd(pkmn_moves)
		tab_format(pkmn_names)
		tab_format(pkmn_types)
		tab_format(pkmn_moves)

		for i in range(len(pkmn_types)):
			for base_pkmn_type_str in type_names:
				if base_pkmn_type_str in pkmn_types[i]:
					type_index = pkmn_types[i].index(base_pkmn_type_str)
					substr = pkmn_types[i][type_index:type_index+len(base_pkmn_type_str)]
					#printd(substr)
					#replace_str = color_str(substr,get_type_color(substr))
					pkmn_types[i] = pkmn_types[i].replace(substr,get_type_color(substr) + substr + get_all_resets())
			

		#printd(pkmn_names)
		#printd(pkmn_types)
		#printd(pkmn_moves)
		for j in range(len(team)):
			move_str = ""
			for k in range(j*4,(j*4)+4):
				if k == 0:
					move_str += "{"
				move_str +=  pkmn_moves[k]
				# if end of loop
				if k == (j+4)+4:
					move_str += "}"
			#out_str += "\n" + pkmn_names[j].title() + "[#" + str(team[j]['dexnum']) + "]\t" + pkmn_types[j] + " " + move_str
			#out_str += "\n" + pkmn_names[j].title() + "\t" + pkmn_types[j] + " " + move_str
			out_str += "\n" + str(j) + ": " + pkmn_names[j].title() + pkmn_types[j] + move_str
	
	print(out_str)

	"""
	print_result = ""
	for out_str in out_strs:
		print_result += out_str
	print(print_result)		
	"""

	print("\nteamshow complete.\n")

	#print("\teamshow not yet implemented.\n")

# generate PkHex commands to clipboard
def team_copy():

	team1_cmd_strs, team2_cmd_strs = get_cmd_strs(True)
	assertd(len(team1_cmd_strs) == len(team2_cmd_strs))

	"""
	team1_cmd_strs = []
	team2_cmd_strs = []
	#cmd_strs = []
	for team_num in range(len(teams)):
		team = teams[team_num]
		print("Preparing commands for team " + str(team_num))
		for pkmn_num in range(len(team)):
			pkmn = team[pkmn_num]
			# whitespace is handled by batch handler yes?
			cmd_str = PKMN_dict_to_cmd(pkmn,pkmn_num+1)
			#print("This is the current PkHex command for team " + str(team_num) + ":")
			#print(cmd_str.split('\n')[2])
			print("Entering anything besides \"quit\" will copy the command for pokemon #" + str(pkmn_num))
			proceed = input().replace(" ","").lower()
			if proceed == "quit":
				print("Quitting teamshow.")
				return
			print("Copied command to keyboard.\n")
			if(team_num == 0):
				team1_cmd_strs.append(cmd_str)
			else:
				team2_cmd_strs.append(cmd_str)
			copy_str_to_clipboard(cmd_str)
		#continue
	"""


# generate output file(s)
# generate folder name based on this time stamp
# request team name(s)
# ensure positions in each list here align, i.e. index 0 is referencing team 1 across all these lists
# TODO: implement team_strs to team_save
def team_save():
	#assertd(len(cmd_strs) == len(teams) * ruleset_team_size)
	#assertd(len(out_strs) == len(teams))
	team1_cmd_strs, team2_cmd_strs = get_cmd_strs(False)
	assertd(len(team1_cmd_strs) == len(team2_cmd_strs))
	output_team_file(team1_cmd_strs, "1")
	output_team_file(team2_cmd_strs, "2")
	print("\nteamsave complete\n")
	"""
	for i in range(len(teams)):
		team = teams[i]
		team_str = out_strs[i]
		print("Ouputting file for team " + str(i))
		if(i == 0):
			output_team_file(team1_cmd_strs, i)
		else:
			output_team_file(team2_cmd_strs, i)
	"""

# returns two lists of command strings, one for team1 and one for team2
# if copy_and_halt is True, it will copy to the user's clipboard and wait for input before proceeding
# this most handles all of get_copy(), but much of this functionality is also used by team_save() 
# so I figure its better to keep the function in one place
def get_cmd_strs(copy_and_halt = True):
	global teams
	team1_cmd_strs = []
	team2_cmd_strs = []
	for team_num in range(len(teams)):
		team = teams[team_num]
		for pkmn_num in range(len(team)):
			pkmn = team[pkmn_num]
			cmd_str = PKMN_dict_to_cmd(pkmn,pkmn_num+1)
			if(team_num == 0):
				team1_cmd_strs.append(cmd_str)
			else:
				team2_cmd_strs.append(cmd_str)

			if copy_and_halt:
				#print("This is the current PkHex command for team " + str(team_num) + ":")
				#print(cmd_str.split('\n')[2])
				print("Entering anything besides \"quit\" will copy the command for pokemon #" + str(pkmn_num))
				proceed = input().replace(" ","").lower()
				if proceed == "quit":
					print("Quitting teamshow.")
					return
				print("Copying command to keyboard...")
				copy_str_to_clipboard(cmd_str)
				print("Copied.\n")
	assertd(len(team1_cmd_strs) == len(team2_cmd_strs))
	return team1_cmd_strs, team2_cmd_strs

# load the two teams, each from one of the two supplied output file(s)
def team_load(fname1, fname2):

	for i in range(2):

		current_pkmn = {}
		current_team = []	

		if i == 1:
			fname = fname1
		else:
			fname = fname2 

		if fname == "default":
			if i == 1:
				f = open("teams/" + default_fname1 + out_extension,"r+")
			else:
				f = open("teams/" + default_fname2 + out_extension,"r+")
		else:
			f = open("teams/" + fname + out_extension,"r+")

		for line in f:
			line_formatted = line[1:len(line)-1].strip()
			line_split = line_formatted.split("=")
			
			"""
			if line[0] == "=":
				line_split = line_formatted.split("=")
			elif line[0] == ".":
				line_split = line_formatted.split(".")
			else:
				# unrecognized line
				continue
			printd(line_split)
			"""

			key_str = line_split[0]
			val_str = line_split[1]
			if val_str.isdigit():
				val = int(val_str)
			else:
				val = val_str

			# if we encounter a key_str thats already in our current pokemon, we assume this means we've reached a new pokemon
			# so add the current one to team and proceed
			if key_str in current_pkmn:
				current_team.append(current_pkmn)
				current_pkmn = {}
				continue
			elif key_str == 'Species':
				current_pkmn['dexnum'] = val
			elif "Move" in key_str:
				move_obj = client.get_move(val)		
				move_name = move_obj.name
				current_pkmn[key_str] = [val, move_name]
			else:
				current_pkmn[key_str] = val

			"""
			# the way this is implemented, we build a pokemon until we encounter a new one in the text then add it to the team, 
			# so we don't need slot to index into the team1/team2 lists or anything
			if key_str == "slot":
				pass

			elif key_str == "species":
				current_pkmn['dexnum'] = val_str

			elif key_str == "currentlevel":
				current_pkmn['CurrentLevel'] = val_str

			elif key_str == "":

			else:
				continue
			"""

		teams.append(current_team)

# generate one random pokemon
# try to use strings (variables/values) congruent w/ PkHex
# used by team_make() and get_test_teams()
#TODO: prevent rerandoming same pkmn
#TODO: this could be optimized by 
def randomize_PKMN(existing_team_ids = [], is_legendary = False, enforce_ruleset = True):
	
	# generate the dexnum according to any ruleset restrictions then pass that along to create_pkmn
	# retrieve relevant ruleset attributes
	# TODO: doing this all at once could improve performance over constnatly retrieving these from rs obj ... though maybe theyre cached (??)
	global rs
	banned_dexnums_list = rs.banned_dexnums_list
	underevolved_dexnums_list = rs.underevolved_dexnums_list
	legendary_dexnums_list = rs.legendary_dexnums_list		

	# default case
	if not is_legendary:
		dexnum = get_random_int(1,251)
		#TODO: this could be optimized by only generating random numbers that wouldnt result in a "collision" with these lists
		# 		ideally if such a list were to be built it would be not be built with every call to this function, 
		# 		but once before a series of calls to this function
		while dexnum in existing_team_ids or dexnum in banned_dexnums_list or dexnum in underevolved_dexnums_list: 
			#print("Generated a banned Pokemon: " + banned_dexnums_dict[dexnum][0] + "(" + str(dexnum) + "). Reason for ban: " + banned_dexnums_dict[dexnum][1])
			dexnum = get_random_int(1,251)

	# forced legendary case
	else:
		random_index = get_random_int(0,len(legendary_dexnums_list)-1)
		dexnum = rs.legendary_dexnums_list[random_index]
	return create_pkmn(dexnum,enforce_ruleset)
	
# creates pkmn dict for PkHex/str output
# called only by randomize_PKMN as of now
def create_pkmn(dexnum, enforce_ruleset = True):
	pkmn = {}
	pkmn['dexnum'] = dexnum
	init_static_pkmn_vars(pkmn)
	init_dynamic_pkmn_vars(pkmn, enforce_ruleset)
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
	for label in stat_labels:
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
#TODO: there is probably a "generated n random indices into a list of length m" python function out there which would simplify this
# 		see "random.choice(list)" https://stackoverflow.com/questions/46425645/python-make-every-character-line-random-color-print
def init_dynamic_pkmn_vars(pkmn, enforce_ruleset = True):
	
	# --- get pokemon info ---
	dexnum = pkmn['dexnum']
	pkmn_obj = get_PKMN(dexnum)
	pkmn_name = get_PKMN_name(dexnum)
	pkmn_type_names = get_type_names(pkmn_obj)
	

	# --- select gender ---
	# TODO - this doesnt seem to be working properly
	if(pkmn['dexnum'] in genderless_dexnums):
		pkmn['Gender'] = 2
	else:
		gender_num = get_random_int(0,1)
		assertd(gender_num == 0 or gender_num == 1,"Bad gender_num generated in init_dynamic_pkmn_vars().")
		pkmn['Gender'] = gender_num		


	"""
	# print the types
	if(pkmn_type_names[1]!="None"):
		print("\nGenerated pokemon: " + pkmn_name.title() + " (" + str(pkmn_type_names[0]).capitalize() + ", " +  str(pkmn_type_names[1]).capitalize() + ")")
	else:
		print("Generated pokemon: " + pkmn_name.title() + " (" + str(pkmn_type_names[0]).capitalize() + ")")
	"""

	# --- setup moves ---

	# retrieve ALL possible learnable moves
	# note that by this point, we shouldnt have "banned" pokemon like magikarp, so if we remove banned moves, 
	# there should still be more than 4 learnable moves leftover
	#printd("Getting learnable moves...")
	moves = get_moves(get_PKMN(dexnum),2,True)
	#printd("Got learnable moves.")
	#print("This pokemon can learn " + str(len(moves)) + " moves.")

	# build move_ids and move_names lists
	# these lists should be aligned AND
	# these lists exclude "banned" moves (this loop removes them from moves)
	# doing it all in one loop should align them but...
	# TODO: check alignment (name/id/object match at each index of each list, sizes the same, etc)
	# TODO: ensure this correctly interacts w/ banned moves and wont cause an infinite loop later
	# TODO: perhaps clarify get_moves... is it get learnable moves or get tourney moves? all move processing should be done in one place if possible
	legal_moves = []
	move_ids = []
	move_names = []
	# move_type_names is a list (effectively functions as set tho) of types that have at least 1 move associated with them in this moveset
	#TODO: this would more properly be a set i believe
	#TODO: could potentailly quit a little earleir if you have like 3 moves generated and you need fire and flying moves but none of your moves are fire/flying you might as well restart the moveset
	#TODO: rename to learnable_move_type_names
	move_type_names = []
	# type1_move_names and type2_move_names contain the names of all the learnable moves that are of the pokemon's type 1 and type 2 respectively
	# if the pokemon has no second type, type2_move_names will be an empty list
	type1_moves = []
	type2_moves = []
	global rs
	#print("building moves list...")
	#TODO: should "get_move_names()" be called here instead?
	for i in range(len(moves)):
		move = moves[i]
		move_id = get_move_id(move)
		#print("move id: " + str(move_id))
		if(move_id in rs.banned_move_ids_list):
			#print("move id in banned_ids_list")
			continue
		move_name = get_move_name(move)
		#TODO: why cant we just use move here instead of client.get_move(move_id)?
		move_type_name = client.get_move(move_id).type.name.strip().lower() 
		if(not move in legal_moves and not move_id in move_ids and not move_name in move_names):
			#print("successfully added move named " + move_name)
			legal_moves.append(move)
			move_ids.append(move_id)
			move_names.append(move_name)
			# this should not be added to the above if statement because its ok to generate two moves of the same type
			if not move_type_name in move_type_names:
				move_type_names.append(move_type_name)
			if move_type_name == pkmn_type_names[0]:
				type1_moves.append(move)
			elif pkmn_type_names[1] != "None" and move_type_name == pkmn_type_names[1]:
				type2_moves.append(move)
		#else:
			#print("move, name or id already in existing list")

	# sanity check
	legal_moves_len = len(legal_moves)
	move_ids_len = len(move_ids)
	move_names_len = len(move_names)
	assertd(legal_moves_len == move_ids_len)
	assertd(legal_moves_len == move_names_len)
	# assertd(move_ids_len == move_names_len) # this check technically not necessary... if a = b and a = c then b = c
	# TODO: assert len move_type_names > 0 ... could have all 4 moves of same type for monotype pokmn... if dual type pkmn move_type_names should have len >= 2
	# note that len of move_type_names doesnt need to be the same as other lists, since it is just the set of types used across all moves, not a type for each move
	
	# ensure we have enough moves to work with
	if len(legal_moves) < 4:
		print("init_dynamic_pkmn_vars() failed, not enough moves")
		return

	if(not enforce_ruleset):
		# enforce default case of generate_moves by giving no type list, so they just generate random moves
		# TODO: once "ruleset" is more properly defined in OOP, this should be much cleaner
		generated_moves, generated_move_ids, generated_move_names = generate_moves(moves, [], [])
		assertd(len(generated_moves) == len(generated_move_ids))
		assertd(len(generated_moves) == len(generated_move_names))
		for i in range(len(generated_move_ids)):
			move_prefix = 'Move' + str(i+1)
			pkmn[move_prefix] = (generated_move_ids[i], generated_move_names[i])
		return
	
	# check that our ruleset condition of "have at least one move of each of its types" is even feasible for this pokemon
	# if not, enforce no type restrictions on the moveset (banned moves and other restrictions (such as...??) may still apply)
	# NOTE: we want to make this type restriction check AFTER the learnable moveset has been filtered down to the pool of moves we actually use
	# we wouldn't want to check this before removing banned moves, pass the check and assume its feasible, then its not after banned removals...
	#TODO: change it to requiring as many types as it CAN satisfy (<-- ... I think this comment is no longer applicable...?)
	#TODO: change "moves" and similar lists to learnable moves ... rename vars
	if pkmn_type_names[0] in move_type_names and (pkmn_type_names[1]=="None" or pkmn_type_names[1] in move_type_names):
		type_restriction = True
	else: 
		#print("This pokemon cannot meet the move type restriction.")
		type_restriction = False

	# generate some moves and check any rulesets; if they aren't acceptable rerandom
	successful_moves = False
	moveset_attempts = 0
	while not successful_moves:
		# attempt to generate some moves
		generated_moves, generated_move_ids, generated_move_names = generate_moves(legal_moves, type1_moves, type2_moves)

		# check that at least 1 move from each of the pokemon's types are here
		#TODO: have generate_moves return list of type names instead of essentially rebuilding it here
		generated_move_type_names = []
		for i in range(len(generated_moves)):
			generated_move = generated_moves[i]
			move_id = get_move_id(generated_move)
			move_obj = client.get_move(move_id)
			move_type_name = move_obj.type.name.strip().lower()
			generated_move_type_names.append(move_type_name)
		
		# check types
		#print(pkmn_type_names)
		#print(generated_move_names)
		#print(generated_move_type_names)
		#x = input()
		if type_restriction:
			if pkmn_type_names[0] in generated_move_type_names and (pkmn_type_names[1] == "None" or pkmn_type_names[1] in generated_move_type_names):
				successful_moves = True
		else:
			successful_moves = True

		moveset_attempts += 1

	#print("Successfully generated a moveset after " + str(moveset_attempts) + " attempts.")
	# print("Generated moveset: " + str(generated_move_names) + "\n")

	# set Move1, Move2, Move3, Move4 entries of pkmn dict
	for i in range(len(generated_move_ids)):
		move_prefix = 'Move' + str(i+1)
		pkmn[move_prefix] = (generated_move_ids[i], generated_move_names[i])

	#print("\n" + str(generated_moves))

	

	# comment dump for function
	"""
	print(move_name)
	print(random_index)
	print(used_move_names)
	print(attempted_move_names)
	print(random_indices)
	input()

	#print("The pokemon " + str(dexnum) + " can learn the following moves:")
	#print(move_names)
	#print(move_ids)
	#x = input()

	#print(move_name)
	#print(move_type_name)
	# y = input()
	#move_type = moves[random_index].move.type.strip().lower()

	#print()
	#print(move_str + ": " + used_move_names[i])
	#pkmn['Move' + str(i+1)] = moves[random_index].move.name
	"""

# helper function to generate a set of 4 moves
# this may be called repeatedly until the move set meets the ruleset requirements
def generate_moves(move_list, type1_moves, type2_moves):
	# random_indices is a list of length 4 containing randomly generated numbers that index into the moves lists (thus ranging from 0 to len(moves))
	# ... i think there is a simpler way that doesn't use this
	# random_indices = []

	# the generated_move lists below represent the moves we have currently generated
	# names contains string names, ids contains ids (as with move lists above)
	generated_moves = []
	generated_move_ids = []
	generated_move_names = []
	# move_slot represents the index into generated_moves we are CURRENTLY trying to build; it also represents the # of generated moves
	move_slot = 0
	# first_move_type_name the type name (i.e. "Fire") of the first move this Pokemon is set to learn 
	#first_move_type_name = ""	
	# tracked for performance analysis purposes
	iterations = 0
	#TODO: this algorithm sucks i did it drunk with travis lol
	#		could check that the type requirement is even "meetable" in this area, i had that on todo list
	#TODO: could update the moves list so the RNG gets an updated length and cant generate bad #s? idk
	while len(generated_moves) < 4:
		#TODO: if we tried generating a move on THiS "i", store it in attempted_move_names
		#NOTE: the copy call is important, or else changes to attempted_move_names will be made to used_move_names and vice versa (pointers!)

		# attempted_move_names contains the move names we have attempted for THIS slot
		# if we have tried the move for an earlier slot though (thus in generated_move_names), we shouldn't attempt it again
		attempted_move_names = generated_move_names.copy()

		# select first move among learnable type1 moves (if any)
		if move_slot == 0 and len(type1_moves) != 0:
			random_index = get_random_int(0,len(type1_moves)-1)
			move = type1_moves[random_index]
		# select second move among learnable type2 moves (if any)
		elif move_slot == 1 and len(type2_moves) != 0:
			random_index = get_random_int(0,len(type2_moves)-1)
			move = type2_moves[random_index]
		# default case
		else:
			random_index = get_random_int(0,len(move_list)-1)
			move = move_list[random_index]
		
		#if random_index in random_indices:
		#	continue
		
		if(move in generated_moves):
			continue
		move_id = get_move_id(move)
		if(move_id in generated_move_ids):
			continue
		# ... is the type of move and move_obj different here...?
		move_obj = client.get_move(move_id)
		
		move_name = move_obj.name

		# regardless of whether this move succeeds, add it to attempted list so we won't attempt it again until a succesful move is made
		# (for example, on first generation we may need to make a rock throw)
		# TODO: im not sure whether adding to attempted_move_names
		if(move_name in attempted_move_names):
			#print("continue case 2")
			continue
		attempted_move_names.append(move_name)

		if(move_name in generated_move_names):
			continue

		# print the moves as they are generated
		#print(move_name, end=" ")

		
		# TODO: consider statistical implications or just difference in perforamcen etc... compare these two approaches:
		# 		approach 1: requring move type A on roll 1, then move type B (if any) on roll 2
		#		OR
		#		approach 2: generate moveset, and if type A and type B in the moveset, pass, otherwise reroll
		generated_moves.append(move)
		generated_move_ids.append(move_id)
		generated_move_names.append(move_name)
		move_slot += 1
		iterations += 1

		"""
		move_type_name = move_obj.type.name.strip().lower()
		if(move_slot==0 and move_type_name in pkmn_type_names):
			random_indices.append(random_index)
			used_move_names.append(move_name)
			used_type_name = move_type_name
			attempted_move_names = used_move_names.copy()
			move_slot += 1
		elif(move_slot==1):
			if(pkmn_type_names[1] != "None"):
				if(move_type_name != used_type_name and move_type_name in pkmn_type_names):
					random_indices.append(random_index)
					used_move_names.append(move_name)
					move_slot += 1
				else:
					pass
			else:
				random_indices.append(random_index)
				used_move_names.append(move_name)
				attempted_move_names = used_move_names.copy()
				move_slot += 1
		elif(move_slot>1):
			random_indices.append(random_index)
			used_move_names.append(move_name)
			attempted_move_names = used_move_names.copy()
			move_slot += 1
		"""

	assertd(len(generated_moves) == 4)
	assertd(len(generated_move_ids) == 4)
	assertd(len(generated_move_names) == 4)

	#printd("generate_moves() had " + str(iterations) + " iterations before returning an attempted moveset.")

	return generated_moves, generated_move_ids, generated_move_names


# takes the pokemon dict output by randomize_PKMN and turns it into a readable human string
# this is used in the command line and in output files
def PKMN_dict_to_str(pd):
	#printd(pd)
	out_str = ""
	dex_num = pd['dexnum']
	pkmn_name = get_PKMN_name(dex_num)
	pkmn_obj = get_PKMN(dex_num)
	type_names = get_type_names(pkmn_obj)
	if(type_names[1] == "None"):
		type_str = "(" + type_names[0].capitalize() + ")"
	else:
		type_str = "(" + type_names[0].capitalize() + ", " + type_names[1].capitalize() + ")"
	#nickname = pkmn_name
	out_str += pkmn_name.title() + " [#" + str(dex_num) + "]\t" + type_str + " {"
	#out_str += "\n" + pkmn_name.title() + " (#" + str(dex_num) + ")"
	#out_str += "\n" + pkmn_name.title() + " (#" + str(dex_num) + ") - Lv. " + str(pd['CurrentLevel'])
	# exclude static variables from output since these are constant across all pokemon
	"""
	for stat in stat_labels:
		out_str += "\n--- EV_" + stat + ": " + str(pd['EV_'+stat])
	for stat in stat_labels:
		out_str += "\n--- IV_" + stat + ": " + str(pd['IV_'+stat])
	out_str += "\n--- CurrentFriendship: " + str(pd['CurrentFriendship'])
	out_str += "\n--- HeldItem: " + str(pd['HeldItem'])
	out_str += "\n--- TID: " + str(pd['TID'])
	out_str += "\n--- OT_Name: " + pd['OT_Name']
	"""
	for i in range(1,5):
		move_prefix = "Move" + str(i)
		#move_id = pd[move_prefix][0]
		move_name = pd[move_prefix][1].replace("-"," ").title()
		#out_str += "\n--- " + move_prefix + ": " + move_name
		if i != 4:
			out_str += move_name + ", "
		else:
			out_str += move_name + "}"
	# gender is not an important enough stat for output
	#out_str += "\n--- Gender:" + str(pd['Gender'])
	return out_str
	#TODO: ppups and any other additions to props in pkmn dicts from static/dynamic var init functs or elsewhere

# takes the pokemon dict output by randomize_PKMN and turns it into an exeuctable PkHex cmd
def PKMN_dict_to_cmd(pd,slot_num):
	#printd(pd)
	dex_num = pd['dexnum']
	pkmn_name = get_PKMN_name(dex_num)
	out_str = "=Box=1"
	out_str += "\n=Slot="+str(slot_num)
	out_str += "\n.Species=" + str(dex_num)
	out_str += "\n.Nickname=" + pkmn_name.capitalize()
	#pkmn_name = get_PKMN_name(dex_num)
	out_str += "\n.CurrentLevel=" + str(pd['CurrentLevel'])
	for stat in stat_labels:
		out_str += "\n.EV_" + stat + "=" + str(pd['EV_'+stat])
	for stat in stat_labels:
		out_str += "\n.IV_" + stat + "=" + str(pd['IV_'+stat])
	out_str += "\n.CurrentFriendship=" + str(pd['CurrentFriendship'])
	out_str += "\n.HeldItem=" + str(pd['HeldItem'])
	out_str += "\n.TID=" + str(pd['TID'])
	out_str += "\n.OT_Name=" + pd['OT_Name']
	for i in range(1,5):
		move_str = "Move" + str(i)
		out_str += "\n." + move_str + "=" + str(pd[move_str][0])
	out_str += "\n.Gender=" + str(pd['Gender'])
	return out_str
	#TODO: ppups and any other additions to props in pkmn dicts from static/dynamic var init functs or elsewhere

# outputs the string version of a team and their PkHex batch commands to a file
# team_name may be a number or a string
#TODO: bad variable names here... cmd_lines is a list of cmd_line strings to PkHex, which are more than one line... 
def output_team_file(cmd_lines, team_name):
	assertd(is_list(cmd_lines))
	assertd(is_str(team_name))
	timestamp_str = get_timestamp_str()
	fname = out_dir + out_prefix + str(team_name) + "_" + timestamp_str + out_extension
	print("\nWriting team " + team_name + " to file " + fname + "...")
	output_enum(cmd_lines, fname, None, "\n")
	print("Done.\n")
	"""
	cmd_file = ...
	readable_file = ...
	for cmd in cmd_strs:
		cmd_file.write(cmd)
	"""	
	"""
	f = open(,"w+")
	for cmd_line in cmd_lines:
		# TODO: couldnt you just do f.write(cmd_line)?
		split_line = cmd_line.split('\n')
		for line in split_line:
			f.write(line + "\n")
		f.write("\n")
	f.close()
	"""



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