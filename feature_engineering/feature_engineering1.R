
library(data.table)

# function to calculate hour index
hour_index <- function(date){
    hour = as.numeric(substr(date,12,13))
    minute = as.numeric(substr(date,15,16))
    minute <- ifelse(minute==0,1,2)
    return (hour*2+minute)
}

# load databrute
data <- read.csv('./databrute.csv',colClasses = c('character','NULL','character','NULL','NULL','factor',rep('integer',3)))
data$mydate <- as.Date(data$DATE)
data$hour_index <- hour_index(data$DATE)

# load submission
submission <- fread("./submission.txt",colClasses = c('character','character','NULL'))
submission$mydate <- as.Date(submission$DATE)
dates <- unique(submission$mydate)

# initialise res
data_dates <- data$mydate[order(data$mydate)]

all_dates <- seq(from = data_dates[1], to = data_dates[length(data_dates)], by = "days")

rm(data_dates)

all_hour_index <- seq(1,48)

all_assignment <- levels(data$ASS_ASSIGNMENT)
    
res<- expand.grid(all_dates,all_hour_index,all_assignment)

colnames(res)=c('mydate','hour_index','ASS_ASSIGNMENT')

# aggregate databrute
agg_data <- aggregate(CSPL_RECEIVED_CALLS~mydate+hour_index+ASS_ASSIGNMENT,data=data,sum)

res <- merge(res,agg_data,all.x = T)

# get weekday
weekday <- data[,c('DAY_WE_DS','mydate')]
weekday <- unique(weekday)
weekday$DAY_WE_DS <- factor(weekday$DAY_WE_DS, levels=c('Lundi','Mardi','Mercredi','Jeudi','Vendredi','Samedi','Dimanche'))
weekday$DAY_WE_DS <- as.numeric(weekday$DAY_WE_DS)
res <- merge(res,weekday,all.x=T)

# get month and day number
res$mymonth <- month(res$mydate)
res$myday <- as.numeric(format(res$mydate,'%d'))
res$myyear <- year(res$mydate)

# missing values summary
weekday_NA <- as.numeric(rep(NA,7))
for (i in 1:7){
   weekday_NA[i]= sum(is.na(res[res$DAY_WE_DS==i,4]))
}

assignment_NA <-  as.numeric(rep(NA,28))
for (i in 1:28){
    assignment_NA[i]= sum(is.na(res[res$ASS_ASSIGNMENT==all_assignment[i],4]))
}

# write out raw datasets
Encoding(all_assignment)<- "UTF-8"
paths <- paste0('./rawdata/',all_assignment,sep='')
paths <- paste0(paths,'_dataset.csv',sep='')
for (i in 1:28){
    subset <- res[res$ASS_ASSIGNMENT==all_assignment[i],]
    subset <- subset[order(subset$hour_index,subset$DAY_WE_DS,subset$mydate),]
    subset <- subset[,c(3,1,8,6,7,5,2,4)]
    write.csv(subset,paths[i],row.names = F)
}

