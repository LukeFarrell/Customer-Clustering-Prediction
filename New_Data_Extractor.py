from collections import Counter
import numpy as np
import heapq
import csv
import time as time
import multiprocessing as mp
import os
import sys

def TransData(NumCustomer):
	#Pull Data from Retail CSV
    TransDict = {}
    TransList= {}
	#2011 Retail Data for TrainX
    with open('C:\Users\Luke Farrell\Google Drive\Luke - Shared\Jaeger\JAEG_2011_AdhocTransactionHeaders_DT20160304_T1059_CT365501.csv', 'rb') as retailCsv:
        retailDict = csv.DictReader(retailCsv)
        for row in retailDict:
            if row['CustomerId'] not in TransDict:
                TransDict[row['CustomerId']] = {}
                transaction = "transaction1"
                TransDict[row['CustomerId']][transaction] = [row['TotalTransValue'], row['Quantity'], row['SalesAssociateName'], row['TransDateTime']]
                TransList[row['CustomerId']] = 0
            else:
                TransList[row['CustomerId']] += 1
                transaction = "transaction" + str(TransList[row['CustomerId']])
                TransDict[row['CustomerId']][transaction]= [row['TotalTransValue'], row['Quantity'], row['SalesAssociateName'], row['TransDateTime']]
            if len(TransDict) > NumCustomer/2:
                break
            else:
                pass
    print TransDict
    retailCsv.close()
    print "2011 Retail Extracted"
	#2010 Retail Data for TrainX
    with open('C:\Users\Luke Farrell\Google Drive\Luke - Shared\Jaeger\JAEG_2010_AdhocTransactionHeaders_DT20160304_T1136_CT388935.csv', 'rb') as retailCsv:
        retailDict = csv.DictReader(retailCsv)
        for row in retailDict:
            if row['CustomerId'] not in TransDict:
                TransDict[row['CustomerId']] = {}
                transaction = "transaction1"
                TransDict[row['CustomerId']][transaction] = [row['TotalTransValue'], row['Quantity'], row['SalesAssociateName'], row['TransDateTime']]
                TransList[row['CustomerId']] = 0
            else:
                TransList[row['CustomerId']] += 1
                transaction = "transaction" + str(TransList[row['CustomerId']])
                TransDict[row['CustomerId']][transaction]= [row['TotalTransValue'], row['Quantity'], row['SalesAssociateName'], row['TransDateTime']]
            if len(TransDict) > NumCustomer:
                break
            else:
                pass
        retailCsv.close()
        print "2010 Retail Extracted"
        return TransDict
        
def ProductData(NumCustomer):
    ProductDict = {}
    RepeatCounter = []
	#2011 Product Data
    with open('C:\Users\Luke Farrell\Google Drive\Luke - Shared\Jaeger\JAEG_2011_AdhocTransactionDetails_DT20160304_T1105_CT805591.csv', 'rb') as productCsv:
        DetailDict = csv.DictReader(productCsv)
        for row in DetailDict:
		if row['CustomerId'] not in ProductDict:
			ProductDict[row['CustomerId']] = {}
			product = "product1"
			ProductDict[row['CustomerId']][product] = [row['Product'], row['AspGBP'], row['Colour'], row['Size'], row['Type']]
		else:
			RepeatCounter.append(row['CustomerId'])
			RepeatDict=Counter(RepeatCounter)
			product = "product" + str(RepeatDict[row['CustomerId']])
			ProductDict[row['CustomerId']][product] = [row['Product'], row['AspGBP'], row['Colour'], row['Size'], row['Type']]
		if len(ProductDict) > NumCustomer/2:
			break
		else:
			pass
    productCsv.close()
    print "2011 Product Extracted"
	#2010 Product Data
    with open('C:\Users\Luke Farrell\Google Drive\Luke - Shared\Jaeger\JAEG_2010_AdhocTransactionDetails_DT20160304_T1143_CT891360.csv', 'rb') as productCsv:
        DetailDict = csv.DictReader(productCsv)
        for row in DetailDict:
		if row['CustomerId'] not in ProductDict:
			ProductDict[row['CustomerId']] = {}
			product = "product1"
			ProductDict[row['CustomerId']][product] = [row['Product'], row['AspGBP'], row['Colour'], row['Size'], row['Type']]
		else:
			RepeatCounter.append(row['CustomerId'])
			RepeatDict=Counter(RepeatCounter)
			product = "product" + str(RepeatDict[row['CustomerId']])
			ProductDict[row['CustomerId']][product] = [row['Product'], row['AspGBP'], row['Colour'], row['Size'], row['Type']]
		if len(ProductDict) > NumCustomer:
			break
		else:
			pass
    productCsv.close()
    print "2010 Product Extracted"
	#2012 Retail Data for TrainY
    results.put(ProductDict)
    return ProductDict
    
def TargetData(NumCustomer):
    customerFutureDict = {}
    with open("C:\Users\Luke Farrell\Google Drive\Luke - Shared\Jaeger\JAEG_2012_AdhocTransactionHeaders_DT20160304_T1041_CT329923.csv", 'rb') as newRetailCsv:
        newRetailDict = csv.DictReader(newRetailCsv)
        for row in newRetailDict:
		if row['CustomerId'] not in customerFutureDict:
			customerFutureDict[row['CustomerId']] = [float(row['TotalTransValue'])]
		else:
                  customerFutureDict[row['CustomerId']].append(float(row['TotalTransValue']))
		if len(customerFutureDict) > NumCustomer:
			break
		else:
			pass
    customerFuture = {k:sum(v) for k,v in customerFutureDict.items()}
    newRetailCsv.close()
    print "2012 Target Extracted"
    return customerFuture
    

def MasterData(TransDict, ProductDict, customerFuture):
	#Create Customer Lifetime Value Dictionary
	CLVDict = {}
	for customer in TransDict:
		LifeTime = 0
		TransAvgList = []
		CustomerAvgList = []
		NumProducts = []
		for trans in TransDict[customer]:
		#Calculate Avg Transaction Price
			TransAvgList.append(float(TransDict[customer][trans][0]))
		#Calculate Avg Number of Products per Purchase
			NumProducts.append(int(TransDict[customer][trans][1]))
		#Calculate LifeTime
			FirstDate = (int(TransDict[customer][trans][-1][0:4]),int(TransDict[customer][trans][-1][5:7]), int(TransDict[customer][trans][-1][8:10]))
		RecentDate = (int(TransDict[customer]["transaction1"][-1][0:4]),int(TransDict[customer]["transaction1"][-1][5:7]), int(TransDict[customer]["transaction1"][-1][8:10]))
		if len(TransDict[customer]) > 1:
				LifeTime += (RecentDate[0]-FirstDate[0])*365
				LifeTime += (RecentDate[1]- FirstDate[1])*30
				LifeTime += RecentDate[2] - FirstDate[2]
		#Calculate Avg Price per Product
		prodPrice = []
		for product in ProductDict[customer]:
			prodPrice.append(float(ProductDict[customer][product][1]))
		#Calculate total future spending for Train Y
		if customer not in customerFuture:
			FutureSpending = 0
		else:
			FutureSpending = customerFuture[customer]
		NumVisits = len(TransDict[customer])
		AverageSpent = round(np.average(TransAvgList),4)
		AvgNumProducts = np.average(NumProducts)
		AvgProdPrice = np.average(prodPrice)
		CLV = NumVisits * AverageSpent
		CustomerAvgList.append(FutureSpending)
		CustomerAvgList.append(CLV)
		CustomerAvgList.append(LifeTime)
		CustomerAvgList.append(NumVisits)
		CustomerAvgList.append(AverageSpent)
		CustomerAvgList.append(AvgNumProducts)
		CustomerAvgList.append(AvgProdPrice)
		CLVDict[customer] = CustomerAvgList
	print "" 
	#Create Master Searchable Dictionary with all Information
	MasterDict = {}
	for customer in TransDict:
		MasterDict[customer] = {}
		MasterDict[customer]["Product History"] = ProductDict[customer]
		MasterDict[customer]["Transaction History"] = TransDict[customer]
		MasterDict[customer]["CLV"] = CLVDict[customer]
	#Return The Master Dictionary with all the Information
	print "Data Extraction Finished"
	np.save('MasterDict.npy', MasterDict) 
	return MasterDict

def Data(NumCustomers):
#    start = time.time()
#    results = mp.Queue()
#    jobs = []
#    p1 = mp.Process(target = TransData, args = (NumCustomers,results))
#    jobs.append(p1)
#    p1.start()
#    p2 = mp.Process(target = ProductData, args = (NumCustomers,results))
#    jobs.append(p2)
#    p2.start()
#    p3 = mp.Process(target = TargetData, args = (NumCustomers,results))
#    jobs.append(p3)
#    p3.start()
#    
#    resultsList = []
#    for x in range(len(jobs)):
#        resultsList.append(results.get())
#        
#    for process in jobs:
#        process.join()
#        
#    end = time.time()
#    print end-start
    a = TransData(NumCustomers)
    b = ProductData(NumCustomers)
    c = TargetData(NumCustomers)
    return MasterData(a,b,c)
    







#################################################################################


if __name__ == '__main__':
#Intialize the Numer of Customers you want to extract
#    start = time.time()    
    NumCustomers =100
    Data(NumCustomers)
#    pool = mp.Pool()
#    
#    p1 = pool.map_async(TransData1, (NumCustomers,))
#    p2 = pool.map_async(ProductData1, (NumCustomers,))
#    p3 = pool.map_async(TargetData1, (NumCustomers,))
#    
#    MasterData(p1.get()[0],p2.get()[0],p3.get()[0])
#    end = time.time()
#    print end- start
#    
#    results = mp.Queue()
#    start = time.time()
#    a = TransData(NumCustomers,results)
#    b = ProductData(NumCustomers,results)
#    c = TargetData(NumCustomers,results)
#    MasterData(a,b,c)
#    end = time.time()
#    print end - start 
##    
#    start = time.time()
#    results = mp.Queue()
#    jobs = []
#    p1 = mp.Process(target = TransData, args = (NumCustomers,results))
#    jobs.append(p1)
#    p1.start()
#    p2 = mp.Process(target = ProductData, args = (NumCustomers,results))
#    jobs.append(p2)
#    p2.start()
#    p3 = mp.Process(target = TargetData, args = (NumCustomers,results))
#    jobs.append(p3)
#    p3.start()
#    
#    resultsList = []
#    for x in range(len(jobs)):
#        resultsList.append(results.get())
#        
#    for process in jobs:
#        process.join()
#    
#    MasterData(resultsList[1], resultsList[2], resultsList[0])
#    
#    end = time.time()
#    print end-start