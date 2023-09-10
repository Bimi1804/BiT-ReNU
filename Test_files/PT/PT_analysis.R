library(rstudioapi)
setwd(gsub("/PT_analysis.R","",getSourceEditorContext()$path))



# ---- Import measure files ----
pt01 <- read.csv2(file.path("PT01", "measures_PT01.csv"))
pt02 <- read.csv2(file.path("PT02", "measures_PT02.csv"))
pt03 <- read.csv2(file.path("PT03", "measures_PT03.csv"))
pt04 <- read.csv2(file.path("PT04", "measures_PT04.csv"))
pt05 <- read.csv2(file.path("PT05", "measures_PT05.csv"))
pt06 <- read.csv2(file.path("PT06", "measures_PT06.csv"))


# ---- Group times ----
times <- data.frame(
  PT01_time = pt01[, 1],
  PT02_time = pt02[, 1],
  PT03_time = pt03[, 1],
  PT04_time = pt04[, 1],
  PT05_time = pt05[, 1],
  PT06_time = pt06[, 1]
)
# ---- collect min, median, max times ---- 
PT01_min_time = round(min(pt01[,1]),digits = 3)
PT01_med_time = round(median(pt01[,1]),digits = 3)
PT01_max_time = round(max(pt01[,1]),digits = 3)

PT02_min_time = round(min(pt02[,1]),digits = 3)
PT02_med_time = round(median(pt02[,1]),digits = 3)
PT02_max_time = round(max(pt02[,1]),digits = 3)

PT03_min_time = round(min(pt03[,1]),digits = 3)
PT03_med_time = round(median(pt03[,1]),digits = 3)
PT03_max_time = round(max(pt03[,1]),digits = 3)

PT04_min_time = round(min(pt04[,1]),digits = 3)
PT04_med_time = round(median(pt04[,1]),digits = 3)
PT04_max_time = round(max(pt04[,1]),digits = 3)

PT05_min_time = round(min(pt05[,1]),digits = 3)
PT05_med_time = round(median(pt05[,1]),digits = 3)
PT05_max_time = round(max(pt05[,1]),digits = 3)

PT06_min_time = round(min(pt06[,1]),digits = 3)
PT06_med_time = round(median(pt06[,1]),digits = 3)
PT06_max_time = round(max(pt06[,1]),digits = 3)

min_max_times = c(PT01_min_time,PT01_max_time,
                  PT02_min_time,PT02_max_time,
                  PT03_min_time,PT03_max_time,
                  PT04_min_time,PT04_max_time,
                  PT05_min_time,PT05_max_time,
                  PT06_min_time,PT06_max_time)
median_times = c(PT01_med_time,PT02_med_time,PT03_med_time,PT04_med_time,PT05_med_time,PT06_med_time)
all_times = c(PT01_min_time,PT01_med_time,PT01_max_time,
              PT02_min_time,PT02_med_time,PT02_max_time,
              PT03_min_time,PT03_med_time,PT03_max_time,
              PT04_min_time,PT04_med_time,PT04_max_time,
              PT05_min_time,PT05_med_time,PT05_max_time,
              PT06_min_time,PT06_med_time,PT06_max_time)
times.df <- data.frame(
  Test_id = c("PT.01","PT.02","PT.03","PT.04","PT.05","PT.06"),
  min = c(PT01_min_time,PT02_min_time,PT03_min_time,PT04_min_time,PT05_min_time,PT06_min_time),
  median = c(PT01_med_time,PT02_med_time,PT03_med_time,PT04_med_time,PT05_med_time,PT06_med_time),
  max = c(PT01_max_time,PT02_max_time,PT03_max_time,PT04_max_time,PT05_max_time,PT06_max_time)
)
#write.csv(times.df, "C:\\Users\\mbima\\Desktop\\Times.csv", row.names=FALSE)


# ---- Group memory usage ----
memory <- data.frame(
  PT01_memory = pt01[, 2],
  PT02_memory = pt02[, 2],
  PT03_memory = pt03[, 2],
  PT04_memory = pt04[, 2],
  PT05_memory = pt05[, 2],
  PT06_memory = pt06[, 2]
)




# ---- collect min, median, max memory usage ---- 
PT01_min_memory = min(pt01[,2])
PT01_med_memory = median(pt01[,2])
PT01_max_memory = max(pt01[,2])
PT02_min_memory = min(pt02[,2])
PT02_med_memory = median(pt02[,2])
PT02_max_memory = max(pt02[,2])
PT03_min_memory = min(pt03[,2])
PT03_med_memory = median(pt03[,2])
PT03_max_memory = max(pt03[,2])
PT04_min_memory = min(pt04[,2])
PT04_med_memory = median(pt04[,2])
PT04_max_memory = max(pt04[,2])
PT05_min_memory = min(pt05[,2])
PT05_med_memory = median(pt05[,2])
PT05_max_memory = max(pt05[,2])
PT06_min_memory = min(pt06[,2])
PT06_med_memory = median(pt06[,2])
PT06_max_memory = max(pt06[,2])

min_max_memory = c(PT01_min_memory,PT01_max_memory,
                   PT02_min_memory,PT02_max_memory,
                   PT03_min_memory,PT03_max_memory,
                   PT04_min_memory,PT04_max_memory,
                   PT05_min_memory,PT05_max_memory,
                   PT06_min_memory,PT06_max_memory)
median_times = c(PT01_med_memory,PT02_med_memory,
                 PT03_med_memory,PT04_med_memory,
                 PT05_med_memory,PT06_med_memory)
all_memory = c(PT01_min_memory,PT01_med_memory,PT01_max_memory,
              PT02_min_memory,PT02_med_memory,PT02_max_memory,
              PT03_min_memory,PT03_med_memory,PT03_max_memory,
              PT04_min_memory,PT04_med_memory,PT04_max_memory,
              PT05_min_memory,PT05_med_memory,PT05_max_memory,
              PT06_min_memory,PT06_med_memory,PT06_max_memory)

all_memory_rounded <- round(all_memory,digits = 3)

memory.df <- data.frame(
  Test_id = c("PT.01","PT.02","PT.03","PT.04","PT.05","PT.06"),
  min = all_memory_rounded[c(1,4,7,10,13,16)],
  median = all_memory_rounded[c(2,5,8,11,14,17)],
  max = all_memory_rounded[c(3,6,9,12,15,18)]
)
write.csv(memory.df, "C:\\Users\\mbima\\Desktop\\Memory.csv", row.names=FALSE)



################################################## TIMES BOXPLOTS #####################################################################

# ---- BOXPLOT: TIMES: PT.01 - PT.03 ----
boxplot(times[,1:3],
        names = c("PT.01", "PT.02", "PT03"),
        frame = FALSE, col = "lightskyblue",
        ylab="", xlab = "Performed Tests",
        yaxt="n")
axis(side=2, at=all_times[1:9], las=1)
title(ylab="seconds (min,median,max per Test displayed)", line=3.2)
mytitle = "Execution times for M2T Transformation in BiT-ReNU"
mysubtitle = "With increasing input size, the execution times increase."
mtext(side=3, line=2, at=0.2, adj=0, cex=1.5, mytitle)
mtext(side=3, line=1, at=0.2, adj=0, cex=1, mysubtitle, col="grey30")
abline(h=PT01_med_time, col="black", lty = "dashed", lwd = 1)
abline(h=PT02_med_time, col="black", lty = "dashed", lwd = 1)
abline(h=PT03_med_time, col="black", lty = "dashed", lwd = 1)


# ---- BOXPLOT: TIMES: PT.04 - PT.06 ----
boxplot(times[,4:6],
        names = c("PT.04", "PT.05", "PT06"),
        frame = FALSE, col = "lightskyblue",
        ylab="", xlab = "Performed Tests",
        yaxt="n")
axis(side=2, at=all_times[10:18], las=1)
title(ylab="seconds (min,median,max per Test displayed)", line=3.2)
mytitle = "Execution times for T2M Transformation in BiT-ReNU"
mysubtitle = "With increasing input size, the execution times increase."
mtext(side=3, line=2, at=0.2, adj=0, cex=1.5, mytitle)
mtext(side=3, line=1, at=0.2, adj=0, cex=1, mysubtitle, col="grey30")
abline(h=PT04_med_time, col="black", lty = "dashed", lwd = 1)
abline(h=PT05_med_time, col="black", lty = "dashed", lwd = 1)
abline(h=PT06_med_time, col="black", lty = "dashed", lwd = 1)


# ---- BOXPLOT: TIMES: PT.01 VS PT.04 ----
boxplot(times[,c(1,4)],
        names = c("PT.01", "PT.04"),
        frame = FALSE, col = "lightskyblue",
        ylab="", xlab = "Performed Tests",
        yaxt="n")
axis(side=2, at=all_times[c(2,11)], las=1)
title(ylab="seconds (medians displayed)", line=2.5)
mytitle = "Execution time comparison between PT.01(M2T) and PT.04(T2M)"
mysubtitle = "The T2M Transformation of PT.04 takes longer than M2T of PT.01."
mtext(side=3, line=2, at=0.3, adj=0, cex=1.5, mytitle)
mtext(side=3, line=1, at=0.3, adj=0, cex=1, mysubtitle, col="grey30")
abline(h=PT01_med_time, col="black", lty = "dashed", lwd = 1)
abline(h=PT04_med_time, col="black", lty = "dashed", lwd = 1)


################################################## MEMORY BOXPLOTS #####################################################################

# ---- BOXPLOT: MEMORY: PT.01 - PT.03 ----
boxplot(memory[,1:3],
        names = c("PT.01", "PT.02", "PT03"),
        frame = FALSE, col ="lightskyblue",
        ylab="", xlab = "Performed Tests",
        yaxt="n")
axis(side=2, at=all_memory[1:9],labels = round(all_memory[1:9],digits=1), las=1)
title(ylab="MiB (min,median,max per Test displayed)", line=3.2)
mytitle = "Memory Usage for M2T Transformation in BiT-ReNU"
mysubtitle = "With increasing input size, the memory usage increase."
mtext(side=3, line=2, at=0.2, adj=0, cex=1.5, mytitle)
mtext(side=3, line=1, at=0.2, adj=0, cex=1, mysubtitle, col="grey30")
abline(h=PT01_med_memory, col="black", lty = "dashed", lwd = 1)
abline(h=PT02_med_memory, col="black", lty = "dashed", lwd = 1)
abline(h=PT03_med_memory, col="black", lty = "dashed", lwd = 1)

# ---- BOXPLOT: MEMORY: PT.04 - PT.06 ----
boxplot(memory[,4:6],
        names = c("PT.04", "PT.05", "PT06"),
        frame = FALSE, col = "lightskyblue",
        ylab="", xlab = "Performed Tests",
        yaxt="n")
axis(side=2, at=all_memory[10:18],labels = round(all_memory[10:18],digits=1),las=1)
title(ylab="MiB (min,median,max per Test displayed)", line=3.2)
mytitle = "Memory Usage for T2M Transformation in BiT-ReNU"
mysubtitle = "With increasing input size, the memory usage increase."
mtext(side=3, line=2, at=0.2, adj=0, cex=1.5, mytitle)
mtext(side=3, line=1, at=0.2, adj=0, cex=1, mysubtitle, col="grey30")
abline(h=PT04_med_memory, col="black", lty = "dashed", lwd = 1)
abline(h=PT05_med_memory, col="black", lty = "dashed", lwd = 1)
abline(h=PT06_med_memory, col="black", lty = "dashed", lwd = 1)

# ---- BOXPLOT: TIMES: PT.01 VS PT.04 ----
boxplot(memory[,c(1,4)],
        names = c("PT.01", "PT.04"),
        frame = FALSE, col = "lightskyblue",
        ylab="", xlab = "Performed Tests",
        yaxt="n")
axis(side=2, at=all_memory[c(2,11)],labels = round(all_memory[c(2,11)],digits=1), las=1)
title(ylab="MiB (medians displayed)", line=2.5)
mytitle = "Memory Usage comparison between PT.01(M2T) and PT.04(T2M)"
mysubtitle = "M2T Transformation uses more memory than T2M Transformations."
mtext(side=3, line=2, at=0.3, adj=0, cex=1.5, mytitle)
mtext(side=3, line=1, at=0.3, adj=0, cex=1, mysubtitle, col="grey30")
abline(h=PT01_med_memory,col="black", lty = "dashed", lwd = 1) 
abline(h=PT04_med_memory,col="black", lty = "dashed", lwd = 1) 


