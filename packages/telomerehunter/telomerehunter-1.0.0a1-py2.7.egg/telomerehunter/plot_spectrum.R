# Usage: R --no-save --slave --args <FUNCTION_DIR> <PID> <SPECTRUM_SUMMARY_DIR> <REPEAT_THRESHOLD> <CONSECUTIVE_FLAG> <MAPQ> <BANDING_FILE> < plot_spectrum.R
# Description: Makes a bar plot for each chromosome. The chromosome bands are plotted on the x-axis and the specific telomere reads per million bases 
#              and per billion reads are plotted on the y-axis. Attention: the "junction bands" are not divided by band length (for these bands
#              the y-axis is "specific telomere reads per billion reads"), so the scaling is not correct in comparison to "normal" bands!!! 

# get commandline arguments
commandArgs = commandArgs()
pipeline_dir = commandArgs[5]
pid = commandArgs[6]
spectrum_dir = paste(commandArgs[7], "/", pid, "/", sep="")
repeat_threshold = commandArgs[8]
consecutive_flag = commandArgs[9]
mapq_threshold = commandArgs[10]
banding_file = commandArgs[11]

if (consecutive_flag == "True"){
  count_type = "Consecutive"
}else{
  count_type = "Non-consecutive"
}


source(file.path(pipeline_dir, "/functions_for_plots.R"))


# get spectra
spectrum_tumor = read.table(paste(spectrum_dir, "/tumor_TelomerCnt_", pid,"/", pid, ".spectrum", sep=""), header=TRUE, comment.char="")
spectrum_control = read.table(paste(spectrum_dir, "/control_TelomerCnt_", pid,"/", pid, ".spectrum", sep=""), header=TRUE, comment.char="")


# get total number of reads 
readcount_tumor = read.table(paste(spectrum_dir, "/tumor_TelomerCnt_", pid,"/", pid, "_readcount.tsv", sep=""), header=TRUE, comment.char="")
total_reads_tumor = sum(as.numeric(readcount_tumor[ ,"reads"]))
readcount_control = read.table(paste(spectrum_dir, "/control_TelomerCnt_", pid,"/", pid, "_readcount.tsv", sep=""), header=TRUE, comment.char="")
total_reads_control = sum(as.numeric(readcount_control[ ,"reads"]))


#normalize
spectrum_tumor[ ,4:ncol(spectrum_tumor)] = spectrum_tumor[ ,4:ncol(spectrum_tumor)] * (spectrum_tumor[ ,"reads_with_pattern"] / apply(spectrum_tumor[ ,4:ncol(spectrum_tumor)], 1,sum))
spectrum_control[ ,4:ncol(spectrum_control)] = spectrum_control[ ,4:ncol(spectrum_control)] * (spectrum_control[ ,"reads_with_pattern"] / apply(spectrum_control[ ,4:ncol(spectrum_control)], 1,sum))
spectrum_tumor[ ,4:ncol(spectrum_tumor)] = spectrum_tumor[ ,4:ncol(spectrum_tumor)]*1000000000 / total_reads_tumor
spectrum_control[ ,4:ncol(spectrum_control)] = spectrum_control[ ,4:ncol(spectrum_control)]*1000000000 / total_reads_control


# get band lengths
band_info = read.table(banding_file)
colnames(band_info) = c("chr", "start", "end", "band_name", "stain")
band_info[,"chr"] = gsub("chr", "", band_info[,1])
band_info[,"length"] = band_info[,"end"] - band_info[,"start"]

plot_dir = file.path(spectrum_dir, "plots")

if (!(file.exists(plot_dir))){
  dir.create(plot_dir, recursive=TRUE)
}

for (chr in c(1:22, "X", "Y")){
  
  spectrum_chr_tumor = spectrum_tumor[spectrum_tumor[,"chr"]==chr,]
  spectrum_chr_control = spectrum_control[spectrum_control[,"chr"]==chr,]
  bands=spectrum_chr_tumor[ , "band"]
  
  #normalize by band length
  band_info_chr = band_info[band_info[,"chr"]==chr,]
  spectrum_chr_tumor[2:(nrow(spectrum_chr_tumor)-1),3:ncol(spectrum_chr_tumor)] = spectrum_chr_tumor[2:(nrow(spectrum_chr_tumor)-1),3:ncol(spectrum_chr_tumor)] *(1000000/ band_info_chr[,"length"])
  spectrum_chr_control[2:(nrow(spectrum_chr_control)-1),3:ncol(spectrum_chr_control)] = spectrum_chr_control[2:(nrow(spectrum_chr_control)-1),3:ncol(spectrum_chr_control)] *(1000000/ band_info_chr[,"length"])
    
  height_tumor = t(spectrum_chr_tumor[ ,4:ncol(spectrum_chr_tumor)])
  height_control = t(spectrum_chr_control[ ,4:ncol(spectrum_chr_control)])
  
  height = zipFastener(height_tumor, height_control)
  colnames(height)=NULL
  
  main = paste0(pid,": Telomere Repeat Types in Chr", chr, " (Tumor and Control Sample)")
  plot_file = paste0(plot_dir,"/", pid, "_", chr, ".pdf")
  
  barplot_repeattype(height=height,
                     plot_file=plot_file, width=28, mar=c(5.1, 5.1, 5.1, 9.3),   #width=1000
                     main=main,
                     ylab="Normalized Number of Telomere Reads", #bands: Telomere Reads (per Million Bases and per Billion Reads), junctions: Telomere Reads (per Billion Reads)
                     repeat_threshold=repeat_threshold, count_type=count_type, mapq_threshold=mapq_threshold,
                     inset_legend=c(-0.18,0),
                     labels=bands, cex.axis=0.75, cex.lab=0.9) 
  
  plot_file2 = paste0(plot_dir,"/", pid, "_", chr, ".png")  
  barplot_repeattype(height=height,
                     plot_file=plot_file2, file_type="png", width=28, mar=c(5.1, 5.1, 5.1, 9.3),   #width=1000
                     main=main,
                     ylab="Normalized Number of Telomere Reads", #bands: Telomere Reads (per Million Bases and per Billion Reads), junctions: Telomere Reads (per Billion Reads)
                     repeat_threshold=repeat_threshold, count_type=count_type, mapq_threshold=mapq_threshold,
                     inset_legend=c(-0.18,0),
                     labels=bands, cex.axis=0.75, cex.lab=0.9) 
}
