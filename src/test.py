# for now, loosely following these testing design guides: 
# https://docs.python-guide.org/writing/tests/
# 

class Tester:

	def __init__(self):
		pass

# generates a quick randomly generated team with for testing purposes
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

# ... for now i will just test the movesets of the "competitive viable" pokemon, usually at the end of an evolution
# test the following pokemon:
# --- main case: new "branching" evolutions ---
# 133, 134, 135, 136 and 196, 197 (Eevee and Evos), 
# 43, 44, 45, 182 (Oddish Gen 1 Evos and Bellossom)
# 60, 61, 62, 186 (Poliwag Gen 1 Evos and Politoed)
# 79, 80, 199 (Slowpoke, Slowbro, Slowking)
# 106, 107, 236, 237 (Tyrogue and Evos)
# --- optional case: new (non-branching) evolutions --- 
# steelix
# scizor
# blissey
# kingdra
# crobat
# porygon
# --- optional case: baby pokemon ---
# pichu
# cleffa
# igglybuff# 
# smoochum
# elekid
# magby
# togepi togetic
# TODO: baby pokemon also might be impt to test, esp with moveset generation... 
#	 	even if they are in a consistent "chain" with no branches,
#		and even if they are currently banned in game usage
# TODO: test steelix, scizor, and other pokemon who were given an additional evo in gen 2 (even if it is not a "branch")
def test_corner_case_evolutions():

	# sets might be more appropriate but perhaps keeping an order to the dexnums will come in handy
	# for such a small dataset it doesn't matter
	eevee_dexnums = [133, 134, 135, 136, 196, 197]
	oddish_dexnums = [43, 44, 45, 182]
	poliwag_dexnums = [43, 44, 45, 182]
	slowpoke_dexnums = [79, 80, 199]
	tyrogue_dexnums = [106, 107, 236, 237]

	# test_case_dexnums is a list of lists of ints
	test_case_dexnums = [eevee_dexnums, oddish_dexnums, poliwag_dexnums, slowpoke_dexnums, tyrogue_dexnums]
	for evolution_list in test_case_dexnums:
		for dexnum in evolution_list:
			pkmn = Pokemon(dexnum)
			evo_path = pkmn.get_evolution_chain()
			# print and wait for all of these
			evo_chain = pkmn.get_evolution_chain()

			lm = pkmn.get_learnable_moves()

	return 

# TEST DUMP

# test evolution paths
"""
for dex_num in range(1,252):
	print_evolution_path(dex_num)
	input()
"""