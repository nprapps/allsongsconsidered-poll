library(reshape2)
library(dplyr)

# set working directory
setwd("Desktop")

# load csv
d = read.csv("NPR_BestAlbums - afterPythonScript.csv",stringsAsFactors = FALSE)

# rename columns and delete some
d$X = NULL
d$smelly = NULL
d$Unnamed..0=NULL

# transform from wide format to long format 
d = melt(d,id.vars = c('Timestamp'))

# rename some more columns and delete some more
d$rank = d$variable
d$variable = NULL
d$album = d$value
d$value = NULL
d$X = NULL

# convert rank from factor to character
d$rank = as.character(d$rank)

# replace the rank description with the rank points
d$rank[d$rank=="Rank.1"]= 5
d$rank[d$rank=="Rank.2"]= 4
d$rank[d$rank=="Rank.3"]= 3
d$rank[d$rank=="Rank.4"]= 2
d$rank[d$rank=="Rank.5"]= 1

# convert rank from character to numeric
d$rank = as.numeric(d$rank)

# get only the first five characters of the timestamp (day and month)
d$Timestamp = substr(d$Timestamp,1,5)

# sum up the rank points for each album on each day 
d = d %>% 
  group_by(Timestamp,album) %>%
  summarise(points = sum(rank))

# get rid of the summed up rank points for empty entries 
d[d==""] <- NA
d <- na.omit(d)

# sort by rank points for each day, then give it a rank number 
d = d %>% 
  arrange(Timestamp, -points, album) %>%
  group_by(Timestamp) %>%
  mutate(rank=row_number())

# transform from long format into wide format
d_wide <- dcast(d, album ~ Timestamp)

# replace all NA values with the value 200
d_wide[is.na(d_wide)] <- 200

# write the CSV 
write.csv(d_wide,"RankPerDay.csv")


