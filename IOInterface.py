import struct
import os

ID_VOLTAGE = 0
ID_CURRENT = 1
PAGE_SIZE = 10 # number of records per page which is our blocking factor (b)
# record size is the size of 2 doubles
RECORD_SIZE = 16

def format_float_pairs(pairs):
    return "\n".join(f"{a} {b}" for a, b in pairs) + "\n"

class IOInterface:
    def __init__(self):
        self.access_counter = 0
        self.write_counter = 0
        self.read_counter = 0

        self.read_buffers = []
        self.read_files = []
        self.read_indexes = []
        self.read_handles = []
        self.base_addresses = []
        self.files_erased = []

        self.write_buffers = []
        self.write_indexes = []
        self.write_files = []
    
    def read_page(self, filename):
        if filename in self.read_files:
            for i in range(len(self.read_files)):
                if filename == self.read_files[i]:
                    if self.files_erased[i]:
                        self.files_erased[i] = False
                        for _ in range(PAGE_SIZE):
                            record = self.read_handles[i].read(RECORD_SIZE)
                            if record:
                                self.read_buffers[i].append(struct.unpack("<dd", record))
                            else:
                                break
                        self.access_counter += 1
                        self.read_counter += 1
                        return self.read_buffers[i][0]        
                    if self.read_indexes[i] - self.base_addresses[i] == len(self.read_buffers[i]) and self.read_indexes[i] % PAGE_SIZE != 0:
                        return None
                    if self.read_indexes[i] - self.base_addresses[i] == PAGE_SIZE:
                        self.base_addresses[i] += PAGE_SIZE
                        self.read_buffers[i] = []
                        for _ in range(PAGE_SIZE):
                            record = self.read_handles[i].read(RECORD_SIZE)
                            if record:
                                self.read_buffers[i].append(struct.unpack("<dd", record))
                            else:
                                break
                        if len(self.read_buffers[i]) != 0:
                            self.access_counter += 1
                            self.read_counter += 1
                    if len(self.read_buffers[i]) == 0:
                        return None
                    self.read_indexes[i] += 1
                    # print(self.read_buffers[i], self.read_indexes[i])
                    return self.read_buffers[i][self.read_indexes[i] - self.base_addresses[i] - 1]
        else:
            self.files_erased.append(False)
            self.read_files.append(filename)
            self.read_buffers.append([])
            self.read_indexes.append(1)
            new_handle = open(filename, "rb")
            self.read_handles.append(new_handle)
            self.base_addresses.append(0)

            for _ in range(PAGE_SIZE):
                    record = new_handle.read(RECORD_SIZE)
                    if record:
                        self.read_buffers[-1].append(struct.unpack("<dd", record))
                    else:
                        break
            self.access_counter += 1
            self.read_counter += 1
            return self.read_buffers[-1][0]
            
    def write_all_cached_records(self):
        for i in range(len(self.write_files)):
            with open(self.write_files[i], "ab") as file:
                for record in self.write_buffers[i]:
                    # print(record)
                    file.write(struct.pack("<dd", record[ID_VOLTAGE], record[ID_CURRENT]))
            #print(f"Printing cached records for {i}")
            self.access_counter += 1
            self.write_counter += 1
            #print(f"wrote buffer{i} {self.write_buffers[i]}")
        self.clear_write_buffer()

    def create_buffer(self, filename):
        self.write_files.append(filename)
        self.write_buffers.append([])
        self.write_indexes.append(0)

    def write_page(self, record, filename):
        if filename not in self.write_files:
            self.create_buffer(filename)
        for i in range (len(self.write_files)):
            if self.write_files[i] == filename:
                if self.write_indexes[i] == PAGE_SIZE:
                    with open(filename, "ab") as file:
                        for pair in self.write_buffers[i]:
                            file.write(struct.pack("<dd", pair[ID_VOLTAGE], pair[ID_CURRENT]))
                        self.write_buffers[i] = [record]
                        self.write_indexes[i] = 1
                        #print("writing full page")
                        self.access_counter += 1
                        self.write_counter += 1
                        #print(f"writing {i}")
                else:
                    self.write_buffers[i].append(record)
                    self.write_indexes[i] += 1
                break
    
    def get_acces_counters(self):
        return self.access_counter, self.read_counter, self.write_counter

    def reset_read_buffer(self, filename):
        for i in range(len(self.read_buffers)):
            if filename == self.read_files[i]:
                self.files_erased.pop(i)
                self.read_files.pop(i)
                self.read_buffers.pop(i)
                self.read_indexes.pop(i)
                self.read_handles.pop(i)
                self.base_addresses.pop(i)
                self.access_counter += 1
                self.read_counter += 1
                break
    def clear_write_buffer(self):
        self.write_buffers = []
        self.write_indexes = []
        self.write_files = []
    def clear_file(self, filename):
        with open(filename, "wb") as file:
            if filename in self.read_files:
                for i in range(len(self.read_files)):
                    if filename == self.read_files[i]:
                        self.read_indexes[i] = 0
                        self.base_addresses[i] = 0
                        self.files_erased[i] = True
                        self.access_counter += 1
                        self.write_counter += 1
                        break


    def reset_access_counters(self):
        self.access_counter = 0
        self.write_counter = 0
        self.read_counter = 0
    
    def show_file(self, filename, short=None):
        with open(filename, "rb") as file:
            index = None
            if short:
                for i in range(len(self.read_files)):
                    if self.read_files[i] == short:
                        index = i
                        break
            if index:
                counter = 1
                while self.read_indexes[index] != counter:
                    counter += 1
                    file.read(RECORD_SIZE)
            record = file.read(RECORD_SIZE)
            while record:
                split = struct.unpack("<dd", record)
                print(f"U: {split[ID_VOLTAGE]}, I: {split[ID_CURRENT]}, P: {float(split[ID_VOLTAGE])*float(split[ID_CURRENT])}")
                record = file.read(RECORD_SIZE)

    def __exit__(self):
        self.read_handle.close()