# functions related to timing other functions for performance purposes

# ... i'm abandoning this for now because I realize recursive functions complicate this.
# if i could get rid of those in my code perhaps this would be more feasible.
# NOTE: i was using the second reply in https://stackoverflow.com/questions/7370801/measure-time-elapsed-in-python 
# 		where it seems that the first (using time.time()) is more succinct

"""
from timeit import default_timer as timer

# metrics desired to track:
# 1 function name
# 2 number of calls
# 3 total time length
# 4 average time length
# 5 (not yet implemented) (if DEBUG off and catching exceptions) - # of errors thrown; avg # of errors'

# stats for functions
# a string function name is mapped to a tuple containing the above metrics in that numbered order
# the average time length will not be 
fstats = {}

# ftimers maps a string function name to its "start" time
# used to calculate "run_time" and add this to fstats
fstart_times = {}

# input - fname is string name of function to time/track
# start_timer() should ideally be called IMMEDIATELY at the start of the calling function
# NOTE: technically the timer will be slightly off due to the overhead time between getting/storing the "start" time 
#	    and when we return to the parent function and it actually resumes computation
#		... but this will be inherent/constant to all functions
# 		you could perhaps test this overhead time by starting then immediately stopping a function
#		hopefully the overhead is minimal compared to function computation time...
# output - None (start_timer() returns nothing but starts the timer which tracks the calling function's time
def start_timer():

	# name of the function which called start_timer()
	parent_fname = get_parent_fname()


	# if we don't have an entry in fstats for this function (thus no entry in fstart_times), setup an entry
	# ... actually, we can reduce overhead and just setup that entry when the stats are needed in end_timer()
	"""
	if not parent_fname in fstats:
		# sanity check that fstats and fstart_times keys match
		assertd(not parent_fname in fstart_times, "start_timer(): fstats and fstart_times dont match.")
		
		fstats[parent_fname] = (None, None, None, None, None)
	"""

	# if start_timer() is called, we either shouldn't be tracking 
	assertd(fstart_times[parent_fname] == None)

	# NOTE: we want to record the start time of the function as close to its actual start time as possible
	#		so we should get/store the timestamp right before we return
	# 		i think if that overhead of returning the function was near constnat (might not be w/ OS noise) 
	# 		you might be able to adjust what we store into fstart_times
	
	fstart_times[parent_fname] = timer()


def end_timer():

	# we want to get the end time as close to the end of calling function, so rihgt at the start of end_timer()
	# NOTE: dont use get_time() as we want to minimize overhead
	end_time = timer()

	# name of the function which called end_timer()
	parent_fname = get_parent_fname()

	assertd(parent_fname in fstats)
	assertd(parent_fname in fstart_times)

	fstats[parent_fname] = (None, None, None, None, None)
	# reset the entry in fstart_times so we know we arent tracking this function anymore
	# if space requirements are a concern, could delete the entry in fstart_times
	# ... BUT I could imagine that knowing we WERE tracking the function (but aren't any longer) could be useful
	fstart_times[parent_fname] = None




# input: optional fname
# output: prints the stats associated with all functions and saves them to output test files
def timing_stats(fname = None):

	for 

"""