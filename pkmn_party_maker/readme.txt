----- created by Nathan Giles 6/30/19 -----




--- Intro

These scripts are intended to generate teams of pokemon and then output commands to the "batch editors" of PkHex so that the teams can be modified into a save file available for play in Pokemon Stadium. :)

At a minimum I want the script to be able to generate random Pokemon and random movesets and output the appropriate commands for PkHex. If I understand how these tools work, it SHOULD mean creating a team would be as simple as running the python script, copying its output into PkHex, saving, and booting the emulator. 

Ideally, some features I'd like to sprinkle in would be more customization in HOW the pokemon/moves are randomized... likely for the purpose of streamlining the process, removing BS factors, causing RNG to be less polarizing, or balancing things like team comps and movesets.

Some factors to consider for "balance" (many of these mean "consider the differences of these stats between teams/pokemon when randomizing and keep that difference under a certain threshold":
--- type effectiveness matchups and/or type coverage in general
--- average stats
--- held items
--- EVs/IVs
--- Smogon "tier status" (OU v NU etc)
		--- (this may be an apxn of the other metrics but could also contain a "meta" element that is helpful to slightly tune this but i dont think it should be weighted much)
--- roles 
	--- more of a vague notion but could balance teams around like 1 tank 1 opener 1 support 1 sweeper(special) 1 sweeper(physical) 1baton pass or smt idk... keeping roles balanced or at least sticking to an interesting preset rather than getting RNG'd into "6 tanks"
--- legendaries
	--- not allowed
--- banned pokemon
	--- caterpie,metapod,weedle,kakuna,magikarp
	--- baby pokemon
	--- others(??)



If Marowak is allowed Thick Club its effective base attack should be doubled... I think that roughly should capture that effect




--- Tools Used

Pokepy
API - https://pokeapi.github.io/pokepy/
https://pokeapi.co/docs/v2.html/#berries
GitHub project - https://github.com/PokeAPI/pokepy



PkHex
batch editor guides:
https://github.com/kwsch/PKHeX/issues/516
https://projectpokemon.org/home/forums/topic/45398-using-pkhex-how-to-use-the-batch-editor-in-pkhex/



travis github project "fantasypokemon"
https://github.com/travis4dams/fantasypokemon