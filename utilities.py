
def print_new_cycle(cycle_num):
    print("==========================================\nCycle {:d}".format(cycle_num))

def print_memory_word (s, addr, i):
    ui = i & 0xFFFFFFFF 
    print("{0} 0x{1:08X} 0x{2:08X} {3:d}".format(s, addr, ui, i))

def print_register (s, num, i):
    ui = i & 0xFFFFFFFF 
    print("{0} ${1:02d}=0x{2:08X} {3:d}".format(s, num, ui, i))

def print_register_dump (num, i):
    ui = i & 0xFFFFFFFF 
    print("${0:02d}=0x{1:08X}({2:11d})    ".format(num, ui, i), end='')

def print_int(s, i):
    print("{0}=0x{1:08X} {2:d}".format(s, i & 0xFFFFFFFF, i), end='')

def println_int(s, i):
    print("{0}=0x{1:08X} {2:d}".format(s, i & 0xFFFFFFFF, i))

def int_to_signed_32 (v):
    """
    Input: v is an integer
    Output: the value if the lower 32 bits are considered as 2's complement numbers 
    """
    v = v & 0xFFFFFFFF  # only lower 32 bits
    if (v & 0x80000000) :   # check the sign
        v = v - 0x100000000
    return v

def int_to_unsigned_32 (v):
    """
    Input: v is an integer
    Output: Only lower 32 bits are kept
    """
    return (v & 0xFFFFFFFF)  # only lower 32 bits

def int_to_signed_16 (v):
    """
    Input: v is an integer
    Output: the value if the lower 16 bits are considered as 2's complement numbers 
    """
    v = v & 0xFFFF      # only lower 16 bits
    if (v & 0x8000) :   # check the sign
        v = v - 0x10000
    return v

def print_signal(name, v, n):
    """
    Input: Name, v, n
    Output: None
    """
    if (n == 1) : 
        v = v & 1
        fmt = ""
        print (name+"="+str(v))
    elif (n < 16) :
        fmt = "0b{0:0"+str(n)+"b}";
    elif (n == 16) :
        fmt = "0x{0:04X}";
        v = v & 0xFFFF;
    else : 
        fmt = "0x{0:08X}";
        v = v & 0xFFFFFFFF;
    if (fmt != "") :
        print (name+"="+fmt.format(v)+" "+str(int_to_signed_32(v)))
    return 

def print_signals_1(sig):
    print_signal("opcode", sig.opcode, 6);
    print_signal("funct", sig.funct, 6);
    print_signal("rs", sig.rs, 5);
    print_signal("rt", sig.rt, 5);
    print_signal("rd", sig.rd, 5);
    print_signal("immediate", sig.immediate, 16);
    print_signal("RegDst", sig.RegDst, 1);
    print_signal("Jump", sig.Jump, 1);
    print_signal("Branch", sig.Branch, 1);
    print_signal("MemRead", sig.MemRead, 1);
    print_signal("MemtoReg", sig.MemtoReg, 1);
    print_signal("ALUOp", sig.ALUOp, 2);
    print_signal("MemWrite", sig.MemWrite, 1);
    print_signal("ALUSrc", sig.ALUSrc, 1);
    print_signal("RegWrite", sig.RegWrite, 1);
    print_signal("Sign_extended_immediate", sig.Sign_extended_immediate, 32);
    print_signal("ALU_operation", sig.ALU_operation, 4);
    print_signal("Branch_address", sig.Branch_address, 32);
    print_signal("Jump_address", sig.Jump_address, 32);
    print_signal("Write_register", sig.Write_register, 5);

def print_signals_2(sig):
    print_signal("RF_read_data_1", sig.RF_read_data_1, 32);
    print_signal("RF_read_data_2", sig.RF_read_data_2, 32);
    print_signal("ALU_input_2", sig.ALU_input_2, 32);
    print_signal("ALU_result", sig.ALU_result, 32);
    print_signal("Zero", sig.Zero, 1);
    print_signal("MEM_read_data", sig.MEM_read_data, 32);
    print_signal("Write_data", sig.Write_data, 32);
    print_signal("PCSrc", sig.PCSrc, 1);
    print_signal("PC_branch", sig.PC_branch, 32);
    print_signal("PC_new", sig.PC_new, 32);

def load_file(MEM, filename):
    # load data/instructions from the file
    import re
    pattern = re.compile('^((0x)*([0-9A-Fa-f]+))\s+((0x)*([0-9A-Fa-f]+))')
    MEM.set_memwrite(1);
    MEM.set_memread(0);
    with open(filename) as file:
        for line in file:
            m = re.search(pattern, line)
            if (m):
                address = int(m.group(1), 0)
                value = int(m.group(4), 0)
                MEM.set_address(address);
                MEM.set_data(value);  # may use int_to_signed_32(value) 
                MEM.run();
                # print ("Mem[%s]=%s"% ( hex(address),hex(value)))
                #need to set the value in memory module
    MEM.set_memwrite(0);
    return

if __name__ == '__main__':
    test = 'sig'
    "Test " + test
    if (test == 'print'):
        print_signal("B", 1, 1)
        print_signal("R", 31, 5)
        print_signal("Immd", 0xFABC, 16)
        print_signal("PC", 0x040000C4, 32)
        print_signal("RV", -1, 32)
        print_int("NoNL", -1)
        println_int("WithNL", -2)
    elif (test == 'load'):
        from hardware import Memory
        I_Mem = Memory()
        load_file(I_Mem, "input.txt")
        I_Mem.dump()
    elif (test == 'sig'):
        from signals import Signals
        sig = Signals()
        print_signals_1(sig)
        print_signals_2(sig)

