def show_file(filename="data.txt"):
    with open(filename, "r") as file:
        record = file.readline()
        i = 0
        while i<50 and record:
            split = record.split()
            print(f"U: {split[0]}, I: {split[1]}, P: {float(split[0])*float(split[1])}")
            record = file.readline()
            i+=1
show_file(filename="dist_test_data.txt")