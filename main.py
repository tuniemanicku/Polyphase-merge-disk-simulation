from IOInterface import *
import generate_data
import os

VOLTAGE_INDEX = 0
ELECTRIC_CURRENT_INDEX = 1
DATA_FILE = "data.txt"

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

#2.Merge loop TODO
"""
for i in range(4):
    show_file()
    os.system("pause")
"""
#Final result
print("disk accesses:",file_interface.access_counter)
#show_file()