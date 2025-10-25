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

        self.write_buffers = []
        self.write_indexes = []
        self.write_files = []

    def read_page(self, index, filename):
        if filename == self.read_file:
            if index - self.base_address == len(self.read_buffer) and index%PAGE_SIZE != 0: #reached the end of file
                return None
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
            if len(self.read_buffer) == 0:
                return None
            return self.read_buffer[index-self.base_address]
        elif filename == self.read_file2:
            if index - self.base_address2 == len(self.read_buffer) and index%PAGE_SIZE != 0: #reached the end of file
                return None
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
            
    def write_all_cached_records(self):
        for i in range(len(self.write_files)):
            with open(self.write_files[i], "a") as file:
                file.write(''.join(self.write_buffers[i]))
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
                    with open(filename, "a") as file:
                        file.write(''.join(self.write_buffers[i]))
                        self.write_buffers[i] = [record]
                        self.write_indexes[i] = 1
                        self.access_counter += 1
                        #print(f"writing {i}")
                else:
                    self.write_buffers[i].append(record)
                    self.write_indexes[i] += 1
                break
    
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
        self.write_buffers = []
        self.write_indexes = []
        self.write_files = []
    def clear_file(self, filename):
        with open(filename, "w") as file:
            pass
    def __exit__(self):
        self.read_handle.close()