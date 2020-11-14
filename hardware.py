import re
import random
from utilities import print_register, print_register_dump, print_memory_word, int_to_signed_32  

# Hardware modules

class Register:
    """
    set_data:   Set input of the register
    set_write:  Set the write signal to 1
    read:       Read value from the register
    clock:      Set input of the register to the value of the register 
    ------
    Note that without .set_write(), .clock() will not save the input value
    """
    def __init__(self):
        self.data_in = 0
        self.write = 0
        self.data = 0
    def set_data(self, d):
        self.data_in = d 
    def set_write(self, w = 1):
        self.write = w
    def read(self):
        return self.data
    def clock(self):
        if (self.write != 0):
            self.data = self.data_in

class RegisterFile:
    def __init__(self):
        self.data = [0]*32
        self.read_register_1 = 0
        self.read_register_2 = 0
        self.write_register = 0
        self.write_data = 0
        self.read_data_1 = 0
        self.read_data_2 = 0
        self.regwrite = 0
        self.verbose = 0
    def set_read_registers(self, r1, r2):
        self.read_register_1 = r1 & 0x1F
        self.read_register_2 = r2 & 0x1F
    def set_write_register(self, wr):
        self.write_register = wr & 0x1F
    def set_write_data(self, d):
        self.write_data = d 
    def set_regwrite(self, d = 1):
        self.regwrite = d
    def get_read_data_1(self):
        if (self.verbose > 0):
            print_register ("RF_R1", self.read_register_1, self.data[self.read_register_1])
        return self.data[self.read_register_1]
    def get_read_data_2(self):
        if (self.verbose > 0):
            print_register ("RF_R2", self.read_register_2, self.data[self.read_register_2])
        return self.data[self.read_register_2]
    def clock(self):
        if (self.regwrite != 0):
            if (self.write_register > 0):
                self.data[self.write_register] = self.write_data
                if (self.verbose > 0):
                    print_register("RF_W", self.write_register, self.write_data)
    def set_verbose(self, v):
        self.verbose = v
    def dump(self):
        for i in range(len(self.data)): 
            print_register_dump(i, self.data[i])
            if ((i & 3) == 3): 
                print("");

class Memory:
    """
    set_address:    Set the address of I/O operation
    set_data:       Set input data
    set_memread:    Set the memory read signal to 1
    set_memwrite:   Set the memory write signal to 1
    get_data:       Read value from out 
    clock:          Set input of the register to the value of the register 
    run:            To execute read/write memory
    ------
    Note that without .set_memwrite(), .run() will not save the input value
    """
    def __init__(self):
        self.data = {}
        self.address = 0
        self.data_in = 0
        self.data_out = 0
        self.read = 0
        self.write = 0
        self.verbose = 0
    def set_address(self, addr):
        self.address = addr
    def set_data(self, d):
        self.data_in = d 
    def set_memread(self, v = 1):
        self.read = v 
    def set_memwrite(self, v = 1):
        self.write = v
    def get_data(self): 
        return self.data_out
    def run(self):
        if (self.read == 0 and self.write == 0):
            return
        if (self.address < 0 or self.address >= 0x80000000):
            print("Error: Membery address 0x{0:08X} ({0:d}) is too large.".format(self.address))
        if ((self.address & 3) != 0):
            print("Error: Membery address 0x{0:08X} ({0:d}) is not aligned.".format(self.address))
        if (self.read != 0):
            if (self.address in self.data):
                self.data_out = self.data[self.address]
            else:
                self.data_out = 0
            if (self.verbose > 0):
                print_memory_word ("MEM_R", self.address, self.data_out)
        elif (self.write != 0):
            self.data[self.address] = self.data_in
            if (self.verbose > 0):
                print_memory_word ("MEM_W", self.address, self.data_in)

    def get_starting_address(self):
        if (len(self.data) == 0):
            return 0
        return min(self.data)
        # return min(self.data.keys())

    def get_ending_address(self):
        if (len(self.data) == 0):
            return 0
        return max(self.data)
        # return max(self.data.keys())

    def set_verbose(self, v):
        self.verbose = v

    def dump(self):
        for addr in sorted(self.data.keys()):
            print_memory_word ("MEM_D", addr, self.data[addr])

MAXINT32 = 2147483647 
MININT32 = -2147483648

def ALU_32 (n1, n2, alu_control):
    """
    Input 0000: And
    Input 0001: Or
    Input 0010: Addition
    Input 0110: Substraction
    Input 0111: Set Less Then
    Output: 
        result: Calculated result of the ALU
        zero: Zero signal of ALU(1 if result is zero)
    """
    result = 0
    if (alu_control == 0):
        result = int_to_signed_32(n1 & n2) 
    elif (alu_control == 1):
        result = int_to_signed_32(n1 | n2) 
    elif (alu_control == 2):
        result = (n1 + n2)
        if (result > MAXINT32 or result < MININT32):
            raise ValueError("Arithmetic overflow from addition %d." % result)
    elif (alu_control == 6):
        result = (n1 - n2)
        if (result > MAXINT32 or result < MININT32):
            raise ValueError("Arithmetic overflow from subtraction %d." % result)
    elif (alu_control == 7):
        result = 1 if (n1 < n2) else 0
        """
        n1 &= 0xFFFFFFFF
        n2 &= 0xFFFFFFFF
        sign1 = (n1 >> 31) & 1
        sign2 = (n2 >> 31) & 1
        if (sign1 != sign2):
            result = 1 if (sign1 > sign2) else 0 
        else:
            result = 1 if (n1 < n2) else 0 
        """
    # can check overflow here
    # result >> 31 should be 0 or -1
    zero = 1 if (result == 0) else 0
    return (result, zero)

def MUX_2_1(o_0, o_1, control):
    """
    2-1 MUX
    """
    return o_1 if control else o_0

def AND_2(d0, d1):
    """
    Two-input AND gate.
    """
    return (d0 & d1)


if __name__ == '__main__':
    test = 'MEM'
    print ("Test " + test)
    if (test == 'RF'):
        RF = RegisterFile()
        RF.set_verbose(1)
        RF.set_regwrite(1)
        for i in range(32): 
            RF.set_write_register(i)
            v = (int((random.random() - 0.5) * 0x100000000))
            RF.set_write_data(v)
            RF.clock()
        RF.dump()
    elif (test == 'MEM'):
        MEM = Memory()
        MEM.set_verbose(1)
        MEM.dump()
        MEM.set_memwrite(1)
        MEM.set_memread(0)

        a = 0x40240;
        for i in range(16):
            MEM.set_address(a)
            v = (int((random.random() - 0.5) * 0x100000000))
            MEM.set_data(v)
            MEM.run()
            a += 4
        MEM.dump()
        from utilities import println_int
        println_int ("Staring address", MEM.get_starting_address())
        println_int ("Ending  address", MEM.get_ending_address())

