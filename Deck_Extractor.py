import sqlite3
import sys
import os
import string
import shutil
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import asksaveasfilename
from tkinter import *

def save_deck_text(card_name_array, end_name, out_path):
	
	#removes .ydk extension from deck's file's name
	end_name = end_name.replace(".ydk","")
	#opens tk GUI...
	root = Tk()
	root.withdraw()
	#gets/creates filename as per (text file, opening window in output path specified in paths.txt file, default extension of .txt, with default name being the name of the deck file)
	end_name = asksaveasfilename(initialdir = out_path,  defaultextension = ".txt", initialfile = end_name)
	
	with open(end_name, 'w') as d:
		for i in card_name_array:
			if i == "Main Deck: " or i == "Extra Deck: " or i == "Side Deck: ":
				d.write("\n")
			d.write(i)
			d.write("\n")

def extract():

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
	
	#invoke tkinter GUI
	root = Tk()
	#hides tkinter background window
	root.withdraw()
	#opens open file dialogue, default directory is the /deck folder from your specified YgoPro directory
	deck_name = askopenfilename(filetypes = (("YgoPro Deck Files", "*.ydk"), ("All Files", "*.*")), initialdir = deck_path)
	
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
						#First three lines catch  the section headers and replace them with nicer headers.
						if str(deck_list_temp[i]) == '#main':
							temp_array.append(cardname.replace('#main','Main Deck: '))
						elif str(deck_list_temp[i]) == '#extra':
							temp_array.append(cardname.replace('#extra',"Extra Deck: "))
						elif str(deck_list_temp[i]) == '!side':
							temp_array.append(cardname.replace('!side',"Side Deck: "))
						#Otherwise, just append the card code for now
						else:
							temp_array.append(str(deck_list_temp[i]))
					
				#if card id is found
				else:
					#remove the extra characters picked up from SQlite
					cardname = str(cardname)
					cardname = cardname.replace("',)","")
					cardname = cardname.replace("('","")
					cardname = cardname.replace('",)',"")
					cardname = cardname.replace('("',"")
					#if this is the first .cdb, append card name
					if data_number == 0:
						temp_array.append(cardname)
					#otherwise overwrite card id with card name in the array
					else:
						temp_array[i] = cardname
		data_number += 1
						
	#opens save file dialogue with name of deck as default
	save_deck_text(temp_array, os.path.basename(deck_name), output_path)

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

update_cdbs()
extract()
