import pokepy

# ----- GLOBAL VARIABLES -----

# main pokepy client
client = pokepy.V2Client()

# main interface object (see interface.py)
intf = None


# dict mapping acceptable input commands to their help descriptions
# this is used for "help" output
help_instructions = {
'help':'Displays a list of acceptable commands.', 
'quit':'Terminates the script.', 
'ruleset':'Describes the current ruleset. Typing \"ruleset edit <rule_number> <value>\" will edit that rule to that value if permissible.', 
'teammake':'Creates the number of teams according the ruleset. Entering \"teammake <team_number>\" will replace that team with a new team.', 
'teamedit':'Edits a specific Pokemon. Type \"teamedit <team_number> <slot_number>\" to reselect that pokemon.', 
'teamprint':'Prints the current teams in PkHex format to console, copies it to clipboard, and creates the appropriate output file(s). Typing \"teamprint <team_number>\" will do this for only that team.'
}

# main list of teams used by players
teams = []

# number of teams to build per instance of "teammake" run
default_num_teams = 2

# name of "Pokedex" folder
dex_folder = "../res/dex_entries/"

# list of string pokemon types
type_names = ['Bug', 'Dark', 'Dragon', 'Electric', 'Fighting', 'Fire', 'Flying', 'Ghost', 'Grass', 'Ground', 'Ice', 'Normal', 
'Poison', 'Psychic', 'Rock', 'Steel', 'Water']

# ideally write this out to a file somewhere or cache it or smt
file_list = []

# list of banned dexNums
banned_dexnums_list = [10, 11, 13, 14, 129, 132, 150, 151, 172, 173, 174, 175, 201, 235, 236, 238, 239, 240, 249, 250, 251]

# dict of banned dexNums mapped to a tuple containing (name, ban_reason)
banned_dexnums_dict = {
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