from os import system, name, makedirs
import os
from time import sleep
from datetime import date
from sys import exit
import json
from tkinter import Entry, Label

output_file = 'timesheet.txt' # default file where entries will be stored as output
total = [0,0,0] # total sum of all entries, stored in order of hours, minutes, seconds
current_date = date.today() # store today's current date
# 1 = prompt for filename


def get_row_info(row):
    """Return a list with the hours, minutes, and seconds of an individual row."""
    row_info = [int(row[0].get()), int(row[1].get()), int(row[2].get())]
    return row_info

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


data = [load_dataset('commands.json')] # hold different json files for access during runtime
data.append(load_dataset('preferences.json'))

time_sheet = "" # empty string to hold timesheet output

def timesheet_setup():
    """
    Setup timesheet file with chosen formatting options,
    information (date, numbered entries etc) and spacing.
    """
    global data, time_sheet
    if data[1]["date_info_output"] == "True":
        time_sheet += f"|Date recorded| -> {current_date}\n"
    time_sheet += "Entries: \n"

def reset_preferences():
    """Reset all user-preferences to default values."""
    print("\nResetting user preferences to default values...\n")
    data[1]['file_folder'] = "False"
    data[1]['entry_confirmation'] = "True"
    data[1]['auto_txt'] = "True"
    data[1]['entry_format'] = "separate_prompt"
    data[1]['date_info_output']
    with open('preferences.json', 'w') as file:
        json.dump(data[1], file, indent=2)
    data[1] = load_dataset('preferences.json')
    print(format_json(data[1]))


def preferences():
    """
    Alter various preferences related to the program, including
    output location (save files)
    """
    # Needs to be reworked for GUI
    return None

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

def entry_format_set():
    """
    Set the entry format (what values the user is prompted for when typing in
    entries) to the specified value. Should support a broad variety of formats
    for versatility and adapability for a wide breadth of uses.
    """
    print(f"Current format is {data[1]['entry_format']}.\n")
    print("Available formats include: \n")
    ans = input("Enter the name of a format and the current\n"
    +"format will be switched to the specified format\n"
    +"ie: 'condensed_prompt' will switch to condensed format.\n\n")
    while(True):
        if ans == "separate_prompt":
            data[1]["entry_format"] = "separate_prompt"
            with open('preferences.json', 'w') as file:
                json.dump(data[1], file, indent=2)

            data[1] = load_dataset('preferences.json')
            print("Entry format successfully changed to separate prompt.\n")
            break
        elif ans == "condensed_prompt":
            data[1]["entry_format"] = "condensed_prompt"
            with open('preferences.json', 'w') as file:
                json.dump(data[1], file, indent=2)

            data[1] = load_dataset('preferences.json')
            print("Entry format successfully changed to condensed prompt.\n")
            break
        elif ans == "simplified_prompt":
            data[1]["entry_format"] = "simplified_prompt"
            with open('preferences.json', 'w') as file:
                json.dump(data[1], file, indent=2)

            data[1] = load_dataset('preferences.json')
            print("Entry format successfully changed to simplified prompt.\n")
            break
        else:
            print("Unsupported format, please enter one of the available formats:")


def log_time():
    output = [] # create empty list to store output
    while(True):
        try:
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
                break
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
                break
            elif data[1]["entry_format"] == "simplified_prompt":
                hrs = 0
                mts = int(input("Minutes: "))
                sec = int(input("Seconds: "))
                if data[1]['entry_confirmation'] == 'True':
                    print(f"{mts} minutes, and {sec} seconds, correct?")
                    ans = input("Enter (y/n), type 'submit' to finish entry: \n")
                else:
                    # if entry_confirmation is false, show a different prompt
                    ans = input("Type 'submit' to finish entry, or enter to continue.\n")
                    output = [hrs, mts, sec, ans] # store time, response to prompt
                break
        except ValueError:
            print("Expecting integer values, please try again with a valid entry.")
            continue
    return output


def add_to_total(entry):
    global total, time_sheet
    # add entered values to total
    total[0] += entry[0]
    total[1] += entry[1]
    total[2] += entry[2]
    time_sheet += (f"-> {entry[0]} hours, {entry[1]} minutes,"
    + f" {entry[2]} seconds\n")

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
    clear_screen()
    print("Submitting...")
    sleep(1)

    add_to_total(entry)
    format_time()

    time_sheet += (f"|# Total: {total[0]} hours, {total[1]} minutes,"
    +f" {total[2]} seconds #|")

    print(time_sheet)
    input("Press enter to continue.")

    clear_screen()

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
            file_path = os.path.join(output_directory, output_file)
        else:
            print(f"{file_path} will be overwritten.")

    # write recorded time to file using specified name
    with open(file_path, 'w') as file:
        file.write(time_sheet)
        print(f"Entries saved to: \n'{file_path}'\n")


    while(True):
        ans = input("Fill out another timesheet? (y/n)\n")
        if ans.lower() == 'n':
            exit_program()
        elif ans.lower() == 'y':
            entry_mode = 1
            reset_values()
            clear_screen()
            break
        else:
            print("Expecting 'y' or 'n'...\n")
            sleep(2)
            clear_screen()
            continue