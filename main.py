from IOInterface import *
import generate_data
import os
import time
VOLTAGE_INDEX = 0
ELECTRIC_CURRENT_INDEX = 1
DATA_FILE = "dist_test_data.txt"

TAPE_1 = "tape1.txt"
TAPE_2 = "tape2.txt"
TAPE_3 = "tape3.txt"

def show_file(filename=DATA_FILE):
    with open(filename, "r") as file:
        record = file.readline()
        while record:
            split = record.split()
            print(f"U: {split[ID_VOLTAGE]}, I: {split[ID_CURRENT]}, P: {float(split[ID_VOLTAGE])*float(split[ID_CURRENT])}")
            record = file.readline()

def calculate_power(record):
    return float(record[VOLTAGE_INDEX]) * float(record[ELECTRIC_CURRENT_INDEX])
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
longer_tape = None
longer_no_of_runs = None
n_tape1 = 1
last_record_tape1 = None
last_number_tape1 = None
n_tape2 = 0
last_record_tape2 = None
last_number_tape2 = None
next_record = file_interface.read_page(DATA_FILE)
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
        next_record = file_interface.read_page(DATA_FILE)
        if not next_record:
            longer_tape = TAPE_1
            longer_no_of_runs = n_tape1
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
        next_record = file_interface.read_page(DATA_FILE)
        index += 1
        if not next_record:
            longer_tape = TAPE_2
            longer_no_of_runs = n_tape2
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
#---------------------------------------------
#print("Longer tape after initial distribution:", longer_tape)
shorter_tape = None
shorter_tape_size = 0
if longer_tape == TAPE_2:
    shorter_tape = TAPE_1
    shorter_tape_size = n_tape1
    longer_tape_size = n_tape2
else:
    shorter_tape = TAPE_2
    shorter_tape_size = n_tape2
    longer_tape_size = n_tape1
destination_tape = TAPE_3
#print("Shorter tape after initial distribution:", shorter_tape)

#2.Merge loop TODO
file_sorted = False
phase_counter = 1
shorter_tape_empty = False
shorter_record = None
longer_record = None

while not file_sorted:
    print(f"Start of phase {phase_counter}, n={shorter_tape_size}")
    shorter_record = (file_interface.read_page(shorter_tape) if not shorter_record else shorter_record) #to wlozyc do ifa czy poprzedni rekord przeczytany czy None
    if not shorter_record: #write rest of the longer to destination
        pass
    else:
        shorter_record_val = calculate_power(shorter_record)
    longer_record = (file_interface.read_page(longer_tape) if not longer_record else longer_record) #to wlozyc do ifa czy poprzedni rekord przeczytany czy None
    if not longer_record: #end algorithm
        file_sorted = True
        shorter_tape_empty = True
    else:
        longer_record_val = calculate_power(longer_record)
    run_counter_short = 0
    run_counter_long = 0
    while not shorter_tape_empty:
        #time.sleep(0.5)
        #if phase_counter > 1:
        #        print(f"sh:{shorter_record_val}, l:{longer_record_val}")
        if run_counter_short == run_counter_long and longer_record and shorter_record:
            if shorter_record_val > longer_record_val:
                file_interface.write_page(longer_record, destination_tape)
                next_record = file_interface.read_page(longer_tape)
                if not next_record: #dummy
                    run_counter_long += 1
                else:
                    next_record_val = calculate_power(next_record)
                    if next_record_val < longer_record_val:
                        run_counter_long += 1
                    longer_record_val = next_record_val
                    longer_record = next_record
            else:
                file_interface.write_page(shorter_record, destination_tape)
                next_record = file_interface.read_page(shorter_tape)
                if not next_record: #dummy
                    run_counter_short += 1
                else:
                    next_record_val = calculate_power(next_record)
                    if next_record_val < shorter_record_val:
                        run_counter_short += 1
                    shorter_record_val = next_record_val
                    shorter_record = next_record
        else:
            if run_counter_short > run_counter_long:
                file_interface.write_page(longer_record, destination_tape)
                next_record = file_interface.read_page(longer_tape)
                if not next_record: #dummy
                    run_counter_long += 1
                else:
                    next_record_val = calculate_power(next_record)
                    if next_record_val < longer_record_val:
                        run_counter_long += 1
                    longer_record_val = next_record_val
                    longer_record = next_record
            else:
                file_interface.write_page(shorter_record, destination_tape)
                next_record = file_interface.read_page(shorter_tape)
                if not next_record: #dummy
                    run_counter_short += 1
                else:
                    next_record_val = calculate_power(next_record)
                    if next_record_val < shorter_record_val:
                        run_counter_short += 1
                    shorter_record_val = next_record_val
                    shorter_record = next_record
        if run_counter_short == shorter_tape_size and run_counter_long == shorter_tape_size:
            shorter_tape_empty = True

    file_interface.write_all_cached_records()
    show_file(filename=destination_tape)
    file_interface.reset_read_buffer(shorter_tape)
    shorter_record = longer_record
    longer_record = None

    #switching tapes for the cycle
    temp = destination_tape
    destination_tape = shorter_tape
    shorter_tape = longer_tape
    longer_tape = temp

    #print("longer",longer_tape)
    #print("shorter",shorter_tape)
    #print("dst",destination_tape)
    file_interface.clear_file(destination_tape)
    shorter_tape_empty = False
    #set new short_tape_length and check whether file sorted
    longer_tape_size -= shorter_tape_size
    longer_tape_size, shorter_tape_size = shorter_tape_size, longer_tape_size
    if shorter_tape_size == 0:
        file_sorted = True
        print("File sorted")
    elif input("Press enter to continue: ") == "exit": #means to exit mid-simulation
        file_sorted = True
    #os.system("pause")
    phase_counter += 1

#Final result
print("disk accesses:",file_interface.get_acces_counter())
