----- created 6/30/19 -----

----- Copyright Disclaimer -----

THIS PROJECT AND ALL OF ITS RELATED PROGRAMS AND RESOURCES ARE ENTIRELY NON-PROFIT AND ARE INTENDED TO BE USED UNDER FAIR USE COPYRIGHT POLICY.

Copyright Disclaimer Under Section 107 of the Copyright Act 1976, allowance is made for "fair use" for purposes such as criticism, comment, news reporting, teaching, scholarship, and research. Fair use is a use permitted by copyright statute that might otherwise be infringing. Non-profit, educational or personal use tips the balance in favor of fair use.

NO REVENUE IS DERIVED FROM THIS PROJECT IN ANY FORM WHATSOEVER (including social media views, Patreon or other monetary crowdfunding platforms, etc.) 

Pokemon and all related Intellectual Property (IP) are subject to copyright by its respective owners, including Nintendo, Nintendo of America, Game Freak, and any other related owning or publishing entities. The contributors to this project do not claim any ownership of said IP, and again, no revenue is derived from this project by any means. Please support the official release.

This project is intended to expand the skills and experience of the developers, and to provide personal, non-profit entertainment for users. 

The contributors to this project do not condone illegaly obtaining copyrighted software. This project will not supply ROMs or other related files (or information on how to obtain them) to users. The user is assumed to have obtained such files by legal means. Furthermore, in its current state as of 8.7.19, this project does not even directly interact with ROMs or other related files. 

The contributors to this project do not assume any legal responsibility for any client's misuse of software, including but limited to misrepresenting the Pokemon franchise or using this program to earn revenue in an illegal fashion.



----- Introduction -----

These scripts are intended to generate random teams of Pokemon that meet certain rules. These teams can then be converted into commands used by the program "PkHex" to modify the save of a GBC ROM ("game") file so that the teams are available for play in Pokemon Stadium. :)

The standard use case is as simple as running the python script, pasting the output into PkHex to modify the save files, and booting the emulator. 

The script's main commands are:

teammake - generates two teams of random pokemon according to the ruleset.
teamedit - rerandoms a specified pokemon.
teamshow - displays the current teams.
teamcopy - copies the "PkHex command" text for each Pokemon, one at a time, to the Windows clipboard, to be pasted into the "Batch Editor" of PkHex.
teamsave - saves each team to a .txt file so it can be loaded or referenced later. Currently, teams are automatically saved after teammake and teamedit.
teamload - loads two teams, one from each of two provided file paths, into the program.

The standard ruleset is as follows:

--- no banned pokemon

	--- baby

	--- legendaries

	--- unevolved


--- moveset restrictions

	--- a Pokemon's learnable moves includes those it can learn from leveling, a prior evolution, TM/HM, Tutors, and even Special Events
		--- Special Event moves may be flagged as "illegal" (pink text) in Pokemon Stadium 2, but are technically legal

	--- Pokemon's first move is of its first type (if possible)

	--- Pokemon's second move is of its second type (if possible)

	--- "inferior" moves are replaced with learnable "superior" moves
		--- i.e. if Charmander can learn Tackle and Strength, do not include Tackle in its learnable move pool

	--- no banned moves
		--- most banned moves are banned because they are useless or nearly useless in comba (i.e. Teleport, Bind, Mud-Slap, Tackle, etc.)
		--- most moves that depend on the user/enemy BEING sleep are banned
			--- i.e. Dream Eater, Snore, Nightmare, Sleep Talk, etc.
			--- ideally these moves are unbanned and instead the program simply gives these moves only when the appropriate associated move is also present
		--- most moves that depend on gender are banned
			--- gender isn't working correctly in the script rn so ... banned
		--- more controversial/opinionated bans
			--- Double Team and Minimize 
				--- evasion stacking needs a specific response, and with randomized moves, imo a Pokemon with high evasion may be practically unstoppable
			--- Mud-Slap
				--- too many Ground pokemon are randoming this as their required Ground move, and it makes them less threatening and the games longer and less exciting.
				--- this move can have legitimate use and eventually should be unbanned as it is less problematic than evasion buffs (since you can simply swap out if your accuracy is debuffed too much)... but given our current implementation, its coming up too much. 
			--- Rage
				--- imo just not good and gets randomed too much since basically every Pokemon can learn it
			--- False Swipe
			--- Return/Frustration
				--- currently Pokemon are set to 0 happiness, making Return do minimum damage (sometimes <1 damage!) and Frustration does max
					--- as a workaround... just do neither
				--- even if Frustration is viable and enabled, the move would appear really often since practically every Pokemon can learn it

	--- (not yet enforced) a pokemon must have at least one damaging move (unclear if moves inflicting Poison status are "damaging" but I'd say yes)



----- Resources -----

"Github Project Root Folder" - where this project is maintained
- htps://github.com/travis4dams/fantasypokemon

"Pokepy" - main data source backend
API 
- https://pokeapi.github.io/pokepy/
- https://pokeapi.co/docs/v2.html/#berries
GitHub
- https://github.com/PokeAPI/pokepy

"Projec64" - suggested N64 emulator
- https://www.pj64-emu.com/download/project64-latest

"PkHex" - program used to modify GBC Save files
batch editor guides
- https://github.com/kwsch/PKHeX/issues/516
- https://projectpokemon.org/home/forums/topic/45398-using-pkhex-how-to-use-the-batch-editor-in-pkhex/


----- Installation / Setup -----

This script is currently only tested on a standard Windows 10 operating system.

To run this script, the following programs are needed:
--- Python3 (https://www.python.org/download/releases/3.0/)
--- PkHex (https://projectpokemon.org/home/files/file/1-pkhex/)
--- N64 Emulator
	--- I use Project64 v2.2.0.3. However as of 8.7.19 they seem to be up to v2.3.2-202. If you get a recent version I'm sure it'll work fine.
		--- https://www.pj64-emu.com/download/project64-latest

You will also need ROM files for Pokemon Stadium 2 for the N64, and a Generation 2 (Gold, Silver or Crystal; aka "GSC") GBC ROM and .sav file. (As noted in the copyright disclaimer, the contributors to this project will NEVER supply ROMs or information on how to obtain them.)

I STRONGLY SUGGEST CREATING A COPY OF THE SAVE FILE if it is one that you care about. The program works by OVERWRITING EXISTING POKEMON, so obviously you don't want to include Pokemon you intend to keep.

Once you have these files downloaded, you'll want to first point your N64 Emulator to the GBC ROM and .sav files you intend to load into Pokemon Stadium for play. Since the original N64 loaded in GBC data through "transfer paks" attached to the controller, your emulator probably models this by having the save file associated with your controller. So, make sure to plug in the controllers you intend to use. (You may also want to setup your controller input settings if you haven't already).

For Project64, I point the emulator to the .sav file by selecting "Options", "Configure Controller Plugin", "Controller Pak", and then supply the path to GB Rom file and Sav file in the associated fields. If you're playing a two player game, you'll want each controller to point to a DIFFERENT .sav (and perhaps a different ROM too, I've only tested it with two independent ROMs). It's fine if the saves/ROMs are copies of each other, you just want seperate files. 

After pointing Project64 to the ROM and .sav files, start PkHex. Using "File" > "Open", open the first save file that you intend to edit your first team into. You should see the Pokemon storage boxes from the save. You can view a Pokemon by right clicking and selecting "View", and you can override the Pokemon in a current slot with the Pokemon you are currently viewing by right clicking that slot and selecting "Set". Ultimately we will be trying to edit the Pokemon into the "Party-Battle Box". For now, go ahead and open up the "Batch Editor" which allows us to enter in text commands that the program uses to setup the Pokemon for us. Open the Batch Editor by selecting "Tools" then "Data" then "Batch Editor". This will open a text box with some other options. We will simply be repeatedly pasting text into the text box then hitting "Run".

Now, start the main.py script in the src folder using python. So far it only supports command prompt ("terminal") use. The script contains many commands (see their description above, or the help command in terminal). You can generate two teams with teammake, then rerandom specific pokemon with teamedit if you'd like. 

Next, we will copy the commands from our program into PkHex. Enter the "teamcopy" command into the terminal. Then, each time you press a key, the program will copy a bunch of text to your Windows clipboard. Simply Alt+Tab back to PkHex, paste the text into the text box, and hit Run (make sure there are no leading/trailing newlines). You should see a message saying something like "Modified 1/200 Files"; press OK to dismiss the message. Repeat this process by Alt+Tab'ing back to the terminal, pressing any key to copy another set of text commands, then Alt+Tab back and paste over what you currently have. Do this for all 6 members of the first team.

After that we have to move the Pokemon from Box 1 to the Party (I couldn't find a way for the commands to edit them into the party directly, but I bet there is a way). Go to the first Pokemon in Box 1, right click and select "View", then go to "Party-Battle Box", and then right click the first pokemon in the Box and select "Set" to replace it with your viewed Pokemon. Do this for all 6 pokemon on your team.

To finish our changes to the save, we need to go to "File" > "Export Sav" > "Export Main". Save the file with the same name as the save file you loaded. You should get a notice that the file already exists and that this will overwrite it; that's fine.

Now repeat the process by opening another save file in PkHex and load in the next 6 pokemon from team 2 into this second save file.

After all that, if you've set everything up right, you should be able to boot up Pokemon Stadium 2 in your emulator client, and the modified save files will be loaded in like GBC games in the N64's transfer pak.

Enjoy, and please report any bugs you encounter! :)



----- Future Plans -----

This project was originally envisioned to be a part of a "fantasy pokemon league" akin to a fantasy football league. This could mean many possible things, but one conception involves picking (or randomizing) a "pool" of pokemon, then successively battling with teams (subsets of your pool) of Pokemon with other teams from friends in the league, gaining experience and changing your team along the way, until perhaps a "season end" is reached and performance stats are compared.

However, in its current state, this project is focused on creating interesting Level 100 teams for "one-off" Pokemon Stadium battles. Much of this functionality could extend to a "fantasy pokemon" league though. Furthermore, extensive playtesting could inform us as to what factors lead to "interesting" or "competitive" battles, thus allowing us to develop a more balanced and enjoyable fantasy league later on. 

In terms of generating pokemon for one-off battles, this project would benefit from having more customization in HOW the pokemon/moves are generated. 

New features typically should accomplish at least one of the following: 
--- streamline the generation process
--- remove/limit unfair/uninteresting gameplay factors
--- cause luck (aka, randon number generation or "RNG") to be less polarizing
	--- we can't do much about crits or other in-game things...
	--- BUT we can do things like making sure one team doesn't get a strong advantage just by chance
--- balance/tune things like team compositions and movesets
	--- in other words make each team feel more well-rounded or purposeful
--- enhance the replay value of battles by making them more fun, interesting, varied, or competitive 
--- add creative and fun new matchups, team strategies, moveset strategies and ways to battle  

There are many factors which could be considered when balancing teams, movesets and so on. I've listed some below, but there are likely many more possible ideas. 

When balancing a factor, a meaningful question is often, "If teams/pokemon differ in this factor, does that significantly impact performance/success? If so, how can this effect be mitigated?"

--- type effectiveness 
	--- specific matchups given the current teams
	--- or perhaps just type coverage in general
--- average stats
--- held items
--- EVs/IVs
	--- If Marowak is allowed Thick Club its effective base attack could be doubled... that could roughly capture the effect in lieu of held items.
--- "competitive ranking"
	--- this could be approximated by Smogon "tier status" (OU v NU etc)
		--- it could also maybe be aggregated with other fanmade tier lists, if they differ significantly
		--- note that a tier ranking might effectively function as the assessment given by all the other metrics ... BUT this "human rated" element might inform what constitutes a "good" move/pokemon/whatever
--- roles 
	--- more of a vague notion but could balance teams around like 1 tank 1 opener 1 support 1 sweeper(special) 1 sweeper(physical) 1baton pass or smt idk... keeping roles balanced or at least sticking to an interesting preset rather than getting RNG'd into "6 tanks"
--- legendaries
	--- obviously tips the scales



