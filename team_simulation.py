#doesnt work in iteration 2

import os
import csv


players = []
teams = {}

#======================================================================

top_team_captians = 18
just_pr = False
by_de = False

#========================================================================

if by_de:
	file_loc = "outputs/team_sheet_de"
	file_used = "outputs/de_list_cleaned.csv"
else:
	file_loc = "outputs/team_sheet_re"
	file_used = "outputs/re_list_cleaned.csv"

with open(file_used, "r") as f:
	csv_f = csv.reader(f)
	for row in csv_f:
		f1,f2,f3 = row
		players.append([f1,f2,f3])

players.reverse()
#print(players)

for player in range(0,top_team_captians):
	name = str(player+1)
	teams[name] = [players[player]]
for player in range(top_team_captians):
	del players[0]

for a in range(2):
	x = top_team_captians
	for team in range(0,top_team_captians):
		teams.setdefault(str(x), [])
		teams[str(x)].append(players[0])
		del players[0]
		x = x-1

if just_pr:
	with open(file_loc, "w") as file:
		for key, value in teams.items():
			line = str(value)
			file.write(line)
else:
	with open(file_loc, "w") as file:
		for key, value in teams.items():
			line = str(value)+"\n"

			file.write(line)
