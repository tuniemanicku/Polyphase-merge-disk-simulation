#generate Voltage and Current data
import struct
from random import random as rand
NUMBER_OF_RECORDS = 1_005

def generate_records(n_user=0, n_gen=NUMBER_OF_RECORDS):
    with open("data.bin", "wb") as file:
        for id in range(n_gen):
            u = rand()*20
            i_c = rand()
            file.write(struct.pack("<dd", u, i_c)) #P:{u*i_c}\n")
    create_records(n_start=n_gen, n=n_user)

def create_records(n_start, n):
    with open("data.bin", "ab") as file:
        for id in range(n_start, n_start+n):
            record = input("U I: ").split()
            file.write(struct.pack("<dd", float(record[0]), float(record[1])))