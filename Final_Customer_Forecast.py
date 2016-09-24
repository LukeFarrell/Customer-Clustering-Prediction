import csv
from sklearn import svm
import sys
import warnings
sys.path.insert(0, '/Users/lukefarrell/Desktop/Customer_Forecasting')
import Final_Customer_Hyper_Clustering as Clustering
from sklearn.preprocessing import StandardScaler
import time as time
import numpy as np
from numpy import average
import matplotlib.pyplot as plt

ClusterScore = {}


#---------------------------------------------- Extract or Collect the Customer Data & save to a Final CSV -------------------------------------------

def DataWriter(ExtractNew,numClusters, EventPlot, ColorPlot):
	#Run Clustering Algorithm Layer
    a = Clustering.KClustering(ExtractNew,numClusters, EventPlot, ColorPlot)
    #Assign each return to its proper name
    MasterDict = a[0]
    ClassificationDict = a[1]
    TestDict = a[2]
    print ""
    print "Writing Files  :"
	#Save Training Data to a CSV (named based on number of Clusters used)
    data = [["Customer", "Cluster", "Future Total", "Past CLV", "LifeTime","Num Vists", "Avg Trans Price", "Total Past Spending", "Avg Num Products", "Avg Prod Price"]]
    for customer in ClassificationDict:
        data.append([customer, ClassificationDict[customer], MasterDict[customer]["CLV"][0], MasterDict[customer]["CLV"][1], MasterDict[customer]["CLV"][2], MasterDict[customer]["CLV"][3],MasterDict[customer]["CLV"][4],MasterDict[customer]["CLV"][5],MasterDict[customer]["CLV"][6],MasterDict[customer]["CLV"][7]])
        MasterDict[customer]["Cluster Number"] = ClassificationDict[customer]
    with open("C:\Users\Luke Farrell\Desktop\ClusterFiles\TrainCLV"+str(numClusters)+".csv", "w") as f:
        b = csv.writer(f, delimiter=',')
        b.writerows(data)
		
	#Save Testing Data to a CSV (name based on number of Clusters used)
    Testdata = [["Customer", "Cluster", "Future Total", "Past CLV", "LifeTime","Num Vists", "Avg Trans Price","Total Past Spending", "Avg Num Products", "Avg Prod Price"]]
    for customer in TestDict:
        Testdata.append([customer, TestDict[customer], MasterDict[customer]["CLV"][0], MasterDict[customer]["CLV"][1], MasterDict[customer]["CLV"][2], MasterDict[customer]["CLV"][3],MasterDict[customer]["CLV"][4],MasterDict[customer]["CLV"][5],MasterDict[customer]["CLV"][6],MasterDict[customer]["CLV"][7]])
        MasterDict[customer]["Cluster Number"] = TestDict[customer]
    with open("C:\Users\Luke Farrell\Desktop\ClusterFiles\TestCLV"+str(numClusters)+".csv", "w") as f:
        b = csv.writer(f, delimiter=',')
        b.writerows(Testdata)

    #Pass on the Master Dictionary
    return MasterDict
#---------------------------------------------- Function plots Actual Values vs Predicted values -------------------------------------------

def plotValues(PredictY, TestY):
    #Plot the Actual Values as green circles
    plt.plot(TestY, 'go')
    #Plot the Predicted Values as red Xs
    plt.plot(PredictY,'r+')
    #Plot the graph
    plt.show()
    #Required for proper exiting on Windows click anywhere on the image (On Mac just x out of the image)
    # plt.waitforbuttonpress()
    # plt.close()

#-------------------------------------------------- Main Method that Builds SVMs & Does Analysis ------------------------------------------------

def ClusterModeling(ExtractNew, numClusters, WriteNew, EventPlot, ColorPlot, plotResults, TestClusters):    
    MasterDict = 0
    start = time.time()
    #Intialize Cluster Scoring
    plt.close()
    global ClusterScore
    ClusterScore[numClusters] = []

	#If the New CSVs arent Written or for dif num of Clusters Run Clustering Again & Store Data
    if WriteNew == True:
        MasterDict = DataWriter(ExtractNew, numClusters, EventPlot, ColorPlot)
    else:
        pass

	#Extract all the Final Data from CLV file
    #Create Training Sets of Data
    print "Extracting Files :"
    TrainCLVcsv = np.genfromtxt ('C:\Users\Luke Farrell\Desktop\ClusterFiles\TrainCLV'+str(numClusters)+".csv", delimiter=",")
    Clusters = TrainCLVcsv[:,1][1:]
    CustomerIDs = TrainCLVcsv[:,0][1:]
    TrainY = TrainCLVcsv[:,2][1:]  #Must be next 12 months of spending total
    TrainX = TrainCLVcsv[:,3:][1:] #Must be the present 12 Monthss
    
    #Create Testing Sets of Data
    TestCLVcsv = np.genfromtxt ('C:\Users\Luke Farrell\Desktop\ClusterFiles\TestCLV'+str(numClusters)+".csv", delimiter=",")
    TestCustomers = TestCLVcsv[:,0][1:]
    TClusters = TestCLVcsv[:,1][1:]
    TestY = TestCLVcsv[:,2][1:]  #Target Values of the 12 months of spending total
    TestX = TestCLVcsv[:,3:][1:] #Input Values of the Customer's History
    
    #Begin Looping through each Cluster Seperately
    TestDict = {}
    AvgScore = []
    for Z in TestClusters:
        print ""
        print "CLUSTER", str(Z), "SUMMARY:"
		#Initialize Cluster Data Lists
        cluster1X = []
        TrainYCluster1 = []
        Test1X = []
        Test1Y = []
        AverageSpending = []
        AverageLT = []
        TestCustomerID = []
		#Divide out only the Cluster of Interest
        #Collect the Training Set 
        for index in range(0,len(Clusters)):
            if Clusters[index] == Z-1:
                cluster1X.append(TrainX[index])
                TrainYCluster1.append(TrainY[index])
                AverageSpending.append(TrainX[index][3])
                AverageLT.append(TrainX[index][1])
        
        #Collect the Testing Set
        for index in range(0,len(TClusters)):
            if TClusters[index] == Z-1:
                Test1X.append(TestX[index])
                Test1Y.append(TestY[index])
                TestCustomerID.append(TestCustomers[index])

        #Sclae Values for each cluster
        if len(cluster1X) > 1 and len(Test1X) > 1:
            Scaler = StandardScaler()
            Scaler.fit(cluster1X)
            TrainXCluster1 = Scaler.transform(cluster1X)
            TestXCluster1 = Scaler.transform(Test1X)
            
            TrainXCluster1 = np.ndarray.tolist(TrainXCluster1)
            TestXCluster1 = np.ndarray.tolist(TestXCluster1)

            #Fit the Support Vector Machine Linear Regressor to the Train Data
            Modeling = svm.LinearSVR()
            Modeling.fit(TrainXCluster1, TrainYCluster1)
            TestValues1 = []
            warnings.filterwarnings("ignore", category=DeprecationWarning) 

            #Test the  finished model on the Test Data and Make Predictions
            for x in range(len(TestXCluster1)):
                p = Modeling.predict(TestXCluster1[x])[0]
                TestValues1.append(p)

            #Do analysis on how good the model is
            Error = []
            Score = Modeling.score(TestXCluster1,Test1Y)
            ClusterScore[numClusters].append(Score)
            AvgScore.append(Score)
            PercentError = []

            #Create a test dictionary for plotting later
            for x in range(len(TestValues1)):
                TestDict[TestCustomerID[x]] = [Z, TestValues1[x], Test1Y[x]]

                #Calculate the Error on Predicions
                Error.append(abs(TestValues1[x]-Test1Y[x]))
                if Test1Y[x] != 0:
                    PercentError.append(100*(abs((Test1Y[x]-TestValues1[x])/Test1Y[x])))

            #Print out Results from the Clustering
            print 'Number of Customers               :  ' , len(Test1X), "customers"
            print 'LifeTime                          :  ' , round(average(AverageLT),2), "days"
            print 'Average Past Spending             : $' , round(average(AverageSpending),2)
            print 'Average Future Spending           : $' , round(average(TrainYCluster1),2)
            print 'Deviation of Future Spending      : $' , round(np.std(TrainYCluster1),2)
            print 'Average Error                     :  ' , round(average(Error),2)
            print 'Percent Error                     :  ' , round(average(PercentError),2) , "%"
            print 'FINESS SCORE                      :  ' , Score
            
            #Call the Plot Actual vs Prediction Function
            if plotResults == True:
                plotValues(TestValues1, Test1Y)
            else:
                pass
        
        #In case the cluster is too small to create a model create an exception
        else:
            print "Error : Cluster Too Small"
            pass
    a = FinalPlot(TestDict,AvgScore)

    end= time.time()
    print ""
    print "Total Time: ", round((end - start)/60,2), "Minutes"
    if MasterDict != 0:
        return MasterDict
	
#---------------------------------------------- Extract or Collect the Customer Data & save to a Final CSV -------------------------------------------

def FinalPlot(TestDict,AvgScore):
    #Instantiate more Analysis
    Cluster = []
    Prediction = []
    Actual = []
    Error = []
    Error2 = []   
    Error3 = []
    Blank = []
    index = 0
    #Create Overall results across all the Clusters
    for customer in TestDict:
        Cluster.append(TestDict[customer][0])
        Prediction.append(TestDict[customer][1])
        Actual.append(TestDict[customer][2])
        Error.append(TestDict[customer][1]-TestDict[customer][2])
        Error2.append(abs(TestDict[customer][2]-TestDict[customer][1]))
        if TestDict[customer][2] != 0:
            E = 100*(abs(TestDict[customer][2]-TestDict[customer][1])/abs(TestDict[customer][2]))
            if E < 10e10:
                Error3.append(E)
                Blank.append(index)
                index+=1

    #Print Overall Results 
    print ""
    print "OVERALL RESULTS:"
    print "Overall Average Error      : ", average(Error2)
    print "Overall Standard Deviation : ", np.std(Error2)
    print "Overall Percent Error      : ", average(Error3)
    print "Overall Model Score        : ", average(AvgScore)

    #Plot All the Errors and Color them based on their Cluster Identity

#----------------------------------------------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
	#Start Timer
    start = time.time()
    ErrorList = []
    ScoreList = []
    PercentList = []
    DeviationList = []
    #Plot the Customers & Their Info (Write New must be True in order for Plot Clusters to be True)
    EventPlot = False
    #Plot Cluster Classifiction (Write New must be True in order for Plot Clusters to be True)
    ColorPlot = True
    #Write a New file
    WriteNew = False
    #Intialize Number of Customers to Extract (If all = 10e36)
    ExtractNew = False
    #Intialize the number of Customer Clusters 
    numClusters = 8
    #Plot Test Results for each Cluster
    plotResults = False
    #A list of Clusters you want to Test (max = NumClusters)
    TestClusters = [x for x in range(1,numClusters+1)]
    #Call the Clustering Function
    a = ClusterModeling(ExtractNew, numClusters, WriteNew, EventPlot, ColorPlot, plotResults, TestClusters)
    #End Timer
    end= time.time()
    
    print ""
    print "Total Time: ", round((end - start)/60,2), "Minutes"
	

