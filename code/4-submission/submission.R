#-------------------------------------------------------------
# do following when you start from many files of ASS departments, 
# create submission file WITHOUT Telephonie and CAT
#-------------------------------------------------------------
# read all csv prediction files, except Telephonie and CAT
inputPath = 'D:/3A/ML/project/AXA-wensi/pred_data_v3/'
paths <- list.files(inputPath)
# store all ASS departments' names in <lables>
labels <- unlist(strsplit(paths,'_'))[seq(1,length(paths)*2,2)]
labels <- labels[order(labels)]
paths <- paths[order(labels)]
labels <- labels[c(1:4,6:7,9:length(labels))] 
paths <- paths[c(1:4,6:7,9:length(paths))]
paths <- paste0(inputPath,paths)

# function to calculate hour index
hour_index <- function(date){
    hour = as.numeric(substr(date,12,13))
    minute = as.numeric(substr(date,15,16))
    minute <- ifelse(minute==0,1,2)
    return (hour*2+minute)
}

submissionPath = 'D:/3A/ML/project/AXA-wensi/submission.txt'
submission_data = read.csv(submissionPath,sep='\t', fileEncoding = 'UTF-8')
# change data type in submission_data
submission_data$DATE <- as.character(submission_data$DATE)
submission_data$mydate <- as.Date(substr(submission_data$DATE,1,10))
submission_data$hour_index <- hour_index(submission_data$DATE)
submission_data$ASS_ASSIGNMENT <- as.character(submission_data$ASS_ASSIGNMENT)
submission_data <- submission_data[order(submission_data$ASS_ASSIGNMENT),]
# store all ASS departments 
all_assignment <- unique(submission_data$ASS_ASSIGNMENT)
all_assignment <- all_assignment[order(all_assignment)]


for( i in 2:25){
    assign_data <- read.csv(paths[i], fileEncoding = 'UTF-8')
    assign_data$ASS_ASSIGNMENT <- all_assignment[i]
    assign_data$hour_index <- round(assign_data$hour_index*48)
    assign_data<-assign_data[,c(1,2,6,22)]
    submission_data <- merge(submission_data,assign_data,all.x = T)
    submission_data$prediction[!is.na(submission_data$CSPL_RECEIVED_CALLS)]<-submission_data$CSPL_RECEIVED_CALLS[!is.na(submission_data$CSPL_RECEIVED_CALLS)]
    submission_data$CSPL_RECEIVED_CALLS<-NULL
}

write.csv(submission_data,'./tel/submission4_tel_cat.csv', row.names = F, fileEncoding = 'UTF-8')
rm(list=ls())

#-------------------------------------------------------------
# do following when you start from loading submission file WITHOUT Telephonie and CAT
# SVR: tel, Boost: CAT
#-------------------------------------------------------------
submission_data <- read.csv('./tel/submission4_tel_cat.csv', fileEncoding = 'UTF-8')
submission_data$ASS_ASSIGNMENT <- as.character(submission_data$ASS_ASSIGNMENT)
submission_data$mydate <- as.Date(submission_data$mydate)
# store all ASS departments 
all_assignment <- as.character(unique(submission_data$ASS_ASSIGNMENT))
all_assignment <- all_assignment[order(all_assignment)]
# SVR prediction for Telephonie
# add Telephonie to submission data 
assign_data<-read.csv('./tel/pred_tel.csv', fileEncoding = 'UTF-8')
assign_data$ASS_ASSIGNMENT <- all_assignment[26]
assign_data$hour_index <- round(assign_data$hour_index*48)
assign_data<-assign_data[,c(1,2,7,24)]
assign_data$mydate<-as.Date(assign_data$mydate)
submission_data <- merge(submission_data,assign_data,all.x = T)
submission_data$prediction[!is.na(submission_data$CSPL_RECEIVED_CALLS)]<-submission_data$CSPL_RECEIVED_CALLS[!is.na(submission_data$CSPL_RECEIVED_CALLS)]
submission_data$CSPL_RECEIVED_CALLS<-NULL
# Boost prediction for CAT
# add CAT to submission data
assign_data<-read.csv('./tel/CAT_dataset.v3.csv',header = F, fileEncoding = 'UTF-8')
colnames(assign_data) <- c('mydate','hour_index','CSPL_RECEIVED_CALLS')
assign_data$mydate<-as.Date(assign_data$mydate)
assign_data$ASS_ASSIGNMENT <-all_assignment[1]
submission_data <- merge(submission_data,assign_data,all.x = T)
submission_data$prediction[!is.na(submission_data$CSPL_RECEIVED_CALLS)]<-submission_data$CSPL_RECEIVED_CALLS[!is.na(submission_data$CSPL_RECEIVED_CALLS)]
submission_data$CSPL_RECEIVED_CALLS<-NULL


#-------------------------------------------------------------
# do following when you start from loading submission file WITHOUT Telephonie and CAT
# Boost: tel, Boost: CAT
#-------------------------------------------------------------
submission_data <- read.csv('./tel/submission4_tel_cat.csv', fileEncoding = 'UTF-8')
submission_data$ASS_ASSIGNMENT <- as.character(submission_data$ASS_ASSIGNMENT)
submission_data$mydate <- as.character(submission_data$mydate)
submission_data$DATE <- as.Date(submission_data$mydate)
# store all ASS departments 
all_assignment <- as.character(unique(submission_data$ASS_ASSIGNMENT))
all_assignment <- all_assignment[order(all_assignment)]

assign_data <- read.csv('./tel/Telephonie_dataset_v4.csv',header = F, fileEncoding = 'UTF-8')
colnames(assign_data) <- c('mydate','hour_index','CSPL_RECEIVED_CALLS')
assign_data$mydate<-as.Date(assign_data$mydate)
assign_data$ASS_ASSIGNMENT <-all_assignment[26]
submission_data <- merge(submission_data,assign_data,all.x = T)
submission_data$prediction[!is.na(submission_data$CSPL_RECEIVED_CALLS)]<-submission_data$CSPL_RECEIVED_CALLS[!is.na(submission_data$CSPL_RECEIVED_CALLS)]
submission_data$CSPL_RECEIVED_CALLS<-NULL
# Boost prediction for CAT
# add CAT to submission data
assign_data<-read.csv('./tel/CAT_dataset.v3.csv',header = F, fileEncoding = 'UTF-8')
colnames(assign_data) <- c('mydate','hour_index','CSPL_RECEIVED_CALLS')
assign_data$mydate<-as.Date(assign_data$mydate)
assign_data$ASS_ASSIGNMENT <-all_assignment[1]
submission_data <- merge(submission_data,assign_data,all.x = T)
submission_data$prediction[!is.na(submission_data$CSPL_RECEIVED_CALLS)]<-submission_data$CSPL_RECEIVED_CALLS[!is.na(submission_data$CSPL_RECEIVED_CALLS)]
submission_data$CSPL_RECEIVED_CALLS<-NULL


#-------------------------------------------------------------
# write total submission data to file
#-------------------------------------------------------------
# read original data
originalPath <- './submission.txt'
originalData <- read.csv(originalPath,sep='\t', fileEncoding = 'UTF-8')
originalData$DATE <- as.character(originalData$DATE)
originalData$ASS_ASSIGNMENT <- as.character(originalData$ASS_ASSIGNMENT)
originalData$prediction <- NULL
# store required columns to res
submission_data$prediction[submission_data$prediction<0] <- 0
res <- submission_data[,c(4,1,5)]
res$DATE <- as.character(res$DATE)
res$ASS_ASSIGNMENT <- as.character(res$ASS_ASSIGNMENT)
res <- res[order(res$DATE,res$ASS_ASSIGNMENT),]
# merge res to originalData
originalData <- merge(originalData, res, all.x = T, sort = F)


write.table(originalData,'./submission_v3.txt',row.names = F,sep='\t',quote = F, fileEncoding = "UTF-8") 
