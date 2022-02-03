from os import system, name
import os
from time import sleep
from datetime import date
from sys import exit
import json
from tkinter import Entry, Label

current_date = date.today() # store today's current date

def get_row_info(row):
    """Return a list with the hours, minutes, and seconds of an individual row."""
    try:
        row_info = [int(row[0].get()), int(row[1].get()), int(row[2].get())]
        return row_info
    except(ValueError):
        print("Error, expecting integer values.")
        # if invalid values detected, fill in with empty (0) entries
        row_info = [0, 0, 0]
    finally:
        return row_info


def format_time(total):
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
    return total


def calculate_total(entries):
    """Add up each individual total for hours, minutes, and seconds to get current total time."""
    total = [0, 0, 0]
    for entry in entries:
        row = get_row_info(entry)
        total[0] += row[0] # add hours to total
        total[1] += row[1] # add minutes to total
        total[2] += row[2] # add seconds to total
    total = format_time(total) # format total
    return total

# def save_entries():
    

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
    # Needs to be reworked for GUI
    return None


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
    print("Terminating program...")
    sleep(1)
    exit()


def save_entries():
    global output_file, runtime, entry_mode
    #Needs to be reworked for GUI
    return None
