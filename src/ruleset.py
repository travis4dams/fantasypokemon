from helper_functions import *

# ----- DEFAULT RULESET CONSTANTS -----

# list of banned pokemon (by dexnum)
#TODO: assert ids in this list and others match the ids in their respective dicts
#TODO: banned lists should probably be sets, or merged with dicts (no need for redundant objects, muddies design/debugging)
default_banned_dexnums_list = [10, 11, 13, 14, 129, 132, 144, 145, 146, 149, 150, 151, 172, 173, 174, 175, 201, 235, 236, 238, 239, 240, 
243, 244, 245, 248, 249, 250, 251]

# dict of banned pokemon (by dexnum) mapped to a tuple containing (name, ban_reason)
# the default reasons are:
#	1 - < 4 learnable moves (i.e. metapod/magikarp)
#	2 - Legendary or pseudo-legendary
# 	3 - Baby pokemon
default_banned_dexnums_dict = {
10:("Caterpie","Less than four learnable moves"),
11:("Metapod","Less than four learnable moves"), 
13:("Weedle","Less than four learnable moves"), 
14:("Kakuna","Less than four learnable moves"), 
129:("Magikarp","Less than four learnable moves"), 
132:("Ditto","Less than four learnable moves"), 
144:("Articuno","Legendary, although inside stadium rentals."),
145:("Zapdos","Legendary, although inside stadium rentals."),
146:("Moltres","Legendary, although inside stadium rentals."),
149:("Dragonite","Psuedo-legendary, although inside stadium rentals."),
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
243:("Raikou","Legendary, although inside stadium rentals."),
244:("Entei","Legendary, although inside stadium rentals."),
245:("Suicune","Legendary, although inside stadium rentals."),
248:("Tyranitar","Psuedo-legendary, although inside stadium rentals."),
249:("Lugia","Legendary and outside stadium rentals."), 
250:("Ho-oh","Legendary and outside stadium rentals."), 
251:("Celebi","Legendary and outside stadium rentals.")
}

# list of legendary dexNums
default_legendary_dexnums_list = [144, 145, 146, 149, 150, 151, 243, 244, 245, 248, 249, 250, 251]

# list of legendary dexNums
default_legendary_dexnums_dict = {
144:("Articuno","Legendary, although inside stadium rentals."),
145:("Zapdos","Legendary, although inside stadium rentals."),
146:("Moltres","Legendary, although inside stadium rentals."),
149:("Dragonite","Psuedo-legendary, although inside stadium rentals."),
150:("Mewtwo","Legendary and outside stadium rentals"), 
151:("Mew","Legendary and outside stadium rentals"),
243:("Raikou","Legendary, although inside stadium rentals."),
244:("Entei","Legendary, although inside stadium rentals."),
245:("Suicune","Legendary, although inside stadium rentals."),
248:("Tyranitar","Psuedo-legendary, although inside stadium rentals."),
249:("Lugia","Legendary and outside stadium rentals."), 
250:("Ho-oh","Legendary and outside stadium rentals."), 
251:("Celebi","Legendary and outside stadium rentals.")
}

# list of underevolved pkmn
# inferred from:
# https://www.ign.com/wikis/pokemon-go/List_of_Pokemon_(Pokedex)
# https://www.ign.com/wikis/pokemon-go/List_of_Gen_2_Pokemon_(Johto_Pokedex)
#TODO: double check this list and build dict... some of this overlaps w/ banned (esp baby) list

default_underevolved_dexnums_list = [1,2,4,5,7,8,10,11,13,14,16,17,19,21,23,25,27,29,30,32,33,35,37,39,41,43,44,46,48,50,
52,54,56,58,60,61,63,64,66,67,69,70,71,72,74,75,77,79,81,84,86,88,90,92,93,96,98,100,102,104,109,111,113,116,117,118,120,129,
133,138,140,147,148,152,153,155,156,158,159,161,163,165,167,170,172,173,174,175,177,179,180,183,187,188,191,194,204,209,216,
218,220,223,228,231,236,246,247]

# list of banned move_ids
default_banned_move_ids_list = [3,6,10,20,33,35,40,49,82,83,99,100,104,117,132,138,141,150,167,171,173,189,206,213,214,216,218,249,250]

# dict of banned move_ids mapped to a string of the move name
#TODO: get move names in same format as pokepy
#TODO: assert move_id<-> name mappings correspond w/ those of pokepy/PkHex
default_banned_moves_dict = {3:"Double Slap",
6:"Pay Day",
10:"Scratch",
20:"Bind",
33:"Tackle",
35:"Wrap",
40:"Poison Sting",
49:"Sonic Boom",
82:"Dragon Rage",
83:"Fire Spin",
99:"Rage",
100:"Teleport",
104:"Double Team",
107:"Minimize",
117:"Bide",
132:"Constrict",
138:"Dream Eater",
141:"Leech Life",
150:"Splash",
167:"Triple Kick",
171:"Nightmare",
173:"Snore",
189:"Mud-Slap",
206:"False Swipe",
213:"Attract",
214:"Sleep Talk",
216:"Return",
218:"Frustration",
249:"Rock Smash",
250:"Whirlpool"}


# if a pokemon that can learn an inferior move can also learn its superior move, replace it with the superior move
# dont just replace inferior moves with superior moves - i.e. seaking may know peck but not drill peck or w/e
#TODO: double check list validity esp w/ fighting/normal moves
#TODO: a move could be inferior to two moves, and BOTH moves should be incldued in the list, perhaps in some priorit order...
#		such that if an inferior move was randomly selected, it knows which superior move to replace it with... or rerandom among those options...
#		ofc, if a < b < c, don't include b, just c... 
# 		but if a < b and a < c this doesn't tell us about b and c
#		it could be both c and b are better than a, but due to unique new qualities b ? c comes down to some subjective value judgment
# 		i.e. suppose gust is weaker than wing attack and weaker than drill peck by both power and accuracy in both cases... BUT 
#		wing attack has increased crit and drill peck has chance to lower defense... which to choose? randomly select.
#		i.e. see gust entry... map each to a list of superior move(s) not just one move... or just have calling funct handle that or smt
#		in such a case 16:("Gust",[(17,"Wing Attack"),(65,"Drill Peck")])
# 		its also impt to notice that just because a < b and a < c, we want entries for a->b and a->c 
# 		because one pokemon may be able to learn a and b but not c, while another learns a and c but not b
# 		TL;DR: FOR NOW THE WORKAROUND is just pick an arbitrarily "better move" and we only have one entry
# dict format is id1:(name2,id2,name2)
# built by going to https://bulbapedia.bulbagarden.net/wiki/List_of_moves and sorting by type then just knowing which replaces what... 
# needs to have better or same power and better or same accuracy with no loss of "special effects" 
# (multihit moves are considered a special effect)
#TODO: i may have mentioned htis elsewhere already but... consider statistical implications here. its possible that 
# 		... OR with the way its implemented in the program, 
# 		there's actually less of a chance of getting certain moves than if we did replacements by hand 
#		(i.e. by hand might be "if rolled this then replace with this" ... while the algorithim might be "just limit initial roll options")
#TODO: make sure this interacts w/ banned moves correctly (i.e. if we start handling a move do we still want it in inferior dict or what)
default_inferior_moves_dict = {
44:("Bite",242,"Crunch"),
84:("Thunder Shock",85,"Thunderbolt"),
52:("Ember",53,"Flamethrower"),
16:("Gust",17,"Wing Attack"),
64:("Peck",17,"Wing Attack"),
122:("Lick",247,"Shadow Ball"),
71:("Absorb",202,"Giga Drain"),
79:("Sleep Powder",147,"Spore"),
28:("Sand Attack",189,"Mud-Slap"),
8:("Ice Punch",58,"Ice Beam"),
62:("Aurora Beam",58,"Ice Beam"),
1:("Pound",70,"Strength"),
5:("Mega Punch",70,"Strength"),
6:("Pay Day",70,"Strength"),
10:("Scratch",70,"Strength"),
10:("Scratch",70,"Strength"),
11:("Vice Grip",70,"Strength"),
13:("Razor Wind",70,"Strength"),
15:("Cut",70,"Strength"),
21:("Slam",70,"Strength"),
30:("Horn Attack",70,"Strength"),
33:("Tackle",70,"Strength"),
173:("Snore",70,"Strength"),
206:("False Swipe",70,"Strength"),
216:("Return",70,"Strength"),
218:("Frustration",70,"Strength"),
# technically sludge bomb may have a lower chance to poison than some of these moves but i think most would find this a fair trade
40:("Poison Sting",188,"Sludge Bomb"),
51:("Acid",188,"Sludge Bomb"),
123:("Smog",188,"Sludge Bomb"),
124:("Sludge",188,"Sludge Bomb"),
139:("Poison Gas",92,"Toxic"),
60:("Psybeam",94,"Psychic"),
# confusion technically has a chance to confuse so it isnt strictly inferior to psychic but... practically so
93:("Confusion",94,"Psychic"),
149:("Psywave",94,"Psychic"),
88:("Rock Throw",157,"Rock Slide"),
# metal claw has 95% acc and steel wing 90% acc, and metal claw has 10% +1 attack proc... this is a judgment call but yeah
232:("Metal Claw",211,"Steel Wing"),
55:("Water Gun",57,"Surf"),
61:("Bubble Beam",57,"Surf"),
127:("Waterfall",57,"Surf"),
145:("Bubble",57,"Surf"),
250:("Whirlpool",57,"Surf")
}

class Ruleset:

	# Ruleset is initialized with a "ruleset_flag", which determines which initialize function it calls
	def __init__(self, ruleset_flag = 0):

		if (ruleset_flag == 0):
			self.init_default()
		else:
			printd("Unhandled ruleset_flag for Ruleset.__init__(): " + str(ruleset_flag))

	def init_default(self):

		# banned pokemon
		self.banned_dexnums_list = default_banned_dexnums_list
		self.banned_dexnums_dict = default_banned_dexnums_dict

		# legendary pokemon
		self.legendary_dexnums_list = default_legendary_dexnums_list
		self.legendary_dexnums_dict = default_legendary_dexnums_dict

		# underevolved pokemon
		self.underevolved_dexnums_list = default_underevolved_dexnums_list

		self.banned_move_ids_list = default_banned_move_ids_list
		self.banned_moves_dict = default_banned_moves_dict

		self.inferior_moves_dict = default_inferior_moves_dict

		# option request player and trainer names
		self.request_pt_names = False

	# the rules that can be editted:
	# # of legendary pokemon required
	# # of repeat types allowed
	# banned dexnums
	# banned moveids
	# LATER:
	# # of pokemon generated (team size)
	# require specific dexnums (i.e. "I want a Chamander and a Pikachu on my team plus four others")
	# generally edit algorithms behind move/pkmn generation
	def edit_rule(self):
		pass

	def parse_rule_subcmds(self, subcmds):
		pass


		