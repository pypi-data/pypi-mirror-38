#!/usr/bin/python


import os
import sys, getopt
import re
import pysam

# Description: filters telomere reads from an input BAM file and counts the total number of reads mapped to each band
def filter_telomere_reads(bam_file, band_file, out_dir, pid, sample, repeat_threshold, mapq_threshold, t_type, c_type, g_type, j_type, consecutive_flag, remove_duplicates):

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
	bamfile = pysam.Samfile( bam_file, "rb" )

	# open filtered file for writing
	filtered_file_path = out_dir + "/" + pid + "_filtered.bam"
	filtered_file = pysam.Samfile(filtered_file_path, "wb", template=bamfile)



	############################################################################
	### check if repeat threshold needs to be set individually for each read ###
	############################################################################
	
	if repeat_threshold == 'n':
		slow_version=True
	else:
		slow_version=False
	
	#slow_version=False

	#if repeat_threshold == 0:


		#### check if read lengths of the first 100 non-supplementary or secondary alignments are the same
		#cntr=0
		
		#for read in bamfile.fetch(until_eof=True):   

			#if read.is_secondary:		#skips all secondary alignments (only needed for RNA analysis!)
				#continue

			#if read.flag >= 2048:						# skip supplementary alignments
				#continue
			      
			#cntr+=1
			
			#if cntr == 1:
				#read_length = len(read.seq)
			#else:
				#if read_length != len(read.seq):
					#slow_version=True
					#print "read lengths in sample differ: repeat threshold will be set individually for each read"
					#break
				
			#if cntr == 100:	
				#break

		#if slow_version==False:
			#repeat_threshold = int(round(float(read_length)*6/100))
			#print "repeat_threshold was not set by user!\nRead length is " + str(read_length) + ".\nRepeat threshold is set to " + str(repeat_threshold) + "."
			
		## close and reopen bamfile to start reading bam file again from beginning
		#bamfile.close()
		#bamfile = pysam.Samfile( bam_file, "rb" )



	############################
	### make chromosome list ###
	############################

	# autodetect chromosome prefix in BAM file
	references = bamfile.references    # are sorted in the order of the tids

	if references[0][0:3] == "chr":
		bam_chr_prefix = "chr"
	else:
		bam_chr_prefix = ''

	# Generate list of chromosome names.
	chromosome_list = [ str(i) for i in range(1,22+1) ] + ["X","Y"]
	chromosome_list_with_prefix = [bam_chr_prefix + chr for chr in chromosome_list]



	################################################
	### make band, spectrum and gc content lists ###
	################################################

	# Read list of chromosome bands for each chromosome, strip chromosome prefixes.
	bands_list = { chr:{ "band_name":[], "end":[] } for chr in chromosome_list + ["unmapped"] }

	# make spectrum list which will be written to spectrum file
	spectrum_list = { chr:{} for chr in chromosome_list }


	for line in open( band_file, "r" ):

		try:
			line = line.rstrip().split()
			
	#		start = line[1]
			end = line[2]
			band_name = line[3]

			chrom_name = ""

			if line[0][:3] == "chr":
				chrom_name = line[0][3:]
			else:
				chrom_name = line[0]

			bands_list[chrom_name]["band_name"] += [band_name]
			bands_list[chrom_name]["end"] += [int(end)]
			
			spectrum_list[chrom_name][band_name]={"reads":0}

			
		except:

			print( "Invalid line in banding file: \'"+" ".join( line )+"\'" )


	# add unmapped to spectrum list
	spectrum_list["unmapped"] = {"unmapped": {"reads":0 } }

	bands_list["unmapped"]["band_name"] += ["unmapped"]
	bands_list["unmapped"]["end"] += [0]


	# make GC content list
	gc_content_list = { gc_content:0 for gc_content in range(0,100+1) } 




	#############################
	### loop through BAM file ###
	#############################

	# remember last chromosome and it's spectrum list
	lastChromosome = ''
	chromosomeLsEnd = None
	chromosomeLsBand = None
	spectrumTemp = None
	spectrumTemp2 = None
	spectrumUnmapped = spectrum_list["unmapped"]["unmapped"]
	sequence = ""
	chr_offset = len(bam_chr_prefix)
	#initialize band index and chromosome band last looked at
	i = 0
	band = ''


	if slow_version == False:
		for read in bamfile.fetch(until_eof=True):   

			if read.is_secondary:		#skips all secondary alignments (only needed for RNA analysis!)
				continue
			  
			if remove_duplicates == True and read.is_duplicate:		#if duplicate flag is set: skip all reads that are flagged as optical or PCR duplicate
				continue
			      
			if read.flag >= 2048:						# skip supplementary alignments
				continue
			  
			sequence = read.seq
			read_length = len(sequence)
			
			
			# get gc content and add to list (if the fraction of Ns <= 0.2)
			n_count = sequence.count('N')
			
			if float(n_count)/float(read_length) <= 0.2:
				gc_content = int(round(float(sequence.count('C') + sequence.count('G')) / float(read_length - n_count) * 100))
				gc_content_list[gc_content] += 1
		

			# get reference
			tid = read.tid
			ref_name = ''
			if tid != -1:
				ref_name = references[tid]

			#get chromosome and band
			if read.is_unmapped or ref_name not in chromosome_list_with_prefix or read.mapq < mapq_threshold :  # all reads mapped to decoy sequences or with a low mapping quality are defined as unmapped
				spectrumTemp2 = spectrumUnmapped

			else:
				chromosome = ref_name[chr_offset:]

				# for new chromosome
				if chromosome != lastChromosome:
					chromosomeLsEnd = bands_list[chromosome]["end"]
					chromosomeLsBand = bands_list[chromosome]["band_name"]
					lastChromosome = chromosome
					i = 0                              # band index
					band = chromosomeLsBand[i]
					spectrumTemp = spectrum_list[chromosome][band]
				

				read_start_pos = read.pos
				
				# check if read is in new band
				while read_start_pos > chromosomeLsEnd[i] and i <= len(chromosomeLsEnd) :
					i += 1
					band = chromosomeLsBand[i]
					spectrumTemp = spectrum_list[chromosome][band]
				

				spectrumTemp2 = spectrumTemp


			# add +1 to reads mapped to this band
			spectrumTemp2["reads"] += 1
			
			# check if read has the specified amount of patterns, else skip
			if consecutive_flag == False and len(re.findall(patterns_regex_forward, sequence)) < repeat_threshold and len(re.findall(patterns_regex_reverse, sequence)) < repeat_threshold:
				continue
			elif consecutive_flag == True and not re.search("(" + patterns_regex_forward + "){" + str(repeat_threshold) + "}", sequence) and not re.search("(" + patterns_regex_reverse + "){" + str(repeat_threshold) + "}", sequence):
				continue


			# write read to filtered file
			filtered_file.write(read)
			
			
			
			
	else:	# set repeat threshold individually for each read
		for read in bamfile.fetch(until_eof=True):   

			if read.is_secondary:		#skips all secondary alignments (only needed for RNA analysis!)
				continue
			  
			if remove_duplicates == True and read.is_duplicate:		#if duplicate flag is set: skip all reads that are flagged as optical or PCR duplicate
				continue
			      
			if read.flag >= 2048:						# skip supplementary alignments 
				continue
			  
			sequence = read.seq
			read_length = len(sequence)
			
			
			# get gc content and add to list (if the fraction of Ns <= 0.2)
			n_count = sequence.count('N')
			
			if float(n_count)/float(read_length) <= 0.2:
				gc_content = int(round(float(sequence.count('C') + sequence.count('G')) / float(read_length - n_count) * 100))
				gc_content_list[gc_content] += 1
				
				
			# get reference
			tid = read.tid
			ref_name = ''
			if tid != -1:
				ref_name = references[tid]


			#get chromosome and band
			if read.is_unmapped or ref_name not in chromosome_list_with_prefix or read.mapq < mapq_threshold :  # all reads mapped to decoy sequences or with a low mapping quality are defined as unmapped
				spectrumTemp2 = spectrumUnmapped

			else:
				chromosome = ref_name[chr_offset:]

				# for new chromosome
				if chromosome != lastChromosome:
					chromosomeLsEnd = bands_list[chromosome]["end"]
					chromosomeLsBand = bands_list[chromosome]["band_name"]
					lastChromosome = chromosome
					i = 0                              # band index
					band = chromosomeLsBand[i]
					spectrumTemp = spectrum_list[chromosome][band]
				

				read_start_pos = read.pos
				
				# check if read is in new band
				while read_start_pos > chromosomeLsEnd[i] and i <= len(chromosomeLsEnd) :
					i += 1
					band = chromosomeLsBand[i]
					spectrumTemp = spectrum_list[chromosome][band]
				

				spectrumTemp2 = spectrumTemp


			# add +1 to reads mapped to this band
			spectrumTemp2["reads"] += 1
			
			
			repeat_threshold = int(round(float(read_length)*6/100))
			
			# check if read has the specified amount of patterns, else skip
			if consecutive_flag == False and len(re.findall(patterns_regex_forward, sequence)) < repeat_threshold and len(re.findall(patterns_regex_reverse, sequence)) < repeat_threshold:
				continue
			elif consecutive_flag == True and not re.search("(" + patterns_regex_forward + "){" + str(repeat_threshold) + "}", sequence) and not re.search("(" + patterns_regex_reverse + "){" + str(repeat_threshold) + "}", sequence):
				continue


			# write read to filtered file
			filtered_file.write(read)





	#############################
	### write read count file ###
	#############################

	# open spectrum file for writing
	readcount_file = open(out_dir + "/" + pid + "_readcount.tsv", "w")

	# header
	readcount_file.write( "chr\tband\treads\n")

	#write line for each chromosome band
	for chromosome in chromosome_list + ["unmapped"]:

		for band in bands_list[chromosome]["band_name"]:
		  
			readcount_file.write( "%s\t%s\t%i\n" % (chromosome, band, spectrum_list[chromosome][band]["reads"]))


	#############################
	### write gc content file ###
	#############################

	# open gc content file for writing
	gc_content_file = open(out_dir + "/" + pid + "_" + sample + "_gc_content.tsv", "w")

	# header
	gc_content_file.write( "gc_content_percent\tread_count\n")

	#write line for each gc content
	for gc_content in range(0,100+1) :  
	  
		gc_content_file.write( "%i\t%i\n" % (gc_content, gc_content_list[gc_content]))



	##########################
	### close file handles ###
	##########################

	bamfile.close()
	filtered_file.close()
	readcount_file.close()
	gc_content_file.close()

	############################
	### index filtered file  ###  
	############################

	pysam.index(filtered_file_path)



	##################################
	### sort filtered file by name ###  
	##################################

	os.system("samtools sort -n " + filtered_file_path + " " + out_dir + "/" + pid + "_filtered_name_sorted")



