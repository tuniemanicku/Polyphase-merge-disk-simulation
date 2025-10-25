from IOInterface import *
import generate_data
import os

VOLTAGE_INDEX = 0
ELECTRIC_CURRENT_INDEX = 1
DATA_FILE = "data.txt"

TAPE_1 = "tape1.txt"
TAPE_2 = "tape2.txt"
TAPE_3 = "tape3.txt"

def show_file(filename=DATA_FILE):
    with open(filename, "r") as file:
        record = file.readline()
        while record:
            print(record)
            record = file.readline()

def calculate_power(record):
    arr = record.split()
    return float(arr[VOLTAGE_INDEX]) * float(arr[ELECTRIC_CURRENT_INDEX])
"""
input_valid = False
while not input_valid:
    try:
        n_user = int(input("Number of records to type: "))
        n_gen = int(input("Number of records to generate: "))
        input_valid = True
    except:
        input_valid = False
generate_data.generate_records(n_user=n_user, n_gen=n_gen)
"""
#Starting state of the file
#show_file(filename=DATA_FILE)
file_interface = IOInterface()
file_interface.clear_file("tape1.txt")
file_interface.clear_file("tape2.txt")
file_interface.clear_file("tape3.txt")

#sorting
#1.Initial distribution - Fibonacci
larger_tape = None
larger_no_of_runs = None
n_tape1 = 1
last_record_tape1 = None
last_number_tape1 = None
n_tape2 = 0
last_record_tape2 = None
last_number_tape2 = None
next_record = file_interface.read_page(0, DATA_FILE)
next_record_val = calculate_power(next_record)

finish1 = None
finish2 = None

index = 1
first_run = True
runs_read1 = 0
runs_read2 = 0

all_runs_distributed = False
while not all_runs_distributed:
    n_tape1 += n_tape2
    last_record_tape1 = next_record
    last_number_tape1 = next_record_val
    if finish1: #check for coalescing
        if finish1 <= last_number_tape1:
            runs_read1 -= 1
    while runs_read1 < n_tape1:
        next_record = file_interface.read_page(index, DATA_FILE)
        index += 1
        if not next_record:
            larger_tape = TAPE_1
            larger_no_of_runs = n_tape1
            all_runs_distributed = True
            file_interface.write_page(last_record_tape1, "tape1.txt")
            break
        next_record_val = calculate_power(next_record)
        file_interface.write_page(last_record_tape1, "tape1.txt")
        if next_record_val < last_number_tape1:
            runs_read1 += 1
        if runs_read1 == n_tape1:
            finish1 = last_number_tape1
        if runs_read1 < n_tape1:
            last_number_tape1 = next_record_val
            last_record_tape1 = next_record

    if all_runs_distributed:
        break

    n_tape2 += n_tape1
    last_record_tape2 = next_record
    last_number_tape2 = next_record_val
    if finish2: #check for coalescing
        if finish2 <= last_number_tape2:
            runs_read2 -= 1
    while runs_read2 < n_tape2:
        next_record = file_interface.read_page(index, DATA_FILE)
        index += 1
        if not next_record:
            larger_tape = TAPE_2
            larger_no_of_runs = n_tape2
            all_runs_distributed = True
            file_interface.write_page(last_record_tape1, "tape2.txt")
            break
        next_record_val = calculate_power(next_record)
        file_interface.write_page(last_record_tape2, "tape2.txt")
        if next_record_val < last_number_tape2:
            runs_read2 += 1
        if runs_read2 == n_tape2:
            finish2 = last_number_tape2
        if runs_read2 < n_tape2:
            last_number_tape2 = next_record_val
            last_record_tape2 = next_record
    
file_interface.write_all_cached_records()
print("Larger tape after initial distribution:", larger_tape)
shorter_tape = (TAPE_1 if larger_tape == TAPE_2 else TAPE_2)
print("Shorter tape after initial distribution:", shorter_tape)

#2.Merge loop TODO
file_sorted = False
phase_counter = 1
shorter_tape_empty = False
while not file_sorted:
    print(f"Start of phase {phase_counter}")
    shorter_tape_index = 0
    larger_tape_index = 0
    while not shorter_tape_empty:
        shorter_record = file_interface.read_page(shorter_tape_index, shorter_tape)
        shorter_record_val = calculate_power(shorter_record)
        shorter_tape_index += 1
        larger_record = file_interface.read_page(larger_tape_index, larger_tape)
        larger_record_val = calculate_power(larger_record)
        larger_tape_index += 1


    file_sorted = True
    show_file()
    os.system("pause")
    phase_counter += 1

#Final result
print("disk accesses:",file_interface.access_counter)
#show_file()