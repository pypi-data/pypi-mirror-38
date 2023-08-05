# Usage: R --no-save --slave --args <FUNCTION_DIR> <PID> <SPECTRUM_SUMMARY_DIR> <REPEAT_THRESHOLD> <CONSECUTIVE_FLAG> <MAPQ> < plot_spectrum.R
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


# get spectra
spectrum_tumor = read.table(paste(spectrum_dir, "/tumor_TelomerCnt_", pid,"/", pid, ".spectrum", sep=""), header=TRUE, comment.char="")
spectrum_tumor = spectrum_tumor[spectrum_tumor[,"chr"]=="unmapped",]

spectrum_control = read.table(paste(spectrum_dir, "/control_TelomerCnt_", pid,"/", pid, ".spectrum", sep=""), header=TRUE, comment.char="")
spectrum_control = spectrum_control[spectrum_control[,"chr"]=="unmapped",]


# get total number of reads 
readcount_tumor = read.table(paste(spectrum_dir, "/tumor_TelomerCnt_", pid,"/", pid, "_readcount.tsv", sep=""), header=TRUE, comment.char="")
total_reads_tumor = sum(as.numeric(readcount_tumor[ ,"reads"]))
readcount_control = read.table(paste(spectrum_dir, "/control_TelomerCnt_", pid,"/", pid, "_readcount.tsv", sep=""), header=TRUE, comment.char="")
total_reads_control = sum(as.numeric(readcount_control[ ,"reads"]))

#normalize
spectrum_tumor[ ,4:ncol(spectrum_tumor)] = spectrum_tumor[ ,4:ncol(spectrum_tumor)] * (spectrum_tumor[ ,"reads_with_pattern"] / sum(spectrum_tumor[ ,4:ncol(spectrum_tumor)]))
spectrum_control[ ,4:ncol(spectrum_control)] = spectrum_control[ ,4:ncol(spectrum_control)] * (spectrum_control[ ,"reads_with_pattern"] / sum(spectrum_control[ ,4:ncol(spectrum_control)]))
spectrum_tumor[ ,4:ncol(spectrum_tumor)] = spectrum_tumor[ ,4:ncol(spectrum_tumor)]*1000000 / total_reads_tumor
spectrum_control[ ,4:ncol(spectrum_control)] = spectrum_control[ ,4:ncol(spectrum_control)]*1000000 / total_reads_control


height_tumor = t(spectrum_tumor[ ,4:ncol(spectrum_tumor)])
height_control = t(spectrum_control[ ,4:ncol(spectrum_control)])

height = cbind(height_tumor, height_control)
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


plot_file = paste0(plot_dir,"/", pid, "_unmapped.pdf")

barplot_repeattype(height=height,
                   width=14,
                   plot_file=plot_file,
                   main=main,
                   cex.main=1,
                   repeat_threshold=repeat_threshold, count_type=count_type, mapq_threshold=mapq_threshold,
                   axis=FALSE, , axis_simple=TRUE, labels=c("Tumor", "Control"), xlas=1, tick=FALSE, cex.axis=0.85, cex.lab=0.9, inset_legend=c(-0.63,0), cex.names=0.9) 



plot_file2 = paste0(plot_dir,"/", pid, "_unmapped.png")
barplot_repeattype(height=height,
                   width=14,
                   plot_file=plot_file2,
                   file_type="png",
                   main=main,
                   cex.main=1,
                   repeat_threshold=repeat_threshold, count_type=count_type, mapq_threshold=mapq_threshold,
                   axis=FALSE, , axis_simple=TRUE, labels=c("Tumor", "Control"), xlas=1, tick=FALSE, cex.axis=0.85, cex.lab=0.9, inset_legend=c(-0.63,0), cex.names=0.9) 
