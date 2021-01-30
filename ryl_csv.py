#thanks to Tallitus#4827 

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
		de = ["null"]
		for key, value in fix_de.items():
			if key == raw_de:
				de = value

	#find largest number that could represent re as re
	if pr_re_list != []:
		re_ce = (heapq.nlargest(1, pr_re_list, key=None))
		re_ce = re_ce = str(re_ce).strip("[]'Rr()+/ -")

	#if no number given see if input matches dictionary fix and switch otherwise output null
	else:
		re_ce = "na"
		for key, value in fix_pr.items():
			if key == raw_re:
				re_ce = value

	#create a clean list of records from csv 
	clean_list.append([raw_discord,discord,re_ce,de])


print(clean_list)

ln.packcsv("Tallitus",clean_list)

