# Description: contains functions for plotting scripts of TelomereHunter

library(ggplot2)
library(reshape2)
library(grid)
library(gridExtra)

# zipFastener for TWO dataframes of unequal length
zipFastener <- function(df1, df2, along=2)
{
  # parameter checking
  if(!is.element(along, c(1,2))){
    stop("along must be 1 or 2 for rows and columns
         respectively")
  }
  # if merged by using zip feeding along the columns, the
  # same no. of rows is required and vice versa
  if(along==1 & (ncol(df1)!= ncol(df2))) {
    stop ("the no. of columns has to be equal to merge
          them by zip feeding")
    }
    if(along==2 & (nrow(df1)!= nrow(df2))) {
        stop ("the no. of rows has to be equal to merge them by
              zip feeding")
    }

    # zip fastener preperations
    d1 <- dim(df1)[along]
    d2 <- dim(df2)[along]
    i1 <- 1:d1           # index vector 1
    i2 <- 1:d2 + d1      # index vector 2

    # set biggest dimension dMax
    if(d1==d2) {
        dMax <- d1
    } else if (d1 > d2) {
        length(i2) <- length(i1)    # make vectors same length, 
        dMax <- d1                  # fill blanks with NAs   
    } else  if(d1 < d2){
        length(i1) <- length(i2)    # make vectors same length,
        dMax <- d2                  # fill blanks with NAs   
    }
    
    # zip fastener operations
    index <- as.vector(matrix(c(i1, i2), ncol=dMax, byrow=T))
    index <- index[!is.na(index)]         # remove NAs
    
    if(along==1){
        colnames(df2) <- colnames(df1)   # keep 1st colnames                  
        res <- rbind(df1,df2)[ index, ]  # reorder data frame
    }
    if(along==2) res <- cbind(df1,df2)[ , index]           

    return(res)
}


# function for making bar plots
barplot_repeattype <- function (height,
                                plot_file, file_type="pdf", width=550, mar=c(3.1, 5.1, 5.1, 9.3),
                                main, ylab="Telomere Reads (per Million Reads)",
                                repeat_threshold, count_type, mapq_threshold,
                                legend.text=row.names(height), inset_legend=c(-0.34,0),
                                axis=TRUE, axis_simple=FALSE, labels="", xlas=2, tick=TRUE, cex.axis=1, cex.lab=1, cex.main=1.2, cex.names=1,
                                pid_info=NULL) {

  col = c("indianred4", "indianred2", "khaki4", "khaki3", "lightblue4", "lightblue2", "orange", "khaki2")

  if(file_type=="png"){
    png(plot_file, width = width, height = 14, units ="cm", res=300)
  }else if(file_type=="pdf"){    
    pdf(plot_file, width = width*0.4, height = 14*0.4)
  }

  par(mar=mar, xpd=TRUE)
  mp = barplot(height,
               col=col,
               main=main,
               ylab=ylab,
               las=xlas,
               cex.main=cex.main,
               cex.axis=cex.axis,
               cex.lab=cex.lab,
               cex.names=cex.names,
               border=NA)
  
  legend.title = paste(repeat_threshold, count_type, "Repeats", "\nMapq Threshold =", mapq_threshold)
  legend_pos = legend("topright", inset=inset_legend, title=legend.title, legend=legend.text, fill=col, bty="n", cex= 0.75, border="white")  
  
  xleft = legend_pos$rect[["left"]]
  ytop = legend_pos$rect[["top"]]
  ybottom = ytop - legend_pos$rect[["h"]]
  xright = xleft + legend_pos$rect[["w"]]
  rect(xleft, ybottom, xright, ytop+(ytop-ybottom)/10) 
  
  if (axis==TRUE){
    mp2 = (mp[seq(1,length(mp),2)] + mp[seq(2,length(mp),2)]) / 2
    axis(1, labels=labels, at=mp2, las=xlas, tick=tick, cex.axis=cex.axis)
  } else if (axis_simple==TRUE){
    axis(1, labels=labels, at=mp, las=xlas, tick=tick, cex.axis=cex.axis)
  }
  
  if (is.data.frame(pid_info)){
    text = ""
    for (col in colnames(pid_info)){
      text = paste0(text, col, ": ", pid_info[1,col], "\n")
    }
    mtext("Patient Information\n", padj=1, side=4, las=1, line=1, font=2, cex=0.75)
    mtext(text, padj=1.15, side=4, las=1, line=1, cex=0.75)
    
  }
  
  garbage = dev.off()   # message from dev.off is not printed
}


grid_arrange_shared_legend <- function(plot_list, title, plot_file_prefix, width=18, height=30) {
  plots <- plot_list
  g = ggplotGrob(plots[[1]] + theme(legend.position="bottom"))$grobs
  legend <- g[[which(sapply(g, function(x) x$name) == "guide-box")]]
  lheight <- sum(legend$height)
  
  for (plot_type in c("png", "pdf")){
    
    if (plot_type=="png"){png(paste0(plot_file_prefix,".png"), width=width, height=height, units="cm", res=300)}  
    if (plot_type=="pdf"){pdf(paste0(plot_file_prefix,".pdf"), width=width*0.4, height=height*0.4)} 
      
    grid.arrange(
      do.call(arrangeGrob, lapply(plots, function(x)
        x + theme(legend.position="none"))),
      legend,
      ncol = 1,
      heights = unit.c(unit(1, "npc") - lheight, lheight),
      main=textGrob(title,gp=gpar(fontsize=20,font=2)))
    
    invisible(dev.off())   # message from dev.off is not printed  
  }
}


