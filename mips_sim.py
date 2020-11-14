#!/usr/bin/python3

import sys, re
import core_sc, utilities

def     sys_error(s):
    print ("Error: " + s)
    exit(1)

argc = len(sys.argv)
if (argc < 2): 
    sys_error("Usage: mips_sim input_file [num_cycles] [-v]")

verbose = 0
cycles = 0
mode = 0

for a in sys.argv[2:]:
    if (a == '-v'):
        verbose = 1
    elif (a == '-p1'):
        mode = 1
    elif (a == '-q'):
        mode = 0xE 
    else: 
        cycles = int(a)

if (cycles < 0): 
    sys_error("Number of cycles must be nonnegative ({}).".format(cycles));

core = core_sc.Core_SC()
utilities.load_file(core.I_Mem, sys.argv[1])
core.I_Mem.dump()
core.set_PC(core.I_Mem.get_starting_address())

core.I_Mem.set_verbose(verbose)
core.RF.set_verbose(verbose)
core.set_mode(mode)

actual_cycles = core.run(cycles)

core.RF.dump()
core.D_Mem.dump()
print("Number of cycles=%d" % actual_cycles)

