import pokepy
import ruleset

#TODO: 	much of the functionality here should be wrapped into Pokemon objects
#		so that outside functions don't have to deal with stuff related to pokepy

# ----- PGLOBALS VARIABLES -----

# debug flag 
# rintd, assertd (often used as function I/O checks) and other potential statements only execute if this flag is enabled
# DEBUG generally causes more verbose output
# DEUBG makes the program more likely to halt due to unexpected inputs/outputs/conditions
# considering these factors, enabling DEBUG may cause the script to run significantly slower
# if DEBUG is disabled, it may prevent timing.py timing, or it may override this and continue functioning regardless of DEBUG
DEBUG = True

# main pokepy client
client = pokepy.V2Client()

# ruleset
rs = ruleset.Ruleset(0)

# main list of teams used by players
teams = []

# number of teams to build per instance of "teammake" run
default_num_teams = 2

# name of "Pokedex" folder
dex_folder = "../res/dex_entries/"

# list of string pokemon types
all_type_names = ['bug', 'dark', 'dragon', 'electric', 'fighting', 'fire', 'flying', 'ghost', 'grass', 'ground', 'ice', 'normal', 
'poison', 'psychic', 'rock', 'steel', 'water']

# ideally write this out to a file somewhere or cache it or smt
file_list = []

# list of genderless dexNums
# inferred from https://bulbapedia.bulbagarden.net/wiki/List_of_Pok%C3%A9mon_by_gender_ratio
genderless_dexnums = [81, 82, 100, 101, 120, 121, 137, 233, 132, 144, 145, 146, 150, 151, 201, 243, 244, 245, 249, 250, 251]

# list of moves with hyphens in the names all in lower case
hyphenated_moves = ["lock-on", "mud-slap", "double-edge", "self-destruct", "soft-boiled"]

# number of pokemon on a given team, usually 6
ruleset_team_size = 6

# the labels of each combat stat; used to generate EV/IV properties of pokemon
stat_labels = ['ATK','DEF','HP','SPA','SPD','SPE']

# the number of pokemon that are allowed to have a given type
# if this is -1 it means we won't bother checking for this
# i.e. ruleset_repeated_types == 2 --> no more than 2 pokemon have a given type (aka you cant have more than 2 fire types)
# i.e. ruleset_repeated_types == 1 --> no two pokemon share a type (aka you cant have more than 1 flying type)
ruleset_repeated_types = -1

# number of legendaries that will be rolled when generating a team
# if 0, no legendaries are required
# max of 6
num_required_legendaries = 0

# 38 (Nintales) has some alolan evolution or w/e so might be a part of this list
fairy_type_dexnums = [35,36,39,40,122,173,174,175,176,183,184,209,210]

fairy_type_move_ids = [186, 204, 236]

# ----- REFERENCE TEXT -----

"""

pokemon class reference - pokepy.resources_v2.PokemonResource

"""