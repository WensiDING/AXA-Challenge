paths <- paste0('./rawdata/',all_assignment,sep='')
paths <- paste0(paths,'_dataset.csv',sep='')
length_ass <- length(all_assignment)

path_finaldata <- paste0('./finaldata/',all_assignment,sep='')
path_finaldata <- paste0(path_finaldata,'_dataset.csv',sep='')


path_data_v1 <- paste0('./data_v1/',all_assignment,sep='')
path_data_v1 <- paste0(path_data_v1,'_dataset_v1.csv',sep='')

path_data_v2 <- paste0('./data_v2/',all_assignment,sep='')
path_data_v2 <- paste0(path_data_v2,'_dataset_v2.csv',sep='')

path_data_v3 <- paste0('./data_v3/',all_assignment,sep='')
path_data_v3 <- paste0(path_data_v3,'_dataset_v3.csv',sep='')


for (l in 1:length_ass){

    tech_axa_data <- read.csv(paths[l]) 
    
    # dealing with na
    
    # for( i in 1:length(tech_axa_data[,1])){
    #     if (is.na(tech_axa_data[i,8])){
    #         year <- tech_axa_data[i,3]
    #         month <- tech_axa_data[i,4]
    #         weekday <- tech_axa_data[i,6]
    #         hour <- tech_axa_data[i,7]
    #         tech_axa_data[i,8]<- mean(tech_axa_data[((tech_axa_data$myyear==year) & (tech_axa_data$mymonth==month) & (tech_axa_data$DAY_WE_DS==weekday) & (tech_axa_data$hour_index==hour)),8],na.rm=T)
    #         }
    # }
    tech_axa_data$mydate <- as.Date(tech_axa_data$mydate)
    tech_axa_data[is.na(tech_axa_data[,8]),8] <- 0
    
    # column for recording the recieved call numbers of the same hour seven days ago 
    # and of the same day seven days ago
    day_summary <- aggregate(CSPL_RECEIVED_CALLS~mydate,data=tech_axa_data,FUN = sum)
    tech_axa_data$samehour_sevendays <- NA
    tech_axa_data$sameday_sevendays <- NA
    for( i in 1:length(tech_axa_data[,1])){
        if(sum(tech_axa_data$mydate==(tech_axa_data$mydate[i]-7))!=0){
            row1 <- which((tech_axa_data$mydate==(tech_axa_data$mydate[i]-7)) & (tech_axa_data$hour_index==tech_axa_data$hour_index[i]))
            tech_axa_data$samehour_sevendays[i] <- tech_axa_data$CSPL_RECEIVED_CALLS[row1]
            row2 <- which(day_summary$mydate==(tech_axa_data$mydate[i]-7))
            tech_axa_data$sameday_sevendays[i] <- day_summary[row2,2]
        }
    }
    
    # column for recording the recieved call numbers of last week average
    tech_axa_data$last_week <- NA
    for( i in 1:length(tech_axa_data[,1])){
        weekday_num <- tech_axa_data$DAY_WE_DS[i]
        date <- tech_axa_data$mydate[i]-7-weekday_num+1
        week_calls <- rep(NA,7)
        for(j in 0:6){
            check <- sum(day_summary$mydate==(date+j))
            if (check == 0){
                week_calls[j+1] <- NA
            }else{
                week_calls[j+1] <- day_summary$CSPL_RECEIVED_CALLS[day_summary$mydate==(date+j)] 
            }
        }
        tech_axa_data$last_week[i] <- mean(week_calls,na.rm = T)
    }
    
    # column for recording the recieved call numbers of last month average
    tech_axa_data$last_month <- NA
    month_summary <- aggregate(cbind(CSPL_RECEIVED_CALLS,rep(1,length(myyear)))~myyear+mymonth,data=tech_axa_data,FUN = sum)
    month_summary$CSPL_RECEIVED_CALLS <- month_summary$CSPL_RECEIVED_CALLS/(month_summary$V2/48)
    for (i in 2:36){
        year <- as.integer((i-2)/12)
        row1 <- which(month_summary$myyear==(2011+year) & month_summary$mymonth==(i-1-12*year))
        result <- month_summary$CSPL_RECEIVED_CALLS[row1] 
        year <- as.integer((i-1)/12)
        tech_axa_data$last_month[(tech_axa_data$myyear== (2011+year)) & (tech_axa_data$mymonth == (i-12*year))] <- result
    }
    # output the final data
    tech_axa_data <- tech_axa_data[,c(8,2,3,4,5,6,7,9,10,11,12)]
    write.csv(tech_axa_data,path_finaldata[l],row.names = F)
    
    # output the first version dataset
    v1 <- tech_axa_data[! is.na(tech_axa_data$samehour_sevendays),]
    v1 <- v1[,c(1,4,5,6,7,8,9,10)]
    v1$mymonth <- v1$mymonth/12
    v1$myday <- v1$myday/31
    v1$DAY_WE_DS <- v1$DAY_WE_DS/7
    v1$hour_index <- v1$hour_index/48
    maxs <- apply(v1[,c(6,7,8)],2,max)
    mins <- apply(v1[,c(6,7,8)],2,min)
    ranges <- maxs - mins
    v1[,c(6,7,8)] <- sweep(v1[,c(6,7,8)],2,mins,'-')
    v1[,c(6,7,8)] <- sweep(v1[,c(6,7,8)],2,ranges,'/')
    write.csv(v1,path_data_v1[l],row.names = F)
    # output the second version dataset
    v2<-v1
    v2$mymonth1 <-sin(v2$mymonth*pi)
    v2$mymonth2 <-cos(v2$mymonth*pi)
    v2$myday1 <- sin(v2$myday*pi)
    v2$myday2 <- cos(v2$myday*pi)
    v2$DAY_WE_DS1 <-sin(v2$DAY_WE_DS*pi)
    v2$DAY_WE_DS2 <-cos(v2$DAY_WE_DS*pi)
    v2$hour_index1 <- sin(v2$hour_index*pi)
    v2$hour_index2 <- cos(v2$hour_index*pi)
    v2<-v2[,c(1,6:16)]
    
    write.csv(v2,path_data_v2[l],row.names = F)
    
    # output the third version dataset
    v3<-v1
    v3$mymonth2<-v3$mymonth^2
    v3$mymonth3<-v3$mymonth^3
    v3$mymonth4<-v3$mymonth^4
    v3$myday2<-v3$myday^2
    v3$myday3<-v3$myday^3
    v3$myday4<-v3$myday^4
    v3$DAY_WE_DS2<-v3$DAY_WE_DS^2
    v3$DAY_WE_DS3<-v3$DAY_WE_DS^3
    v3$DAY_WE_DS4<-v3$DAY_WE_DS^4
    v3$hour_index2<-v3$hour_index^2
    v3$hour_index3<-v3$hour_index^3
    v3$hour_index4<-v3$hour_index^4
    
    write.csv(v3,path_data_v3[l],row.names = F)
    rm(day_summary)
    rm(month_summary)
    rm(tech_axa_data)
    rm(v1)
    rm(v2)
    rm(v3)
}
