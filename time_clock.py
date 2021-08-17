from os import system, name, path
from time import sleep
from sys import exit
import json

runtime = True # init value to True to start program loop
command_phrases=['submit', 'formats-help'] # phrases which can be used during program execution
output_file = 'timesheet.txt' # default file where entries will be stored as output
time_sheet = "Entries: \n" # base template for time-sheet file
total = [0,0,0] # total sum of all entries, stored in order of hours, minutes, seconds
entry_mode = 0 # handles different operational modes for the entry prompt, 0 = don't prompt for filename,
# 1 = prompt for filename

def load_dataset(data_path: str) :
    """
    Load the json object at specified path into data.
    """
    json_file = open(data_path)
    return json.load(json_file)

data = [load_dataset('commands.json')] #hold different json files for access during runtime


def intro():
	"""Introduce the user to program functionality, entry format."""
	global runtime, command_phrases, output_file
	print("Welcome to Timeclock, a simple terminal application.")
	print("You can add entries in hours, minutes, and seconds.")
	print("When you are finished with entry, type 'submit'.\n")
	print("To see available entry formats, type 'formats-help'.\n")
	print("To set filename for saving timesheet, type 'filename-set'.\n")
	print("For a full list of available commands, type 'commands'\n")
	ans = input("Hit enter to continue, or type a command.\n")
	while ans != '':
		if ans.lower() == 'filename-set':
			filename=input("Enter name for txt output of timesheet: ")
			print(f"Entries will be written to {filename}.\n\n")
			output_file = filename
		elif ans.lower() == 'formats-help':
			with open('input_formats.txt') as file:
				print(file.read())
		elif ans.lower() == 'commands':
				for key, value in data[0].items():
					if(key == "Available Commands"):
						print(f"{key}\n")
						continue
					print(f"-> {key} | {value}\n")
		elif ans.lower() == 'clear':
			clear_screen()
		elif ans.lower() == 'exit':
			clear_screen()
			exit("Exiting...")
		else: 
			print(f"Unrecognized command: {ans}\n")
		ans = input("\nHit enter to continue, or type a command.\n")
	runtime = True # set value to true to execute main loop
	
def entry_prompt():
	global time_sheet, runtime, total, output_file, entry_mode
	if entry_mode == 1:
		filename = input("Enter filename for new timesheet:\n"
		+ "[leave blank to use the same filename again]\n")
		if filename == "":
			filename = output_file
		print(f"Entries will be written to {filename}.\n\n")
		output_file = filename
		entry_mode = 0
	while True:
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
			format_time()
			time_sheet += f"-> {hrs} hours, {mts} minutes, {sec} seconds\n"
			time_sheet += f"|# Total: {total[0]} hours, {total[1]} minutes, {total[2]} seconds #|"
			sleep(1)
			clear_screen()
			break

def format_time():
	"""
	Format the current total values, converting values
	greater than or equal to 60 to their equivalent larger
	time denominations (ie: 120 seconds becomes 2 minutes,
	180 minutes becomes three hours and so on).
	"""
	index = 0
	for item in total:
		if item / 60 >= 1 and index != 0:
			item_remainder = item % 60
			quotient = int(item / 60)
			total[index - 1] += quotient
			total[index] = item_remainder
		index += 1

			
def save_entries():
	global time_sheet, output_file, runtime, entry_mode
	if path.isfile(output_file):
	    ans=input(f"Are you sure you want to overwrite the file {output_file}?\n")
	    if ans.lower() == 'n' or ans.lower() == 'no':
	        output_file = input("Choose an alternate filename for output: ")
	    else:
	        print(f"{output_file} will be overwritten.")
	        
	with open(output_file, 'w') as file:
	    file.write(time_sheet)
	
	print(f"Entries saved to '{output_file}'\n")
	ans = input("Fillout another timesheet? (y/n)\n")
	if ans.lower() != 'y':
		runtime = False
		print("Exiting...")
	else:
		entry_mode = 1


def clear_screen():
	"""Clear the terminal/console of any generated text."""
	# make use of 'cls' command to clear screen in Windows
	if name == 'nt':
		system('cls')
	# use 'clear' for all other operating systems (linux, macosx etc)
	else:
		system('clear')

def main():
	intro()
	while runtime:
		entry_prompt()
		print(time_sheet)
		save_entries()	

if __name__ == '__main__':	
	main()
