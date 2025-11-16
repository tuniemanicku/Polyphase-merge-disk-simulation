import struct

# size of 2 doubles
RECORD_SIZE = 16

def show_file(filename="tape3.bin"):
    with open(filename, "rb") as file:
        record = file.read(RECORD_SIZE)
        while record:
            split = struct.unpack("<dd", record)
            print(f"U: {split[0]}, I: {split[1]}, P: {float(split[0])*float(split[1])}")
            record = file.read(RECORD_SIZE)
show_file(filename="data.bin")
print("d-1")
show_file(filename="tape1.bin")
print("1-2")
show_file(filename="tape2.bin")
print("2-3")
show_file(filename="tape3.bin")
"""test_data = [
    (15.198071226668809, 0.4704053192398422),
    (4.091171605923423, 0.9967549438931322),
    (3.612326235964982, 0.97088785662258),
    (17.563344698579545, 0.9226192676644175),
    (17.80615571913698, 0.06151555773471096),
    (4.259903119310183, 0.6698819065185879),
    (11.559245291883919, 0.315479987604973),
    (8.427997835998838, 0.48212246727507546),
    (0.696041351923129, 0.036687864492110256),
    (12.15019639209347, 0.9269155248745491),
    (18.261553357154025, 0.3681740021147223),
    (3.5283599433694435, 0.410239613557716),
    (8.438605298672519, 0.7763449243130509),
    (17.9173122223758, 0.920704921731227),
    (11.26817821335078, 0.8428508514412367)
]

with open("dist_test_data.bin", "wb") as file:
    for i in range(len(test_data)):
        file.write(struct.pack("<dd", test_data[i][0], test_data[i][1]))

with open("dist_test_data.bin", "rb") as file:
    value = file.read(RECORD_SIZE)
    while value:
        record = struct.unpack("<dd", value)
        print(record)
        value = file.read(RECORD_SIZE)"""