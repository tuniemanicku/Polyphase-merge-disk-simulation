import struct

ID_VOLTAGE = 0
ID_CURRENT = 1
PAGE_SIZE = 10
# record size is the size of 2 doubles
RECORD_SIZE = 16

def format_float_pairs(pairs):
    return "\n".join(f"{a} {b}" for a, b in pairs) + "\n"

class IOInterface:
    def __init__(self):
        self.access_counter = 0

        self.recently_read = ""

        self.read_buffer = []
        self.read_index = 0
        self.read_file = ""
        self.read_handle = None
        self.file_index = 0

        self.read_buffer2 = []
        self.read_index2 = 0
        self.read_file2 = ""
        self.read_handle2 = None
        self.file_index2 = 0

        self.read_buffer3 = []
        self.read_index3 = 0
        self.read_file3 = ""
        self.read_handle3 = None
        self.file_index3 = 0

        self.write_buffers = []
        self.write_indexes = []
        self.write_files = []

    def read_page(self, filename):
        if filename == self.read_file:
            if self.read_index - self.base_address == len(self.read_buffer) and self.read_index%PAGE_SIZE != 0: #reached the end of file
                return None
            if self.read_index - self.base_address == PAGE_SIZE:
                self.base_address += PAGE_SIZE
                self.read_buffer = []
                for _ in range(PAGE_SIZE):
                    record = self.read_handle.read(RECORD_SIZE)
                    if record:
                        self.read_buffer.append(struct.unpack("<dd", record))
                    else:
                        break
                if len(self.read_buffer) != 0:
                    #print("End of buffer1 next access")
                    self.access_counter += 1
            self.recently_read = self.read_file
            if len(self.read_buffer) == 0:
                return None
            self.read_index += 1
            return self.read_buffer[self.read_index-self.base_address-1]
            # return float(split[ID_VOLTAGE]), float(split[ID_CURRENT])
        elif filename == self.read_file2:
            if self.read_index2 - self.base_address2 == len(self.read_buffer2) and self.read_index2%PAGE_SIZE != 0: #reached the end of file
                return None
            if self.read_index2 - self.base_address2 == PAGE_SIZE:
                self.base_address2 += PAGE_SIZE
                self.read_buffer2 = []
                for _ in range(PAGE_SIZE):
                    record = self.read_handle2.read(RECORD_SIZE)
                    if record:
                        self.read_buffer2.append(struct.unpack("<dd", record))
                    else:
                        break
                if len(self.read_buffer2) != 0:
                    #print("End of buffer2 next access")
                    self.access_counter += 1
            self.recently_read = self.read_file2
            if len(self.read_buffer2) == 0:
                return None
            self.read_index2 += 1
            return self.read_buffer2[self.read_index2-self.base_address2-1]
            # return float(split[ID_VOLTAGE]), float(split[ID_CURRENT])
        elif filename == self.read_file3:
            if self.read_index3 - self.base_address3 == len(self.read_buffer3) and self.read_index3%PAGE_SIZE != 0: #reached the end of file
                return None
            if self.read_index3 - self.base_address3 == PAGE_SIZE:
                self.base_address3 += PAGE_SIZE
                self.read_buffer3 = []
                for _ in range(PAGE_SIZE):
                    record = self.read_handle3.read(RECORD_SIZE)
                    if record:
                        self.read_buffer3.append(struct.unpack("<dd", record))
                    else:
                        break
                if len(self.read_buffer3) != 0:
                    #print("End of buffer3 next access")
                    self.access_counter += 1
            self.recently_read = self.read_file3
            if len(self.read_buffer3) == 0:
                return None
            self.read_index3 += 1
            return self.read_buffer3[self.read_index3-self.base_address3-1]
            # return float(split[ID_VOLTAGE]), float(split[ID_CURRENT])
        else:
            if self.recently_read == "":
                #print("Replacing older buffer or placing first")
                self.access_counter += 1
                if self.read_handle:
                    self.read_handle.close()
                self.read_handle = open(filename, "rb")
                i = 0
                #print("index",index)
                self.base_address = 0#index-(index%PAGE_SIZE)
                #print(self.base_address)
                self.read_buffer = []

                for _ in range(PAGE_SIZE):
                    record = self.read_handle.read(RECORD_SIZE)
                    if record:
                        self.read_buffer.append(struct.unpack("<dd", record))
                    else:
                        break
                self.read_file = filename
                self.recently_read = self.read_file
                self.read_index = 1
                return self.read_buffer[self.read_index-self.base_address-1]
                # return split[ID_VOLTAGE], split[ID_CURRENT]
            elif self.read_file2 == "":
                #print("Replacing older buffer")
                self.access_counter += 1
                if self.read_handle2:
                    self.read_handle2.close()
                self.read_handle2 = open(filename, "rb")
                i = 0
                self.base_address2 = 0#index-(index%PAGE_SIZE)
                self.read_buffer2 = []

                for _ in range(PAGE_SIZE):
                    record = self.read_handle2.read(RECORD_SIZE)
                    if record:
                        self.read_buffer2.append(struct.unpack("<dd", record))
                    else:
                        break
                self.read_file2 = filename
                self.recently_read = self.read_file2
                self.read_index2 = 1
                return self.read_buffer2[self.read_index2-self.base_address2-1]
                # return float(split[ID_VOLTAGE]), float(split[ID_CURRENT])
            elif self.read_file3 == "":
                #print("Replacing older buffer")
                self.access_counter += 1
                if self.read_handle3:
                    self.read_handle3.close()
                self.read_handle3 = open(filename, "rb")
                i = 0
                self.base_address3 = 0#index-(index%PAGE_SIZE)
                self.read_buffer3 = []

                for _ in range(PAGE_SIZE):
                    record = self.read_handle3.read(RECORD_SIZE)
                    if record:
                        self.read_buffer3.append(struct.unpack("<dd", record))
                    else:
                        break
                self.read_file3 = filename
                self.recently_read = self.read_file3
                self.read_index3 = 1
                return self.read_buffer3[self.read_index3-self.base_address3-1]
                # return float(split[ID_VOLTAGE]), float(split[ID_CURRENT])
            else:
                #print("Replacing older buffer or placing first")
                self.access_counter += 1
                if self.read_handle:
                    self.read_handle.close()
                self.read_handle = open(filename, "rb")
                i = 0
                #print("index",index)
                self.base_address = 0#index-(index%PAGE_SIZE)
                #print(self.base_address)
                self.read_buffer = []

                for _ in range(PAGE_SIZE):
                    record = self.read_handle.read(RECORD_SIZE)
                    if record:
                        self.read_buffer.append(struct.unpack("<dd", record))
                    else:
                        break
                self.read_file = filename
                self.recently_read = self.read_file
                self.read_index = 1
                return self.read_buffer[self.read_index-self.base_address-1]
                # return split[ID_VOLTAGE], split[ID_CURRENT]

            
    def write_all_cached_records(self):
        for i in range(len(self.write_files)):
            with open(self.write_files[i], "ab") as file:
                for record in self.write_buffers[i]:
                    # print(record)
                    file.write(struct.pack("<dd", record[ID_VOLTAGE], record[ID_CURRENT]))
            #print(f"Printing cached records for {i}")
            self.access_counter += 1
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
                        #print(f"writing {i}")
                else:
                    self.write_buffers[i].append(record)
                    self.write_indexes[i] += 1
                break
    
    def get_acces_counter(self):
        return self.access_counter

    def reset_read_buffer(self, filename):
        if filename == self.read_file:
            self.read_buffer = []
            self.read_index = 0
            self.read_file = ""
            if self.read_handle:
                self.read_handle.close()
            self.file_index = 0
        elif filename == self.read_file2:
            self.read_buffer2 = []
            self.read_index2 = 0
            self.read_file2 = ""
            if self.read_handle2:
                self.read_handle2.close()
            self.file_index2 = 0
        elif filename == self.read_file3:
            self.read_buffer3 = []
            self.read_index3 = 0
            self.read_file3 = ""
            if self.read_handle3:
                self.read_handle3.close()
            self.file_index3 = 0
    def clear_write_buffer(self):
        self.write_buffers = []
        self.write_indexes = []
        self.write_files = []
    def clear_file(self, filename):
        with open(filename, "wb") as file:
            if filename == self.read_file:
                self.read_index = 0
            elif filename == self.read_file2:
                self.read_index2 = 0
    def get_read_index(self, filename):
        if filename==self.read_file:
            print(self.read_index)
        if filename==self.read_file2:
            print(self.read_index2)
    def print_read_index(self):
        print(self.read_file)
        print(self.read_file2)
    def __exit__(self):
        self.read_handle.close()