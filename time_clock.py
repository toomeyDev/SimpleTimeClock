from os import system, name, path
from time import sleep
from sys import exit

runtime = False # init value to False until ready for execution
command_phrases=['submit', 'formats-help'] # phrases which can be used during program execution
output_file = 'timesheet.txt' # default file where entries will be stored as output
time_sheet = "Entries: \n" # base template for time-sheet file
total = [0,0,0] # total sum of all entries, stored in order of hours, minutes, seconds

def intro():
	"""Introduce the user to program functionality, entry format."""
	global runtime, command_phrases, output_file
	print("Welcome to Timeclock, a simple terminal application.")
	print("You can add entries in hours, minutes, and seconds.")
	print("When you are finished with entry, type 'submit'.\n")
	print("To see available entry formats, type 'formats-help'.\n")
	print("To set filename for saving timesheet, type 'filename-set'.")
	ans = input("Hit enter to continue, or type a command.\n")
	if ans.lower() == 'filename-set':
	    filename=input("Enter name for txt output of timesheet: ")
	    print(f"Entries will be written to {filename}.\n\n")
	    output_file = filename
	elif ans.lower() == 'formats-help':
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
		format_time()
		time_sheet += f"-> {hrs} hours, {mts} minutes, {sec} seconds\n"
		time_sheet += f"|# Total: {total[0]} hours, {total[1]} minutes, {total[2]} seconds #|"
		sleep(1)
		runtime = False
		clear_screen()

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
    global time_sheet, output_file
    if path.isfile(output_file):
	    ans=input(f"Are you sure you want to overwrite the file {output_file}?")
	    if ans.lower() == 'n' or ans.lower() == 'no':
	        output_file = input("Choose an alternate filename for output: ")
	    else:
	        print(f"{output_file} will be overwritten.")
	        
    with open(output_file, 'w') as file:
	    file.write(time_sheet)
	
    print(f"Entries saved to '{output_file}'")


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
