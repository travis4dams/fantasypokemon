# ----- CREATED BY Nathan Giles 6/30/19 -----

# ----- INFORMATION -----
# main.py is the main script behind the Pokemon Team Maker program
# it contains some global variables related to files and game setup
# it contains functions that implement the main features of the script (team generation and editing, ruleset view and editing, etc.)

# NOTE: this entire project currently only implements pokemon, features and functions from Gen 2, but could be extended to other generations later 

# ----- GENERAL TODO LIST IDEAS -----
# see todo.txt and TODO notes throughout

# ----- IMPORTED PACKAGES -----

# project packages
from helper_functions import *
from pglobals import *
import pkpywrapper
from pokemon import *
from move import *
import cmd_interface
from pokedb import *
import ruleset
from timing import *

# external packages
import sys
import colorama
import random

# previously used packages (kept for reference's sake)
#import re
#from webrequest import main_request

# ----- MAIN VARIABLES -----

# team output file variables
out_dir = "../teams/" 		# location of team output folder
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
default_player1_name = "Player 1"
default_team1_name =  "Team 1"
default_player2_name =  "Player 2"
default_team2_name =  "Team 2"
team_strs = [default_player1_name, default_team1_name, default_player2_name, default_team2_name]

# default file names
default_fname1 = "pkmnteam_1_2019-07-17_22.48.59"
default_fname2 = "pkmnteam_2_2019-07-17_22.48.59"

# ----- MAIN FUNCTIONS -----

# entry point of program
#TODO: context handling for commands... i.e. teamshow w/ no made teams
#TODO: simplify global variable and initialization design
def main():

	# start timing.py variables related to start of script
	start_script()

	# reset command prompt colors
	reset_style()
	reset_color()

	# generic init message before more "colorful" introduction by cmdintf
	print("\nStart of program.\n")

	# dummy function for testing purposes; does nothing unless specified below
	alt_main()

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

# a function used for testing purposes that is called in the beginning of main
# if desired, this function may call squit() and thus override regular script functionality
def alt_main():
	#test_repeat_team_make()
	#test_move_in()
	#test_create_all_pokemon()
	#test_pkpy_move_cache
	#test_move_cache()
	#squit()
	return

# setups any relevantvariables from pglobals
# ... I originally tried to have some of the asserts in pglobals.py but that was causing recursive import problems I think
# init_vars() could be split into check_vars() which would only be called if(DEBUG)
#TODO: 	this is not interacting with global variables as expected. 
# 		instead it seems simpler to just initialize global variables in the global namespace (i.e. above "main variables" area)
def init_vars():

	start_timer()

	# setup and check ruleset
	global rs
	rs = ruleset.Ruleset()
	assertd(num_required_legendaries <= ruleset_team_size and num_required_legendaries <= 6)

	# check Pokepy client
	assertd(client != None and isinstance(client, pokepy.api.V2Client),"PokePy client did not initialize correctly.")
	
	#TODO: 	check other vars from pglobals.py, so if something is changed there to a bad value, this will catch it 
	# 		rather than not being noticed or being hidden amongst some other error
	#load_full_moves()

	end_timer()

# generates a quick randomly generated team with  for testing purposes
def get_test_teams():
	start_timer()
	printd("Generating test teams...")
	global teams
	for team_num in range(2):
		team = []
		for slot_num in range(6):
			team.append(randomize_PKMN([],False,False))
		teams.append(team)
	printd("Done generating test teams.")
	end_timer()

# for testing purposes
# attempts to call create_pokemon on all legal dexnums
# NOTE: currently dexnum == 132 (Ditto) will cause this to fail since get_learnable_moves < 4
def test_create_all_pokemon():
	start_timer()
	printd("Testing creation of all pokemon...")
	# TODO: replace any hard-coded int value of 251 (that deals with max POKEMON dexnum... max move id is also coincidentally 251)
	# 		across entire program with reference to this
	for i in range(1,Pokemon.max_dexnum):
		printd("Testing creation of pokemon " + str(i))
		p = create_pkmn(i, True)
	end_timer()

def test_repeat_team_make():
	start_timer()
	printd("Repeatedly testing team_make...")
	iterations = 10
	i = 0
	while i < iterations:
		printd("Repeat team_make iteration " + str(i))
		team_make()
		i += 1
	end_timer()

def test_pkpy_move_cache():
	start_timer()
	
	iterations = 10

	start_timer("test_pkpy_move_cache misses")
	printd("Loading 251 pokepy moves...")
	# should all be cache misses
	for j in range(iterations):
		for i in range(1,252):
			#printd("Loading pokepy move " + str(i))
			get_pkpy_move(i)
	end_timer("test_pkpy_move_cache misses")

	# should all be cache hits
	start_timer("test_pkpy_move_cache hits")
	printd("Reloading 251 pokepy moves (should be cache hits)...")
	for j in range(iterations):
		for i in range(1,252):
			#printd("Loading pokepy move " + str(i))
			get_pkpy_move(i)
	end_timer("test_pkpy_move_cache hits")

	end_timer()

def test_move_cache():
	start_timer()
	
	printd("Loading 251 moves...")
	# should all be cache misses
	for i in range(1,252):
		#printd("Loading move " + str(i))
		Move(i)

	printd("move_cache_hits: " + str(Move.move_cache_hits))

	# should all be cache hits
	printd("Reloading 251 moves (should be cache hits)...")
	for i in range(1,252):
		#printd("Loading move " + str(i))
		Move(i)

	end_timer()

# test if, for a move m and set of moves s, "m in s" is an O(1) or O(N) operation
# ... results suggested they are close and maybe not a concern for optimization, but with a dataset with a meager length of 251,
# O(1) and O(N) it may not be distinguishable
def test_move_in():
	start_timer()

	max_move_id = Move.max_move_id

	# setup single moveset
	singleton_move_set = set()
	singleton_move = Move(1)
	singleton_move_set.add(singleton_move)

	# setup all moveset
	all_move_set = set()
	for i in range(max_move_id):
		all_move_set.add(Move(i+1))

	# call the relevant test function a relevant number of iterations

	repeat_iterations = 1

	for i in range(max_move_id * repeat_iterations):
		test_singleton_set(singleton_move_set, singleton_move)

	for i in range(max_move_id * repeat_iterations):
		test_singleton_set(singleton_move_set, None)

	for i in range(repeat_iterations):
		for j in range(max_move_id):
			m = Move(j+1)
			test_all_set(all_move_set, m)

	for i in range(max_move_id * repeat_iterations):
		test_all_set(all_move_set, None)

	end_timer()

def test_singleton_set(singleton_set, m):
	#assertd(is_move(m))
	#assertd(len(singleton_set) == 0)
	start_timer()
	result = m in singleton_set
	end_timer()
	return result

def test_all_set(all_set, m):
	#assertd(is_move(m))
	#assertd(len(singleton_set) == Move.max_move_id)
	start_timer()
	result = m in all_set
	end_timer()
	return result

def get_teams_length():
	global teams
	return len(teams)

def get_team(i):
	assertd(is_int(i))
	global teams
	assertd(i < len(teams))
	return teams[i]

# help function - called to list and desctibe commands
def help(cmdintf):
	start_timer()
	print("\nList of commands:")
	for cmd in cmdintf.base_cmd_list:
		print("\n" + cmd)
		print(cmdintf.help_instructions[cmd] + "\n")
	print()
	end_timer()

# "script quit" function - called to close everything out
# quit() is a reserved python function 
def squit(quit_msg = None):

	global timing_ignores_DEBUG

	if(timing_ignores_DEBUG or DEBUG):
		display_timing_stats()

	printd("pkmn_move_cache_hits: " + str(pkpywrapper.pkmn_move_cache_hits))
	printd("move_cache_hits: " + str(Move.move_cache_hits))

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

	start_timer()

	# global variables - not sure this is necessary?
	global teams
	global rs
	global num_required_legendaries

	# check parameter(s)
	assertd(replace_team_num == None or 
		( is_int(replace_team_num) and replace_team_num >= 0 and replace_team_num < len(teams)), 
		"Bad input to team_make(): " + str(replace_team_num))

	# based on input arguments, user wants to build all teams
	if replace_team_num == None:
		print("Beginning to build a total of " + str(default_num_teams) + " teams...")

		# record start time for performance measuring purposes
		# ... however we are also tracking the full function runtime with start_timer()
		# TODO: organize this so we arent tracking time twice. request timer from timing.py instead of tracking it here
		start = get_time()

		# temporary workaround for allowing us to call team_make multiple times
		# i could imagine that instead of this, it could be fun to generate more teams than are actually used in battle (2), 
		# so players can choose among randomed teams
		teams = []

		# build each team
		for team_num in range(default_num_teams):
			print("Building team " + str(team_num+1) + "...")
			team = []
			team_ids = []

			# build pokemon for this team until team size requirement met
			while len(team) < ruleset_team_size:

				# random a pkmn
				# we also force rolling a legendary until we meet the num_required_legendaries requirement (if any)
				if len(team) < num_required_legendaries: 					
					pkmn = randomize_PKMN(team_ids, True)
				else:
					pkmn = randomize_PKMN(team_ids, False)

				# add pkmn to team
				team.append(pkmn)
				team_ids.append(pkmn.dexnum)

				# sanity check that team lists are in acceptable range
				assertd(len(team) > 0 and len(team) <= ruleset_team_size)
				assertd(len(team_ids) > 0 and len(team_ids) <= ruleset_team_size)

				# NOTE: currently does nothing (check_and_update_team just passes)
				# if the team is full (about to exit loop), check that it meets the type requirement (no more than 2 pkmn share a type)
				# if yes, continue
				# if no, randomly choose a pkmn breaking the type rule, and rerandom that pokemon
				# TODO: we may wanna check any rules that just deal with dexnums before calculating movesets, 
				# 		so we arent wasting time building moves just to be rerandomed
				if len(team) == ruleset_team_size:
					team = check_and_update_team(team)

			# team passed - add to teams
			teams.append(team)

		# evaluate runtime
		end = get_time()
		elapsed_time = round(end - start)

		# sanity check that teams list is correct size
		assertd(len(teams) == default_num_teams, 
			"team_make assumes it completed successfuly but did not create the correct number of teams.")		

		# completion message
		print("\nteammake done building " + str(len(teams)) + " teams after " + str(elapsed_time) + " seconds.\n")

		# ask for input names for players and their teams
		# depending on user input, this may edit the team_strs list
		input_player_and_team_names()

		# save and show team after building it
		team_save()
		team_show()

	# based on input arguments, user wants to replace (aka "rebuild" or "rerandom") a specific team
	#TODO: implement
	"""
	else:
		team = []
		while len(team) < ruleset_team_size:
			pkmn = randomize_PKMN()
			team.append(pkmn)
		teams[replace_team_num] = team
		print("Done replacing team " + replace_team_num + " with a new team.")
	"""

	#printd("team_make end")

	end_timer()

#TODO: implement this
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
		type_names = pkmn.get_type_names()
		type_name1 = type_names[0]
		# CHANGE - check that len(type_names) > 1 before fetching type_name2
		type_name2 = type_names[1]
		#TODO: assert=d is a type string, len != 0, etc
		assertd(is_str(type_name1) and type_name1 != "None")
		assertd(is_str(type_name2))
		if(not type_name1 in type_name_stats):
			type_name_stats[type_name1] = [1,[dexnum]]
		else:
			type_count = type_name_stats[type_name1][0]
			existing_ids = type_name_stats[type_name1][1]
			type_name_stats[type_name1][0] = type_count+1
			existing_ids.append(dexnum)
		if type_name2 != "None":
			if not type_name2 in type_name_stats:
				type_name_stats[type_name2] = [1,[dexnum]]
			else:
				type_count = type_name_stats[type_name2][0]
				existing_ids = type_name_stats[type_name2][1]
				type_name_stats[type_name2][0] = type_count+1
				existing_ids.append(dexnum)

	#printd(type_name_stats)

	#input() 

	# go through all the types that we have, if we have one more than twice, randomly reselect one of the "offenders"
	# this "reslect" occurs by replacing team with a new list that excludes these pokemon, then repeats the loop
	# rerandom_ids contains the dexnums of the pokemon to exclude from the new list
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
		dexnum = pkmn['dexnum']
		if not dexnum in rerandom_ids:
			team_update.append(pkmn)
		#else:
			#printd("dexnum " + str(dexnum) + " is getting rerolled.")

	return team_update

	printd(team_copy)

	input()
	"""

#TODO: consistent use of player/trainer var/text/comment naming
def input_player_and_team_names():

	# catch all statement for calling code (rather than writing if statements everywhere else)
	# if ruleset disallows requesting player and trainer names, just keep default values 
	global rs
	if not rs.request_pt_names:
		return

	# player1_name_input
	player1_name_input = input_and_time("\nWho is player 1?\n")
	player1_name_input_formatted = player1_name_input.strip()
	if player1_name_input_formatted == "":
		player1_name_input_formatted = default_player1_name
		team1_name_input_formatted = default_team1_name
	else:
		# team1_name_input
		team1_name_input = input_and_time("\n" + player1_name_input_formatted + ", do you have a name for your team?\n")
		team1_name_input_formatted = team1_name_input.strip()
		if team1_name_input_formatted == "":
			team1_name_input_formatted = default_team1_name

	# player2_name_input
	player2_name_input = input_and_time("\nWho is player 2?\n")
	player2_name_input_formatted = player2_name_input.strip()
	if player2_name_input_formatted == "":
		player2_name_input_formatted = default_player2_name
		team2_name_input_formatted = default_team2_name
	else:
		# team2_name_input
		team2_name_input = input_and_time("\n" + player2_name_input_formatted + ", do you have a name for your team?\n")
		team2_name_input_formatted = team2_name_input.strip()
		if team2_name_input_formatted == "":
			team2_name_input_formatted = default_team2_name

	global team_strs
	team_strs = [player1_name_input_formatted, team1_name_input_formatted, player2_name_input_formatted, team2_name_input_formatted]

# rerandom a specific pokemon on a specific team
def team_edit(team_num, slot_num, is_legendary = False):

	start_timer()

	# check and setup inputs
	global teams
	assertd(is_int(team_num) and team_num >= 0 and team_num < len(teams))
	assertd(is_int(slot_num))
	teams_len = len(teams)
	assertd(team_num < teams_len)
	team = teams[team_num]
	assertd(is_list(team))
	team_len = len(teams)
	assertd(slot_num < team_len)

	# start message
	print("Replacing the Pokemon in slot " + str(slot_num) + " of team " + str(team_num) + " with a new Pokemon...")

	# replace the pokemon
	replaced_pkmn = teams[team_num][slot_num]
	new_team_ids = []
	# this assumes you CAN rerandom the same pokemon with team_edit
	for i in range(len(team)):
		if i != slot_num:
			new_team_ids.append(team[i].get_dexnum())
	teams[team_num][slot_num] = randomize_PKMN(new_team_ids, is_legendary)

	# end message
	print("Done replacing.")

	end_timer()

# output the teams to console
# TODO: rather than using a global var for team_strs, change team_show and team_make so it handles inputs w/ cmdintf correctly... 
# TODO: ... also input handling and debugging asserts etc on team_strs here and elsewhere
def team_show(team_num = None):

	start_timer()

	# load and check teams list
	global teams
	if(len(teams)==0):
		print("\nThere are no teams to print.\n")
		return

	# team_strs contains player/team names; they may be set to default values
	global team_strs
	#printd(team_strs)

	# UNIMPLEMENTED - print only that team
	if team_num != None:
		return
	
	# build output string
	out_str = ""

	# go through teams
	for i in range(len(teams)):

		team = teams[i]

		# --- parse player/team names ---

		# NOTE: the cases for combinations for player/team names are as follows:
		# 		Case 1: neither player nor team name supplied
		#		Case 2: player name supplied but not team name
		# 		Case 3:	both player and team name supplied 
		#		there is no case where they can have no player name supplied while having a team name supplied

		# identify the default player name for this loop iteration
		if i == 0:
			default_player_name = default_player1_name
		else:
			default_player_name = default_player2_name

		# parse player name
		player_name = team_strs[i*2]
		player_name_postfix = "\'s "

		# identify the default team name for this loop iteration
		if i == 0:
			default_team_name = default_team1_name
		else:
			default_team_name = default_team2_name

		# parse team name 
		team_name = team_strs[(i*2)+1]
		if team_name != default_team_name: # team name is specified
			team_name = "\"" + team_name + "\""
		elif player_name != default_player_name: # team name is not specified, but trainer name is
			team_name = "team"
		else: # team and player names are not specified - give a generic name for the team
			team_name = "\"Team " + str(i+1) + "\""
		
		if i == 0:
			num_newlines = 1
		else:
			num_newlines = 2
		
		out_str += "\n"*num_newlines + player_name + player_name_postfix + team_name + ":"

		# --- done parsing player/team names ---

		# parse each pokemon's names, types, and moves, and then add to the respective team list
		# these strings are grouped together so they can be tab aligned with tab_format based on the longest string
		team_species_names = []
		team_nicknames = []
		team_types = []

		# team_moves is handled differently - we keep track of a list AND dict mapping move names to their move objects
		# we track the dict is so we don't have to call Move.get_move() with a string input later
		team_moves_strs = []
		team_moves = {}

		# iterate through this team
		for j in range(len(team)):

			# grab info for each pokemon
			pkmn = team[j]
			pid = pkmn.get_dexnum()

			# pkmn_name is species name plus some surrounding text and dexnum, i.e. pkmn_name == "Bulbasaur [#1]" 
			# (I believe there are no preceding 0's for the dexnum, so its [#1] not [#001])
			pkmn_name = pkmn.get_species_name() + " [#" + str(team[j].get_dexnum()) + "]"
			team_species_names.append(pkmn_name)	

			# pkmn_nickname is nickname surrounding by quotes
			pkmn_nickname = "\"" + pkmn.get_nickname() + "\""
			team_nicknames.append(pkmn_nickname)

			# get the string version of this pokemon, and use that to get some info about it
			# this is a sloppy workaround until i get better OOP design w/ pokemon and moves
			pkmn_str = str(pkmn)	

			# pkmn_type_names is a list of type names. examples: ["Water"] ... or ... ["Rock", "Ground"]
			pkmn_type_names = pkmn.get_type_names()
			team_types.append(str(pkmn_type_names).replace('\'',''))
		
			# pkmn_move_strs stores the move strings for THIS pokemon
			# team_move_strs stores the move strings for all pokemon in this team
			pkmn_moves = pkmn.get_moves()
			for k in range(len(pkmn_moves)):
				m = pkmn_moves[k]
				m_name = m.get_name()
				team_moves[m_name] = m
				team_moves_strs.append(m_name)

		# instead of converting team_moves into a list, we need to keep track of a team_moves_strs independently
		# since a list allows duplicates but a dict does not
		#team_moves_strs = list(team_moves)
	
		# tab align pokemon names, types, and moves (per team)
		# NOTE: this must be done BEFORE any text coloring, or else it will not format properly
		tab_format(team_species_names)
		tab_format(team_nicknames)
		tab_format(team_types)
		tab_format(team_moves_strs)

		# color the move strings AFTER they've been tab formatted
		for j in range(len(team_moves_strs)):
			move_name_detabbed = team_moves_strs[j].strip() # strip it off the tabs we just gave it so we can index into team_moves
			m = team_moves[move_name_detabbed]
			mtypename = m.get_type_str() # name of the move's type, i.e. m == Fire Blast --> mtypename == "Fire"			
			type_color_str = get_type_color(mtypename)			
			colored_str = type_color_str + team_moves_strs[j] + get_all_resets()			
			team_moves_strs[j] = colored_str

		# this is a sloppy workaround to take "(Ice, Water)" string from the strings in team_types,
		# then find the base type names in them aka "Ice" and "Water", then replace those with colored versions
		# there is surely a cleaner/quicker way to do this
		for j in range(len(team_types)):

			# team_types[j] is a string i.e. "[Ice, Water]" with the []'s INSIDE the string

			type_pair = team_types[j].replace('[','').replace(']','').split(',') # type_pair list of two type strings i.e. ["Ice", "Water"]

			for type_str in type_pair:

				for base_pkmn_type_str in all_type_names:

					# standardize format
					base_pkmn_type_str_lower = base_pkmn_type_str.lower()
					type_str_lower = type_str.lower()

					# this base type is in the type_str
					if base_pkmn_type_str_lower in type_str_lower:
						type_index = type_str_lower.index(base_pkmn_type_str_lower)
						substr = type_str[type_index:type_index+len(base_pkmn_type_str)]
						team_types[j] = team_types[j].replace(substr,get_type_color(substr.title()) + substr.title() + get_all_resets())
						break	

		# build the final output string
		# TODO: repeatedly adding to end of string is very costly in time since strings are immutable... find a better solution
		for j in range(len(team)):

			# build the move string
			move_str = ""
			for k in range(j*4,(j*4)+4):
				# the 1st (k == 0), 5th (k == 4), 9th (k == 8) and so on move strings start the list of four moves for that pokemon
				if (k)%4 == 0:
					move_str += "{"
				# the 4th (k == 3), 8th (k == 7), 12th (k == 11) and so on move strings end the list of four moves for that pokemon
				move_str += team_moves_strs[k]
				if (k+1)%4 == 0:
					move_str += "}"

			# add to out_str
			out_str += "\n" + str(j) + ": " + team_species_names[j].title() + team_nicknames[j] + team_types[j] + move_str
	
	print(out_str)

	print("\nteamshow complete.\n")

	end_timer()

# generate PkHex commands to clipboard
def team_copy():
	start_timer()
	team1_cmd_strs, team2_cmd_strs = get_cmd_strs(True)
	assertd(len(team1_cmd_strs) == len(team2_cmd_strs))
	end_timer()

# generate output file(s)
# generate folder name based on this time stamp
# request team name(s)
# ensure positions in each list here align, i.e. index 0 is referencing team 1 across all these lists
# TODO: implement team_strs to team_save
def team_save():
	start_timer()
	#assertd(len(cmd_strs) == len(teams) * ruleset_team_size)
	#assertd(len(out_strs) == len(teams))
	team1_cmd_strs, team2_cmd_strs = get_cmd_strs(False)
	assertd(len(team1_cmd_strs) == len(team2_cmd_strs))
	output_team_file(team1_cmd_strs, "1")
	output_team_file(team2_cmd_strs, "2")
	end_timer()

# returns two lists of PkHex command strings, one for team1 and one for team2
# if copy_and_halt, the PkHex command for each pokemon will copy to the user's clipboard and wait for input before proceeding
# this most handles all of get_copy(), but much of this functionality is also used by team_save() 
# so I figure its better to keep the function in one place
def get_cmd_strs(copy_and_halt = True):

	start_timer()

	global teams

	# setup the cmd_strs lists
	team1_cmd_strs = []
	team2_cmd_strs = []

	# iterate through teams
	for team_num in range(len(teams)):
		team = teams[team_num]

		# iterate through this team's pokemon
		for pkmn_num in range(len(team)):

			# get the cmd_str for this pokemon and add to respective cmd_str lists
			pkmn = team[pkmn_num]
			cmd_str = pkmn.to_cmd(pkmn_num+1)
			if(team_num == 0):
				team1_cmd_strs.append(cmd_str)
			else:
				team2_cmd_strs.append(cmd_str)

			# if copy_and_halt, copy the PkHex command for this pkmn to the user's clipboard and wait for input before proceeding
			if copy_and_halt:
				print("Entering anything besides \"quit\" will copy the command for pokemon #" + str(pkmn_num))
				proceed = input().replace(" ","").lower()
				if proceed == "quit":
					print("Quitting teamshow.")
					return
				print("Copying command to keyboard...")
				copy_str_to_clipboard(cmd_str)
				print("Copied.\n")

	# sanity check length of cmd_strs lists
	assertd(len(team1_cmd_strs) == ruleset_team_size)
	assertd(len(team1_cmd_strs) == len(team2_cmd_strs))

	end_timer()

	return team1_cmd_strs, team2_cmd_strs

# load the two teams, each from one of the two supplied output file(s)
def team_load(fname1, fname2):
	start_timer()
	print("\nAttempting to load file named " + str(fname1) + " into team1...")
	load_team_file(fname1,default_fname1)
	print("\nDone loading team1.")
	print("\nAttempting to load file named " + str(fname2) + " into team2...")
	load_team_file(fname2,default_fname2)
	print("\nDone loading team2.")
	#TODO: should the team files we load already have the player and team names in them?
	input_player_and_team_names()
	print("\nteamload complete.\n")
	end_timer()

# helper function for team_load()
# attempts to load fname, or backup_fname if loading fname fails (backup_fname is usually a default fname)
# returns None if loading 
def load_team_file(fname, backup_fname = None):

	start_timer()

	global out_dir

	# reformat and check fname
	assertd(is_str(fname))
	fname_formatted = fname.strip()
	assertd(fname_formatted != "")

	# if user supplied a fname, attempt to open that file	 
	loaded_fname = "" # loaded_fname is used for debugging purposes
	if fname_formatted.lower() != "default":

		fpath = out_dir + fname_formatted + out_extension

		try:
			f = open(fpath,"r+")
			loaded_fname = fname_formatted

		# failed to open user supplied file
		except FileNotFoundError as ex:

			# we do not have a legit backup file - return None
			if not is_str(backup_fname) or backup_fname.strip() == "":
				printd("File not found for load_team_file(): " + str(fpath) + " ... returning None.")
				return None
			# we have a legit backup file - attempt to load it
			else:
				printd("File not found for load_team_file(): " + str(fpath) + " ... attempting to load backup: " + str(backup_fname))
				backup_fpath = out_dir + backup_fname + out_extension
				try:
					f = open(fbackup_fpathpath,"r+")
					loaded_fname = backup_fname
				# failed to load backup file
				except FileNotFoundError as ex2:
					printd("Failed to load backup: " + str(backup_fpath) + " ... returning None")
					return None

	# if user did not supply a fname, attempt to open default (backup) file
	else:		

		backup_fpath = out_dir + backup_fname + out_extension

		try:
			f = open(backup_fpath,"r+")
			loaded_fname = backup_fname

		# failed to load default file
		except FileNotFoundError as ex2:
			printd("Failed to load default: " + str(backup_fpath) + " ... returning None")
			return None

	# NOTE: if this point is reached, f loaded properly (aka f is an open file)
	# TODO: consider checking it is properly formatted somehow (currently check_load_file always passes)
	f = check_load_file(f)
	if f == None:
		printd("Check_load_file() failed on " + loaded_fname)

	# current_team is a list of the Pokemon objects associated with this team file
	current_team = []

	# current_pkmn is a Pokemon object that is currently being processed in the file
	# current_pkmn == None until reaching the 1st "Species" line, and is reset upon reaching subsequent Species lines
	current_pkmn = None

	# go through each line 	of the input file
	for line in f:

		# remove the first character from the input line (always a "=" or "."), then strip whitespace
		line_formatted = line[1:len(line)-1].strip()

		# each line is in the form "attribute=val", so we can split on "=" and get key_str/val_str
		line_split = line_formatted.split("=")
		key_str = line_split[0]
		val_str = line_split[1]

		# parse the string as an integer if possible
		if val_str.isdigit():
			val = int(val_str)
		else:
			val = val_str

		# the attributes in the following if/else structure are in the same order as they are encounter in a load file

		# "Box" and "Slot" lines are unused
		if key_str == "Box" or key_str == "Slot":
			continue

		# once we reach a "Species" attribute beyond the first, we know we've encountered a new pokemon
		# so add the current one to team and proceed
		elif key_str == 'Species':

			assertd(is_legal_dexnum(val))

			# this isn't the first pokemon in the team: add what we've got to teams list
			if current_pkmn != None:
				assertd(current_pkmn.is_initialized())
				current_team.append(current_pkmn)

			# regardless of slot_num position, initialize a new pokemon with this dexnum
			current_pkmn = Pokemon()		
			current_pkmn.set_dexnum(val)

		# nickname
		elif key_str == 'Nickname':	
			assertd(is_legal_nickname(val))
			current_pkmn.set_nickname(val)

		# level
		elif key_str == "CurrentLevel":
			assertd(is_legal_level(val))
			current_pkmn.set_level(val)

		# EVs
		elif "EV_" in key_str:
			# assertd(len(key_str) == 6) # because of EV_HP, we can't assume it will be in the form "EV_XYZ"
			# ... so just grab from EV_ to end and let assertd's check it
			stat_str = key_str[3:]
			assertd(is_legal_stat_str(stat_str))
			assertd(is_legal_ev(val))
			current_pkmn.set_ev(stat_str,val)

		# IVs
		elif "IV_" in key_str:
			# assertd(len(key_str) == 6) # because of EV_HP, we can't assume it will be in the form "EV_XYZ"
			# ... so just grab from EV_ to end and let assertd's check it
			stat_str = key_str[3:]
			assertd(is_legal_stat_str(stat_str))
			assertd(is_legal_iv(val))
			current_pkmn.set_iv(stat_str,val)

		# friendship
		elif key_str == 'CurrentFriendship':	
			assertd(is_legal_friendship(val))
			current_pkmn.set_friendship(val)

		# held item id
		elif key_str == 'HeldItem':	
			assertd(is_legal_held_item_id(val))
			current_pkmn.set_held_item_id(val)

		# OT_id
		elif key_str == 'TID':	
			assertd(is_legal_OT_id(val))
			current_pkmn.set_OT_id(val)

		# OT_name
		elif key_str == 'OT_Name':	
			assertd(is_legal_OT_name(val))
			current_pkmn.set_OT_name(val)
		
		# moves
		elif "Move" in key_str:
			#move_obj = get_pkpy_move(val)		
			#move_name = move_obj.name
			move_num = int(key_str[key_str.index("Move")+4])
			m = Move(val)
			current_pkmn.set_move(move_num, m)

		# gender_id
		elif key_str == 'Gender':	
			assertd(is_legal_gender_id(val))
			current_pkmn.set_gender_id(val)

		# if it's a line with an unrecognized key_str, try skipping it and moving on
		else:
			#setattr(current_pkmn, key_str, val)
			printd("Bad key_str in line of load team file " + str(loaded_fname) + ": " + str(key_str) + " ... attempting to skip line and continue.")
			continue

	# if we've exited the loop, means reached end of file, so add last pokemon too
	current_team.append(current_pkmn)

	# finish by adding current_team to teams
	teams.append(current_team)

	end_timer()

# checks if the file f is a properly formatted team .txt file
# since it must iterate through the file, it returns a pointer to the start of the file if it is a properly formatted file
# if it is improperly formatted, returns None
#TODO: implement
def check_load_file(f):
	return f

# generate one random pokemon
# try to use strings (variables/values) congruent w/ PkHex
# used by team_make() and get_test_teams()
#TODO: prevent rerandoming same pkmn
#TODO: this could be optimized by 
def randomize_PKMN(existing_team_ids = [], is_legendary = False, enforce_ruleset = True):

	start_timer()

	# generate the dexnum according to any ruleset restrictions then pass that along to create_pkmn
	# disallowed_dexnums is a set
	disallowed_dexnums = get_disallowed_dexnums()

	# default case
	if not is_legendary:
		# TODO: this could be optimized by only generating random numbers that wouldnt result in a "collision" with these lists
		# 		ideally if such a list were to be built it would be not be built with every call to this function, 
		# 		but once before a series of calls to this function
		dexnum = get_random_int(1,251)	

		# while loop keeps rerandoming a dexnum until it meets requirements
		# checking presence in disallowed_dexnums is faster than repeatedly calling is_disallowed_dexnum
		timer_identifier = "randomize_PKMN rerandom dexnum"
		start_timer(timer_identifier)
		while dexnum in disallowed_dexnums or dexnum in existing_team_ids: 
			dexnum = get_random_int(1,251)
		end_timer(timer_identifier)

		# sanity check
		assertd(is_allowed_dexnum(dexnum))
		assertd(not dexnum in existing_team_ids)

	# forced legendary case
	else:
		random_index = get_random_int(0,len(legendary_dexnums_list)-1)
		dexnum = rs.legendary_dexnums_list[random_index]
		assertd(is_allowed_dexnum(dexnum))

	result = create_pkmn(dexnum,enforce_ruleset)

	end_timer() 

	return result

def is_allowed_dexnum(dexnum):
	assertd(is_positive_int(dexnum))
	return dexnum not in get_disallowed_dexnums()

def is_disallowed_dexnum(dexnum):
	assertd(is_positive_int(dexnum))
	return not is_allowed_dexnum(dexnum)

# returns set of all disallowed dexnums
# helper function for randomize_PKMN() and testing functions (i.e. test_create_all_pokemon)
# TODO: concise design with this and pokemon.is_legal_dexnum
def get_disallowed_dexnums():

	# load the ruleset
	global rs

	# retrieve relevant ruleset attributes
	# TODO: doing this all at once could improve performance over constnatly retrieving these from rs obj ... though maybe theyre cached (??)
	# TODO: banned lists should probably be sets
	banned_dexnums_list = rs.banned_dexnums_list
	underevolved_dexnums_list = rs.underevolved_dexnums_list
	legendary_dexnums_list = rs.legendary_dexnums_list	

	disallowed_dexnums = set(banned_dexnums_list).union(set(underevolved_dexnums_list)).union(set(legendary_dexnums_list))

	return disallowed_dexnums
	
# creates Pokemon object for PkHex/str output
# I believe this is called only by randomize_PKMN as of now
def create_pkmn(dexnum, enforce_ruleset = True):
	start_timer()
	pkmn = Pokemon()
	pkmn.set_dexnum(dexnum)
	init_static_pkmn_vars(pkmn)
	init_dynamic_pkmn_vars(pkmn, enforce_ruleset)
	assertd(pkmn.is_initialized())
	end_timer()
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
#TODO: random TIDs
#TODO: current player name
#TODO: pp ups
def init_static_pkmn_vars(pkmn):
	start_timer()
	pkmn.set_level(100)
	for label in stat_labels:
		pkmn.set_ev(label, 65535)
		pkmn.set_iv(label, 15)
	pkmn.set_friendship(0)
	pkmn.set_held_item_id(0)
	pkmn.set_OT_id(48011)
	pkmn.set_OT_name("Nate")
	end_timer()

# stats that are randomized:
# dexnumber (already given)
# moves
# gender (if that pkmn is not genderless)
# (for fun) - "garble" up the nickname
# (for fun) - isShiny
#TODO: there is probably a "generated n random indices into a list of length m" python function out there which would simplify this
# 		see "random.choice(list)" https://stackoverflow.com/questions/46425645/python-make-every-character-line-random-color-print
def init_dynamic_pkmn_vars(pkmn, enforce_ruleset = True):

	start_timer()
	
	# --- get the name(s) of the pokemon's type(s) ---
	#pkmn_type_names = pkmn.get_type_names()	

	dexnum = pkmn.get_dexnum()

	# --- select gender ---
	# TODO - this doesnt seem to be working properly
	if(dexnum in genderless_dexnums):
		pkmn.set_gender_id(2)
	else:
		gender_num = get_random_int(0,1)
		assertd(gender_num == 0 or gender_num == 1,"Bad gender_num generated in init_dynamic_pkmn_vars().")
		pkmn.set_gender_id(gender_num)

	# --- setup moves ---

	moveset = pkmn.get_random_moveset(enforce_ruleset)

	# set Move1, Move2, Move3, Move4 entries of pkmn dict
	for i in range(len(moveset)):
		pkmn.set_move(i+1, moveset[i])

	end_timer()

# outputs the string version of a team and their PkHex batch commands to a file
# team_name may be a number or a string
#TODO: bad variable names here... cmd_lines is a list of cmd_line strings to PkHex, which are more than one line... 
def output_team_file(cmd_lines, team_name):
	start_timer()
	assertd(is_list(cmd_lines))
	assertd(is_str(team_name))
	timestamp_str = get_timestamp_str()
	fname = out_dir + out_prefix + str(team_name) + "_" + timestamp_str + out_extension
	print("\nWriting team " + team_name + " to file " + fname + "...")
	output_enum(cmd_lines, fname, None, "\n")
	print("Done.\n")
	end_timer()

# ----- END -----

if __name__ == "__main__":
	main()
