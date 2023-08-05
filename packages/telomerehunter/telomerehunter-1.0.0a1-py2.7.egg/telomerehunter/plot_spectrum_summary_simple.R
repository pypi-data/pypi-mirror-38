# Usage: R --no-save --slave --args <FUNCTION_DIR> <PID> <SPECTRUM_SUMMARY_DIR> <REPEATHRESHOLD> <CONSECUTIVE_FLAG> <MAPQ> <PATHO_PID_INFO> < plot_spectrum_summary_simple.R
# Description: Makes a bar plot of the number of telomere reads (per million reads) in the different fractions of a
#              sample (only tumor or control). If a file containing patient information is specified, the information is shown in the legend.

# get commandline arguments
commandArgs = commandArgs()
pipeline_dir = commandArgs[5]
pid = commandArgs[6]
spectrum_dir = paste(commandArgs[7], "/", pid, "/", sep="")
repeat_threshold = commandArgs[8]
consecutive_flag = commandArgs[9]
mapq_threshold = commandArgs[10]
pid_info_path = commandArgs[11]


if (consecutive_flag == "yes"){
  count_type = "Consecutive"
}else{
  count_type = "Non-consecutive"
}

source(file.path(pipeline_dir, "/functions_for_plots.R"))


# get spectrum
spectrum_tumor_file = paste(spectrum_dir, "/tumor_TelomerCnt_", pid,"/", pid, ".spectrum", sep="")
spectrum_control_file = paste(spectrum_dir, "/control_TelomerCnt_", pid,"/", pid, ".spectrum", sep="")
                            
if (file.exists(spectrum_tumor_file)){
  sample="Tumor"
  spectrum = read.table(spectrum_tumor_file, header=TRUE, comment.char="")
  read_count_file = paste(spectrum_dir, "/tumor_TelomerCnt_", pid,"/", pid, "_readcount.tsv", sep="")
}else{
  sample="Control"
  spectrum = read.table(spectrum_control_file, header=TRUE, comment.char="")
  read_count_file = paste(spectrum_dir, "/control_TelomerCnt_", pid,"/", pid, "_readcount.tsv", sep="")
}



plot_dir = file.path(spectrum_dir, "plots")

if (!(file.exists(plot_dir))){
  dir.create(plot_dir, recursive=TRUE)
}

# make empty spectrum summary tables
spectrum_summary = matrix(data=0, nrow=4, ncol=(ncol(spectrum)-2), byrow=TRUE)
row.names(spectrum_summary)=c("intra_chromosomal", "subtelomeric", "junction_spanning", "intra_telomeric")
colnames(spectrum_summary) = colnames(spectrum)[3:ncol(spectrum)]
spectrum_summary = data.frame(spectrum_summary)


# get intra-telomeric reads (= unmapped reads)
spectrum_summary["intra_telomeric",] = spectrum[spectrum[,"chr"]=="unmapped",3:ncol(spectrum)]


for (chr in c(1:22, "X", "Y")){
  spectrum_chr = spectrum[spectrum[,"chr"]==chr,3:ncol(spectrum)]
  
  # get junction spanning reads
  spectrum_summary["junction_spanning", ] = spectrum_summary["junction_spanning", ] + spectrum_chr[1,] + spectrum_chr[nrow(spectrum_chr),]
  
  # get subtelomeric reads (= first and last band)
  spectrum_summary["subtelomeric", ] = spectrum_summary["subtelomeric", ] + spectrum_chr[2,] + spectrum_chr[nrow(spectrum_chr)-1,]
  
  # get intra-chromosomal reads (= all other bands) 
  spectrum_summary["intra_chromosomal", ] = spectrum_summary["intra_chromosomal", ] + apply(spectrum_chr[3:(nrow(spectrum_chr)-2),], 2, sum)   
  
}


# get total number of reads 
readcount = read.table(read_count_file, header=TRUE, comment.char="")
total_reads = sum(as.numeric(readcount[ ,"reads"]))


#normalize
spectrum_summary_norm = spectrum_summary[,2:ncol(spectrum_summary)] * (spectrum_summary[,"reads_with_pattern"] / apply(spectrum_summary[ ,2:ncol(spectrum_summary)], 1,sum))
spectrum_summary_norm = spectrum_summary_norm * (1000000 / total_reads)


height = t(spectrum_summary_norm)
colnames(height) = NULL

plot_file = paste0(plot_dir,"/", pid, "_summary.pdf")
if (nchar(pid)<11){
  main = paste0(pid,": Telomere Repeat Types in ", sample, " Sample")
}else{
  main = paste0(pid,":\nTelomere Repeat Types in ", sample, " Sample")
}

# get patient info (if provided)
if (! is.na(pid_info_path)){
  pid_info = read.table(pid_info_path, header=TRUE)
  row.names(pid_info)=pid_info$PID
  pid_info = pid_info[pid, colnames(pid_info)!="PID"]
}else{
  pid_info=NA
}

barplot_repeattype(height=height,
                   plot_file=plot_file,
                   width=20,
                   main=main,
                   repeat_threshold=repeat_threshold, count_type=count_type, mapq_threshold=mapq_threshold,
                   axis=FALSE, axis_simple=TRUE, labels=c("Intrachromosomal", "Subtelomeric", "Junction Spanning", "Intratelomeric"), xlas=1, tick=FALSE, cex.axis=0.85,
                   pid_info=pid_info, cex.lab=0.9) 


plot_file2 = paste0(plot_dir,"/", pid, "_summary.png")
barplot_repeattype(height=height,
                   plot_file=plot_file2,
                   file_type="png",
                   width=20,
                   main=main,
                   repeat_threshold=repeat_threshold, count_type=count_type, mapq_threshold=mapq_threshold,
                   axis=FALSE, axis_simple=TRUE, labels=c("Intrachromosomal", "Subtelomeric", "Junction Spanning", "Intratelomeric"), xlas=1, tick=FALSE, cex.axis=0.85,
                   pid_info=pid_info, cex.lab=0.9) 

