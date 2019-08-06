# ----- INFORMATION -----

# pkpywrapper.py mainly serves as a wrapper of the pokepy API to streamline its use
# put another way, pkpywrapper.py serves to set up data/objects related to Pokemon 

# ----- IMPORTED PACKAGES -----

# project packages
from pglobals import *
from helper_functions import *

# external packages
import pokepy
import beckett.exceptions

# previouslly used packages
#from main import squit

# ----- pkpywrapper VARIABLES -----

# maps pkmn dexnums to pokemon objs that have already been loaded
#TODO: not sure this actually works with global variables correctly
pkmn_obj_cache = {}

# use an intenger dexNum to index into this list for the pokepy move object associated with it
# used by get_moves to save loading time if we already determined the moves learnable by a pokemon
pkmn_move_cache = [None]*251
pkmn_move_cache_hits = 0

move_id_to_name_dict = {1:'Pound',
2:'Karate Chop',
3:'Double Slap',
4:'Comet Punch',
5:'Mega Punch',
6:'Pay Day',
7:'Fire Punch',
8:'Ice Punch',
9:'Thunder Punch',
10:'Scratch',
11:'Vice Grip',
12:'Guillotine',
13:'Razor Wind',
14:'Swords Dance',
15:'Cut',
16:'Gust',
17:'Wing Attack',
18:'Whirlwind',
19:'Fly',
20:'Bind',
21:'Slam',
22:'Vine Whip',
23:'Stomp',
24:'Double Kick',
25:'Mega Kick',
26:'Jump Kick',
27:'Rolling Kick',
28:'Sand Attack',
29:'Headbutt',
30:'Horn Attack',
31:'Fury Attack',
32:'Horn Drill',
33:'Tackle',
34:'Body Slam',
35:'Wrap',
36:'Take Down',
37:'Thrash',
38:'Double-Edge',
39:'Tail Whip',
40:'Poison Sting',
41:'Twineedle',
42:'Pin Missile',
43:'Leer',
44:'Bite',
45:'Growl',
46:'Roar',
47:'Sing',
48:'Supersonic',
49:'Sonic Boom',
50:'Disable',
51:'Acid',
52:'Ember',
53:'Flamethrower',
54:'Mist',
55:'Water Gun',
56:'Hydro Pump',
57:'Surf',
58:'Ice Beam',
59:'Blizzard',
60:'Psybeam',
61:'Bubble Beam',
62:'Aurora Beam',
63:'Hyper Beam',
64:'Peck',
65:'Drill Peck',
66:'Submission',
67:'Low Kick',
68:'Counter',
69:'Seismic Toss',
70:'Strength',
71:'Absorb',
72:'Mega Drain',
73:'Leech Seed',
74:'Growth',
75:'Razor Leaf',
76:'Solar Beam',
77:'Poison Powder',
78:'Stun Spore',
79:'Sleep Powder',
80:'Petal Dance',
81:'String Shot',
82:'Dragon Rage',
83:'Fire Spin',
84:'Thunder Shock',
85:'Thunderbolt',
86:'Thunder Wave',
87:'Thunder',
88:'Rock Throw',
89:'Earthquake',
90:'Fissure',
91:'Dig',
92:'Toxic',
93:'Confusion',
94:'Psychic',
95:'Hypnosis',
96:'Meditate',
97:'Agility',
98:'Quick Attack',
99:'Rage',
100:'Teleport',
101:'Night Shade',
102:'Mimic',
103:'Screech',
104:'Double Team',
105:'Recover',
106:'Harden',
107:'Minimize',
108:'Smokescreen',
109:'Confuse Ray',
110:'Withdraw',
111:'Defense Curl',
112:'Barrier',
113:'Light Screen',
114:'Haze',
115:'Reflect',
116:'Focus Energy',
117:'Bide',
118:'Metronome',
119:'Mirror Move',
120:'Self-Destruct',
121:'Egg Bomb',
122:'Lick',
123:'Smog',
124:'Sludge',
125:'Bone Club',
126:'Fire Blast',
127:'Waterfall',
128:'Clamp',
129:'Swift',
130:'Skull Bash',
131:'Spike Cannon',
132:'Constrict',
133:'Amnesia',
134:'Kinesis',
135:'Soft-Boiled',
136:'High Jump Kick',
137:'Glare',
138:'Dream Eater',
139:'Poison Gas',
140:'Barrage',
141:'Leech Life',
142:'Lovely Kiss',
143:'Sky Attack',
144:'Transform',
145:'Bubble',
146:'Dizzy Punch',
147:'Spore',
148:'Flash',
149:'Psywave',
150:'Splash',
151:'Acid Armor',
152:'Crabhammer',
153:'Explosion',
154:'Fury Swipes',
155:'Bonemerang',
156:'Rest',
157:'Rock Slide',
158:'Hyper Fang',
159:'Sharpen',
160:'Conversion',
161:'Tri Attack',
162:'Super Fang',
163:'Slash',
164:'Substitute',
165:'Struggle',
166:'Sketch',
167:'Triple Kick',
168:'Thief',
169:'Spider Web',
170:'Mind Reader',
171:'Nightmare',
172:'Flame Wheel',
173:'Snore',
174:'Curse',
175:'Flail',
176:'Conversion 2',
177:'Aeroblast',
178:'Cotton Spore',
179:'Reversal',
180:'Spite',
181:'Powder Snow',
182:'Protect',
183:'Mach Punch',
184:'Scary Face',
185:'Feint Attack',
186:'Sweet Kiss',
187:'Belly Drum',
188:'Sludge Bomb',
189:'Mud-Slap',
190:'Octazooka',
191:'Spikes',
192:'Zap Cannon',
193:'Foresight',
194:'Destiny Bond',
195:'Perish Song',
196:'Icy Wind',
197:'Detect',
198:'Bone Rush',
199:'Lock-On',
200:'Outrage',
201:'Sandstorm',
202:'Giga Drain',
203:'Endure',
204:'Charm',
205:'Rollout',
206:'False Swipe',
207:'Swagger',
208:'Milk Drink',
209:'Spark',
210:'Fury Cutter',
211:'Steel Wing',
212:'Mean Look',
213:'Attract',
214:'Sleep Talk',
215:'Heal Bell',
216:'Return',
217:'Present',
218:'Frustration',
219:'Safeguard',
220:'Pain Split',
221:'Sacred Fire',
222:'Magnitude',
223:'Dynamic Punch',
224:'Megahorn',
225:'Dragon Breath',
226:'Baton Pass',
227:'Encore',
228:'Pursuit',
229:'Rapid Spin',
230:'Sweet Scent',
231:'Iron Tail',
232:'Metal Claw',
233:'Vital Throw',
234:'Morning Sun',
235:'Synthesis',
236:'Moonlight',
237:'Hidden Power',
238:'Cross Chop',
239:'Twister',
240:'Rain Dance',
241:'Sunny Day',
242:'Crunch',
243:'Mirror Coat',
244:'Psych Up',
245:'Extreme Speed',
246:'Ancient Power',
247:'Shadow Ball',
248:'Future Sight',
249:'Rock Smash',
250:'Whirlpool',
251:'Beat Up'}

move_name_to_id_dict = {'Pound':1,
'Karate Chop':2,
'Double Slap':3,
'Comet Punch':4,
'Mega Punch':5,
'Pay Day':6,
'Fire Punch':7,
'Ice Punch':8,
'Thunder Punch':9,
'Scratch':10,
'Vice Grip':11,
'Guillotine':12,
'Razor Wind':13,
'Swords Dance':14,
'Cut':15,
'Gust':16,
'Wing Attack':17,
'Whirlwind':18,
'Fly':19,
'Bind':20,
'Slam':21,
'Vine Whip':22,
'Stomp':23,
'Double Kick':24,
'Mega Kick':25,
'Jump Kick':26,
'Rolling Kick':27,
'Sand Attack':28,
'Headbutt':29,
'Horn Attack':30,
'Fury Attack':31,
'Horn Drill':32,
'Tackle':33,
'Body Slam':34,
'Wrap':35,
'Take Down':36,
'Thrash':37,
'Double-Edge':38,
'Tail Whip':39,
'Poison Sting':40,
'Twineedle':41,
'Pin Missile':42,
'Leer':43,
'Bite':44,
'Growl':45,
'Roar':46,
'Sing':47,
'Supersonic':48,
'Sonic Boom':49,
'Disable':50,
'Acid':51,
'Ember':52,
'Flamethrower':53,
'Mist':54,
'Water Gun':55,
'Hydro Pump':56,
'Surf':57,
'Ice Beam':58,
'Blizzard':59,
'Psybeam':60,
'Bubble Beam':61,
'Aurora Beam':62,
'Hyper Beam':63,
'Peck':64,
'Drill Peck':65,
'Submission':66,
'Low Kick':67,
'Counter':68,
'Seismic Toss':69,
'Strength':70,
'Absorb':71,
'Mega Drain':72,
'Leech Seed':73,
'Growth':74,
'Razor Leaf':75,
'Solar Beam':76,
'Poison Powder':77,
'Stun Spore':78,
'Sleep Powder':79,
'Petal Dance':80,
'String Shot':81,
'Dragon Rage':82,
'Fire Spin':83,
'Thunder Shock':84,
'Thunderbolt':85,
'Thunder Wave':86,
'Thunder':87,
'Rock Throw':88,
'Earthquake':89,
'Fissure':90,
'Dig':91,
'Toxic':92,
'Confusion':93,
'Psychic':94,
'Hypnosis':95,
'Meditate':96,
'Agility':97,
'Quick Attack':98,
'Rage':99,
'Teleport':100,
'Night Shade':101,
'Mimic':102,
'Screech':103,
'Double Team':104,
'Recover':105,
'Harden':106,
'Minimize':107,
'Smokescreen':108,
'Confuse Ray':109,
'Withdraw':110,
'Defense Curl':111,
'Barrier':112,
'Light Screen':113,
'Haze':114,
'Reflect':115,
'Focus Energy':116,
'Bide':117,
'Metronome':118,
'Mirror Move':119,
'Self-Destruct':120,
'Egg Bomb':121,
'Lick':122,
'Smog':123,
'Sludge':124,
'Bone Club':125,
'Fire Blast':126,
'Waterfall':127,
'Clamp':128,
'Swift':129,
'Skull Bash':130,
'Spike Cannon':131,
'Constrict':132,
'Amnesia':133,
'Kinesis':134,
'Soft-Boiled':135,
'High Jump Kick':136,
'Glare':137,
'Dream Eater':138,
'Poison Gas':139,
'Barrage':140,
'Leech Life':141,
'Lovely Kiss':142,
'Sky Attack':143,
'Transform':144,
'Bubble':145,
'Dizzy Punch':146,
'Spore':147,
'Flash':148,
'Psywave':149,
'Splash':150,
'Acid Armor':151,
'Crabhammer':152,
'Explosion':153,
'Fury Swipes':154,
'Bonemerang':155,
'Rest':156,
'Rock Slide':157,
'Hyper Fang':158,
'Sharpen':159,
'Conversion':160,
'Tri Attack':161,
'Super Fang':162,
'Slash':163,
'Substitute':164,
'Struggle':165,
'Sketch':166,
'Triple Kick':167,
'Thief':168,
'Spider Web':169,
'Mind Reader':170,
'Nightmare':171,
'Flame Wheel':172,
'Snore':173,
'Curse':174,
'Flail':175,
'Conversion 2':176,
'Aeroblast':177,
'Cotton Spore':178,
'Reversal':179,
'Spite':180,
'Powder Snow':181,
'Protect':182,
'Mach Punch':183,
'Scary Face':184,
'Feint Attack':185,
'Sweet Kiss':186,
'Belly Drum':187,
'Sludge Bomb':188,
'Mud-Slap':189,
'Octazooka':190,
'Spikes':191,
'Zap Cannon':192,
'Foresight':193,
'Destiny Bond':194,
'Perish Song':195,
'Icy Wind':196,
'Detect':197,
'Bone Rush':198,
'Lock-On':199,
'Outrage':200,
'Sandstorm':201,
'Giga Drain':202,
'Endure':203,
'Charm':204,
'Rollout':205,
'False Swipe':206,
'Swagger':207,
'Milk Drink':208,
'Spark':209,
'Fury Cutter':210,
'Steel Wing':211,
'Mean Look':212,
'Attract':213,
'Sleep Talk':214,
'Heal Bell':215,
'Return':216,
'Present':217,
'Frustration':218,
'Safeguard':219,
'Pain Split':220,
'Sacred Fire':221,
'Magnitude':222,
'Dynamic Punch':223,
'Megahorn':224,
'Dragon Breath':225,
'Baton Pass':226,
'Encore':227,
'Pursuit':228,
'Rapid Spin':229,
'Sweet Scent':230,
'Iron Tail':231,
'Metal Claw':232,
'Vital Throw':233,
'Morning Sun':234,
'Synthesis':235,
'Moonlight':236,
'Hidden Power':237,
'Cross Chop':238,
'Twister':239,
'Rain Dance':240,
'Sunny Day':241,
'Crunch':242,
'Mirror Coat':243,
'Psych Up':244,
'Extreme Speed':245,
'Ancient Power':246,
'Shadow Ball':247,
'Future Sight':248,
'Rock Smash':249,
'Whirlpool':250,
'Beat Up':251}

# ----- pkpywrapper FUNCTIONS -----

# attempt to fetch pokemon object from Pokepy client and handle any errors
# returns None if it fails (or attempts to crash the program if DEBUG is enabled)
def client_pkmn_request(dexnum):

	start_timer()

	# check input
	assertd(is_int(dexnum),"Bad input to client_pkmn_request(): " + str(dexnum) + " is not an int.")
	assertd(is_gen2_dexnum(dexnum),"dexnum to client_pkmn_request() is out of range: " + str(dexnum))

	#printd(type(dexnum))

	# client request
	try:
		return client.get_pokemon(dexnum)
	except beckett.exceptions.InvalidStatusCodeError as ex:
		raise ValueError("Bad input to client.get_pokemon() in get_PKMN() wrapper: " + str(dexnum)) from None
		return None
	
	# generic catch... but commented out because why not just pass the original error for more info about the error?
	"""
	except:
		raise Exception("Unknown error in get_PKMN() fetching dexnum " + str(dexnum))
		#squit()
	"""

	end_timer()

# input: 1 <= dexnum <= 251
# output: Pokepy Pokemon object given an int Pokedex number
# NOTE: only Gen2 dexnum's are allowed (1-251 inclusive)
# TODO: string name input
def get_PKMN(dexnum):

	start_timer()

	# check input
	assertd(is_int(dexnum),"Bad input to get_PKMN(): " + str(dexnum) + " is not an int.")

	# check if pkmn obj is cached
	if(dexnum in pkmn_obj_cache):
		return pkmn_obj_cache[dexnum]

	# get output, check it, and return if acceptable
	result = client_pkmn_request(dexnum)	
	assertd(result != None and isinstance(result,pokepy.resources_v2.PokemonResource),
		"Bad result from client_pkmn_request() in get_PKMN(). Type: " + get_class_name(result) + " str: " + str(result))

	end_timer()

	return result

# returns the name of the pokemon given an int Pokedex number
def get_PKMN_name(dexnum):

	start_timer()

	# check input
	assertd(is_int(dexnum),"Bad input to get_PKMN_name(): " + str(dexnum) + " is not an int.")
	assertd(is_gen2_dexnum(dexnum),"dexnum to get_PKMN_name() is out of range: " + str(dexnum))

	# attempt to get pokemon object and its name
	result_pkmn = get_PKMN(dexnum)
	assertd(result_pkmn != None and is_pokepy_pkmn(result_pkmn),
		"Bad result from get_PKMN() in get_PKMN_name(). Type: " + get_class_name(result_pkmn) + " str: " + str(result_pkmn))
	result_name = result_pkmn.name
	assertd(is_str(result_name) and result_name!="",
		"Bad retrieved name in get_PKMN_name(). Type: " + get_class_name(result_name) + " str: " + str(result_name))

	end_timer()

	return result_name

# fetches the move name given a move ID OR extracts the name property from a move object 
def get_move_name(o):
	start_timer()
	a = is_int(o)
	b = is_pokepy_move(o)
	assertd(a or b,
		"Bad input to get_move_name(); it is neither an int nor a Pokemon move. Type: " + get_class_name(o) + " str: " + str(o))
	if(a):
		result = client.get_move(o).name
	else:
		result = o.move.name
	end_timer()
	return result
	
# returns a list of the names associated with the move objects/id#s in request_list
def get_move_names(request_list):
	start_timer()
	assertd(is_list(request_list),"Argument to get_move_names() is not a list. Type: " + get_class_name(request_list))
	result = []
	for o in request_list:
		assertd(is_int(o) or is_pokepy_move(o),
			"Bad element in request_list to get_move_names(); it is neither an int nor a Pokemon move. " + 
			"Type: " + get_class_name(o) + " str: " + str(o))
		m_name = get_move_name(o)
		#if m_name not in result:
		result.append(m_name)
	end_timer()
	return result

# the pokepy client requires moves to be in the format "abc-xyz", i.e. "string-shot"... 
# so lower case, no lead/trail whitespace, and multi-word attacks seperated by -'s'
# we attempt to format move_input to this form before sending it to the pokepy client
# returns None if fails (and tries to crash the program if DEBUG enabled)
# int input is preferred for improved performance purposes
def get_pkpy_move(move_input):

	# timer
	start_timer()

	# input check
	input_is_int = is_int(move_input)
	input_is_str = is_str(move_input)
	assertd(input_is_int or input_is_str)

	# default return value
	result = None

	# global variables
	global pkmn_move_cache
	global pkmn_move_cache_hits

	# int input
	if input_is_int:
		
		# input check
		assertd(move_input >= 1 and move_input <= 251)

		# check cache to see if we've loaded this move before
		if pkmn_move_cache[move_input-1] != None:
			# hit/success
			#printd("move cache hit: " + str(move_input-1))			
			result = pkmn_move_cache[move_input-1]			
			pkmn_move_cache_hits += 1
			#printd(type(result))
			end_timer()
			return result

		# print failed move cache case
		#printd("move cache fail: " + str(move_input-1))

		# try loading from pokepyclient. if we get an error, its likely because the input doesnt map to a move
		try:

			# client pokepy move obj
			result = client.get_move(move_input)

			# load new entries into cache
			pkmn_move_cache[move_input-1] = result

			#printd(type(result))
			end_timer()

			return result 

		# failed to load from client
		except beckett.exceptions.InvalidStatusCodeError as ex:
			raise ValueError("Bad input to get_pkpy_move(): " + str(move_input)) from None

			# should not be reached
			end_timer()
			#printd("None case A")
			return None		

	# str input
	elif input_is_str:

		#printd(move_input)
		#print_stack_trace()

		move_input_formatted = move_input.replace('-',' ').title()

		# manual exception handling
		# manually referenced hyphenated_moves in pglobals.py for this... perhaps these should be synchronized
		manual_exceptions = ["double edge", "mud slap", "lock on", "mud slap", "self destruct", "soft boiled"]
		if move_input_formatted.lower() in manual_exceptions:
			move_input_formatted = move_input_formatted.replace(' ','-')

		# we were able to convert the string name to a move id
		if move_input_formatted in move_name_to_id_dict:
			
			move_id = move_name_to_id_dict[move_input_formatted]
			
			# check cache to see if we've loaded this move before
			if pkmn_move_cache[move_id-1] != None:
				# hit/success
				#printd("move cache hit: " + str(move_id-1))
				result = pkmn_move_cache[move_id-1]
				pkmn_move_cache_hits += 1
				
				#printd(type(result))
				end_timer()
				return result

			# print failed move cache case
			else: 
				printd("move cache fail: " + str(move_id-1))
				pass				

		# failed to load from move_name_to_id_dict, or from cache - just load from pokepy client
		#printd("failed to load move name: " + move_input_formatted)
		#input()
		move_input_formatted = move_input.strip().replace(' ','-').lower()

		# try loading from pokepyclient. if we get an error, its likely because the input doesnt map to a move
		try:

			# client pokepy move obj
			result = client.get_move(move_input_formatted)

			# update cache on success
			pkmn_move_cache[result.id-1] = result

			#printd(type(result))
			end_timer()
			return result 

		# failed to load from client
		except beckett.exceptions.InvalidStatusCodeError as ex:
			raise ValueError("Bad input to get_pkpy_move(): " + str(move_input)) from None

			# should not be reached since we just raised an error
			end_timer()
			#printd("None case B")
			return None

	# bad input type
	else:
		assertd(False,"Unrecognized type for get_pkpy_move(): " + str(move_input))
		end_timer()
		#printd("None case C")
		return None

	# catch all case for if-else
	end_timer()
	#printd("None case D")
	return None

# returns int move id associated with move object m
def get_move_id(m):
	start_timer()
	assertd(is_pokepy_move(m),
		"Bad input to get_move_id(); it is not a Pokemon move. Type: " + get_class_name(m) + " str: " + str(m))
	m_id = int(m.move.url.split('/')[-2])
	# 743 is the max pokemon id # according to https://bulbapedia.bulbagarden.net/wiki/List_of_moves
	assertd(is_positive_int(m_id) and m_id < 743,
		"Bad output from get_move_id() move_id bad type or out of range. Type: " + get_class_name(m_id) + " str: " + str(m_id))
	end_timer()
	return m_id

# returns the move object associated with the name name
# pokepy API seems to have moves in the form "word1-word2", i.e. lower case and separated by -'s
def get_move_by_name(name):
	start_timer()
	assertd(is_str(name),
		"Bad input to get_move_by_name(); it is not a Pokemon move. Type: " + get_class_name(name) + " str: " + str(name))
	name = name.strip()
	assertd(name!="",
		"Bad input to get_move_by_name(). Type: " + get_class_name(name) + " str: " + str(name) + " len: " + str(len(name)))
	name = name.lower().replace(' ','-')
	move = client.get_move(name) 
	#assertd(is_pokepy_move(move),
	#	"Bad output from get_move_by_name(). Type: " + get_class_name(move) + " str: " + str(move))
	end_timer()
	return move

# returns a list of move objects associated with each name in name_list
# pokepy API seems to have moves in the form "word1-word2", i.e. lower case and separated by -'s
def get_moves_by_name(name_list):
	start_timer()
	move_objs = []
	for name in name_list:
		move_objs.append(get_move_by_name(name))
	end_timer()
	return move_objs

# returns a list of the "version_group"s associated with this "pokemon-move" 
# (not sure im using pokepy or whatever restful API's terminology correctly)
def get_version_groups(m):
	start_timer()
	assertd(is_pokepy_move(m),
		"Bad input to get_version_groups(); it is not a Pokemon move. Type: " + get_class_name(m) + " str: " + str(m))
	result = m.version_group_details
	assertd(is_list(result),
		"Bad output get_version_groups(); it is not a list. Type: " + get_class_name(result) + " str: " + str(result))
	assertd(len(result)>0,
		"Bad output get_version_groups(); it is an empty list. Type: " + get_class_name(result) + " str: " + str(result) + " len: " + str(len(result)))
	end_timer()
	return result

	# relevant deprecated code from get_learnable_moves
	"""
	used_versions = set(str_move_versions(get_version_groups(pokepy_move)))
	acceptable_used_verion_strs = ["gold-silver", "crystal", "red-blue", "yellow"]
	gen2_criterion = False
	for acceptable_used_verion_str in acceptable_used_verion_strs:
		if acceptable_used_verion_str in used_versions:
			gen2_criterion = True
			break
	if not gen2_criterion:
		continue
	"""

# this functions is called a LOT as we inspect learnable moves
def get_pokepy_move_type_name(pokepy_move):
	#printd(vars(pokepy_move))
	#printd(vars(pokepy_move.move))
	start_timer()
	if isinstance(pokepy_move, pokepy.resources_v2.MoveResource):
		type_name = pokepy_move.type.name
		# do not format input to save processing time
		#type_name = pokepy_move.type.name.strip().lower() 
		if type_name == 'fairy':
			return 'normal'
		return type_name
	#elif isinstance(mv,pokepy.resources_v2.PokemonMoveVersionSubResource)
	else:	
		move_id = int(pokepy_move.move.url.split('/')[-2])
		type_name = get_pkpy_move(move_id).type.name
		#type_name = get_move(move_id).type.name.strip().lower() 
		if type_name == 'fairy':
			return 'normal' 
	end_timer()

# converts a move version object into a string
def str_move_version(mv):
	start_timer()
	assertd(isinstance(mv,pokepy.resources_v2.PokemonMoveVersionSubResource),
		"Bad input to get_version_groups(); it is not a Pokemon move version. Type: " + get_class_name(mv) + " str: " + str(mv))
	result = mv.version_group.name
	assertd(is_str(result),
		"Bad output str_move_version(); it is not a string. Type: " + get_class_name(result) + " str: " + str(result))
	end_timer()
	return result

# converts a series of move version objects into a list of strings
def str_move_versions(mv_list):
	start_timer()
	assertd(is_list(mv_list),
		"Bad input to str_move_versions(); it is not a list. Type: " + get_class_name(mv_list) + " str: " + str(mv_list))
	assertd(len(mv_list)>0,
		"Bad input to str_move_versions(); it is an empty list. Type: " + get_class_name(mv_list) + " str: " + str(mv_list) + " len: " + str(len(mv_list)))
	result = []
	for mv in mv_list:
		assertd(isinstance(mv,pokepy.resources_v2.PokemonMoveVersionSubResource),
			"Bad mv in mv_list in str_move_versions(); it is not a Pokemon move version. Type: " + get_class_name(mv) + " str: " + str(mv))
		result.append(str_move_version(mv))
	assertd(is_list(result),
		"Bad output str_move_versions(); it is not a list. Type: " + get_class_name(result) + " str: " + str(result))
	assertd(len(result)>0,
		"Bad output str_move_versions(); it is an empty list. Type: " + get_class_name(result) + " str: " + str(result) + " len: " + str(len(result)))
	end_timer()
	return result

# capitalizes the names of moves and such in move list
def format_move_list(l):
	start_timer()
	for i in range(len(l)):
		l[i] = l[i].replace('-','')
	end_timer()
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
def move_list_from_file(dexnum):
	start_timer()
	move_list = []
	digits = format_digits(dexnum,3)
	#prefix = "Serebii.net Pokédex - #"
	prefix = "view-source_https___www.serebii.net_pokedex-gs_"
	species_name = get_PKMN_name(dexnum).capitalize()
	postfix = ".shtml"
	#fname = dex_folder + prefix + digits + " - " + species_name + postfix
	fname = dex_folder + prefix + digits + postfix
	printd(fname) 
	fname2 = dex_folder + "view-source_https___www.serebii.net_pokedex-gs_001" + postfix
	printd(fname == fname2)
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
			l = k.split('/')[-1].lower()
			if(l == 'psychict'):
				l = "psychic"
			# ... should this be "l in all_type_names", not "not in" ??
			if(l!="" and l not in all_type_names):
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
	fp.close()
	end_timer()
	return move_list

def organize_move_list(l):
	return "blah"

def pkmn_to_str(name, dexnum):
	return name.title() + " (" + str(dexnum) + ")"

# returns a list of the strings of the types associated with this pokepy pokemon p
# if they have no second type, output[1] == "None"
# returns in lower case
# TODO: standardize string formatting throoguhout so we don't always have to reform input
def extract_type_names(p):

	start_timer()

	pkmn_types = p.types
	pkmn_type_names = []

	pkmn_type1 = pkmn_types[0]
	pkmn_type1_name = pkmn_type1.type.name.strip().lower()
	pkmn_type_names.append(pkmn_type1_name)

	is_monotype = len(pkmn_types) == 1

	if not is_monotype:
		pkmn_type2 = pkmn_types[1]
		pkmn_type2_name = pkmn_type2.type.name.strip().lower()
		pkmn_type_names.append(pkmn_type2_name)

	# replace fairy type pokemon with correct types on a case by case basis
	if 'fairy' in pkmn_type_names:

		dexnum = p.id

		# pokemon that need to be typed "normal"
		normal_type_dexnums = [35, 36, 173, 174, 175, 176, 209, 210]
		if dexnum in normal_type_dexnums:	
			pkmn_type_names = ['normal']

		# Mr. Mime case
		if dexnum == 122:
			pkmn_type_names = ['psychic']

		# Marill and Azumarill cases
		if dexnum == 183 or dexnum == 184:
			pkmn_type_names = ['water']

	"""
	# override fairy type with the correct type (this is idiosyncratic to the pokemon case and just handled by if/else below)
	#TODO: ensure this works correctly with the movesets of normal type pokemon and checking condition below for move type
	if pkmn_type1_name == "fairy":
		pkmn_type1_name = "normal"
	pkmn_type_names.append(pkmn_type1_name)

	# pokemon has a second type
	if not is_monotype:
		pkmn_type2_name = pkmn_type2.type.name.strip().lower()

		# replace fairy with normal
		if(pkmn_type2_name == "fairy"):
			pkmn_type2_name = "normal"

		# if the change from fairy to normal (or something else) causes this pokemon to have the same type twice, instead say second type is None
		if(pkmn_type2_name not in pkmn_type_names):
			pkmn_type_names.append(pkmn_type2_name)

		else:
			pass
			#pkmn_type_names.append("None")

	# pokemon has no second type: add None
	else:
		pass
		#pkmn_type_names.append("None")
	"""

	end_timer()

	return pkmn_type_names

# checks that the nickname n is a string and between 1 and 10 characters inclusive
#TODO: note that this increased to max of 12 charactrers after gen 5 apparently?
def is_legal_nickname(n):
	if not is_str(n):
		return False
	l = len(n)
	return l > 1 and l < 11

# TODO: global variable type_names probably redundant w/ local variables in other functions 
def get_type_color(type_name):
	start_timer()
	assertd(is_str(type_name))
	type_name_formatted = type_name.strip().capitalize()
	assertd(type_name_formatted in all_type_names)
	if type_name_formatted == 'Bug':
		return get_color("green") + get_style("dim")
	elif type_name_formatted == 'Dark':
		return get_color("black") + get_style("bright")	
	elif type_name_formatted == 'Dragon':
		return get_color("blue") + get_style("dim")
	elif type_name_formatted == 'Electric':
		return get_color("yellow") + get_style("bright")
	elif type_name_formatted == 'Fighting':
		return get_color("red") + get_style("normal")
	elif type_name_formatted == 'Fire':
		return get_color("red") + get_style("bright")
	elif type_name_formatted == 'Flying':
		return get_color("cyan") + get_style("normal")
	elif type_name_formatted == 'Ghost':
		return get_color("magenta") + get_style("dim")
	elif type_name_formatted == 'Grass':
		return get_color("green") + get_style("bright")
	elif type_name_formatted == 'Ground':
		return get_color("yellow") + get_style("dim")
	elif type_name_formatted == 'Ice':
		return get_color("cyan") + get_style("bright")
	elif type_name_formatted == 'Normal':
		return get_color("white") + get_style("bright")
	elif type_name_formatted == 'Poison':
		return get_color("magenta") + get_style("normal")
	elif type_name_formatted == 'Psychic':
		return get_color("magenta") + get_style("bright")
	elif type_name_formatted == 'Rock':
		return get_color("red") + get_style("dim")
	elif type_name_formatted == 'Steel':
		return get_color("white") + get_style("dim")
	elif type_name_formatted == 'Water':
		return get_color("blue") + get_style("bright")
	else:
		printd("unrecognized type name to get_type_color(): " + str(type_name))
	end_timer()