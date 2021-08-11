runtime = False # init value to False until ready for execution
command_phrases=['submit']
time_sheet = "Entries: \n"

def intro():
	global runtime
	print("Welcome to Timeclock, a simple terminal application.")
	print("You can add entries in hours, minutes, and seconds.")
	print("When you are finished with entry, type 'submit'\n"
	+"to save entries to a text file.\n")
	print("Enter in format [hrs,min,sec]:")
	
	runtime = True # set value to true to execute main loop

def entry_prompt():
	global time_sheet, runtime
	hrs = input("Hours: ")
	mts = input("Minutes: ")
	sec = input("Sec: ")
	print(f"{hrs} hours, {mts} minutes, and {sec} seconds, is this correct?")
	ans = input("Enter (y/n): ")
	
	# prompt for confirmation
	if ans.lower() == 'y':
		time_sheet += f"-> {hrs} hours, {mts} minutes, {sec} seconds\n"
	elif ans.lower() == 'submit':
		time_sheet += f"-> {hrs} hours, {mts} minutes, {sec} seconds\n"
		print("Submitting...")
		runtime = False
		
def save_entries():
	global time_sheet
	with open('time_sheet.txt', 'w') as file:
		file.write(time_sheet)
	print("Entries saved to 'time_sheet.txt'")
intro()
while runtime:
	entry_prompt()
	print(time_sheet)
save_entries()
