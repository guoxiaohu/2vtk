#! /usr/bin/env python2.7
"""
   script usage:
       ./2vtu.py
"""

import os.path
import sys
import glob
from pyevtk.hl import pointsToVTK
import numpy as np

#input_file=sys.argv[1]
#output_vtu=sys.argv[2]
flds_list=[]
flds_data={}

def get_file_list():
	return glob.glob('*.txt')

def get_file_name(input_file):
	basename = os.path.basename(input_file)
	return os.path.splitext(basename)[0]

def get_num_cols(input_file):
	with file(input_file) as f:
		line=f.readline()
		num_cols=len(line.split())
	return num_cols


def get_coords(input_file):
	return np.loadtxt(input_file, dtype='float64', usecols=(0, 1, 2),unpack=True)

def get_flds(input_file, fld_num):
	return np.loadtxt(input_file, dtype='float64', usecols=tuple([2+fld_num]),unpack=True)

def get_num_flds(input_file):
	num_cols=get_num_cols(input_file)
	return num_cols-3

def set_flds_name(num_flds):
	return ['flds'+str(i) for i in range(1, num_flds+1)]

def set_data_flds(input_file, flds_list, num_flds):
	for i in range(1, num_flds+1):
		print "i=", i
		print flds_list[i-1]
		flds_data[flds_list[i-1]]=get_flds(input_file, i)	
        return flds_data

def write_vtu(input_file, output_vtu):
	# Read coordinates
	x,y,z=get_coords(input_file)

	# Calculate the number of fields data
	num_flds=get_num_flds(input_file)
	print "num_flds=", num_flds

	# Set the name of each field
	flds_list=set_flds_name(num_flds)
	print flds_list

	# Read the fields data
	flds_data=set_data_flds(input_file, flds_list, num_flds)

	#output to vtu
#pointsToVTK(output_vtu, x, y, z, data = {"divr" : fld1, "volume" : fld2})
	pointsToVTK(output_vtu, x, y, z, data = flds_data)
	print 'output vtufile name is', output_vtu+".vtu"

def part2vtus():
	file_lists=get_file_list()
	for input_file in file_lists:
                print "processing ", input_file
		output_vtu=get_file_name(input_file)
                print "processing ", output_vtu
		write_vtu(input_file, output_vtu)

part2vtus()
