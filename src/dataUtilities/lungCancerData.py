'''
Created on Apr 12, 2020

@author: Andrew Davidson
aedavids@ucsc.edu
'''
import logging
import pandas as pd
from pathlib import Path 
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import StratifiedShuffleSplit

########################################################################
class LungCancerData():
    '''
    Assumes TCGA has already been cleaned
    
    This class splits the data into training sets, and labels it lung cancer or not lung cancer
    The resulting data sets are cached on disk. 
    
    this class holds onto a lot of memory
    
    To get machine learning data sets call
        loadTrainData(self, randomSeed)
            self.XTrainNP, self.yTrainSeries (i.e. numpy array,  and pandas series)
        
        loadTestData(self, randomSeed)
            self.XTestNP, selfyTestSeries (i.e. numpy array,  and pandas series)
            
    AEDWIP If you want the encoder use labelsIntoNumericValues()
        self.encoder (sklearn.preprocessing.LabelEncoder)
        
    If you want to get pandas data frames with the extra label column on YDF
        - delete the cache
        - call one of the load functions
        self.XDF and self.YDF will be the dataframes from the TCGA data set with extra columns
        
    If you want the clean tidy version of the TCGA data frames without the lung cancer columns
        self._loadTCGADataFrames(), self.XDF, self.YDF
        
    
    '''
    logger = logging.getLogger(__name__)

    ########################################################################
    def __init__(self, rootDataDir, TCGADataFile):
        '''
        arguments:
            rootDataDir:
                path to all data files.
                example; "~/data"
                
           TCGADataFile:
                the path to a TCGA HDFS file
                example tcga_target_gtex.h5
                        this file should be found under ./rootDataDir/tcga_target_gtex.h5
                 
                ref: https://en.wikipedia.org/wiki/Hierarchical_Data_Format                
        '''
        self.rootDataDir = Path(rootDataDir)
        self.TCGADataFile = Path("{}/{}".format(rootDataDir,TCGADataFile) )
        
        self.lungCancerData = Path("{}/lungCancerData".format(rootDataDir))
        if not self.lungCancerData.exists():
            self.logger.info("creating directory:{}".format(self.lungCancerData))
            self.lungCancerData.mkdir()
            
        self.machineLearningDataFile = Path("{}/machineLeaning.h5".format(self.lungCancerData))   

        self.XDF = None
        self.YDF = None
        self.lungCancerRows = None
        self.notLungCancerRows = None
        
        self.lungCancerLables      =   'lungCancerLables'
        self.lungCancerCategory    =   'lungCancer'
        self.notLungCancerCategory = 'notLungCancer'
        self.lungCancerLableValues =   'lungCancerLablesValues'
        
        self.XTrainNP = None 
        self.XTestNP = None
        self.yTrainSeries = None
        self.yTestSeries = None  
        

        self.encoder = None

    ########################################################################
    def _loadTCGADataFrames(self):
        '''
        loads XDF, and YDF. T
                
        returns:
        '''
        self.logger.info("BEGIN")
        
        if (self.XDF is None) or (self.YDF is None):
            if self.TCGADataFile.exists() :
                store = pd.HDFStore(self.TCGADataFile, mode="r")
                self.logger.info("store.info():{}".format(store.info()))
                self.logger.info("store.keys():{}".format(store.keys()))
            
                self.XDF = pd.read_hdf(self.TCGADataFile, "expression") # RNA Sequence data
                self.YDF = pd.read_hdf(self.TCGADataFile, "labels")
            else :
                self.logger.error("{} not found".format(self.TCGADataFile)) 
                raise FileNotFoundError(self.TCGADataFile)
        
        self.logger.info("END")
        
    ########################################################################
    def loadRowFilter(self):
        '''
        aedwip
        '''
        self.logger.info("BEGIN")        
        self._loadTCGADataFrames()
            
        lungCancerRows = self.YDF['primary_site'].str.contains('Lung', case=False)
        self.lungCancerRows = lungCancerRows
        # ~ is 'not' in pandas
        self.notLungCancerRows = ~lungCancerRows
                        
#         lcrFileName = "lungCancerRowSelectionFilters.h5"
#         if (self.lungCancerRows == None) or (self.notLungCancerRows == None) :
#             lcrp  = Path("{}/{}".format(self.lungCancerData,  lcrFileName)) 
#             self.logger.info("lcrp:{}".format(lcrp))
#             if lcrp.exists():
#                 self.logger.info("loading from cache")
#                 store = pd.HDFStore(lcrp, mode="r")
#                 self.logger.info("store.info():{}".format(store.info()))
#                 self.logger.info("store.keys():{}".format(store.keys()))
#                 
#                 self.lungCancerRows        = pd.read_hdf(lcrp, 'lungCancerRows')
#                 self.notLungCancerCategory = pd.read_hdf(lcrp, 'notLungCancerCategory')
#             else :
#                 # create 
#                 self._loadTCGADataFrames()
#                     
#                 lungCancerRows = self.YDF['primary_site'].str.contains('Lung', case=False)
#                 self.lungCancerRows = lungCancerRows
#                 # ~ is 'not' in pandas
#                 self.notLungCancerRows = ~lungCancerRows
#                 
#                 # save to cache
#                 self.logger.info("saving :{}".format(lcrp))
#                 store = pd.HDFStore(lcrp)
#                 store['lungCancerRows'] = self.lungCancerRows
#                 store['notLungCancerCategory'] = self.notLungCancerCategory
        
        self.logger.info("END")

    ########################################################################
    def _addLungCancerLabels(self):
        self.logger.info("BEGIN")
        
        # http://thomas-cokelaer.info/blog/2014/06/pandas-how-to-compare-dataframe-with-none/
        if (self.lungCancerRows is None) or (self.notLungCancerRows is None) :
            self.loadRowFilter()
            
        if self.lungCancerLables not in self.YDF.columns:
            self.YDF.loc[                :,       self.lungCancerLables  ] = "AEDWIP" # alloc the column
            self.YDF.loc[  self.lungCancerRows,  [self.lungCancerLables] ] = self.lungCancerCategory
            self.YDF.loc[self.notLungCancerRows, [self.lungCancerLables] ] = self.notLungCancerCategory
        
        self.logger.info("END")

    ########################################################################
    def labelsIntoNumericValues(self):
        self.logger.info("BEGIN")
        
        # FIXME: AEDWIP figure out how to let user fetch econder
        # can not call loadTestData would lead to an infinit loop
        #
        # force all that prerequists to be loaded or created
        #self.loadTestData(randomSeed)
        
        self._addLungCancerLabels()
        
        # avoid type self 
        YDF = self.YDF
        
        self.encoder = LabelEncoder()
        self.YDF[self.lungCancerLableValues] = pd.Series(
                    self.encoder.fit_transform(YDF[self.lungCancerLables]), 
                    index=YDF.index)

#         print( YDF.loc[    lungCancerRows, [lungCancerLables,lungCancerLableValues]].head(3) )
#         print()
#         print( YDF.loc[ notLungCancerRows, [lungCancerLables,lungCancerLableValues]].head(3) )
        
        self.logger.info("END")

    ########################################################################
    def _split(self, randomSeed):
        '''
        Split into stratified training and test sets based on classes (i.e. lungCancerLables )
        so that we have equal proportions of each  type in the train and test sets
        '''
        self.logger.info("BEGIN")
        
        if self.XTrainNP and self.XTestNP and self.yTrainSeries and self.yTestSeries:
            return
        
        split = StratifiedShuffleSplit(
            n_splits=1, test_size=0.2, random_state=randomSeed)
        
        # create local vars to reduce typing and line length
        X = self.XDF
        Y = self.YDF
        for train_index, test_index in split.split(X.values, Y[self.lungCancerLableValues]):
            self.XTrainNP, self.XTestNP = X.values[train_index], X.values[test_index]
            self.yTrainSeries, self.yTestSeries = Y[self.lungCancerLableValues][train_index], \
                                Y[self.lungCancerLableValues][test_index]
                                
        
        self.logger.info('')                     
        self.logger.info("**************** AEDWIP")                     
        self.logger.info(self.XTrainNP.shape)
        self.logger.info(self.yTrainSeries.values.shape)
        self.logger.info(self.XTestNP.shape)
        self.logger.info(self.yTestSeries.values.shape)                                    
        self.logger.info("END")
    
    ########################################################################
    def _createMachineLearningDataSets(self, randomSeed):
        self.logger.info("BEGIN")
        
        self._loadTCGADataFrames()
        self.loadRowFilter()
        self._addLungCancerLabels()
        self.labelsIntoNumericValues()
        self._split(randomSeed)
        
        self.logger.info("saving :{}".format(self.machineLearningDataFile))
        store = pd.HDFStore(self.machineLearningDataFile, mode='w')
        
        XTrainDF = pd.DataFrame(self.XTrainNP)
        store['XTrainDF']     = XTrainDF
        
        XTestDF = pd.DataFrame(self.XTestNP)
        store['XTestDF']      = XTestDF
        
        store['yTrainSeries'] = self.yTrainSeries
        store['yTestSeries']  = self.yTestSeries
        
        store.close()
        
        self.logger.info("END")
        
    ########################################################################
    def loadTrainingData(self, randomSeed):
        '''
        argument:
            randomSeed: test set is not in cache uses randomSeed to create
        '''
        self.logger.info("BEGIN")
        
        # http://thomas-cokelaer.info/blog/2014/06/pandas-how-to-compare-dataframe-with-none/
        if (self.XTrainNP is None) or (self.yTrainSeries is None) :
            if not self.machineLearningDataFile.exists():
                self._createMachineLearningDataSets(randomSeed)
            else:
                store = pd.HDFStore(self.machineLearningDataFile, mode="r")
                self.logger.info("store.info():{}".format(store.info()))
                self.logger.info("store.keys():{}".format(store.keys()))
                                
                XTrainDF = pd.read_hdf(self.machineLearningDataFile, 'XTrainDF')
                self.XTrainNP = XTrainDF.to_numpy()
                self.yTrainSeries = pd.read_hdf(self.machineLearningDataFile, 'yTrainSeries')
        
        self.logger.info(self.XTrainNP.shape)
        self.logger.info(self.yTrainSeries.values.shape)
        if self.XTestNP is not None:
            self.logger.info(self.XTestNP.shape)
            self.logger.info(self.yTestSeries.values.shape)        
                
        self.logger.info("END")
                
    ########################################################################
    def loadTestData(self, randomSeed):
        '''
        argument:
            randomSeed: test set is not in cache uses randomSeed to create
        '''
        self.logger.info("BEGIN")
        
        # http://thomas-cokelaer.info/blog/2014/06/pandas-how-to-compare-dataframe-with-none/
        if (self.XTestNP is None) or (self.yTestSeries is None) :
            if not self.machineLearningDataFile.exists():
                self._createMachineLearningDataSets(randomSeed)
            else:
                store = pd.HDFStore(self.machineLearningDataFile, mode="r")
                self.logger.info("store.info():{}".format(store.info()))
                self.logger.info("store.keys():{}".format(store.keys()))
                                
                XTestDF = pd.read_hdf(self.machineLearningDataFile, 'XTestDF')
                self.XTestNP = XTestDF.to_numpy()
                self.yTestSeries = pd.read_hdf(self.machineLearningDataFile, 'yTestSeries')    
    
        if self.XTrainNP is not None:
            self.logger.info(self.XTrainNP.shape)
            self.logger.info(self.yTrainSeries.values.shape)
            
        self.logger.info(self.XTestNP.shape)
        self.logger.info(self.yTestSeries.values.shape)
        
        self.logger.info("END")
    
    
    
    
    
    
    
    
    
    
    