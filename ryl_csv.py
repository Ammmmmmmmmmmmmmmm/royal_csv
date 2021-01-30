import csv
import royalmodule as ln
import os
import re
import heapq

#csv to lists of records in list
raw_list = ln.unpackcsv(ln.newest())

#dictionary of incorrect entries that should be replaced by value
fix_de = {"rank 1 motherfucker":"2300","19xx":"1900"}
fix_pr = {"master sergeant":"18", "Major":"31","1st Lietenant":"24","2nd lt":"22","Captain":"27"}
fix_names = {"brutalglory #5248":"brutalglory#5248","Hosky #8249":"Hosky#8249","ImSoloDoloMan":"ImSoloDoloMan#4177","It's ok":"MRT44#8992","I am already an Extra Thicc member baby":"Doppelsolna#6261", "Purple":"Purple#8192", "A_Singh":"A_Singh#1951", "young abraham ":"abe#2475", "Genesis":"Genesis#0955", "coxinga":"coxinga#3538","Already a member":"Keaton#3947","5242":"Shaun#5242","EstiPesti 6900":"EstiPesti#6900","yES":"Hiver#6844","im dan":"boisenberry#0810", "Kyo_3z":"Kyo_3z#9606", "ggbyers #7732":"ggbyers#7732", "FrankTh3Tank95":"FrankTh3Tank95#8053","Knarloc(#8062)":"Knarloc#8062", "lcomontenegro":"lcomontenegro#2631","JaiLeD":"JaiLeD#9326"}
fix_pr_lies = {"WickedCossack#1242":"99"}
fix_de_lies = {"WickedCossack#1242":"3000"}
fix_draft_response = {"Kyo_3z#9606":"My Dutch hero's name is \"NOOB BASHER THE SECOND\" so draft me pls"}


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
	smoosh = " "+raw_re+" "+raw_de+" "

	#if there is a number that would represent re or de put in a list
	pr_re_list = re.findall(r"[^0-9][0-9][0-9][^0-9]",smoosh)
	pr_de_list = re.findall(r"[0-9][0-9][0-9]+",smoosh)

	#find largest number that could represent de as de
	if pr_de_list != []:
			de  = (heapq.nlargest(1, pr_de_list, key=None))	
			if int(str(de).strip("[]'Rr()+/ -"))//1000 == 0:
				de = "0"+str(de).strip("[]'Rr()+/ -")
			else:
				de = de[0]
	#if no number given see if input matches dictionary fix and switch otherwise output null
	else:
		de = "0000"
		for key, value in fix_de.items():
			if key == raw_de:
				de = value

	#find largest number that could represent re as re
	if pr_re_list != []:
		re_ce = (heapq.nlargest(1, pr_re_list, key=None))
		re_ce = re_ce = str(re_ce).strip("[]'Rr()+/ -")

	#if no number given see if input matches dictionary fix and switch otherwise output null
	else:
		re_ce = "00"
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
for record in sort_by_re_clean:
	for raw_record in good_raw:
		if record[1] == raw_record[3]:
			raw_record.append(record[5])
			sort_by_re_raw.append(raw_record)
#sort by de rank by taking the honest list to replace 			
sort_by_de_clean = sorted(honest_list, key = lambda x: x[3])
for records in sort_by_de_clean:
	for raw_records in good_raw:
		if records[1] == raw_records[3]:
			raw_records.append(records[6])
			sort_by_de_raw.append(raw_records)

print(sort_by_re_raw[71])





#remove team captians from clean and raw list