
# IMPORT STUFF
# ------------

import csv
import pandas as pd
import datetime
import numpy as np




# PREPARE THE ARTICLES PER DAY 
# ----------------------------

# load a CSV 
# create a new header and delete the old one (plus one or two super old dates)
albums = pd.read_csv("Vote For 2016's Best Albums (Responses) - Form Responses 1.csv")

#convert to datetime format (from object to dattime64)
albums["Timestamp"] = pd.to_datetime(albums["Timestamp"])


# check if row is empty, the n remove 
albums = albums.dropna(subset=["Rank 1","Rank 2", "Rank 3", "Rank 4", "Rank 5"])

# remove duplicates within next ten rows 
for i in range(0,len(albums.index)):
	for j in range(i, i+10):
		albums = albums.drop_duplicates(subset=["Rank 1","Rank 2", "Rank 3", "Rank 4", "Rank 5"], keep='last')
		# print i
	
	# check if every column in a row has the some album, then remove 
	if albums.at[i,"Rank 1"] == albums.at[i,"Rank 2"] == albums.at[i,"Rank 3"] == albums.at[i,"Rank 4"] == albums.at[i,"Rank 5"]:
		# print albums.at[i,"Rank 2"]
		print albums.at[i,"Rank 2"]
		albums.replace(albums.at[i,"Rank 2"],np.nan) 
		# print albums.at[i,"Rank 2"]
	

# albums.to_csv('finaltable.csv')






print albums.at[i,"Timestamp"]
while current timestamp is earlier than current timestamp + 5min
iplustime = albums.at[i, "Timestamp"]+datetime.timedelta(minutes=5)
print iplustime
for j in range(i, iplustime)
while albums.at[i, "Timestamp"] <= albums.at[i, "Timestamp"]+datetime.timedelta(minutes=5):
	# remove duplicates 
	print albums.duplicated(subset=["Rank 1","Rank 2", "Rank 3", "Rank 4", "Rank 5"]) == True: 
		
		albums.drop(row)

for i in range(1,len(albums.index)):
	while albums.at[i, "Timestamp"] <= albums.at[i, "Timestamp"]+datetime.timedelta(minutes=5):
		print albums.duplicated(subset=["Rank 1","Rank 2", "Rank 3", "Rank 4", "Rank 5"])
			# print "true"
			# albums.drop(row)



# print type(albums)
# print albums["Timestamp"]
 


