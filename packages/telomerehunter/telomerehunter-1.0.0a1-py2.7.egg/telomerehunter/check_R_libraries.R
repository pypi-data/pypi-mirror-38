#check if R libraries are installed, otherwise install them


pkgTest <- function(x){
    if (!require(x,character.only = TRUE)){
      install.packages(x,dep=TRUE)
      if(!require(x,character.only = TRUE)) stop(paste("R Package\"", x, "\"not found"))
    }
  }


for (library in c('ggplot2', 'reshape2', 'grid', 'gridExtra')){
  pkgTest(library)
}
