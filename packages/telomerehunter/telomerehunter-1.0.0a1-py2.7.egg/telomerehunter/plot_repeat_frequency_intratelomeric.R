# Usage: R --no-save --slave --args <PID> <SPECTRUM_SUMMARY_DIR> <REPEAT_THRESHOLD> <CONSECUTIVE_FLAG> <MAPQ> <T_TYPE> <C_TYPE> <G_TYPE> <J_TYPE> < plot_repeat_frequency_intratelomeric.R
# Description: Makes a histograms of the telomere repeats per intratelomeric read in the tumor and control sample


# get commandline arguments
commandArgs = commandArgs()
pid = commandArgs[5]
spectrum_dir = paste(commandArgs[6], "/", pid, "/", sep="")
repeat_threshold = commandArgs[7]
consecutive_flag = commandArgs[8]
mapq_threshold = commandArgs[9]
t_type = commandArgs[10]
c_type = commandArgs[11]
g_type = commandArgs[12]
j_type = commandArgs[13]


library(ggplot2)
library(grid)
library(gridExtra)

if (consecutive_flag == "True"){
  count_type = "consecutive"
}else{
  count_type = "non-consecutive"
}


repeat_types = c()
if (t_type == "True"){ repeat_types = c(repeat_types, "t")}
if (g_type == "True"){ repeat_types = c(repeat_types, "g")}
if (c_type == "True"){ repeat_types = c(repeat_types, "c")}
if (j_type == "True"){ repeat_types = c(repeat_types, "j")}


frequency_table_file_T = paste0(spectrum_dir, "/tumor_TelomerCnt_", pid, "/", pid, "_repeat_frequency_per_intratelomeric_read.tsv")

if (file.exists(frequency_table_file_T)){
  frequency_table_T = read.table(frequency_table_file_T, header=TRUE)
  frequency_table_T$sample="Tumor"
  frequency_table_T$count = frequency_table_T$count / sum(frequency_table_T$count) * 1000
}else{
  frequency_table_T = matrix(, nrow = 0, ncol = 3)
}


frequency_table_file_C = paste0(spectrum_dir, "/control_TelomerCnt_", pid, "/", pid, "_repeat_frequency_per_intratelomeric_read.tsv")

if (file.exists(frequency_table_file_C)){
  frequency_table_C = read.table(frequency_table_file_C, header=TRUE)
  frequency_table_C$sample="Control"
  frequency_table_C$count = frequency_table_C$count / sum(frequency_table_C$count) * 1000
}else{
  frequency_table_C = matrix(, nrow = 0, ncol = 3)
}


df = data.frame(rbind(as.matrix(frequency_table_T),as.matrix(frequency_table_C)))
df$sample = factor(df$sample, levels=c("Tumor", "Control"))
df$number_repeats = as.numeric(levels(df$number_repeats))[df$number_repeats]
df$count = as.numeric(levels(df$count))[df$count]


p = ggplot(df, aes(x=number_repeats, y=count)) +
  geom_bar(stat = "identity") +
  facet_wrap(~ sample) +
  ggtitle(paste0(pid, ": Frequency of Telomere Repeat Occurrences in Intratelomeric Reads")) +
  theme(plot.title = element_text(face="bold")) +
  xlab("Number of Repeats") +
  ylab("Frequency per Thousand Reads")

filtering_criteria = paste0("Filtering Criteria: ",
                            repeat_threshold, " ", count_type, " repeats",
                           ", mapq threshold = ", mapq_threshold,
                           ", repeat types = ", paste(repeat_types, collapse = ', '))

plot = arrangeGrob(p, sub = textGrob(filtering_criteria, x = 0, hjust = -0.5, vjust=0.1, gp = gpar(fontsize = 12)))


plot_file = paste0(spectrum_dir, "plots/", pid, "_hist_telomere_repeats_per_intratelomeric_read")

for (plot_type in c("png", "pdf")){
  
  if (plot_type=="png"){png(paste0(plot_file,".png"), width=30, height=18, units="cm", res=300)}     
  if (plot_type=="pdf"){pdf(paste0(plot_file,".pdf"), width=30*0.4, height=18*0.4)}
  
  print(plot)
  
  dev.off()
}


