----- created 6/30/19 -----

----- Copyright Disclaimer -----

THIS PROJECT AND ALL OF ITS RELATED PROGRAMS AND RESOURCES ARE ENTIRELY NON-PROFIT AND ARE INTENDED TO BE USED UNDER FAIR USE COPYRIGHT POLICY.

Copyright Disclaimer Under Section 107 of the Copyright Act 1976, allowance is made for "fair use" for purposes such as criticism, comment, news reporting, teaching, scholarship, and research. Fair use is a use permitted by copyright statute that might otherwise be infringing. Non-profit, educational or personal use tips the balance in favor of fair use.

NO REVENUE IS DERIVED FROM THIS PROJECT IN ANY FORM WHATSOEVER (including social media views, Patreon or other monetary crowdfunding platforms, etc.) 

Pokemon and all related Intellectual Property (IP) are subject to copyright by its respective owners, including Nintendo, Nintendo of America, Game Freak, and any other related owning or publishing entities. The contributors to this project do not claim any ownership of said IP, and again, no revenue is derived from this project by any means. Please support the official release.

This project is intended to expand the programming skills and experience of the developers, and to provide personal, non-profit entertainment for users. 

The contributors to this project do not condone illegally obtaining copyrighted software. This project will not supply ROMs or other related files (or information on how to obtain them) to users. The user is assumed to have obtained such files by legal means. Furthermore, in its current state as of 8.7.19, this project does not even directly interact with ROMs or other related files. 

The contributors to this project do not assume any legal responsibility for any client's misuse of software, including but limited to misrepresenting the Pokemon franchise or using this program to earn revenue in an illegal fashion.



----- Introduction -----

In their current state, these scripts generate teams of random Pokemon that meet certain rules. These teams can then be converted into commands used by the program "PkHex" to modify the save of a Game Boy Color (GBC) game (ROM) file so that the teams are available for play in an emulated Pokemon Stadium 2. :)

The standard use case is as simple as running the python script, pasting the output from the script into PkHex to modify the GBC save file, and booting the emulator. 

The script's main commands are:

teammake - generates two teams of random Pokemon according to the ruleset.
teamedit - rerandoms a specified Pokemon.
teamshow - displays the current teams.
teamcopy - copies the "PkHex command" text for each Pokemon, one at a time, to the Windows clipboard, to be pasted into the "Batch Editor" of PkHex.
teamsave - saves each team to a .txt file so it can be loaded or referenced later. Currently, teams are automatically saved after teammake and teamedit.
teamload - loads two teams, one from each of two provided file paths, into the program.


----- Resources -----

"Github Project Root Folder" - where this project is maintained
- htps://github.com/travis4dams/fantasypokemon

Python3 - necessary framework to run the scripts
- https://www.python.org/download/releases/3.0/)

"Pokepy" - main Pokemon "database" backend
API 
- https://pokeapi.github.io/pokepy/
- https://pokeapi.co/docs/v2.html/
GitHub
- https://github.com/PokeAPI/pokepy

"Projec64" - suggested N64 emulator
- https://www.pj64-emu.com/download/project64-latest

"PkHex" - program used to modify GBC Save files
download
- https://projectPokemon.org/home/files/file/1-pkhex/
batch editor guides
- https://github.com/kwsch/PKHeX/issues/516
- https://projectPokemon.org/home/forums/topic/45398-using-pkhex-how-to-use-the-batch-editor-in-pkhex/

pytest - python testing library
- http://doc.pytest.org/
- https://semaphoreci.com/community/tutorials/testing-python-applications-with-pytest



----- Installation / Setup -----

This script is currently only tested on a standard Windows 10 operating system.

To run this script, you need to 1) install a few programs, 2) install two python libraries, 3) download 2 game files, and 4) setup and run the programs.

1) Programs
--- Python3 https://www.python.org/download/releases/3.0/
--- PkHex https://projectPokemon.org/home/files/file/1-pkhex/
--- N64 Emulator https://www.pj64-emu.com/download/project64-latest
	(I use Project64 v2.2.0.3, however as of 8/7/19 they are up to v2.3.2-202. A more recent version should work too.)

2) Python libraries
(The following dependencies can be installed via "pip install")
--- Pokepy https://github.com/PokeAPI/pokepy
--- pytest http://doc.pytest.org/en/latest/getting-started.html

3) Necessary files
--- N64 ROM file for Pokemon Stadium 2 
--- GBC ROM and .sav file for Pokemon Gold, Silver or Crystal. 
NOTE: The .sav file MUST have the first 6 slots of Box 1 filled with any Pokemon.

DISCLAIMER: MAKE A COPY OF THE SAVE FILE IF IT CONTAINS POKEMON YOU CARE ABOUT. The program works by OVERWRITING EXISTING POKEMON in Box 1, so obviously you don't want any Pokemon in the save file that you intend to keep.

4) Setup and Run Programs
Step 1: Emulator Setup 
You need to give your N64 Emulator the location of your GBC ROM and .sav files you intend to load into Pokemon Stadium for play. Make sure to plug in any controllers you intend to use before starting the emulator. You should be able to share a keyboard for multiplayer games if desired. (Because of the way the original N64 worked, your emulator may associate GBC save files with your controller. You may also want to setup your controller input and N64 ROM folder settings if you haven't already).

For Project64, I point the emulator to the .sav file by selecting "Options", "Configure Controller Plugin", "Controller Pak", and then supply the path to GB Rom file and Sav file in the associated fields. If you're playing a multiplayer game, you'll want each controller to have a DIFFERENT .sav (and maybe a different GBC ROM, but I'm not sure if that's necessary; I make a copy to be safe. It's fine if the saves/ROMs are copies of each other, you just want separate files).

After setting up your emulator, I suggest closing it, so that it will reload the GBC files after we edit them later with PkHex. (It may work regardless of being closed but that's my suggestion.)

Step 2: Run this Program and Make/Load Teams
After pointing your emulator to the ROM and .sav files, start the main.py script in this project's src folder using python. So far this project only supports a command prompt ("terminal") interface. The script contains several commands (see their description above, or the help command in terminal). You can generate two teams with teammake, then rerandom specific Pokemon with teamedit if you'd like. You can also load previously saved teams from their file names as they appear in the main team folder.

Step 3: Start PkHex, Open GBC .sav Files, and Open Batch Editor
Next, start PkHex. Using "File" > "Open", open the first save file that you intend to edit your first team into. You should see the Pokemon storage boxes from the save. 

(You can view a Pokemon by right clicking and selecting "View", and you can override the Pokemon in a current slot with the Pokemon you are currently viewing by right clicking that slot and selecting "Set". Ultimately we will be trying to edit the Pokemon into the "Party-Battle Box".)

For now, open up the "Batch Editor" in PkHex which allows us to enter in text commands that PkHex interprets to setup our Pokemon. Open the Batch Editor by selecting "Tools" then "Data" then "Batch Editor". This will open a text box with some other buttons. We will simply be repeatedly pasting text into the text box and hitting "Run".

Step 4: Paste Commands into PkHex
Next, we will copy the commands from this program into PkHex. Enter the "teamcopy" command into the terminal. Then, each time you press a key, the program will copy a bunch of text to your Windows clipboard. Simply Alt+Tab back to PkHex, paste the text into the text box, and hit Run (make sure there are no leading/trailing newlines). If it worked, you should see a message saying something like "Modified 1/200 Files"; press OK to dismiss the message. Repeat this process by Alt+Tab'ing back to the terminal, pressing any key to copy another set of text commands, then Alt+Tab back and paste over what you currently have. Do this for all 6 members of the first team.

If done correctly, this should cause the first 6 Pokemon in Box 1 to be the Pokemon you got from this program.

Step 5: Move Pokemon from Box 1 to Party
After that we have to move the Pokemon from Box 1 to the Party (I couldn't find a way for the commands to edit them into the party directly, but I bet there is a way). Go to the first Pokemon in Box 1, right click and select "View", then go to "Party-Battle Box", and then right click the first Pokemon in the Box and select "Set" to replace it with your viewed Pokemon. Do this for all 6 Pokemon on your team.

Step 6: Export the .sav File
To finish our changes to the GBC .sav, we need to go to "File" > "Export Sav" > "Export Main". Save the file with the same name as the save file you loaded. You should get a notice that the file already exists and that this will overwrite it; that's fine, hit OK.

Step 7: Repeat Steps 3-6 for the Second Team
Now repeat the process by opening the second GBC .sav file in PkHex and load in the next 6 Pokemon from team 2 into this second .sav file.

Step 8: Play Pokemon Stadium 2!
After all that, if you've set everything up right, you should be able to boot up Pokemon Stadium 2 in your emulator client, and the modified save files will be loaded in like GBC games in the N64's transfer pak.

Enjoy, and please report any bugs you encounter! :)



----- "Standard Ruleset" Restrictions -----

The standard ruleset that is currently enforced automatically by the program is as follows:

--- no banned Pokemon

	--- baby

	--- legendaries

	--- unevolved

--- (not yet implemented) can't have a pokemon present in both teams

--- (not yet implemented) you cannot rerandom a pokemon you had previously at any step in the team generation process

--- moveset restrictions

	--- a Pokemon's learnable moves includes those it can learn from leveling, a prior evolution, TM/HM, Tutors, and even Special Events
		--- Special Event moves may be flagged as "illegal" (pink text) in Pokemon Stadium 2, but are technically legal, though extremely rare IRL

	--- Pokemon's first move is of its first type (if possible)

	--- Pokemon's second move is of its second type (if possible)

	--- "inferior" moves are replaced with learnable "superior" moves
		--- i.e. if Charmander can learn Tackle and Strength, include Strength but not Tackle in its learnable move pool

	--- no banned moves
		--- most banned moves are banned because they are useless or nearly useless in combat (i.e. Teleport, Bind, Mud-Slap, Tackle, etc.)
		--- most moves that depend on the user/enemy BEING sleep are banned
			--- i.e. Dream Eater, Snore, Nightmare, Sleep Talk, etc.
			--- ideally these moves are eventually unbanned and instead the program simply only grants these moves when an appropriate associated move is also present
		--- most moves that depend on gender are banned
			--- gender currently isn't working correctly so these moves are banned as a workaround
		--- more controversial/opinionated bans
			--- Double Team and Minimize 
				--- evasion stacking needs a specific response, and with randomized moves, imo a Pokemon with high evasion may be practically unstoppable
				--- furthermore, Double Team is learnable by a large majority of Pokemon, making it frustratingly common for something that needs a niche response.
			--- Mud-Slap
				--- too many Ground Pokemon are randoming this as their required Ground move, and it makes them less threatening than if they had a more legit Ground move (i.e. Earthquake) 
				--- furthermore, its preponderance and secondary effect led to more stall tactics, making games longer and less exciting.
				--- this move can have legitimate use and eventually should be unbanned as it is less problematic than evasion buffs (since you can simply swap out if your accuracy is debuffed too much)... but given our current implementation, its coming up too much. 
			--- Rage
				--- imo just not good and gets randomed too much since basically every Pokemon can learn it
			--- False Swipe
				--- leaves opponent with 1 HP... not the best... meant for catching Pokemon, not fighting
			--- Return/Frustration
				--- currently Pokemon are set to 0 happiness, making Return do minimum damage (sometimes <1 damage!) and Frustration does max
					--- as a workaround... just do neither
				--- even if Frustration is viable and enabled, the move would appear really often since practically every Pokemon can learn it, and might be worse than Strength (??)

	--- (not yet implemented) a Pokemon must have at least one damaging move 
		--- it's unclear if moves whose sole effect is to inflict Poison/Burn status should be considered "damaging" but I'd say no because they:
			--- can't be used more than once on a target
			--- can't be used on a target that already has another status effect
			--- don't deal direct damage
			--- deal relatively low damage
				--- iirc, even Toxic's increasing damage is reset when its victim is swapped out and back in
			--- can be removed via Rest or Heal Bell			
			--- can be prevented with Safeguard
			--- can be blocked by Poison/Steel types
			--- can be removed with items or held items (if/when we use those)
			--- cannot be enhanced by the attacker's stats
		--- technically speaking, I think moves that just Poison/Burn are considered status inflictions, even if the status itself does damage.
		--- besides, technical considerations aside, if a Pokemon could only deal damage via Poison/Burn, it would not be much of a threat, and certainly not a Pokemon you'd want to have as your "last man standing". 



----- Future Plans -----

This project was originally envisioned to be a part of a "fantasy Pokemon league" akin to a fantasy football league. This could mean many possible and fun things, but one conception involves picking (or randomizing) a "pool" of Pokemon (which may change seasonally), then successively battling with teams (subsets of your pool) of Pokemon with other teams from friends in the league, gaining experience and changing your team along the way, until perhaps a "season end" is reached and performance stats are compared.

Another idea for the league involves an alternative selection process. Instead of selecting from the "pool" of Pokemon, you have to catch them in a "Safari" zone kind of thing. This could just be a text-based adventure, or maybe a simple/crude GUI could be made. The safari zone might differ from season to season in terms of its layout, theme, pokemon, mechanics, etc.

However, for right now, this project is just focused on creating interesting Level 100 teams for "one-off" Pokemon Stadium battles. Much of this functionality could extend to a "fantasy Pokemon" league though. Furthermore, extensive playtesting could inform us as to what factors lead to "interesting" or "competitive" battles, thus allowing us to develop a more balanced and enjoyable fantasy league later on. :)

In terms of generating Pokemon for one-off battles, this project would benefit from having more customization in HOW the Pokemon/moves are generated. 

New features typically should accomplish at least one of the following: 
--- streamline the generation process
--- remove/limit unfair/uninteresting gameplay factors
--- cause luck ("RNG") to be less polarizing
	--- we can't do much about crits or other in-game things...
	--- BUT we can do things like making sure one team doesn't get a strong advantage just by chance
--- balance/tune things like team compositions and movesets
	--- in other words make each team feel more well-rounded or purposeful
--- enhance the replay value of battles by making them more fun, interesting, varied, or competitive 
--- add creative and fun new matchups, team strategies, moveset strategies and ways to battle  

There are many factors which could be considered when balancing teams, movesets and so on. I've listed some below, but there are likely many more possible ideas. 

When balancing a factor, a meaningful question is often, "If teams/Pokemon differ in this factor, does that significantly impact performance/success? If so, how can this effect be mitigated?"

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
	--- note that a tier ranking might effectively function as a "meta" assessment of all the other metrics ... BUT this "human rated" element might inform us on what constitutes a "good" move/Pokemon/whatever
--- roles 
	--- more of a vague notion but could balance teams around like 1 tank 1 opener 1 support 1 sweeper(special) 1 sweeper(physical) 1baton pass or smt idk... keeping roles balanced or at least sticking to an interesting preset rather than getting RNG'd into "6 tanks"
--- legendaries
	--- obviously tips the scales



