import sqlite3
import sys
import os
import string
import shutil
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import asksaveasfilename
from tkinter import *


def get_card_type(c, t):
	c.execute("SELECT type FROM datas WHERE id=?", t)
	card_type = str(c.fetchone())
	card_type = card_type.replace("'","")
	card_type = card_type.replace("(","")
	card_type = card_type.replace(')',"")
	card_type = card_type.replace('"',"")
	card_type = card_type.replace(',',"")
	card_type = int(card_type)
	return(card_type)

def get_card_level(c, t):
	c.execute("SELECT level FROM datas WHERE id=?", t)
	card_level = str(c.fetchone())
	card_level = card_level.replace("'","")
	card_level = card_level.replace("(","")
	card_level = card_level.replace(')',"")
	card_level = card_level.replace('"',"")
	card_level = card_level.replace(',',"")
	return(card_level)
	
def card_type_to_array(c, t, deck_counter):

	card_type = get_card_type(c, t)
	#is a monster
	if card_type & 1 == 1:
		if card_type & 64 == 64:#Fusion
			deck_counter[11] += 1
		elif card_type & 8192 == 8192:#Synchro
			deck_counter[12] += 1
		elif card_type & 8388608 == 8388608:#XYZ
			deck_counter[13] += 1
		else:#maindeck monster
			card_level = int(get_card_level(c, t))
			if card_level >= 7:
				deck_counter[0] += 1
			elif card_level >= 5:
				deck_counter[1] += 1
			else:
				deck_counter[2] += 1
	#is a spell
	elif card_type & 2 == 2:
		if card_type & 524288 == 524288:#Field
			deck_counter[7] += 1
		elif card_type & 65536 == 65536:#quick-play
			deck_counter[4] += 1
		elif card_type & 262144 == 262144:#Equip
			deck_counter[5] += 1
		elif card_type & 131072 == 131072:#Continuous
			deck_counter[6] += 1
		else:#normal
			deck_counter[3] += 1
	#is a trap
	else:
		if card_type & 1048576 == 1048576:#Counter
			deck_counter[10] += 1
		elif card_type & 131072 == 131072:#Continuous
			deck_counter[9] += 1
		else:#normal
			deck_counter[8] += 1
	return(deck_counter)
	
	#deck_counter indices
	#0 Monsters 7+
	#1 Monsters 5-6
	#2 Monsters 1-4
	#3 Normal Spells
	#4 Quick-Play Spells
	#5 Equip Spells
	#6 Continuous Spells
	#7 Field Spells
	#8 Normal Traps
	#9 Continuous Traps
	#10 Counter Traps
	#11 Fusion
	#12 Synchro
	#13 XYZ
	
	#Monster 0x1
	#Spell 0x2 --Normal Spells plainly use this, no need to use the "Normal" for monsters.
	#Trap 0x4 --Same goes for Normal traps
	#Normal 0x10
	#Effect 0x20 --Don't forget this because your card may be immune to Skill Drain but we have to be fair for everyone unless it's really a unique card.
	#Fusion 0x40
	#Ritual 0x80 --This is both for the Monster and the Spell
	#Spirit 0x200
	#Union 0x400
	#Gemini 0x800
	#Tuner 0x1000
	#Synchro 0x2000
	#Flip 0x200000
	#Toon 0x400000
	#Xyz 0x800000
	#Pendulum 0x1000000
	#Quick-Play 0x10000
	#Continuous 0x20000 --Same goes here, both Spell and Traps use this.
	#Equip 0x40000
	#Field 0x80000
	#Counter 0x100000

def save_deck_text(card_name_array, end_name, out_path, deck_counter, side_deck_counter):
	
	#removes .ydk extension from deck's file's name
	end_name = end_name.replace(".ydk","")
	#opens tk GUI...
	root = Tk()
	root.withdraw()
	#gets/creates filename as per (text file, opening window in output path specified in paths.txt file, default extension of .txt, with default name being the name of the deck file)
	file_name = asksaveasfilename(initialdir = out_path,  defaultextension = ".txt", initialfile = end_name)
	
	#totals for Main and Extra Decks
	total_monsters = deck_counter[0] + deck_counter[1] + deck_counter[2]
	total_spells = deck_counter[3] + deck_counter[4] + deck_counter[5] + deck_counter[6] + deck_counter[7]
	total_traps = deck_counter[8] + deck_counter[9] + deck_counter[10]
	total_extra = deck_counter[11] + deck_counter[12] + deck_counter[13]
	
	#totals for Side Deck
	side_total_monsters = side_deck_counter[0] + side_deck_counter[1] + side_deck_counter[2]
	side_total_spells = side_deck_counter[3] + side_deck_counter[4] + side_deck_counter[5] + side_deck_counter[6] + side_deck_counter[7]
	side_total_traps = side_deck_counter[8] + side_deck_counter[9] + side_deck_counter[10]
	side_total_extra = side_deck_counter[11] + side_deck_counter[12] + side_deck_counter[13]
	
	with open(file_name, 'w') as d:
		d.write(end_name + '\n' + '\n')
		d.write('Card Count:' + '\n')
		
		d.write(str(total_monsters+total_spells+total_traps) + ' Cards in Main Deck' + '\n'+ '\n')
		
		d.write(str(total_monsters) + ' Monster Cards total' + '\n')
		d.write('\t' + str(deck_counter[0]) + ' Level 7+' + '\n')
		d.write('\t' + str(deck_counter[1]) + ' Level 5-6' + '\n')
		d.write('\t' + str(deck_counter[2]) + ' Level 1-4' + '\n' + '\n')
		
		d.write(str(total_spells) + ' Spell Cards' + '\n')
		d.write('\t' + str(deck_counter[3]) + ' Normal Spell Cards' + '\n')
		d.write('\t' + str(deck_counter[4]) + ' Quick-Play Spell Cards' + '\n')
		d.write('\t' + str(deck_counter[5]) + ' Equip Spell Cards' + '\n')
		d.write('\t' + str(deck_counter[6]) + ' Continuous Spell Cards' + '\n')
		d.write('\t' + str(deck_counter[7]) + ' Field Spell Cards' + '\n' + '\n')
		
		d.write(str(total_traps) + ' Trap Cards' + '\n')
		d.write('\t' + str(deck_counter[8]) + ' Normal Trap Cards' + '\n')
		d.write('\t' + str(deck_counter[9]) + ' Continuous Trap Cards' + '\n')
		d.write('\t' + str(deck_counter[10]) + ' Counter Trap Cards' + '\n' + '\n')
		
		d.write(str(total_extra) + ' Fusion, Synchro, & XYZ Monsters' + '\n')
		d.write('\t' + str(deck_counter[11]) + ' Fusion Monsters' + '\n')
		d.write('\t' + str(deck_counter[12]) + ' Synchro Monsters' + '\n')
		d.write('\t' + str(deck_counter[13]) + ' XYZ Monsters' + '\n' + '\n')
		
		d.write(str(total_extra) + ' Cards in Side Deck' + '\n')
		d.write('\t' + str(side_total_monsters) + ' Main Deck Monsters' + '\n')
		d.write('\t' + str(side_total_spells) + ' Spell Cards' + '\n')
		d.write('\t' + str(side_total_traps) + ' Traps Card' + '\n')
		d.write('\t' + str(side_total_extra) + ' Fusion, Synchro, & XYZ Monsters' + '\n')
		
		current_card = ''
		
		for i in card_name_array:
			if i == '#created by ...':
				i = ''
			elif i == '#main':
				d.write("\n")
				d.write('Main Deck:')
				d.write("\n")
			elif i == '#extra':
				d.write("\n")
				d.write('Extra Deck:')
				d.write("\n")
			elif i == '!side':
				d.write("\n")
				d.write('Side Deck:')
				d.write("\n")
			elif current_card != i:
				multiplicity = card_name_array.count(i)
				current_card = i
				d.write(str(multiplicity) + ' x ' + i)
				d.write("\n")
		d.close()

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
	#[Monsters 7+, Monsters 5-6, Monsters 1-4, Normal Spells, Quick-Play Spells, Equip Spells, Continuous Spells, Field Spells, Normal Traps, Continuous Traps, Counter Traps, Fusion, Synchro, XYZ]
	deck_counter = [0,0,0, 0,0,0,0,0, 0,0,0, 0,0,0]
	#remembers if a particular card has been already read (some cards appear in more than 1 database)
	count_only_once = []
	#switches between main/extra and side deck
	in_side_deck = 0
	#cards in side deck
	side_deck_counter = [0,0,0, 0,0,0,0,0, 0,0,0, 0,0,0]
	
	
	#iterarates through every .cdb file in directory. Will fail if program is in different folder than the .cdb files.
	for file in [doc for doc in os.listdir(copied_cdb_path) if doc.endswith(".cdb")]:
		con = sqlite3.connect(file)
		with con:
			c = con.cursor()
			#iterate through all the lines.
			for i in range(len(deck_list_temp)):
				#remove newlines, ensures is string
				if data_number == 0:
					deck_list_temp[i] = str(deck_list_temp[i]).strip()
				
				#switches between deck and side deck
				if deck_list_temp[i] == '!side':
					in_side_deck = 1
				elif deck_list_temp[i] == '#main':
					in_side_deck = 0
				
				#put id number in a format to be parsed by sql
				t = (deck_list_temp[i],)
				
				#grabs every name that matches card id (should only be 1)
				c.execute("SELECT name FROM texts WHERE id=?", t)
				cardname = c.fetchone()
				
				#if the current .cdb does not have current card id...
				if cardname is None:
					#if this is the first .cdb, append the card id number as a placeholder
					if data_number == 0:
						temp_array.append(deck_list_temp[i])
						count_only_once.append(0)
				#if card id is found
				else:
					#remove the extra characters picked up from SQlite
					cardname = str(cardname)
					cardname = cardname.replace("',)","")
					cardname = cardname.replace("('","")
					cardname = cardname.replace('",)',"")
					cardname = cardname.replace('("',"")
					cardname = cardname.strip()
					#if this is the first .cdb, append card name
					if data_number == 0:
						temp_array.append(cardname)
						if in_side_deck == 0:
							deck_counter = card_type_to_array(c, t, deck_counter)
						else:
							side_deck_counter = card_type_to_array(c, t, side_deck_counter)
						count_only_once.append(1)
					#otherwise overwrite card id with card name in the array
					else:
						temp_array[i] = cardname
						if count_only_once[i] == 0:
							if in_side_deck == 0:
								deck_counter = card_type_to_array(c, t, deck_counter)
							else:
								side_deck_counter = card_type_to_array(c, t, side_deck_counter)
							count_only_once[i] = 1
					
		data_number += 1
						
	#opens save file dialogue with name of deck as default
	save_deck_text(temp_array, os.path.basename(deck_name), output_path, deck_counter, side_deck_counter)

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