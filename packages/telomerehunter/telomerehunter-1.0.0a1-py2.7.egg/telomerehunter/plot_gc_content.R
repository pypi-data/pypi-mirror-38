# Usage: R --no-save --slave --args <FUNCTION_FILE> <PID> <OUTPUT_DIR> < /home/sieverli/svn/ngs2/trunk/pipelines/TelomerePipeline2/src/plot_gc_content.R
# Description: Makes a summary plot of the GC content per read for all reads and for intratelomeric reads in the tumor and control sample

# get commandline arguments
commandArgs = commandArgs()
pipeline_dir = commandArgs[5]
pid = commandArgs[6]
out_dir = paste(commandArgs[7], "/", pid, "/", sep="")


source(file.path(pipeline_dir, "functions_for_plots.R"))

# get gc content tables
gc_content_file_T = paste0(out_dir, "/tumor_TelomerCnt_", pid, "/", pid, "_tumor_gc_content.tsv")
gc_content_file_C = paste0(out_dir, "/control_TelomerCnt_", pid, "/", pid, "_control_gc_content.tsv")
gc_content_file_intratel_T = paste0(out_dir, "/tumor_TelomerCnt_", pid, "/", pid, "_intratelomeric_tumor_gc_content.tsv")
gc_content_file_intratel_C = paste0(out_dir, "/control_TelomerCnt_", pid, "/", pid, "_intratelomeric_control_gc_content.tsv")

gc_content_T = read.table(gc_content_file_T, header=TRUE)
gc_content_C = read.table(gc_content_file_C, header=TRUE)
gc_content_intratel_T = read.table(gc_content_file_intratel_T, header=TRUE)
gc_content_intratel_C = read.table(gc_content_file_intratel_C, header=TRUE)


# add percentage of reads to gc content tables
gc_content_T$fraction_of_reads = gc_content_T$read_count/sum(gc_content_T$read_count)
gc_content_C$fraction_of_reads = gc_content_C$read_count/sum(gc_content_C$read_count)
gc_content_intratel_T$fraction_of_reads = gc_content_intratel_T$read_count/sum(gc_content_intratel_T$read_count)
gc_content_intratel_C$fraction_of_reads = gc_content_intratel_C$read_count/sum(gc_content_intratel_C$read_count)


#make plot
plot_dir = file.path(out_dir, "/plots")
plot_file_prefix = paste0(plot_dir, "/",  pid, "_gc_content")

if (!(file.exists(plot_dir))){
  dir.create(plot_dir, recursive=TRUE)
}


df_all = data.frame(gc_content_percent=gc_content_T$gc_content_percent, tumor=gc_content_T$fraction_of_reads, control=gc_content_C$fraction_of_reads)
dfm_all = melt(df_all, id.var = c("gc_content_percent"), variable.name="sample", value.name="fraction_of_reads")

plot_all = ggplot(dfm_all, aes(gc_content_percent, fraction_of_reads, group=sample, color = sample)) +
  geom_line() +
  theme(legend.title=element_blank()) +
  ggtitle("All Reads") +
  xlab("GC Content [%]") +
  ylab("Fraction of Reads") 



df_intratel = data.frame(gc_content_percent=gc_content_intratel_T$gc_content_percent, tumor=gc_content_intratel_T$fraction_of_reads, control=gc_content_intratel_C$fraction_of_reads)
dfm_intratel = melt(df_intratel, id.var = c("gc_content_percent"), variable.name="sample", value.name="fraction_of_reads")

plot_intratel = ggplot(dfm_intratel, aes(gc_content_percent, fraction_of_reads, group=sample, color = sample)) +
  geom_line() +
  ggtitle("Intratelomeric Reads") +
  xlab("GC Content [%]") +
  ylab("Fraction of Reads") +
  geom_segment(aes(x = 0, y = 0.01, xend = 100, yend = 0.01), color="darkgrey")  #add line at 1%


grid_arrange_shared_legend(plot_list=list(plot_all, plot_intratel), title=paste0(pid, ": GC Content"), plot_file_prefix=plot_file_prefix)

