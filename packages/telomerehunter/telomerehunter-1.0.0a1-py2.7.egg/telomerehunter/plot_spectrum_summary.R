# Usage: R --no-save --slave --args <FUNCTION_DIR> <PID> <SPECTRUM_SUMMARY_DIR> <REPEAT_THRESHOLD> <CONSECUTIVE_FLAG> <MAPQ> <PATH_TO_PID_INFO> < plot_spectrum_summary.R
# Description: Makes a bar plot of the number of telomere reads (per million reads) in the different fractions of the tumor and
#              control sample. If a file containing patient information is specified, the information is shown in the legend.

# get commandline arguments
commandArgs = commandArgs()
pipeline_dir = commandArgs[5]
pid = commandArgs[6]
spectrum_dir = paste(commandArgs[7], "/", pid, "/", sep="")
repeat_threshold = commandArgs[8]
consecutive_flag = commandArgs[9]
mapq_threshold = commandArgs[10]
pid_info_path = commandArgs[11]


if (consecutive_flag == "True"){
  count_type = "Consecutive"
}else{
  count_type = "Non-consecutive"
}

source(file.path(pipeline_dir, "/functions_for_plots.R"))

# get spectra
spectrum_tumor = read.table(paste(spectrum_dir, "/tumor_TelomerCnt_", pid,"/", pid, ".spectrum", sep=""), header=TRUE, comment.char="")
spectrum_control = read.table(paste(spectrum_dir, "/control_TelomerCnt_", pid,"/", pid, ".spectrum", sep=""), header=TRUE, comment.char="")


plot_dir = file.path(spectrum_dir, "plots")

if (!(file.exists(plot_dir))){
  dir.create(plot_dir, recursive=TRUE)
}

# make empty spectrum summary tables
spectrum_summary_T = matrix(data=0, nrow=4, ncol=(ncol(spectrum_tumor)-2), byrow=TRUE)
row.names(spectrum_summary_T)=c("intra_chromosomal", "subtelomeric", "junction_spanning", "intra_telomeric")
colnames(spectrum_summary_T) = colnames(spectrum_tumor)[3:ncol(spectrum_tumor)]
spectrum_summary_T = data.frame(spectrum_summary_T)

spectrum_summary_C = matrix(data=0, nrow=4, ncol=(ncol(spectrum_tumor)-2), byrow=TRUE)
row.names(spectrum_summary_C)=c("intra_chromosomal", "subtelomeric", "junction_spanning", "intra_telomeric")
colnames(spectrum_summary_C) = colnames(spectrum_control)[3:ncol(spectrum_control)]
spectrum_summary_C = data.frame(spectrum_summary_C)


# get intra-telomeric reads (= unmapped reads)
spectrum_summary_T["intra_telomeric",] = spectrum_tumor[spectrum_tumor[,"chr"]=="unmapped",3:ncol(spectrum_tumor)]
spectrum_summary_C["intra_telomeric",] = spectrum_control[spectrum_control[,"chr"]=="unmapped",3:ncol(spectrum_control)]


for (chr in c(1:22, "X", "Y")){
  spectrum_chr_tumor = spectrum_tumor[spectrum_tumor[,"chr"]==chr,3:ncol(spectrum_tumor)]
  spectrum_chr_control = spectrum_control[spectrum_control[,"chr"]==chr,3:ncol(spectrum_control)]
  
  # get junction spanning reads
  spectrum_summary_T["junction_spanning", ] = spectrum_summary_T["junction_spanning", ] + spectrum_chr_tumor[1,] + spectrum_chr_tumor[nrow(spectrum_chr_tumor),]
  spectrum_summary_C["junction_spanning", ] = spectrum_summary_C["junction_spanning", ] + spectrum_chr_control[1,] + spectrum_chr_control[nrow(spectrum_chr_control),]
    
  # get subtelomeric reads (= first and last band)
  spectrum_summary_T["subtelomeric", ] = spectrum_summary_T["subtelomeric", ] + spectrum_chr_tumor[2,] + spectrum_chr_tumor[nrow(spectrum_chr_tumor)-1,]
  spectrum_summary_C["subtelomeric", ] = spectrum_summary_C["subtelomeric", ] + spectrum_chr_control[2,] + spectrum_chr_control[nrow(spectrum_chr_control)-1,]
  
  # get intra-chromosomal reads (= all other bands) 
  spectrum_summary_T["intra_chromosomal", ] = spectrum_summary_T["intra_chromosomal", ] + apply(spectrum_chr_tumor[3:(nrow(spectrum_chr_tumor)-2),], 2, sum)   
  spectrum_summary_C["intra_chromosomal", ] = spectrum_summary_C["intra_chromosomal", ] + apply(spectrum_chr_control[3:(nrow(spectrum_chr_control)-2),], 2, sum)   
  
}


# get total number of reads 
readcount_tumor = read.table(paste(spectrum_dir, "/tumor_TelomerCnt_", pid,"/", pid, "_readcount.tsv", sep=""), header=TRUE, comment.char="")
total_reads_tumor = sum(as.numeric(readcount_tumor[ ,"reads"]))
readcount_control = read.table(paste(spectrum_dir, "/control_TelomerCnt_", pid,"/", pid, "_readcount.tsv", sep=""), header=TRUE, comment.char="")
total_reads_control = sum(as.numeric(readcount_control[ ,"reads"]))


#normalize
spectrum_summary_norm_T = spectrum_summary_T[,2:ncol(spectrum_summary_T)] * (spectrum_summary_T[,"reads_with_pattern"] / apply(spectrum_summary_T[ ,2:ncol(spectrum_summary_T)], 1,sum))
spectrum_summary_norm_C = spectrum_summary_C[,2:ncol(spectrum_summary_C)] * (spectrum_summary_C[,"reads_with_pattern"] / apply(spectrum_summary_C[ ,2:ncol(spectrum_summary_C)], 1,sum))
spectrum_summary_norm_T = spectrum_summary_norm_T * (1000000 / total_reads_tumor)
spectrum_summary_norm_C = spectrum_summary_norm_C * (1000000 / total_reads_control)


spectrum_summary = zipFastener(spectrum_summary_norm_T, spectrum_summary_norm_C, 1)


height = t(spectrum_summary)
colnames(height) = NULL

plot_file = paste0(plot_dir,"/", pid, "_summary.pdf")
if (nchar(pid)<11){
  main = paste0(pid,": Telomere Repeat Types in Tumor and Control Sample")
}else{
  main = paste0(pid,":\nTelomere Repeat Types in Tumor and Control Sample")
}

# get patient info (if provided)
if (! is.na(pid_info_path)){
  pid_info = read.table(pid_info_path, header=TRUE)
  row.names(pid_info)=pid_info$PID
  pid_info = pid_info[pid, colnames(pid_info)!="PID"]
#  right_mar=13.5
#  width = 580
}else{
  pid_info=NA
#  right_mar=11.5
#  width = 550
}

barplot_repeattype(height=height,
                   plot_file=plot_file,
                   width=20,
                   main=main,
                   repeat_threshold=repeat_threshold, count_type=count_type, mapq_threshold=mapq_threshold,
                   axis=TRUE, labels=c("Intrachromosomal", "Subtelomeric", "Junction Spanning", "Intratelomeric"), xlas=1, tick=FALSE, cex.axis=0.85,
                   pid_info=pid_info, cex.lab=0.9) 

plot_file2 = paste0(plot_dir,"/", pid, "_summary.png")
barplot_repeattype(height=height,
                   plot_file=plot_file2,
                   file_type="png",
                   width=20,
                   main=main,
                   repeat_threshold=repeat_threshold, count_type=count_type, mapq_threshold=mapq_threshold,
                   axis=TRUE, labels=c("Intrachromosomal", "Subtelomeric", "Junction Spanning", "Intratelomeric"), xlas=1, tick=FALSE, cex.axis=0.85,
                   pid_info=pid_info, cex.lab=0.9) 

