inputPath <- './data_v1/'
paths <- list.files(inputPath)
all_assignment <- unlist(strsplit(paths,'_'))[seq(1,length(paths)*3,3)]
outputPath <- './data_xgboost_v1/'
output_paths <- paste0(outputPath,paths,sep='')
paths <- paste0(inputPath,paths,sep='')
length_ass <- length(all_assignment)
for ( i in 1:length_ass){
    data <- read.csv(paths[i])
    for(j in 2:8){
        data[,j]<- paste0(j-2,':',data[,j])
    }
    write.table(data,output_paths[i],sep=' ',col.names = F,row.names = F,quote = F, fileEncoding = 'UTF-8')
}


inputPath <- './pred_data_v3/'
paths <- list.files(inputPath)
all_assignment <- unlist(strsplit(paths,'_'))[seq(1,length(paths)*2,2)]
Encoding(all_assignment)<- "UTF-8"
outputPath <- './format_input_test/'
output_paths <- paste0(outputPath,paths,sep='')
merge_paths <- paste0('merge_',paths)
merge_paths <- paste0(outputPath,merge_paths)
paths <- paste0(inputPath,paths,sep='')
length_ass <- length(all_assignment)

for ( i in 1:length_ass){
    data <- read.csv(paths[i])
    data$CSPL_RECEIVED_CALLS <- 0
    # merge_data <- data[,c(2,6)]
    # merge_data$hour_index<-round(merge_data$hour_index*48)
    # write.csv(merge_data,merge_paths[i],sep=' ',row.names = F,quote=F)
    data <- data[,c(1,3:21)]
    for(j in 2:20){
        data[,j]<- paste0(j-2,':',data[,j])
    }
    write.table(data,output_paths[i],sep=' ',col.names = F,row.names = F,quote = F)
}