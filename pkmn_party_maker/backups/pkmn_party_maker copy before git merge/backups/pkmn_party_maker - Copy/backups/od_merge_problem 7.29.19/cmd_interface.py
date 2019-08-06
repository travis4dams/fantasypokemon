from main import teams, help, squit, ruleset_cmd, team_make, team_edit, team_show, team_copy, team_save, team_load
from helper_functions import *

class CmdInterface:

	# ----- CLASS VARIABLES -----

	# <insert class variables here>

	# ----- INSTANCE ATTRIBUTES AND __init__() ----

	# initialize instance - currently no instance variables... but I felt and OOP approach to the cmdinterface could pay off later
	def __init__(self):

		# list of acceptable input commands
		self.base_cmd_list = ['help','quit','ruleset','teammake','teamedit','teamshow','teamcopy','teamsave','teamload']

		# dict mapping acceptable input commands to their help descriptions
		# this is used for "help" output
		self.help_instructions = {
			'help':'Displays a list of acceptable commands.', 
			'quit':'Terminates the script.', 
			'ruleset':'Describes the current ruleset. Typing \"ruleset edit <rule_number> <value>\" will edit that rule to that value if permissible.', 
			'teammake':'Creates the number of teams according the ruleset. Entering \"teammake <team_number>\" will replace that team with a new team.', 
			'teamedit':'Edits a specific Pokemon. Type \"teamedit <team_number> <slot_number>\" to reselect that pokemon.', 
			'teamshow':'Prints the current teams as readable text to console. Typing \"teamshow <team_number>\" will display only that team.',
			'teamcopy':'Copies the current teams as PkHex commands to clipboard, one Pokemon at a time.',
			'teamsave':"Saves the current teams to the appropriate output file(s).",
			'teamload':"Loads two given team files."
			}

		#TODO: also map command names to functions here so its more succintly/clearly defined and makes checking setup easier

		assertd(is_list(self.base_cmd_list) != 0,
			"In CmdInterface.__init__(): base_cmd_list is not a list.")

		assertd(len(self.base_cmd_list) != 0,
			"In CmdInterface.__init__(): base_cmd_list is empty.")

		assertd(is_dict(self.help_instructions) != 0,
			"In CmdInterface.__init__(): help_instructions is not a dict.")

		assertd(len(self.help_instructions) != 0,
			"In CmdInterface.__init__(): help_instructions is empty.")

		assertd(len(self.base_cmd_list) == len(self.help_instructions.keys()),
			"In CmdInterface.__init__(): Not all base commands have help instructions.")

	# ----- INSTANCE METHODS -----

	# greeting to the user
	def welcome_message(self):
		# welcome/introduction
		reset_all()
		set_color("red")
		print("\n")
		print("                                ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~                                ")
		print("                --------------- ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ---------------                " + get_all_resets())
		print(get_color("white") + "~~~~~~~~~~~~~~~ --------------- Welcome to Pokemon Team Maker! --------------- ~~~~~~~~~~~~~~~")
		print("                --------------- ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ---------------                ")
		print("                                ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~                                ")
		print("\n")
		reset_all()
		# output list of commands
		print("The possible commands are:")
		print_list(self.base_cmd_list)
		print()

	# input loop that continuously interprets user commands until they quit
	def input_loop(self):
		# accept user input
		full_cmd = input("Please input a command:\n")
		formatted_cmd = self.format_cmd(full_cmd)
		escape_cmds = [None, "", "quit", "\n", "\t"]

		# main user input loop
		while formatted_cmd not in escape_cmds:
			self.interpret_cmd(formatted_cmd)
			full_cmd = input("Please input a command:\n")
			formatted_cmd = self.format_cmd(full_cmd)

		if formatted_cmd in escape_cmds:
			print("You have elected to quit the script. Shutting down.")
			squit()

		# should not be reached
		assertd(False,"should not be reached")

	# simple function to remove any bad characters in input
	# this is useful so formatting is standardized in all areas
	def format_cmd(self, full_cmd):
		assertd(is_str(full_cmd),
			"Bad full_cmd to format_cmd(). Type: " + get_class_name(full_cmd) + " str: " + str(full_cmd))
		return full_cmd.lower().strip()

	# attempts to parse formatted string cmd and call appropriate functions
	# stuff like https://tinyurl.com/yynealaa might be useful here
	def interpret_cmd(self, formatted_cmd):
		assertd(is_str(formatted_cmd),
			"Bad formatted_cmd to interpret_cmd(). Type: " + get_class_name(formatted_cmd) + " str: " + str(formatted_cmd))

		# list of command and subcommand(s) (if any)
		input_cmd_list = formatted_cmd.lower().split(' ')

		# base_cmd is the "root" command string without any arguments (i.e. "make" in "make 1" but not the arguments like "1")
		base_cmd = input_cmd_list[0]

		# if base_cmd is unrecognized, simply alert the user and return to the input loop
		if(not base_cmd in self.base_cmd_list):
			print("\nUnrecognized command: " + base_cmd + "\n")
			return

		# parse base command, interpret any subcommands, and pass any arguments onto the appropriate function in main
		# if any input is faulty, parse_subcmds() will print errors and return None
		# functions that never use arguments won't call parse_subcmds()
		# subcmds lists all the arguments; the if/elif/else cases below then unpack and pass on those arguments (i.e. teamedit)
		#TODO: looking into *args or w/e could probably simplify a lot of this
		subcmds = self.parse_subcmds(input_cmd_list)
		if subcmds == None:
			return

		if base_cmd == 'help':
			help(subcmds[0]) # help takes no arguments from the command prompt, but we pass it the cmdinterface object
		elif base_cmd == 'quit': # while loop condition in input_loop() but eh should handle this but eh just incase
			assertd(False,"base_cmd should not be quit to interpret_cmd()")
			squit()
		elif base_cmd == 'ruleset':
			ruleset_cmd()
		elif base_cmd == 'teamshow':
			if(len(subcmds)>0):
				team_show(subcmds[0])
			else:
				team_show()
		elif base_cmd == 'teamcopy':
			team_copy()
		elif base_cmd == 'teamsave':
			team_save()
		elif base_cmd == 'teammake':
			if(len(subcmds)>0):
				team_make(subcmds[0])
			else:
				team_make()
		elif base_cmd == 'teamedit':
			team_edit(subcmds[0], subcmds[1], subcmds[2])

		elif base_cmd == 'teamload':
			if(len(subcmds) > 0 and subcmds[0] == "default"):
				team_load("default","default")
			elif(len(subcmds) == 2):
				team_load(subcmds[0],subcmds[1])
			else:
				print("Bad input for teamload")

		# this else case should not be reached based on "if(base_cmd not in self.base_cmd_list)" check above
		else:
			assertd(False,"Should not be reached.")
			print("Unrecognized command: " + cmd)
		return

	# ensures that proper input is given to main command functions
	# returns list
	# returns an empty list if it parsed no subcommands
	# returns None if there was an error parsing subcommands
	# TODO: check is_int here and elsewhere
	def parse_subcmds(self, input_cmd_list):
		assertd(is_list(input_cmd_list),
			"Bad input_cmd_list to parse_subcmds(). Type: " + get_class_name(input_cmd_list) + " str: " + str(input_cmd_list))

		base_cmd = input_cmd_list[0]

		subcmds = []

		#NOTE: technically, the else of elif's below shouldnt be necessary if you are returning cases properly within each if...
		# 		but elif's can just help prevent checking each if and just streamlines things imo

		# help - takes only this cmdinterface object as an argument so return a list containing only self (which is used by help() for output)
		if base_cmd == 'help':
			return [self]

		# quit - takes no arguments so return an empty list
		elif base_cmd == 'quit':
			return subcmds

		# ruleset - (currently) takes no arguments so return an empty list
		#TODO: ruleset arguments
		elif base_cmd == 'ruleset':
			return subcmds

		# teamshow
		elif base_cmd == 'teamshow':
			# if no optional arguments supplied by user, pass no arguments to teamshow
			if len(input_cmd_list) <= 1:
				return subcmds
			# subcmd exists, check that its an int
			subcmd = input_cmd_list[1]
			if not is_int(subcmd):
				print("Team number argument to teamshow is not an integer: " + str(subcmd))
				return None
			# subcmd is an int, check if its in range
			if subcmd < 0 or subcmd >= len(teams):
				print("Team number argument to teamshow out of range: " + str(subcmd) + ". There are currently " + str(len(teams)) + " teams.")
				return None
			# subcmd is good, add it to subcmds and return subcmds
			subcmds = [subcmd]
			return subcmds

		elif base_cmd == 'teamcopy':
			return subcmds

		elif base_cmd == 'teamsave':
			return subcmds

		# teammake
		elif base_cmd == 'teammake':
			# if no optional arguments supplied by user, pass no arguments to teammake
			if len(input_cmd_list) <= 1:
				return subcmds
			# subcmd exists, check that its an int
			subcmd = int(input_cmd_list[1])
			if not is_int(subcmd):
				print("Team number argument to teammake is not an integer: " + str(subcmd))
				return None
			# subcmd is an int, check if its in range
			if subcmd < 0 or subcmd >= len(teams):
				print("Team number argument to teammake out of range: " + str(subcmd) + ". There are currently " + str(len(teams)) + "teams.")
				return None
			# subcmd is good, add it to subcmds and return subcmds
			subcmds = [subcmd]
			return subcmds

		# teamedit
		elif base_cmd == 'teamedit':
			if len(input_cmd_list) < 3:
				print("Incorrect number of inputs to teamedit: Got " + str(len(input_cmd_list))-1 + ", expected 3 or 4.")
				return None
			# check that team_num is an int
			team_num = int(input_cmd_list[1])
			if not is_int(team_num): 
				print("Team number argument to teamedit is not an integer: " + str(team_num))
				return None
			# team_num is an int, check if its in range
			if team_num < 0 or team_num >= len(teams):
				print("Team number to teamedit out of range: " + str(team_num) + ". There are currently only " + str(len(teams)) + "teams.")
				return None
			# team_num is good, check slot_num
			team = teams[team_num]
			# check that slot_num is an int
			slot_num = int(input_cmd_list[2])
			if not is_int(slot_num):
				print("Slot number argument to teamedit is not an integer: " + str(slot_num))
				return None
			if slot_num < 0 or slot_num >= len(team):
				print("Slot number to teamedit out of range: " + str(slot_num) + ". There are currently only " + str(len(teams)) + "slots.")
				return None
			legendary_bool = False
			if len(input_cmd_list) > 3:
				legendary_flag = int(input_cmd_list[3])
				if legendary_flag == 1:
					legendary_bool = True
			subcmds = [team_num, slot_num, legendary_bool]
			return subcmds

		elif base_cmd == 'teamload':
			if len(input_cmd_list) != 3:
				print("Incorrect number of inputs to teamload: Got " + str(len(input_cmd_list))-1 + ", expected 2 filenames.")
				return None
			# check that fname1 is a str
			fname1 = input_cmd_list[1]
			if not is_str(fname1): 
				print("fname1 argument to teamload is not a string: " + str(fname1))
				return None
			# check that fname2 is a str
			fname2 = input_cmd_list[2]
			if not is_str(fname2): 
				print("fname2 argument to teamload is not a string: " + str(fname2))
				return None
			subcmds = [fname1, fname2]
			return subcmds

		# shouldn't be reached based on structure of interpret_cmd()'s if-else structure
		else:
			print("Unrecognized or unhandled command to parse_subcmds(): " + str(base_cmd))
			assertd(False,"Should not be reached.")
			return None

		# shouldn't be reached - cases above should return on their own
		print("Subcmd from parse_subcmds(): " + str(subcmd))
		assertd(False,"Should not be reached.")
		return None