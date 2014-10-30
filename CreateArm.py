#!/usr/bin/python

import os, glob, sys, pickle, struct, collections, time, timeit

SOURCE = "benchmarks/"
DEST = "outs/"
PREFIX = "arm-none-linux-gnueabi-"
LDFLAGS = '-lm -lstdc++ -lgcc'

#Execute command
def csystem(name):
    print name
    rc = os.system(name)
    if rc != 0:
        print 'system call failed: %s' % name
        sys.exit(1)

def build(program):
	csystem("arm-none-linux-gnueabi-gcc -static -o %s.elf %s %s" % (DEST+program,SOURCE+program, LDFLAGS))
	csystem("arm-none-linux-gnueabi-nm -aS %s.elf > %s.nm" % (DEST+program, DEST+program))
	csystem("arm-none-linux-gnueabi-objdump -d %s.elf > %s.od" % (DEST+program, DEST+program))

if __name__ == "__main__":
   for program in os.listdir(SOURCE):
   	   build(program)