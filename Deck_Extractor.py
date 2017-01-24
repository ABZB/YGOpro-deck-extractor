import sqlite3
import sys
import os
import string
import shutil

def extract(deck_name):

	#path for pulling .cdb files
	pathways = []
	with open("paths.txt") as f:
		pathways = f.readlines()
		f.close()
		
	cdb_path = pathways[1]
	cdb_path = cdb_path.strip()
	output_path = pathways[3]
	
	deck_path = cdb_path + "deck/" #pathway to deck folder
	output_path = output_path.strip()

	deck_name = deck_path + deck_name + '.ydk'
        
	#array to store found card names while iterating through databases
	temp_array = []
	
	#check in order to create array in first run, then overwrite as needed in subsequent iterations.
	data_number = 0
	
	#open .ydk file
	with open(deck_name) as f:
		#read card ids from .ydk file
		deck_list_temp = f.readlines()
		f.close()
		
		
	copied_cdb_path = os.getcwd() + "/"
	
	
	#iterarates through every .cdb file in directory. Will fail if program is in different folder than the .cdb files.
	for file in [doc for doc in os.listdir(copied_cdb_path) if doc.endswith(".cdb")]:
		con = sqlite3.connect(file)
		with con:
			c = con.cursor()
			#iterate through all the lines.
			for i in range(len(deck_list_temp)):
				#put id number in a format to be parsed by sql
				t = (str(deck_list_temp[i]),)
				#grabs every name that matches card id (should only be 1)
				c.execute("SELECT name FROM texts WHERE id=?", t)
				cardname = c.fetchone()
				#if the current .cdb does not have current card id...
				if cardname is None:
					#if this is the first .cdb, append the card id number as a placeholder
					if data_number == 0:
						temp_array.append(str(deck_list_temp[i]))
				#if card id is found
				else:
					cardname = str(cardname)
					cardname = cardname.replace("',)","")
					cardname = cardname.replace("('","")
					cardname = cardname.replace('",)',"")
					cardname = cardname.replace('("',"")
					cardname = cardname.replace('!side',"Side Deck: ")
					cardname = cardname.replace('#extra',"Extra Deck: ")
					cardname = cardname.replace('#main',"Main Deck: ")
					#if this is the first .cdb, append card name
					if data_number == 0:
						temp_array.append(cardname)
					#otherwise overwrite card id with card name in the array
					else:
						temp_array[i] = cardname
		data_number += 1
						
	
	
	#request name for output file
	end_name = input('Enter name for output file: ')
	end_name += '.txt'
	end_name = output_path + end_name
	with open(end_name, 'w') as d:
		for i in temp_array:
			if i == "Main Deck: " or i == "Extra Deck: " or i == "Side Deck: ":
				d.write("\n")
				
			d.write(i)
			d.write("\n")

def	update_cdbs():
	#grab paths from text file
	pathways = []
	with open("paths.txt") as f:
		pathways = f.readlines()
		f.close()
	cdb_path = pathways[1]
	main_folder_path = pathways[1]

	#remove newline character
	main_folder_path = main_folder_path.strip()
	cdb_path = cdb_path.strip() + "expansions/" #pathway to .cdb folder

	#If they add new subfolders, update this list
	directories_list = ['',"live//","live2016//","live2017//","liveanime//"]

	#append various subfolders
	for iter in range(len(directories_list)):
		directories_list[iter] = cdb_path + directories_list[iter]

	#get current directory
	current_directory = os.getcwd() + '//'

	#avoids overwriting of same filename in different subfolders
	filenumber = 0

	#copy over .cdb databases
	for paths in directories_list:
		for file in [doc for doc in os.listdir(paths) if doc.endswith(".cdb")]:
			shutil.copy2(paths + os.path.basename(file), current_directory + str(filenumber) + os.path.basename(file))
			filenumber += 1 
	shutil.copy2(main_folder_path + 'cards.cdb', current_directory + 'cards.cdb')

			

deck_name = input('Input Deck Name: ')
update_cdbs()
extract(deck_name)
