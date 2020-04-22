#!/usr/bin/env python3
# coding: utf-8
'''
Created on Apr 12, 2020

@author: Andrew Davidson
aedavids@ucsc.edu
'''


#from IPython.display import display, HTML
import logging
import numpy as np
import pandas as pd
import pathlib as pl
import requests

########################################################################
class TCGA_Target_GTex :
    '''
    Download gene expression and clinical data from the UCSC Xena Toil re-compute
    
    public functions:
        __init__(dataDir)
        loadTCGA_Target_GTex()
        
    references:
        - https://xenabrowser.net/datapages/?host=https://toil.xenahubs.net
    '''
    
    logger = logging.getLogger(__name__)

    ########################################################################
    def __init__(self, dataDir):
        '''
        arguments:
            dataDir: an object of type pathlib.Path
            the data store location on local system
        '''
        
        if not isinstance(dataDir, pl.Path):
            raise ValueError("dataDir must e of type Path, see pathlib package")
        
        self.dataDir               = dataDir
        self.tcgaTargetGtexPath    = dataDir.joinpath("tcga_target_gtex.h5")
        self.rawGenExpDataPath     = dataDir.joinpath("TcgaTargetGtex_rsem_gene_tpm.gz")
        self. pandasDataSourcePath = dataDir.joinpath("TcgaTargetGtex_rsem_gene_tpm.h5")
        self.rawPhenotypeDataPath  = dataDir.joinpath("TcgaTargetGTEX_phenotype.txt.gz")

        # do not hold onto data frames
        # they take up a lot of memory
        
    ########################################################################
    def loadTCGA_Target_GTex(self):
        '''
        Download gene expression and clinical data from the UCSC Xena Toil re-compute 
        data set wrangle, and store in an hdf5 file for quick loading machine learning. 
        This data set comprises gene expression data for twenty thousand tumor and 
        normal samples processed using the exact same genomics pipeline and therefore 
        can be compared to each other.
    
        Each of the source data set consists of a float vector, log2(TPM+0.001) 
    
        samples missing either the 'category' or 'disease'labels are dropped. 
        There should not be an NaN values
    
        The first time you run this function will be slow. On a fast machine first run 
        may take 20 min. It will down load data files from Xena and run pipe like 
        
        The only file you need locally is tcga_target_gtex.h5
        
        arguments:
            dataDir: a Path object. E.G ../data
            
        returns:XDF, YDF objects of type pandas DataFrame
            XDF: 
                numberOfSamples = 19,130
                number of gene expression features = 60,498
                
            YDF:
                numberOfSamples = 19,130
                number of label features = 7
            
    
        you can delete the following files to save a little disk space
    
        ```
        cd data
        rm TcgaTargetGTEX_phenotype.txt.gz
        rm TcgaTargetGtex_rsem_gene_tpm.gz 
        rm TcgaTargetGtex_rsem_gene_tpm.h5
        ```
    
        TODO: 
        explore gene expression values. 
        if a features has a large number of log2(0.001) values it means the original 
        data had zero TPM
        
       references:
            - https://xenabrowser.net/datapages/?host=https://toil.xenahubs.net
            - https://github.com/rcurrie/tumornormal/blob/master/ingest.ipynb
        '''
        
        if self.tcgaTargetGtexPath.exists() :
            XDF = pd.read_hdf(self.tcgaTargetGtexPath, "expression")
            YDF = pd.read_hdf(self.tcgaTargetGtexPath, "labels")
            
        else:
            self.logger.info("rawGenExpDataPath:{}".format(self.rawGenExpDataPath))
    
            self._downLoadGeneExpressionFromXenaHub()
            XDF= self._loadRawExpressionDF()
            
            self._downLoadPhenotypeFromXenaHub()
            YDF = self._loadRawPhenotypeDF()
            
            # shape must match Y, we also want in a ML friend format
            # i.e. rows are samples
            XDF = XDF.transpose()
            
            XDF, YDF, nullRowIdx = self._dropRowsIfMissingMetadata(XDF, YDF)
            self.logger.info("nullRowIdx:{}".format(nullRowIdx))
    
            tcgaTargetGtexPath = self._saveTCGA_Target_GtextDataFrames(XDF, YDF)
            self.logger.info("tcgaTargetGtexPath:{}".format(tcgaTargetGtexPath))
            
        return(XDF, YDF)

    #
    # private functions
    #
    
    ########################################################################    
    def _loadRawExpressionDF(self):
        '''
        This can be slow if h5 version does not exist locally, will create data from gz
        
        arguments:
            dataDir:
                path to local data directory. type pathlib
                example: ../data/TcgaTargetGtex_rsem_gene_tpm.gz
                
        returns
            expressionDF: type pandas data frame
            The shape of the data frame matches the xena hub data
            E.G. geneExpression x samples
        '''    
        # AEDWIP load gene expresion pandas data frame
        self.logger.info("sourceFile:{}".format(self.pandasDataSourcePath))
        if not self.pandasDataSourcePath.exists():
            self.logger.info("Converting expression to dataframe and storing in hdf5 file")
            expressionDF = pd.read_csv(self.rawGenExpDataPath, sep="\t", index_col=0) \
                                        .astype(np.float32)
            
            expressionDF.to_hdf(self.pandasDataSourcePath, 
                                           "expression", mode="w", format="fixed")
                
        else : 
            expressionDF = pd.read_hdf(self.pandasDataSourcePath, "expression") 
        
        return expressionDF

    ########################################################################    
    def _downLoadGeneExpressionFromXenaHub(self):
        '''
        will down load data if it is not on local disk . This can take a while
        
        arguments:
            dataDir:
                path to local data directory. type pathlib
                example: '../data'
                
        returns:
            rawDataPath, path to file on local system. type pathlib
        '''
#         rawDataPath = dataDir.joinpath("TcgaTargetGtex_rsem_gene_tpm.gz")
        if not self.rawGenExpDataPath.exists():
            self.logger.info("Downloading TCGA, TARGET and GTEX expression data from UCSC Xena")
            url = "https://toil.xenahubs.net/download/TcgaTargetGtex_rsem_gene_tpm.gz"
            self.logger.info("url:{}".format(url))
            response = requests.get(
                    url, 
                    stream=True,
                    # ERROR: cannot verify toil.xenahubs.net's certificate, issued by `/C=US/O=Amazon/OU=Server CA 1B/CN=Amazon':
                    #verify=False 
                    ) 
            response.raise_for_status()
            #totalLengthStr = response.headers.get('content-length')
            #totalLength = int(totalLengthStr)
    
            with open(self.rawGenExpDataPath, "wb") as f:
                dataLength = 0
                for chunk in response.iter_content(chunk_size=32768):
                    dataLength += len(chunk)
                    f.write(chunk)
                    
        #return rawDataPath    
    
    ########################################################################    
    def _loadRawPhenotypeDF(self):
        '''
        This can be slow if h5 version does not exist locally, will create data from gz
        
        arguments:
            dataDir:
                path to local data directory. type pathlib
                example: .../data/TcgaTargetGTEX_phenotype.txt.gz
        '''   
        
        # rename original column names
        # Index(['detailed_category', 'primary disease or tissue', '_primary_site',
        #  '_sample_type', '_gender', '_study'],
        # dtype='object'
        
        colNames = ["id", "category", "disease", "primary_site", "sample_type", "gender", "study"]
        phenotypeDF = pd.read_table(
                            self.rawPhenotypeDataPath, compression="gzip", 
                            header=0, 
                            names=colNames,
                            sep="\t", encoding="ISO-8859-1", index_col=0, 
                            dtype="str").sort_index(axis="index")
        
        # Compute and add a tumor/normal column - TCGA and TARGET have some normal samples, GTEX is all normal.
        phenotypeDF["tumor_normal"] = phenotypeDF.apply(
            lambda row: "Normal" if row["sample_type"] in ["Cell Line", "Normal Tissue", "Solid Tissue Normal"]
        else "Tumor", axis=1)  
        
        # debug
        # for colName in phenoTypeDF.columns:
            # self.logger.info("\n:{}".format(colName))
            # self.logger.info( phenoTypeDF.loc[:,[colName]].isnull().sum() )
        
        return phenotypeDF
    
    ########################################################################    
    def _downLoadPhenotypeFromXenaHub(self):
        '''
        will down load data if it is not on local disk . This can take a while
        
        arguments:
            dataDir:
                path to local data directory. type pathlib
                example: '../data'
                
        returns:
            rawDataPath, path to file on local system. type pathlib
        '''
        if not self.rawPhenotypeDataPath.exists():
            url = "https://toil.xenahubs.net/download/TcgaTargetGTEX_phenotype.txt.gz"
            self.logger.info("Downloading {}".format(url))
            with open(self.rawPhenotypeDataPath, "wb") as f:
                f.write(requests.get(url).content)
                        
    ########################################################################
    def _dropRowsIfMissingMetadata(self, geneExprDF, phenoDF): 
        '''
        drops rows from the data frames where 'category','disease' is null
        Note, drop is not done 'inplace'
        
        arguments
            geneExprDF, phenoDF:
                pandas data frames. Assume the rows are samples
                geneExprDF has gene expresion data
                phenoDF has meta data. E.G. labels
                
        returns (cleanGeneExprDF, cleanPhenoDF [null row idx])
            bad row idx are integer
        '''
    
        tmpDF = phenoDF.loc[:, ['category','disease']]
        # https://stackoverflow.com/a/14033137
        nullRowIdx = pd.isnull(tmpDF).any(1).to_numpy().nonzero()[0]
        
        cleanGeneExprDF = geneExprDF.drop( geneExprDF.index[ nullRowIdx ], inplace=False )
        cleanPhenoDF    =    phenoDF.drop( phenoDF.index[ nullRowIdx ],    inplace=False )
        
        return (cleanGeneExprDF, cleanPhenoDF, nullRowIdx)

    ########################################################################
    def testDropRowsIfMissingMetadata(self):
        v = np.reshape( np.array( np.arange(1,18 + 1)), (6,3) )
        testExpDF = pd.DataFrame(v
                           ,columns=['a', 'b', 'c' ],
                           index=['m', 'n', 'o', 'p', 'q', 'r' ]
                          )
        #self.logger.info(testExpDF)
        #display(HTML(testExpDF.to_html()))
    
    
        # testPheDF = pd.DataFrame(aedwp,
        #                    columns=['category', 'disease', 'foo' ],
        #                    index=['m', 'n', 'o', 'p', ]
        #                   )
    
        AEDWIP = None
        phenoTypeDF = AEDWIP
        testPheDF = phenoTypeDF.iloc[0:6, [0, 1, 2] ].copy(deep=True)
        # display(HTML(testPheDF.to_html()))
    
        testPheDF.iloc[[1,3], 0] = np.NaN
        testPheDF.iloc[[2], 1] = np.NaN
        #display(HTML(testPheDF.to_html()))
    
        self.logger.info('\n\n\n\n ********** BEGIN test ******')
        t = self.dropRowsIfMissingMetadata(testExpDF, testPheDF)
        cleanGeneExprDF, cleanPhenoDF, nullRowIdx = t
        #display(HTML(cleanGeneExprDF.to_html()))
        #display(HTML(cleanPhenoDF.to_html()))
        self.logger.info('nullRowIdx:{}'.format(nullRowIdx))
    
    ########################################################################
    def _saveTCGA_Target_GtextDataFrames(self, exprDF, labelDF):
        '''
        export data in h5 file format. exprDF will be transposed before write
        arguments:
            dataDir:
                directory on local system to write file to
                type: Path
                example "../data"
                
            exprDF, labelDF
                type: pandas data frames
                
        returns:
            tcgaTargetGtexPath:
                type: Path
        '''    
        with pd.HDFStore(self.tcgaTargetGtexPath, "w") as store:
            store["expression"] = exprDF.sort_index(axis="columns")
            store["labels"] = labelDF.astype(str)
    

# tcgaTargetGtexPath = saveTCGA_Target_GtextDataFrames(dataDir, expressionDF, phenoTypeDF)
# self.logger.info(tcgaTargetGtexPath)




