from os import system, name
from time import sleep
from sys import exit

runtime = False # init value to False until ready for execution
command_phrases=['submit', 'formats-help'] # phrases which can be used during program execution
time_sheet = "Entries: \n" # base template for time-sheet file
total = [0,0,0] # total sum of all entries, stored in order of hours, minutes, seconds

def intro():
	"""Introduce the user to program functionality, entry format."""
	global runtime, command_phrases
	print("Welcome to Timeclock, a simple terminal application.")
	print("You can add entries in hours, minutes, and seconds.")
	print("When you are finished with entry, type 'submit'\n"
	+"to save entries to a text file.\n")
	print("To see available entry formats, type 'formats-help'\n")
	ans = input("Hit enter to continue, or type a command.\n")
	if ans.lower() == 'formats-help':
		with open('input_formats.txt') as file:
			print(file.read())
	elif ans.lower() == 'exit':
		clear_screen()
		exit("Exiting...")
	runtime = True # set value to true to execute main loop
	
def entry_prompt():
	global time_sheet, runtime, total
	hrs = input("Hours: ")
	mts = input("Minutes: ")
	sec = input("Sec: ")
	print(f"{hrs} hours, {mts} minutes, and {sec} seconds, is this correct?")
	ans = input("Enter (y/n), type 'submit' to finish entry: ")
	
	# prompt for confirmation
	if ans.lower() == 'y':
		# add entered values to total
		total[0] += int(hrs)
		total[1] += int(mts)
		total[2] += int(sec)
		
		time_sheet += f"-> {hrs} hours, {mts} minutes, {sec} seconds\n"
		clear_screen()
	elif ans.lower() == 'submit':
		print("Submitting...")
		# add entered values to total
		total[0] += int(hrs)
		total[1] += int(mts)
		total[2] += int(sec)
		time_sheet += f"-> {hrs} hours, {mts} minutes, {sec} seconds\n"
		time_sheet += f"|# Total: {total[0]} hours, {total[1]} minutes, {total[2]} seconds #|"
		sleep(1)
		runtime = False
		clear_screen()
		
def save_entries():
	global time_sheet
	with open('time_sheet.txt', 'w') as file:
		file.write(time_sheet)
	print("Entries saved to 'time_sheet.txt'")

def clear_screen():
	"""Clear the terminal/console of any generated text."""
	# make use of 'cls' command to clear screen in Windows
	if name == 'nt':
		system('cls')
	# use 'clear' for all other operating systems (linux, macosx etc)
	else:
		system('clear')
	
intro()
while runtime:
	entry_prompt()
	print(time_sheet)
save_entries()
