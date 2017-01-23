import os
import shutil
import string

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
