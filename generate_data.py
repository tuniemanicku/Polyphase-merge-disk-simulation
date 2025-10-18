#generate Voltage and Current data
from random import random as rand
NUMBER_OF_RECORDS = 1_005

def generate_records(n_user=0, n_gen=NUMBER_OF_RECORDS):
    with open("data.txt", "w") as file:
        for id in range(n_gen):
            u = rand()*20
            i_c = rand()
            file.write(f"{u} {i_c} P:{u*i_c}\n")
    create_records(n_start=n_gen, n=n_user)

def create_records(n_start, n):
    with open("data.txt", "a") as file:
        for id in range(n_start, n_start+n):
            record = input("U I: ").split()
            file.write(f"{float(record[0])} {float(record[1])}\n")
    