# this script is used to build relevant database files 

from pkpywrapper import *

out_dir = "../res/"

moves_fname = "full_moves"

moves_ftype = ".txt"

# outputs a file containining all the learnable moves of all the pokemon in gen 2 pokedex
# each line is in the following format
# "<dex_num>:(<name>,<move_list>"
# where move_list is the string version of the list of learnable move names
# once this file is built, it should save time retrieving moves later
#TODO: this could be sped up  by writing the lines as we build the moves_dict
def output_full_moves_file():

	output_dict = {}

	for i in range(1,252):
		pkmn = get_PKMN(i)
		pkmn_name = get_PKMN_name(i)
		print("Generating entry for " + pkmn_to_str(pkmn_name, i))
		learnable_moves = get_moves(pkmn)
		learnable_move_names = get_move_names(learnable_moves)
		output_dict[i] = (pkmn_name, learnable_move_names)

	print("Done generating entries.")

	fname = out_dir + moves_fname + moves_ftype

	output_enum(output_dict, fname, None, "\n")

	print("Done building full moves file.")

# loads all the moves from the "full" moves file
# this should make get_moves() faster
def load_full_moves():
	print("load full moves start")
	fname = out_dir + moves_fname + moves_ftype
	result_dict = load_input_file(fname)
	#print(result_dict)
	for k in result_dict:
		move_name_list_str = result_dict[k]
		print(move_name_list_str)
		move_name_list_substr = move_name_list_str[move_name_list_str.index('[')+1:len(move_name_list_str)-2]
		move_name_list = move_name_list_substr.replace('\'','').split(',')
		move_objs = get_moves_by_name(move_name_list)
		pkmnwrapper.pkmn_move_cache[int(k)] = move_objs
	print("load full moves end")