"""
Created on Tue Sept 14:40:01 2016

@author: Luke Farrell
"""

import Final_Customer_Forecast as MasterProgram

#If you want to extract a new Master Dictionary (Must be True First Time running the Pogram)
ExtractNew = False

#Intialize the number of Customer Clusters 
numClusters = 8

#Write the Clustering Calculations to a New File (Must be True First Time running the program & for all new number of clusters)
WriteNew = True

#Plot the 3D Cluster Events (No coloring but has customer click functionality)(Write New must be True in order for Plot Clusters to be True)(VERY SLOW)
EventPlot = False

#Plot Cluster Classifiction (Has coloring based on customer cluster identiy)(Write New must be True in order for Plot Clusters to be True)(Recommended)
ColorPlot = True

#Plot Test Results for each Cluster 
plotResults = True

#A list of Clusters you want to Test (Usually just all of them (dont need to change))
TestClusters = [x for x in range(1,numClusters+1)]

#Call the Final Function
MasterProgram.ClusterModeling(ExtractNew, numClusters, WriteNew, EventPlot, ColorPlot, plotResults, TestClusters)


#------------------Intructions-------------------------#
#At first run it with Extract New = False bc I uploaded the premade dictionary
	#This will allow you to see the program run all the way through (hopefully)

#If you want to Extract New Data you have to change the File Names & Possibly the csv headers in Final_Data_Extractor.py to the ones on your computer
	#Try Running it then, if it doesnt work it probably broke during the CLV calculations in Final_Data_Extractor.py (hopefully not)
	#It should take a little bit to extract all the data, the time break down is in the Results papers I sent 

#The event plot takes a long ass time (like over 15-20 minutes) so only do it once or twice if you're interested

#If you want to look at the customer plots more directly feel free to go into Final_Customer_Hyper_Clustering.py and just run the code from there.
#It should just make which ever plot you choose

