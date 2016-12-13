# Poll for All Songs Considered

The data comes from the All Songs Considered listener poll that asks listener for their favourite album in 2016. 
The survey data and the final ranking can be found here: https://docs.google.com/spreadsheets/d/1PWiRGDG1GlBFXfcwMRunZQqWEQa-XltlEBhUpaVNcv4/edit#gid=2123144803


### The Way to Delicious Ranking Data: 

1 . Export the poll data as a csv and transform it into a long format in R with this command: 
```
library(reshape2)
d = read.csv("data.csv",stringsAsFactors = FALSE)
d = melt(d,id.vars = c('Timestamp'))
```

2 . Clean it up in OpenRefine (`Text Facet` > `Clusters`)

3 . Clean it up a bit more by hand in Google Spreadsheet, to have the same Artist-Album-Combination for cases like "Rihanna, Anti" and "Anti" and "Rihanna"

4 . Convert the data back to a wide format in Google Spreadsheet and export it as csv.

5 . Run the `BestAlbumsCleaner.py`. The Python script does the following:
- Remove duplicate lines if the appear within an hour 
- Remove complete empty entries
- Remove lines in which the same artist was mentioned in all five entry fields. 

6 . Run the `161217_RankingAlbums.R` script. The R script does the following: 
- Convert the data from a wide format into a long format
- Assigns a weighting value to each rank and sums these values up for each album per day. 
- Gives back a ranking for the most voted albums per day. If an album was not mentioned at a certain day, the album gets the ranking "200".
- Exports it as a wide format as a csv

7 . Upload that csv to Google Spreadsheet and sum up the individual rankings per day. 

Aaaaaand you made it. 
Ready is the ranking for the All Songs Considered Listener Poll. 
