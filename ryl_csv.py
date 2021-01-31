#version 1.1
import csv
import royalmodule as ln
import os
import re
import heapq

#csv to lists of records in list
raw_list = ln.unpackcsv(ln.newest())

#dictionary of incorrect entries that should be replaced by value
fix_de = {"rank 1 motherfucker":2300,"19xx":1900}
fix_pr = {"master sergeant":18, "Major":31,"1st Lietenant":24,"2nd lt":22,"Captain":27}
fix_names = {"brutalglory #5248":"brutalglory#5248","Hosky #8249":"Hosky#8249","ImSoloDoloMan":"ImSoloDoloMan#4177","It's ok":"MRT44#8992","I am already an Extra Thicc member baby":"Doppelsolna#6261", "Purple":"Purple#8192", "A_Singh":"A_Singh#1951", "young abraham ":"abe#2475", "Genesis":"Genesis#0955", "coxinga":"coxinga#3538","Already a member":"Keaton#3947","5242":"Shaun#5242","EstiPesti 6900":"EstiPesti#6900","yES":"Hiver#6844","im dan":"boisenberry#0810", "Kyo_3z":"Kyo_3z#9606", "ggbyers #7732":"ggbyers#7732", "FrankTh3Tank95":"FrankTh3Tank95#8053","Knarloc(#8062)":"Knarloc#8062", "lcomontenegro":"lcomontenegro#2631","JaiLeD":"JaiLeD#9326"}
fix_pr_lies = {"WickedCossack#1242":33}
fix_de_lies = {"WickedCossack#1242":2300}
fix_draft_response = {"Kyo_3z#9606":"My Dutch hero's name is \"NOOB BASHER THE SECOND\" so draft me pls", " challenger_marco#8536":"Hi,I myself have a wide civ pool and play any style you want ,if you grab me i'd be giving the mascot as i have challenger in my name ,i don't give up games easily & will try my best to win in any case whether it's rigged or going against the odds doesn't matter ,the challenge will still be there!"}
team_captians = []

'''create clean list with proper inputs'''
clean_list = []
skip = True
for player_list in raw_list:
	#skip the names of the fields
	if skip:
		skip = False
		continue
	#every field in csv 
	raw_date,raw_akn1,raw_steam,raw_discord,raw_timezone,raw_akn2,raw_re,raw_de,raw_akn3,raw_civ,raw_statement = player_list

	#---fix discord names that are wrong---
	is_discord_correct = None
	is_discord_correct = re.search(r"[a-zA-Z0-9_]+#[0-9][0-9][0-9][0-9]$", raw_discord)
	
	if is_discord_correct is not None:
			discord = raw_discord
	elif raw_discord in fix_names:
		discord = fix_names[raw_discord]
	else:
		discord = "Needs to be fixed:"+raw_discord

	#---fix and clean pr so only the number is shown---

	pr_re_list = []
	pr_de_list = []

	#add spaces to end so regex can pick up only 2 consecutive digits for re and 3+ for de
	smoosh_re = " "+raw_re+" "
	smoosh_de = " "+raw_de+" "
	#if there is a number that would represent re or de put in a list
	pr_re_list = re.findall(r"[^0-9][0-9][0-9][^0-9]",smoosh_re)
	pr_de_list = re.findall(r"[0-9][0-9][0-9]+",smoosh_de)

	for x in range(0,len(pr_de_list)):
		pr_de_list[x] = int(str(pr_de_list[x]).strip("[]'Rr()+/ -"))
	for x in range(0,len(pr_re_list)):
		pr_re_list[x] = int(str(pr_re_list[x]).strip("[]'Rr()+/ -"))

	#find largest number that could represent de as de
	if pr_de_list != []:
			de  = (heapq.nlargest(1, pr_de_list, key=None))	
			if int(str(de).strip("[]'Rr()+/ -"))//1000 == 0:
				de = int("0"+str(de).strip("[]'Rr()+/ -"))
			else:
				de = de[0]
			for key, value in fix_de.items():
				if key == raw_de:
					de = value
	#if no number given see if input matches dictionary fix and switch otherwise output null
	else:
		de = 0000
		for key, value in fix_de.items():
			if key == raw_de:
				de = value

	#find largest number that could represent re as re
	if pr_re_list != []:
		re_ce = (heapq.nlargest(1, pr_re_list, key=None))
		re_ce = int(str(re_ce).strip("[]'Rr()+/ -"))
		for key, value in fix_pr.items():
			if key == raw_re:
				re_ce = value
	#if no number given see if input matches dictionary fix and switch otherwise output null
	else:
		re_ce = 00
		for key, value in fix_pr.items():
			if key == raw_re:
				re_ce = value

	#create a clean list of records from csv 
	clean_list.append([raw_discord,discord,re_ce,de,raw_statement])

#print(clean_list)

'''fix lies don finds'''

honest_list = clean_list
#add another field
for record in range(0,len(honest_list)):
	honest_list[record].append('')
	honest_list[record].append('')

#goes through names and if name is key in lies dictionary we change the input
for num in range(0,len(honest_list)):
	if honest_list[num][1] in fix_pr_lies:
		honest_list[num][2] = fix_pr_lies[honest_list[num][1]]
		honest_list[num][5] = "RoyaL predicts incorrect complete edition rank. "
#de rank fixer of liars
for num in range(0,len(honest_list)):
	if honest_list[num][1] in fix_de_lies:
		honest_list[num][3] = fix_de_lies[honest_list[num][1]]
		honest_list[num][6] = "RoyaL predicts incorrect definitive edition rank." 
#add draft responses
for num in range(0,len(honest_list)):
	if honest_list[num][1] in fix_draft_response and honest_list[num][4] == '':
		honest_list[num][4] = fix_draft_response[honest_list[num][1]]

#print(honest_list)

'''sort raw list by clean list'''

#sort the ranks with two lists prioritizing de and one prioritizing re and versions of both with raw ranks instead of cleaned
sort_by_de_clean = []
sort_by_re_clean = []
sort_by_de_raw = []
sort_by_re_raw = []
good_raw = raw_list
del good_raw[0]

#add draft response to raw list and swap improper discord names
for num,record in enumerate(good_raw):
	new_statement = ''
	for new_record in honest_list:	
		if record[3] == new_record[0] and new_record[4] != '' and record[10] == '':
			good_raw[num][10] = new_record[4]
			break
	for num,rlist in enumerate(honest_list):
		if record[3] == rlist[0]:
			good_raw[num][3] = rlist[1]


#sort by re rank by taking the honest list to replace 
sort_by_re_clean = sorted(honest_list, key = lambda x: x[2])
sort_by_re_de_insert = []
#create the two lists
for record in range(0,len(sort_by_re_clean)):
	if int(sort_by_re_clean[record][2]) == 0:
		sort_by_re_de_insert.append(sort_by_re_clean[record])
for record in sort_by_re_de_insert:
	for records in sort_by_re_clean: 
		if record == records:
			del sort_by_re_clean[sort_by_re_clean.index(records)]
sort_by_re_de_insert = sorted(sort_by_re_de_insert, key = lambda x: x[3])
#insert de onlys into re list
for record in range(0,len(sort_by_re_de_insert)):
	for recordx in range(0,len(sort_by_re_clean)):
		if sort_by_re_clean[recordx][3] >= sort_by_re_de_insert[record][3] and sort_by_re_clean[recordx][3] != 0:
			sort_by_re_clean.insert(recordx,sort_by_re_de_insert[record])
			break

		if record+1 == len(sort_by_re_de_insert) and recordx+1 == len(sort_by_re_clean):
			#will fix later?
			print("ran")
			for x in sort_by_re_se_insert:
				if x not in sort_by_re_clean:
					sort_by_re_clean.append(x)


#create raw list
for record in sort_by_re_clean:
	for raw_record in good_raw:
		if record[1] == raw_record[3]:
			sort_by_re_raw.append(raw_record+[record[5]])


#sort by de rank by taking the honest list to replace 			
sort_by_de_clean = sorted(honest_list, key = lambda x: x[3])
sort_by_de_re_insert = []
#split lists
for record in range(0,len(sort_by_de_clean)):
	if int(sort_by_de_clean[record][3]) == 0:
		sort_by_de_re_insert.append(sort_by_de_clean[record])
for record in sort_by_de_re_insert:
	for records in sort_by_de_clean: 
		if record == records:
			del sort_by_de_clean[sort_by_de_clean.index(records)]
sort_by_de_re_insert = sorted(sort_by_de_re_insert, key = lambda x: x[2])

#insert re onlys into de list
for record in range(0,len(sort_by_de_re_insert)):
	for recordx in range(0,len(sort_by_de_clean)):
		#print("{} >= {}".format(sort_by_de_clean[recordx][2],sort_by_de_re_insert[record][2]))
		if sort_by_de_clean[recordx][2] >= sort_by_de_re_insert[record][2] and sort_by_de_clean[recordx][2] != 0:
			#print("true")
			sort_by_de_clean.insert(recordx,sort_by_de_re_insert[record])
			break

		if record+1 == len(sort_by_de_re_insert) and recordx+1 == len(sort_by_de_clean):
			#print("ran")
			for x in sort_by_de_re_insert:
				if x not in sort_by_de_clean:
					sort_by_de_clean.append(x)



for records in sort_by_de_clean:
	for raw_records in good_raw:
		if records[1] == raw_records[3]:
			sort_by_de_raw.append(raw_records+[records[6]])

#print(sort_by_re_raw)
#print(sort_by_de_raw)

#smoosh lists


'''EXPORT THEM ALL'''
#export for tad,vivid,don to look at
for record in range(0,len(sort_by_de_raw)):
	if sort_by_de_raw[record][3] in team_captians:
		del sort_by_de_raw[record]
	raw_date,raw_akn1,raw_steam,raw_discord,raw_timezone,raw_akn2,raw_re,raw_de,raw_akn3,raw_civ,raw_statement,raw_RoyaL = sort_by_de_raw[record]
	raw_steam = "=HYPERLINK(\""+raw_steam +"\")"
	sort_by_de_raw[record] = [raw_discord.replace(',', ' '),raw_re.replace(',', ' '),raw_de.replace(',', ' '),raw_steam.replace(',', ' ')]

for record in range(0,len(sort_by_re_raw)):
	if sort_by_re_raw[record][3] in team_captians:
		del sort_by_re_raw[record] 
	raw_date,raw_akn1,raw_steam,raw_discord,raw_timezone,raw_akn2,raw_re,raw_de,raw_akn3,raw_civ,raw_statement,raw_RoyaL = sort_by_re_raw[record]
	raw_steam = "=HYPERLINK(\""+raw_steam +"\")"
	sort_by_re_raw[record] = [raw_discord.replace(',', ' '),raw_re.replace(',', ' '),raw_de.replace(',', ' '),raw_steam.replace(',', ' ')]

sort_by_re_raw.reverse()
sort_by_de_raw.reverse()

ln.packcsv("de_list.csv",(sort_by_de_raw))
ln.packcsv("re_list.csv",(sort_by_re_raw))

#export for team simulation

re_output = []

for record in sort_by_re_clean:
	rawname,name,pr,elo,statement,liece,liede = record
	re_output.append([name,pr,elo])
print(re_output)
ln.packcsv("re_list_cleaned.csv",(re_output))	


de_output =[]

for record in sort_by_de_clean:
	rawname,name,pr,elo,statement,liece,liede = record
	de_output.append([name,pr,elo])

ln.packcsv("de_list_cleaned.csv",(de_output))