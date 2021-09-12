from os import system, name, makedirs
import os
from time import sleep
from sys import exit, path
import json

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


def format_json(json_file) :
    """Format a json file for easy legibility."""
    output = ""
    for key, value in json_file.items():
        if(key == "Available Commands" or key == "Preferences"):
            output += (f"\n{key}:\n")
            continue
        output +=(f"-> {key} | {value}\n")
    return output    


data = [load_dataset('commands.json')] #hold different json files for access during runtime
data.append(load_dataset('preferences.json'))
# menu functionality (intro, set filename, display help, commands


def intro():
    """Introduce the user to program functionality, entry format."""
    print("Welcome to Timeclock, a simple terminal application.")
    print("You can add entries in hours, minutes, and seconds.")
    print("When you are finished with entry, type 'submit'.\n")
    print("To see available entry formats, type 'formats-help'.\n")
    print("To set filename for saving timesheet, type 'filename-set'.\n")
    print("For a full list of available commands, type 'commands'\n")
    print("To see this message again at any time, type 'intro'\n")


def set_filename():
    global output_file
    """Set the filename where finished timesheet results will be saved."""
    filename=input("Enter name for text output of new timesheet: \n"
    +f"[Leave empty to reuse the current filename {output_file}]")
    if filename == '':
        filename = output_file
    
    filename = txt_append(filename) # if auto_txt is true, append '.txt'
    print(f"Entries will be written to {filename}.\n\n")
    output_file = filename


def txt_append(input_string: str):
    """
    Append '.txt' to the end of the provided string
    if 'auto_txt' == True
    """
    if data[1]["auto_txt"] == "True":    
        if input_string.find('.txt') == -1:
            input_string += '.txt'
            return input_string
    return input_string


def reset_preferences():
    """Reset all user-preferences to default values."""
    print("\nResetting user preferences to default values...\n")
    data[1]['file_folder'] = "False"
    data[1]['entry_confirmation'] = "True"
    data[1]['auto_txt'] = "True"
    with open('preferences.json', 'w') as file:
        json.dump(data[1], file)
    data[1] = load_dataset('preferences.json')
    print(format_json(data[1]))
        

def preferences():
    """
    Alter various preferences related to the program, including
    output location (save files) 
    """
    print(format_json(data[1]))
    print("To change preferences, enter the name of a preference\n"
    +"followed by 'true' or 'false', ie: file_folder true will\n"
    +"set the file_folder option to true.\nType 'reset' to"
    + " reset all preferences to default values.")
    ans = None
    while ans != "":
        ans = input("\nType 'exit' to leave preference settings.\n").lower()
        if ans == "file_folder true":
            data[1]['file_folder'] = "True"
            with open('preferences.json', 'w') as file:
                json.dump(data[1], file)
            data[1] = load_dataset('preferences.json')    
            print(format_json(data[1]))
            # create output folder if it does not exist
            file_folder()
        elif ans == "file_folder false":
            data[1]['file_folder'] = "False"
            with open('preferences.json', 'w') as file:
                json.dump(data[1], file)
            data[1] = load_dataset('preferences.json')
            print(format_json(data[1]))
        elif ans == "entry_confirmation true":
            data[1]['entry_confirmation'] = "True"
            with open('preferences.json', 'w') as file:
                json.dump(data[1], file)
            data[1] = load_dataset('preferences.json')
            print(format_json(data[1]))
        elif ans == "entry_confirmation false":
            data[1]['entry_confirmation'] = "False"
            with open('preferences.json', 'w') as file:
                json.dump(data[1], file)
            data[1] = load_dataset('preferences.json')
            print(format_json(data[1]))
        elif ans == "auto_txt false":
            data[1]["auto_txt"] = "False"
            with open('preferences.json', 'w') as file:
                json.dump(data[1], file)
            data[1] = load_dataset('preferences.json')
            print(format_json(data[1]))
        elif ans == "auto_txt true":
            data[1]["auto_txt"] = "True"
            with open('preferences.json', 'w') as file:
                json.dump(data[1], file)
            data[1] = load_dataset('preferences.json')
            print(format_json(data[1]))
        elif ans == "entry_format separate_prompt":
            data[1]["entry_format"] = "separate_prompt"
            with open('preferences.json', 'w') as file:
                json.dump(data[1], file)
            data[1] = load_dataset('preferences.json')
            print(format_json(data[1]))
        elif ans == "entry_format condensed_prompt":
            data[1]["entry_format"] = "condensed_prompt"
            with open('preferences.json', 'w') as file:
                json.dump(data[1], file)
            data[1] = load_dataset('preferences.json')
            print(format_json(data[1]))
        elif ans == "entry_format simplified_prompt":
            data[1]["entry_format"] = "simplified_prompt"
            with open('preferences.json', 'w') as file:
                json.dump(data[1], file)
            data[1] = load_dataset('preferences.json')
            print(format_json(data[1]))
        elif ans == "reset":
            reset_preferences()
        elif ans == "exit":
            print("Exiting preferences... \n")
            break
            
    
def formats_help():
    """
    Display information about available formats and current format
    settings for time entry.
    """
    with open('input_formats.txt') as file:
        print(file.read())
        

def file_folder():
    """
    Create a diectory for storing timesheet output if it doesn't
    exist, and toggle the use of this directory if user changes
    'file_folder' preference to false.
    """
    if data[1]['file_folder'] == "True":
        if not os.path.exists('output'):
            makedirs('output')
    print(f"New output directory created at {os.path.abspath('output')}")


def commands_list():
    """
    Display a list of available commands to the user from the
    'commands.json' file.
    """
    print(format_json(data[0]))
        

def clear_screen():
    """Clear the terminal/console of any generated text."""
    # make use of 'cls' command to clear screen in Windows
    if name == 'nt':
        system('cls')
    # use 'clear' for all other operating systems (linux, macosx etc)
    else:
        system('clear')


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
        ans = input("Hit enter to continue, or type a command.\n").lower()
    else:
        ans = input("Hit enter to start a timesheet, or type a command.\n").lower()
    while ans != '':
        if ans == 'filename-set':
            set_filename()
        elif ans == 'formats-help':
            formats_help()
        elif ans == 'set-entry-format':
            set_entry_format()
        elif ans == 'directory-set':
            directory_set()
        elif ans == 'intro':
            intro()
        elif ans == 'commands':
            commands_list()
        elif ans == 'clear':
            clear_screen()
        elif ans == 'preferences':
            preferences()    
        elif ans == 'exit':
            exit_program()
        else: 
            print(f"Unrecognized command: {ans}\n")
        
        ans = input("\nHit enter to continue, or type a command.\n")

def set_entry_format():
    """
    Set the entry format (what values the user is prompted for when typing in
    entries) to the specified value. Should support a broad variety of formats
    for versatility and adapability for a wide breadth of uses.
    """
    print(f"Current format is {data[1]['entry_format']}.\n")
    print("Available formats include: \n")
    formats_help()
    ans = input("Enter the name of a format and the current\n"
    +"format will be switched to the specified format\n"
    +"ie: 'condensed_prompt' will switch to condensed format.\n\n")
    if ans == "separate_prompt":
        data[1]["entry_format"] = "separate_prompt"
        with open('preferences.json', 'w') as file:
            json.dump(data[1], file)
        data[1] = load_dataset('preferences.json')
        
        print("Entry format successfully changed to separate prompt.\n")
    elif ans == "condensed_prompt":
        data[1]["entry_format"] = "condensed_prompt"
        with open('preferences.json', 'w') as file:
            json.dump(data[1], file)
        data[1] = load_dataset('preferences.json')
        print("Entry format successfully changed to condensed prompt.\n")
    elif ans == "simplified":
        # placeholder pending implementation of simplified prompt
        print("simplified")


def log_time():
    output = [] # create empty list to store output
    if data[1]["entry_format"] == "separate_prompt":
        hrs = int(input("Hours: "))
        mts = int(input("Minutes: "))
        sec = int(input("Sec: "))
        if data[1]['entry_confirmation'] == 'True':
            print(f"{hrs} hours, {mts} minutes, and {sec} seconds, correct?")
            ans = input("Enter (y/n), type 'submit' to finish entry: \n")
        else:
            # if entry_confirmation is false, show a different prompt
            ans = input("Type 'submit' to finish entry, or enter to continue.\n")
        output = [hrs, mts, sec, ans] # store time, response to prompt
    elif data[1]["entry_format"] == "condensed_prompt":
        condensed = input("Enter in order 'hrs' 'min' 'sec'\n"
        +"on a single line separated by spaces: ")
        num_values = [int(s) for s in condensed.split() if s.isdigit()]
        hrs = num_values[0]
        mts = num_values[1]
        sec = num_values[2]
        if data[1]['entry_confirmation'] =='True':
            print(f"{hrs} hours, {mts} minutes, and {sec} seconds, correct?")
            ans = input("Enter (y/n), type 'submit to finish entry: \n")
        else:
            ans = input("Type 'submit' to finish entry, or enter to continue.\n")
        output = [hrs, mts, sec, ans]
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
    print(f"Current Total: {total[0]} hours, {total[1]} minutes," 
    +f" {total[2]} seconds")


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
    
    print(time_sheet)
    sleep(2)
    clear_screen()

    
def entry_sequence():
    global time_sheet, runtime, total, output_file, entry_mode
    if entry_mode == 1:
        set_filename()
        entry_mode = 0
    while True:
        entry = log_time() #entry[0]=hrs, entry[1]=mts, entry[2]=sec
        ans = entry[-1] # store user response to validation prompt
        if data[1]['entry_confirmation'] == 'True':
            if ans == 'y':
                add_to_total(entry)
            elif ans == 'submit':
                submit_time(entry)
                break
            else:
                print("Discarding entry...")
                sleep(1)
                clear_screen()
        else:
            if ans == 'submit':
                submit_time(entry)
                break
            elif ans == '':
                add_to_total(entry)


def reset_values():
    """Reset values necessary for running the program to initial state."""
    global total, time_sheet
    total = [0,0,0]
    time_sheet = "Entries: \n"

            
def save_entries():
    global output_file, runtime, entry_mode
    
    # set directory to save finished timesheet to
    output_directory = os.getcwd()
    if data[1]['file_folder'] == "True":
        output_directory = 'output'
    # join directory path and filename for write operation
    file_path = os.path.join(output_directory, output_file)
    # check to see if current file already exists
    if os.path.isfile(file_path):
        ans=input(f"Are you sure you want to overwrite the file {file_path}?\n")
        if ans.lower() == 'n' or ans.lower() == 'no':
            output_file = input("Choose an alternate filename for output: ")
            output_file = txt_append(output_file) # if auto_txt is true, append '.txt'
            file_path = os.path.join(output_directory, output_file)
        else:
            print(f"{file_path} will be overwritten.")

    # write recorded time to file using specified name                
    with open(file_path, 'w') as file:
        file.write(time_sheet)
        print(f"Entries saved to '{file_path}'\n")
    
    ans = input("Fill out another timesheet? (y/n)\n")
    if ans.lower() != 'y':
        exit_program()
    else:
        entry_mode = 1
        reset_values()
        clear_screen()
        
        
def main():
    intro()
    while True:
        menu_sequence()
        entry_sequence()
        save_entries()

if __name__ == '__main__':
    main()
    
