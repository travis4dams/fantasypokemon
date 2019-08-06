move_list = []
fp = open("Serebii.net Pokédex - #001 - Bulbasaur.html",'r')
line = fp.readline()
while line!="":
	#line = line.strip()
	if("https://www.serebii.net/attackdex" in line and "</a>" in line):
		a_index = line.index("</a>")
		i = a_index
		while(i >= 0):
			if(line[i] == ">"):
				break
			i -= 1
		if(i >= 0):
			move_line = line[i+1:a_index]
			if(move_line!="" and "Gen" not in move_line):
				move_list.append(move_line)
	line = fp.readline()
print(move_list)
print(len(move_list))