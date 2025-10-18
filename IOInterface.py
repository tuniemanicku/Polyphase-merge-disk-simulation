ID_VOLTAGE = 0
ID_CURRENT = 1
PAGE_SIZE = 10

class IOInterface:
    def __init__(self):
        self.access_counter = 0

        self.recently_read = ""

        self.read_buffer = []
        self.read_index = 0
        self.read_file = ""
        self.read_handle = None

        self.read_buffer2 = []
        self.read_index2 = 0
        self.read_file2 = ""
        self.read_handle2 = None

        self.write_buffer = []
        self.write_index = 0
        self.write_file = ""

    def read_page(self, index, filename):
        #print("file",filename, "rf1", self.read_file,"rf2", self.read_file2, "rr", self.recently_read)
        if filename == self.read_file:
            if index - self.base_address == len(self.read_buffer) and index%PAGE_SIZE != 0: #reached the end of file
                return None
            #print(index, self.base_address)
            if index - self.base_address == PAGE_SIZE:
                self.access_counter += 1
                self.base_address += PAGE_SIZE
                self.read_buffer = []
                for _ in range(PAGE_SIZE):
                    record = self.read_handle.readline()
                    if record:
                        self.read_buffer.append(record)
                    else:
                        break
            self.recently_read = self.read_file
            #print(self.base_address)
            if len(self.read_buffer) == 0:
                return None
            return self.read_buffer[index-self.base_address]
        elif filename == self.read_file2:
            if index - self.base_address2 == len(self.read_buffer) and index%PAGE_SIZE != 0: #reached the end of file
                return None
            #print(index, self.base_address)
            if index - self.base_address2 == PAGE_SIZE:
                self.access_counter += 1
                self.base_address2 += PAGE_SIZE
                self.read_buffer2 = []
                for _ in range(PAGE_SIZE):
                    record = self.read_handle2.readline()
                    if record:
                        self.read_buffer2.append(record)
                    else:
                        break
            self.recently_read = self.read_file2
            if len(self.read_buffer2) == 0:
                return None
            return self.read_buffer2[index-self.base_address2]
        else:
            if self.recently_read == self.read_file2 or self.recently_read == "":
                #print("rf1")
                self.access_counter += 1
                if self.read_handle:
                    self.read_handle.close()
                self.read_handle = open(filename, "r")
                i = 0
                #print("index",index)
                self.base_address = index-(index%PAGE_SIZE)
                #print(self.base_address)
                while i < self.base_address:
                    self.read_handle.readline()
                    i += 1
                self.read_buffer = []

                for _ in range(PAGE_SIZE):
                    record = self.read_handle.readline()
                    if record:
                        self.read_buffer.append(record)
                    else:
                        break
                self.read_file = filename
                self.recently_read = self.read_file
                return self.read_buffer[index-self.base_address]
            else:
                #print("rf2")
                self.access_counter += 1
                if self.read_handle2:
                    self.read_handle2.close()
                self.read_handle2 = open(filename, "r")
                i = 0
                self.base_address2 = index-(index%PAGE_SIZE)
                while i < self.base_address2:
                    self.read_handle2.readline()
                    i += 1
                self.read_buffer2 = []

                for _ in range(PAGE_SIZE):
                    record = self.read_handle2.readline()
                    if record:
                        self.read_buffer2.append(record)
                    else:
                        break
                self.read_file2 = filename
                self.recently_read = self.read_file2
                return self.read_buffer2[index-self.base_address2]


    def reset_write_buffer(self, record):
        if self.write_file != "":
            self.access_counter += 1
            with open(self.write_file, "a") as file:
                file.write(''.join(self.write_buffer))
        self.write_buffer = [record]
        self.write_index = 1
    def reset_write_buffer_end(self):
        if self.write_file != "":
            self.access_counter += 1
            with open(self.write_file, "a") as file:
                file.write(''.join(self.write_buffer))
            print(self.write_buffer)
    def write_page(self, record, filename):
        if filename == self.write_file:
            if self.write_index == PAGE_SIZE:
                self.reset_write_buffer(record)
            else:
                self.write_buffer.append(record)
                self.write_index += 1
        else:
            self.reset_write_buffer(record)
            self.write_file = filename
    
    def get_acces_counter(self):
        return self.access_counter

    def clear_read_buffer(self):
        self.recently_read = ""

        self.read_buffer = []
        self.read_index = 0
        self.read_file = ""
        if self.read_handle:
            self.read_handle.close()

        self.read_buffer2 = []
        self.read_index2 = 0
        self.read_file2 = ""
        if self.read_handle2:
            self.read_handle2.close()

    def clear_write_buffer(self):
        self.write_buffer = []
        self.write_index = 0
        self.write_file = ""
    def clear_file(self, filename):
        with open(filename, "w") as file:
            pass
    def __exit__(self):
        self.read_handle.close()