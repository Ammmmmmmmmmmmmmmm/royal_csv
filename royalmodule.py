#for finding the right file
import os
import time

#for newest csv queue
import heapq

#for unpack and fieldv 
import csv


def newest():
	"""Finds newest file added"""
	file_list = os.listdir("inputs")
	latest = os.path.join("inputs",file_list[0])
	for file in file_list:
		if (time.ctime(os.path.getmtime(os.path.join("inputs",file)))) > time.ctime(os.path.getmtime(latest)):
			latest = os.path.join("inputs",file)
	print(latest)
	return latest

def unpackcsv(file):
	"""Unpacks csv into tuples"""
	with open(file, "r") as file:
		csv_file = csv.reader(file, delimiter=',')
		csv_list = list(csv_file)
		return csv_list

def packcsv(file,list_csv):
	"""Makes a csv out of the file,list"""
	#file_location = os.path.join("~","royal_csv","csv_outputs")
	#os.chdir(file_location)
	with open(file, "w") as file:
		for record in list_csv:
			fin_record = ""
			field = ""
			cm = ''
			for num,f in enumerate(record):
				if num > 0:
					cm = ","
				fin_record = fin_record + cm+str(f).strip(" ")
			file.write(str(fin_record).strip("[]")+"\n")