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

# menu functionality (intro, set filename, display help, commands
def intro():
    """Introduce the user to program functionality, entry format."""
    print("Welcome to Timeclock, a simple terminal application.")
    print("You can add entries in hours, minutes, and seconds.")
    print("When you are finished with entry, type 'submit'.\n")
    print("To see available entry formats, type 'formats-help'.\n")
    print("To set filename for saving timesheet, type 'filename-set'.\n")
    print("For a full list of available commands, type 'commands'\n")


def set_filename():
    global output_file
    """Set the filename where finished timesheet results will be saved."""
    filename=input("Enter name for text output of new timesheet: \n"
    +f"[Leave empty to reuse the current filename {output_file}]")
    if filename == '':
        filename = output_file
        
    print(f"Entries will be written to {filename}.\n\n")
    output_file = filename


def formats_help():
    """
    Display information about available formats and current format
    settings for time entry.
    """
    with open('input_formats.txt') as file:
        print(file.read())
        

def commands_list():
    """
    Display a list of available commands to the user from the
    'commands.json' file.
    """
    for key, value in data[0].items():
        if(key == "Available Commands"):
            print(f"{key}\n")
            continue
        print(f"-> {key} | {value}\n")
        

def exit_program():
    """Terminate the program."""
    clear_screen()
    print("Exiting...")
    sleep(1)
    exit()

        
def menu_sequence():
    """Handle user input commands and control-flow of initial menu."""
    global entry_mode
    if(entry_mode == 0):
        ans = input("Hit enter to continue, or type a command.\n")
    else:
        ans = input("Hit enter to start a timesheet, or type a command.\n")
    while ans != '':
        if ans.lower() == 'filename-set':
            set_filename()
        elif ans.lower() == 'formats-help':
            formats_help()
        elif ans.lower() == 'commands':
            commands_list()
        elif ans.lower() == 'clear':
            clear_screen()
        elif ans.lower() == 'exit':
            exit_program()
        else: 
            print(f"Unrecognized command: {ans}\n")
        ans = input("\nHit enter to continue, or type a command.\n")
        

def log_time():
    hrs = int(input("Hours: "))
    mts = int(input("Minutes: "))
    sec = int(input("Sec: "))
    print(f"{hrs} hours, {mts} minutes, and {sec} seconds, correct?")
    ans = input("Enter (y/n), type 'submit' to finish entry: ")
    output = [hrs, mts, sec, ans] # store time, response to prompt
    return output


def add_to_total(entry: []):
    global total, time_sheet
    # add entered values to total
    total[0] += entry[0]
    total[1] += entry[1]
    total[2] += entry[2]
    time_sheet += (f"-> {entry[0]} hours, {entry[1]} minutes," 
    + f" {entry[2]} seconds\n")
    
    # clear screen, print out current timesheet for user
    clear_screen()
    print(time_sheet)


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


def submit_time(entry: []):
    """
    Format and submit current accumulated totals to the
    timesheet string before they are written to output.
    """
    global total, time_sheet
    print("Submitting...")
    sleep(1)
    
    add_to_total(entry)
    format_time()
    
    time_sheet += (f"|# Total: {total[0]} hours, {total[1]} minutes," 
    +f" {total[2]} seconds #|")
    
    clear_screen()
    
def entry_sequence():
    global time_sheet, runtime, total, output_file, entry_mode
    if entry_mode == 1:
        set_filename()
        entry_mode = 0
    while True:
        entry = log_time() #entry[0]=hrs, entry[1]=mts, entry[2]=sec
        ans = entry[3] # store user response to validation prompt
        if ans == 'y':
            add_to_total(entry)
        elif ans == 'submit':
            submit_time(entry)
            break
        else:
            print("Discarding entry...")
            sleep(1)
            clear_screen()


def reset_values():
    """Reset values necessary for running the program to initial state."""
    global total, timesheet
    index = 0
    for value in total:
        total[index] = 0
        index += 1
    timesheet = "Entries: \n"

            
def save_entries():
    global output_file, runtime, entry_mode
    if path.isfile(output_file):
        ans=input(f"Are you sure you want to overwrite the file {output_file}?\n")
        if ans.lower() == 'n' or ans.lower() == 'no':
            output_file = input("Choose an alternate filename for output: ")
        else:
            print(f"{output_file} will be overwritten.")
    # write recorded time to file using specified name
    with open(output_file, 'w') as file:
        file.write(time_sheet)
        print(f"Entries saved to '{output_file}'\n")
    
    ans = input("Fill out another timesheet? (y/n)\n")
    if ans.lower() != 'y':
        exit_program()
    else:
        entry_mode = 1
        reset_values()
        clear_screen()
        
        
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
    while True:
        menu_sequence()
        entry_sequence()
        save_entries()

if __name__ == '__main__':
    main()
    
