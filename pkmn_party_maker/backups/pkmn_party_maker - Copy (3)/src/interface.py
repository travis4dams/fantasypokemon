from main import *

class Interface:

	# ----- CLASS VARIABLES -----
	# list of acceptable input commands
	cmd_list = ['help','quit','ruleset','teammake','teamedit','teamprint']


	# ----- INSTANCE METHODS -----
	def __init__():
		pass

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