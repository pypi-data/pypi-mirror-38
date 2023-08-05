# Usage: R --no-save --slave --args <FUNCTION_DIR> <PID> <SPECTRUM_SUMMARY_DIR> <REPEAT_THRESHOLD> <CONSECUTIVE_FLAG> <MAPQ> < plot_spectrum_simple.R
# Description: makes a bar plot of the number of intratelomeric reads (per million reads) in the tumor and control sample.

# get commandline arguments
commandArgs = commandArgs()
pipeline_dir = commandArgs[5]
pid = commandArgs[6]
spectrum_dir = paste(commandArgs[7], "/", pid, "/", sep="")
repeat_threshold = commandArgs[8]
consecutive_flag = commandArgs[9]
mapq_threshold = commandArgs[10]

if (consecutive_flag == "True"){
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

spectrum = spectrum[spectrum[,"chr"]=="unmapped",]

# get total number of reads 
readcount = read.table(read_count_file, header=TRUE, comment.char="")
total_reads = sum(as.numeric(readcount[ ,"reads"]))


#normalize
spectrum[ ,4:ncol(spectrum)] = spectrum[ ,4:ncol(spectrum)] * (spectrum[ ,"reads_with_pattern"] / sum(spectrum[ ,4:ncol(spectrum)]))
spectrum[ ,4:ncol(spectrum)] = spectrum[ ,4:ncol(spectrum)]*1000000 / total_reads


height = t(spectrum[ ,4:ncol(spectrum)])
colnames(height) = NULL

plot_dir = file.path(spectrum_dir, "plots")

if (!(file.exists(plot_dir))){
  dir.create(plot_dir, recursive=TRUE)
}


if (nchar(pid)<9){
  main = paste0(pid,": Telomere Repeat Types in Intratelomeric Reads")
}else{
  main = paste0(pid,":\nTelomere Repeat Types in Intratelomeric Reads")
}


plot_file = paste(plot_dir,"/", pid, "_unmapped.pdf", sep="")

barplot_repeattype(height=height,
                   width=14,
                   plot_file=plot_file,
                   main=main,
                   cex.main=1,
                   repeat_threshold=repeat_threshold, count_type=count_type, mapq_threshold=mapq_threshold,
                   axis=FALSE, axis_simple=TRUE, labels=c(sample), xlas=1, tick=FALSE, cex.axis=0.85, cex.lab=0.9, inset_legend=c(-0.63,0), cex.names=0.9) 


plot_file2 = paste(plot_dir,"/", pid, "_unmapped.png", sep="")
barplot_repeattype(height=height,
                   width=14,
                   plot_file=plot_file2,
                   file_type="png",
                   main=main,
                   cex.main=1,
                   repeat_threshold=repeat_threshold, count_type=count_type, mapq_threshold=mapq_threshold,
                   axis=FALSE, axis_simple=TRUE, labels=c(sample), xlas=1, tick=FALSE, cex.axis=0.85, cex.lab=0.9, inset_legend=c(-0.63,0), cex.names=0.9) 


