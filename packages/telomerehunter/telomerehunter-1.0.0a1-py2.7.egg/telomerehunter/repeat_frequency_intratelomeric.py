#!/usr/bin/python


import os
import sys, getopt
import re
import pysam


def repeat_frequency_intratelomeric(input_path, out_dir, pid, t_type, c_type, g_type, j_type):

	################################################
	### get patterns and make regular expression ###
	################################################

	patterns_regex_forward = ""
	patterns_regex_reverse = ""

	tcg_forward = ""
	tcg_reverse = ""

	if t_type == True:
		tcg_forward += "T"
		tcg_reverse += "A"
	if g_type == True:
		tcg_forward += "G"
		tcg_reverse += "C"
	if c_type == True:
		tcg_forward += "C"
		tcg_reverse += "G"
		
	if t_type == True or g_type == True or c_type == True:
		patterns_regex_forward += "T[" + tcg_forward + "]AGGG"
		patterns_regex_reverse += "CCCT[" + tcg_reverse + "]A"
		
		if j_type == True:
			patterns_regex_forward += "|"
			patterns_regex_reverse += "|"

	if j_type == True:
		patterns_regex_forward += "TTGGGG"
		patterns_regex_reverse += "CCCCAA"
		
		


	#########################
	### open file handles ###
	#########################

	# open input bam_file for reading
	bamfile = pysam.Samfile( input_path + "/" + pid + "_filtered_intratelomeric.bam", "rb" )


	##################################
	### initialize frequency table ###
	##################################

	frequency_table = { repeats:0 for repeats in range(0,16+1) }

	######################################
	### loop through filtered BAM file ###
	######################################

	for read in bamfile.fetch(until_eof=True):   

		sequence = read.seq

		number_repeats_forward = len(re.findall(patterns_regex_forward, sequence))
		number_repeats_reverse = len(re.findall(patterns_regex_reverse, sequence))
		
		if number_repeats_forward > number_repeats_reverse:
			number_repeats = number_repeats_forward
		else:
			number_repeats = number_repeats_reverse

		try:
		      frequency_table[number_repeats] += 1
		except:
		      frequency_table[number_repeats] = 1       # if key does not exist: add to frequency_table


	##################################
	### write frequency table file ###
	##################################

	# open frequency table file for writing
	frequency_table_file = open(out_dir + "/" + pid + "_repeat_frequency_per_intratelomeric_read.tsv", "w")

	# header
	frequency_table_file.write( "number_repeats\tcount\n")

	#write line for each chromosome band
	for frequency in frequency_table:

		frequency_table_file.write( "%i\t%i\n" % (frequency, frequency_table[frequency]))



	##########################
	### close file handles ###
	##########################

	bamfile.close()
	frequency_table_file.close()










