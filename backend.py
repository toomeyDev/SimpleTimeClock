from os import system, name
from time import sleep
from datetime import date
from sys import exit

current_date = date.today() # store today's current date

def get_row_info(row):
    """Return a list with the hours, minutes, and seconds of an individual row."""
    row_info = []
    # get time for each position in the row (hours/minutes/seconds)
    for time_pos in row:
        try:
            interval_info = int(time_pos.get())
        except(ValueError):
            print("Error, expecting integer value for time value.")
            # if invalid value detected, fill set position to value 0
            interval_info = 0
        finally:
            row_info.append(interval_info)
    return row_info


def format_time(total):
    """
    Format the current total values, converting values
    greater than or equal to 60 to their equivalent larger
    time denominations (ie: 120 seconds becomes 2 minutes,
    180 minutes becomes three hours and so on).
    """
    position = 2
    for interval in reversed(total):
        # only convert minutes/seconds to higher intervals
        if interval / 60 >= 1 and position != 0:
            interval_remainder = interval % 60
            interval_quotient = int(interval / 60)
            total[position - 1] += interval_quotient
            total[position] = interval_remainder
        position -= 1 # track which interval (hr/min/sec) is being converted

    # return the total after any conversions
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
