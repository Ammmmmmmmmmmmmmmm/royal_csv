#doesnt work in iteration 2

import os
import csv

players = []
teams = {}

captains = ["WickedCossack#1242", "aykin#6177","Kaister#5974","Kaiserklein#2520","don_artie#2656","theonlybaus#5720","sircallen#1517","wop#7118","david#6673","antz_is_here#6963","Zanerre#8833","Kyo_3z#9606","n0eL#6983","enki_#0336","Taddy#0618","Keaton#3947"]



#======================================================================

top_team_captians = 16
by_de = True

#========================================================================

if by_de:
	file_loc = "outputs/team_sheet_de.txt"
	file_used = "outputs/de_list_cleaned.csv"
else:
	file_loc = "outputs/team_sheet_re.txt"
	file_used = "outputs/re_list_cleaned.csv"

with open(file_used, "r") as f:
	csv_f = csv.reader(f)
	for row in csv_f:
		f1,f2,f3 = row
		players.append([f1,f2,f3])



players.reverse()



for player in range(0,len(captains)):
	name = str(player+1)
	teams[name] = [captains[player]]


#for player in range(0,len(players)):
#	if players[player][0] in captains:
#		dell_list.append(player)
#for x in dell_list:
#	for num,x in enumerate(players):

#broke ass shit

for x in captains:
	for num,y in enumerate(players):
		if y[0] == x:
			print(players[num])
			del players[num]
print(players)
	

#print(captains)
#print(players)


for a in range(2):
	x = top_team_captians
	for team in range(0,top_team_captians):
		teams.setdefault(str(x), [])
		teams[str(x)].append(players[0])
		del players[0]
		x = x-1


with open(file_loc, "w") as file:
	for key, value in teams.items():
		line = str(value)
		file.write(line)

with open(file_loc, "w") as file:
	for key, value in teams.items():
		line = str(value)+"\n"

		file.write(line)
