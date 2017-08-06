### Program used to prepare raw data for machine language training
### Includes functions to covert cyclic data and standardize continuous data
### Has classifiers for binary comparisons and time delays for outputs
### Input data file cannot have text headers!
### 16 May 2017 Brian Freeman

import time
import pandas as pd
from pandas import ExcelWriter
import numpy as np
import os
import copy
from sklearn import preprocessing

def load_file(datafile,worksheet=0):
### - Load data from excel file function
### Should not have any index on first column, but if it does, will be col 0
### First row should be column headers

    #### Start the clock
    start = time.clock()   
    
    data_fil = pd.read_excel(datafile, 
                sheetname=worksheet, 
                header=0,         #assumes 1st row are header names
                skiprows=None, 
                skip_footer=0, 
                index_col=None, 
                parse_cols=None, #default = None
                parse_dates=False, 
                date_parser=None, 
                na_values=None, 
                thousands=None, 
                convert_float=True, 
                has_index_names=None, 
                converters=None, 
                engine=None)
    # stop clock
    end = time.clock() 
    
    if (end-start > 60):
        print "Data loaded in {0:.2f} minutes".format((end-start)/60.)
    else:
        print "Data loaded in {0:.2f} seconds".format((end-start)/1.)
    
    data = data_fil.fillna(0.).values #convert all NaN to 0. and converts to np.matrix
    
    return data 

def cleanzero(X):
#convert low values to zero
    
    limit = 10e-6  #set limit where less than = 0
    
    Clean = (np.absolute(X) > limit) + 0.  #create vector of 1's and 0's
    Xclean = np.multiply(X,Clean) #elementwise multiply to convert low limits to 0
    
    return Xclean   
                
def makedata():
################### Load raw data from Excel file
    #### if True, save data to file, otherwise don't

    # Put training data file in the same folder as py code but if not, set path
    newpath = 'c:\\\TARS\PhD\Keras'   #example input path
    os.chdir(newpath) 
    ########### Set name of data file
    data_file_name = "raw-trim.xlsx"  #example input file
    print "Loading raw data file:", data_file_name, "\n"

    #Excel WorkSheet 0 = input X data, WorkSheet 1 = input Y data

    XDataSheet = 0

    #load data for processing
    X = load_file(data_file_name,XDataSheet)
    return X
    
def SaveFile(Xtrain, Ytrain, Xverify, Yverify, Xtest, Ytest, SaveData, File):
#################### Save converted data into new Excel file    
    newpath = 'c:\\\TARS\PhD\Keras'   #example output path
    
    if SaveData == True:
    # save files to output file
        filename = File + '.xlsx'    #example output file
        writer = ExcelWriter(filename)
        pd.DataFrame(Xtrain).to_excel(writer,'InputTrain')
        pd.DataFrame(Ytrain).to_excel(writer,'OutputTrain')
        pd.DataFrame(Xverify).to_excel(writer,'InputVerify')
        pd.DataFrame(Yverify).to_excel(writer,'OutputVerify')
        pd.DataFrame(Xtest).to_excel(writer,'InputTest')
        pd.DataFrame(Ytest).to_excel(writer,'OutputTest')
        print'File saved in ', newpath + '\\' + filename
    return
############################### Start Executing 
##### Call data 

start = time.clock()
        
Xt = makedata()
