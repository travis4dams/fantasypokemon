# ----- main description -----

""" 
functions related to timing other functions for performance purposes
timing can be used to track how long a function or even a segment of code takes
if you are tracking a segment of code (and not a function), 
or you are using a function name that is identical to another tracked function name, 
or you simply want to supply an alternate name for a function,
you should supply an alternate function name to start_timer() and end_timer()
a lack of input to start_timer() and end_timer() causes them to default to the calling function's name

NOTE - these functions do nothing if DEBUG is enabled

NOTE - ... based on testing, it seems timing functions is adding SIGNIFICANT overhead (like a factor of 5x) to the overall runtime
		this doesn't mean that our timing of hte functions is necessarily inaccurate, but simply that measuring the time of a function
		is adding significant computational time
		... perhaps the primary cause of my results is having a timer in a really low level (aka super short runtime) function?

NOTE - the timing will be slightly innacurate due to overhead/errors of certain sources
		for start_timer, it introduces overhead in the time it starts start_timer completing until it fetches stores the start_time at the very end
						AND due to inherent programming language function ovehead,
						 the start_time of the function comes before the moment we finish returning to the parent function and resume computation
		for end_timer, overhead time is the time between when 
		... BUT thee errors will be inherent/constant to all functions and thus comparisons are still valid
		you could perhaps test this overhead time by starting then immediately stopping a function, or something similar
		hopefully the overhead is minimal compared to function computation time...
		it then might be possible to remove the overhead from timing estimates...?

METRICS RECORDED:
0 function name
1 number of calls
2 total time length
3 average time length
4 % of all tracked runtimes (the value stored in funct_stats will be an ESTIMATE until given a precise calculation when requested in timing_stats)
5 (not yet implemented) (if DEBUG off and catching exceptions) - # of errors thrown; avg # of errors'
6 (neither added nor implemented) - % of all tracked runtimes MINUS any tracked input() time spent waiting for user input 
									  user input function actually has this value set, but it may not be so relevant, 
								  	  i.e. 150%	would mean user input delay time was 1.5 times the sum of other timed methods			
"""

# ----- todo/ideas/notes -----

"""
 ... i originally abandoned this because I realized recursive functions complicate this
 ... but i gave a potential workaround that should skip subcalls (and also duplicate function names)
 	 i was using the second reply in https://stackoverflow.com/questions/7370801/measure-time-elapsed-in-python 
 	 where it seems that the first (using time.time()) is more succinct

#TODO: determine how to properly handle recursive functions
#TODO: this will struggle with functions that share the same name, and requests the user 
#		... i.e. move.get_id() and pokemon.get_id() or smt like that
#		... we could perhaps have a work around based around their stack trace or code line or some native unique function identifier?
#TODO: similar helper library to monitor space requirements?
#TODO: are there existing extensive "timing" libraries like what im trying to build here? ... 
#		... i should look into modern programming practices and supporting libs and stuff... might be some good debugging python stuff out there

#TODO: as indicated by the description above, "function" is bad naming scheme for something which COULD just be a section of code
# 		... then again any section of code could be considered a sub-function if you wanna get technical.
#		... a better name might fit it or maybe it's technically fine.

#TODO: perhaps having get_time() function here instead of helper_functions would optimize things

#TODO: could track if a function that starts a timer has a parent function being tracked
#		if so, mark it as a child, and use this to somehow give more meaningful measures of which functions are taking the biggest chunks out of runtime 
#TODO: ... could do this to programatically analyze which stack traces take up the most time in the overall script runtime?
# 		in other words, can i programatically detect the most significant algorithms or function trees based on total runtime?
#		... i feel like that's a great idea :D ... there is a lot you could do with this. 
# 		you could maybe include some of the function tree when presenting timing stats. 
# 		or see if the function takes longer when called by different parents, 
# 		suggesting the input types/lengths or just runtime circumstances are different
# 		could perhaps mark recursion in a similar manner, or treat it differently in output stats (i.e. track parent as one version, and children as another)

#TODO: is there some way to detect when a program returns, so that it doesnt have to call end_timer? 
#		we still want end_timer in some cases (i.e. testing, user input) where we want to start and end the timer at specific points

#TODO: could color code the functions based on their algorithnic type... i.e. related to pkmn, move, file I/O, user I/O, pokepy, db loading, etc

#TODO: an OOP "Timer" design to this might (??) help for testing, so we can open and close a set of timers and their stats easily...?

#TODO: this might be complicated, but if we could somehow remove the timer overhead time (by some estimate or other means) from the timing calculations,
		we might be able to 
		i might have hinted at this elsewhere but basically the lowest level timed function may be accurate but because of timer overhead the parent function's time
		will include the overhead time associated with timing that lowest level (child) function

#TODO: add an option to time functions by adding their name at some point in some test function; 
#	   rather than having to put start_timer and end_timer in the function, making it less readable

"""

# ----- imports -----

#from timeit import default_timer as timer
import helper_functions as hf
from pglobals import DEBUG 

# ----- globals -----

# flag indicating whether the execution of these timing functions is independent of DEBUG flag
timing_ignores_DEBUG = False

# funct_stats is a dict mapping a string "function name" to a tuple containing the above metrics in that numbered order#
funct_stats = {}
 
# funct_start_times maps a string function name to its "start" time
# used to calculate "run_time" and add this to funct_stats
funct_start_times = {}

# total_tracked_time is PRESUMED to keep track of the TOTAL time used by ALL functions
# 	(it is "presumed" because it is up to the calling function to call start_script early on... see that function for details)
# total_tracked_time is used to calculate each function's "% of total time" stat
# NOTE: this opriginally was not the same as the runtime of the script. 
#		however, since a parent and a child function could call start_timer(), 
# 		multiple functions were contributing to total_tracked_time at the same moment in time
# 		... a workaround I made for this was making a start_script() function, 
#		... and in lieu of an end_script() function, assume timing_stats is called when the script ends
total_tracked_time = 0

# the PRESUMED start time of the entire script
# see start_script
script_start_time = -1

# the default stat in list of metrics (see description above) that the output stats is sorted by when displaying
default_sort_stat = 2

# ----- functions -----

# sets global variable script_start_time
# it is up to the calling function (should be root of entire script, or root of some testing protocol) to set this as early as possible
def start_script():
	start_time = hf.get_time() # retrieve time as close to call of this function as possible
	global script_start_time
	script_start_time = start_time

# start_timer is meant to begin a "timer" that tracks the runtime of a function or section of code
# IDEALLY, start_timer is called at the VERY BEGINNING (of the relevant section) of the calling function meant to be timed
# 		("relevant" might mean portions after input handling, for example)
# in terms of implementation, start_timer sets up an entry in the funct_start_times dict marking the start time of a function
# NOTE: technically the timers will be slightly off due to over head time. see comment @ top of timing.py.
# input - ...
# output - None (start_timer() returns nothing but tracks the calling function's start time
def start_timer(parent_fname = None):

	# if our output depends on DEBUG and DEBUG is off - don't time anything
	global timing_ignores_DEBUG
	if not timing_ignores_DEBUG and not DEBUG:
		return

	# input is given - use that instead of default
	if parent_fname != None:
		hf.assertd(hf.is_str(parent_fname) and parent_fname.strip() != "")
		
	# default case - use parent function name
	else:
		parent_fname = hf.get_parent_funct_name() 
		

	# if we don't have an entry in funct_stats for this function (thus no entry in funct_start_times), setup an entry
	# ... actually, we can reduce overhead and just setup that entry when the stats are needed in end_timer()
	"""
	if not parent_fname in funct_stats:
		# sanity check that funct_stats and funct_start_times keys match
		hf.assertd(not parent_fname in funct_start_times, "start_timer(): funct_stats and funct_start_times dont match.")
		
		funct_stats[parent_fname] = (None, None, None, None, None)
	"""

	#hf.printd(parent_fname)

	# if start_timer() is trying to use a parent_fname that is ALREADY TRACKED: SKIP this start_timer() call
	# in such a case, the two situations I imagine are:
	#	1 - someone called start_timer on the same function twice without a close
	#		OR 
	# 	2 - its a recursive function 
	# (a function is "tracked" if its entry in funct_start_times != None; a None entry in funct_start_times means it was once tracked)
	# NOTE: if its a recursive function, the "lazy policy" for now is to just skip it.
	#		I believe this effectively lets the root parent call stand as the function instance to track,
	#		which is not a terrible solution I think.
	if parent_fname in funct_start_times and funct_start_times[parent_fname] != None:
		return

	# NOTE: we want to record the start time of the function as close to its actual start time as possible
	#		so we should get/store the timestamp right before we return
	# 		i think if that overhead of returning the function was near constnat (might not be w/ OS noise) 
	# 		you might be able to adjust what we store into funct_start_times
	funct_start_times[parent_fname] = hf.get_time()

	#hf.printd(funct_start_times)

# end_timer is meant to end the "timer" associated with the calling function AND update all of its "independent" stats 
#		("independent" meaning doesn't need reliable estimates of a/an/all other stat(s), such as "percent of total time";
#		 such "dependent" stats will be inaccurate until display_timing_stats is called to close out all timing)
# IDEALLY, end_timer is called at the VERY END (of the relevant section) of the calling function meant to be timed
# 		("relevant" might mean portions after input handling, for example)#		
# in terms of implementation, end_timer sets the relevant entry in funct_start_times dict to None, marking it as "previously tracked"
#		then 
# NOTE: technically the timers will be slightly off due to the overhead time between getting/storing the "start" time 
#	    and when we return to the parent function and it actually resumes computation
#		... but this will be inherent/constant to all functions and thus comparisons are still valid
# 		you could perhaps test this overhead time by starting then immediately stopping a function, or something similar
#		hopefully the overhead is minimal compared to function computation time...
# input - ...
# output - None (start_timer() returns nothing but tracks the calling function's start time
def end_timer(parent_fname = None):

	# we want to get the end time as close to the end of calling function, so rihgt at the start of end_timer()
	# TODO: perhaps dont use get_time() as we want to minimize overhead
	end_time = hf.get_time()

	# if our output depends on DEBUG and DEBUG is off - don't time anything
	global timing_ignores_DEBUG
	if not timing_ignores_DEBUG and not DEBUG:
		return

	# fetch/check parent function name
	if parent_fname == None:
		parent_fname = hf.get_parent_funct_name() # name of the function which called end_timer()
	else:
		hf.assertd(hf.is_str(parent_fname) and parent_fname.strip() != "")

	# sanity check that we have an entry in table of start times
	# if not, workaround is do nothing and return
	hf.assertd(parent_fname in funct_start_times)
	if not parent_fname in funct_start_times:
		return

	# fetch start time
	start_time = funct_start_times[parent_fname]
	
	# if start_time is None, there are two cases I consider:
	#	1 - end_timer was called on a function that was once tracked, but didn't have the proper start_timer() call
	#	2 - end_timer was called on a function that returns a result to a recursive call, thus causing a child function to attempt to end_timer on the parent
	# in either case, if we are ending a timer we are no longer tracking, just do nothing as a workaround
	#hf.assertd(start_time != None) # otherwise 
	if start_time == None:
		return

	# calculate time elapsed
	time_elapsed = end_time - start_time

	# update total runtimes
	global total_tracked_time
	#total_tracked_time += time_elapsed

	# this function hasn't been tracked before - initialize its stats tuple
	if not parent_fname in funct_stats:
		stats = (parent_fname, 0, 0, 0, 0, 0)
	else:
		stats = funct_stats[parent_fname]

	# calculate updated stats
	new_num_calls = stats[1]+1
	new_total_time = round(stats[2] + time_elapsed, 7)
	new_avg_time = round(new_total_time / new_num_calls, 7)
	#new_percent_of_all_tracked = round(new_total_time / total_tracked_time, 5)

	# record updated stats
	funct_stats[parent_fname] = (stats[0], new_num_calls, new_total_time, new_avg_time, 0, 0)

	# reset the entry in funct_start_times so we know we arent tracking this function anymore
	# NOTE: if space requirements are a concern, could delete the entry in funct_start_times
	#		... BUT I could imagine that knowing we WERE tracking the function (but aren't any longer) could be useful
	funct_start_times[parent_fname] = None

# TODO: better description in line w/ other functions. and give input description comments for all functions
# input: optional fname
# output: prints the stats associated with all functions
# funct_stats is unalterred
def display_timing_stats(fname = None):

	# fetching this closest to start of function is best
	end_time = hf.get_time()

	print("\nDisplaying function timing statistics...")

	global total_tracked_time
	global script_start_time

	total_tracked_time = end_time - script_start_time

	print("\nTOTAL RUNTIME: " + str(round(total_tracked_time,2)) + " seconds.\n")

	if hf.input_wait_identifier in funct_stats:
		percent_str = str(round(funct_stats[hf.input_wait_identifier][2] / total_tracked_time, 4) * 100)
		print("\nUser input delay accounted for " + percent_str + "% of the runtime.\n")

	# print stats for all tracked functions
	if fname == None:

		# get the stats and sort by total time
		all_stats = list(funct_stats.values())
		hf.sort_list_of_tuples(all_stats, default_sort_stat, True)

		# lists tracking the STRINGS of every stat, so this can be properly tab formatted
		# the lists are initialized to the label of the column since that should be included in tab formatting
		function_names = ['funct_name']
		function_calls = ['# calls']
		function_total_times = ['total time']
		function_avg_times = ['avg time']
		function_percent_times = ['% of total']
		function_errors = ['# errors']
		for stat_tuple in all_stats:

			#hf.printd(stat_tuple)

			# "independent stats" do not reference total_tracked_time
			function_names.append(str(stat_tuple[0]))
			function_calls.append(str(stat_tuple[1]))
			function_total_times.append(str(stat_tuple[2]))
			function_avg_times.append(str(stat_tuple[3]))

			# "dependent stats" reference total_tracked_time
			current_percent_time = stat_tuple[4]
			current_total_time = stat_tuple[2]
			updated_percent_time = round(current_total_time / total_tracked_time, 5)
			function_percent_times.append(str(updated_percent_time*100)[0:6]+"%")

			# metric for number of errors is unimplemented
			function_errors.append(str(stat_tuple[5]))

		# format the strings to "tab align" them 
		# by padding strings with whitespace so each string is as long as the longest string in the list
		hf.tab_format(function_names)
		hf.tab_format(function_calls)
		hf.tab_format(function_total_times)
		hf.tab_format(function_avg_times)
		hf.tab_format(function_percent_times)
		hf.tab_format(function_errors)

		# assumes function lists are aligned
		for i in range(len(function_names)):
			out_str = function_names[i] + function_calls[i] + function_total_times[i] + function_avg_times[i] + function_percent_times[i] + function_errors[i]
			print(out_str)
			if i == 0:
				print("-"*len(out_str))

	# print stats for a specific function
	else:
		print(str(funct_stats[fname]))

	print("\nDone displaying function timing statistics.\n")
