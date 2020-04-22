'''
Created on Apr 12, 2020

@author: andrew Davidson aedavids@ucsc.edu

class Histogram()
class HistogramLeft(Histogram)
class HistogramRight(Histogram)
'''
import matplotlib.patches as mplpatches
import numpy as np

########################################################################
class Histogram():
    '''
    bars are drawn vertically
    x axis goes from left to right, i.e. 0  to positive
    y axis goes from top to bottom, i.e 0 to positive
    
    public functions:
        __init__(self, panel, x, numBins)
        
    reference: lecture 4
    '''
    ########################################################################
    def __init__(self, panel, x, numBins, RGBTuple=None, alpha=0.5, label=None, scale=None):
        '''
        plots a histogram
        
        arguments:
            panel
            
            x: 
                array like object of values 
            
            numBins: 
                number of equally spaced bins between min(x) and max(x)
                
            RGBTuple: color tuple
                example: (205, 123, 1)
                
            alpha
                a value between 0 and 1
                
            label:
            
            scale:
                boolean
                if true bin counts are convert as follows np.log2(binCounts = 1)
        '''
        self.panel = panel
        self.x = x 
        self.numBins = numBins
        self.color = list( (i/255.0 for i in RGBTuple) ) # comprehensions return generators
        self.alpha = alpha
        self.label = label
        self.scale = scale
        
        self.xMin = np.min(self.x)
        self.xMax = np.max(self.x)
        
        # np.histogram 'bins' argument can be a array like object monotonically increasing values
        # or a scaler. The bins do not have the same width
        # for illustration, we calculate the bins the same way np.histogram would if bin was a scaler        
        self.bins = np.linspace(self.xMin, self.xMax, self.numBins + 1)     
           
        # note len(bins) != len(xHisto) ie. bin is num edges = len(xHisto) + 1
        #leftBoundary <= value < rightBoundary
        
        #   x   x   x   x   x
        # [   [   [   [   [   ]
                
        binCounts, retBins = np.histogram(self.x, self.bins)
        if scale:
            binCounts = np.log2(binCounts + 1)
        
        self.binCounts = binCounts
        self.retBins = retBins
                
        self._plot()
        
    ########################################################################
    def _plot(self):
        '''
        ref: 
            - lecture 4
            - https://docs.scipy.org/doc/numpy/reference/generated/numpy.histogram.html#numpy.histogram
        '''
        # print("x\n{}".format(self.x))
        # print("\nbins:\n{}".format(self.bins))
        

        # print("\nxHisto:\n{}".format(self.xHisto))
        # print("\nretBins:\n{}".format(self.retBins))
        for i in range(0, len(self.binCounts), 1) :
            left, bottom, width, height = self._dimensions(i)
            rectangle=mplpatches.Rectangle( [left,bottom], width, height,
                                       facecolor=self.color,
                                       edgecolor='black',
                                       linewidth=0.1
                                       ,alpha=self.alpha
                                       ,label = self.label
                                       )
            self.panel.add_patch(rectangle)            
            
    ########################################################################
    def _dimensions(self, i):
        bottom = 0
        left = self.bins[i] 
        width = self.bins[i+1] - left
        height = self.binCounts[i]
        return (left, bottom, width, height)
            
########################################################################
class HistogramLeft(Histogram):   
    '''
    - bars are drawn horizontally
    - x axis from left to right goes from positive number to zero
    - y axis goes from top to bottom 0, positive number     
    

    '''
    def __init__(self, panel, x, numBins, RGBTuple=None, alpha=0.5, label=None, scale=None):
        '''
        arguments:
            panel
            
            x: 
                array like object of values 
            
            numBins: 
                number of equally spaced bins between min(x) and max(x)
            
            RGBTuple: color tuple
                example: (205, 123, 1)
                
            alpha
                a value between 0 and 1
                
            label
                            
            scale:
                boolean
                if true bin counts are convert as follows np.log2(binCounts = 1)
        '''        
        super(HistogramLeft, self).__init__(panel, x, numBins, RGBTuple, alpha, label, scale)

    ########################################################################
    def _dimensions(self, i):
        normalBottom = 0
        normalLeft = self.bins[i] 
        normalWidth = self.bins[i+1] - normalLeft
        normalHeight = self.binCounts[i]
        
        width = normalHeight
        height = normalWidth
        bottom = height * i
        left = 0 
        #print("HistogramLeft: left:{} bottom:{} width:{} height:{}".format(left, bottom, width, height))        
        return(left, bottom, width, height)

########################################################################
class HistogramRight(Histogram):   
    '''
    - bars are drawn horizontally
    - x axis from left to right goes from 0 to positive number 
    - y axis goes from top to bottom 0, positive number     
    '''
    def __init__(self, panel, x, numBins, RGBTuple=None, alpha=0.5, label=None, scale=None):
        '''
        arguments:
            panel
            
            x: 
                array like object of values 
            
            numBins: 
                number of equally spaced bins between min(x) and max(x)
            
            RGBTuple: color tuple
                example: (205, 123, 1)
                
            alpha
                a value between 0 and 1
                
            label
                            
            scale:
                boolean
                if true bin counts are convert as follows np.log2(binCounts = 1)
        '''                
        super(HistogramRight, self).__init__(panel, x, numBins, RGBTuple. alpha, label, scale)

    ########################################################################
    def _dimensions(self, i):
        normalBottom = 0
        normalLeft = self.bins[i] 
        normalWidth = self.bins[i+1] - normalLeft
        normalHeight = self.binCounts[i]
        
        width = normalHeight
        height = normalWidth
        bottom = height * i
        left = 0
        #print("HistogramRight: left:{} bottom:{} width:{} height:{}".format(left, bottom, width, height))
        
        return(left, bottom, width, height)

# ########################################################################
# class Histogram():
#     '''
#     bars are drawn vertically
#     x axis goes from left to right, i.e. 0  to positive
#     y axis goes from top to bottom, i.e 0 to positive
#     
#     public functions:
#         __init__(self, panel, x, numBins)
#         
#     reference: lecture 4
#     '''
#     ########################################################################
#     def __init__(self, panel, x, numBins, RGBTuple=(128,128,128), alpha=None, 
#                  semiLog=False, label=None):
#         self.panel = panel
#         self.x = x 
#         self.numBins = numBins
#         self.color = list( (i/255.0 for i in RGBTuple) ) # comprehensions return generators
#         self.alpha = alpha
#         self.label = label
#         
#         self.xMin = np.min(self.x)
#         self.xMax = np.max(self.x)
#         
#         # np.histogram 'bins' argument can be a array like object monotonically increasing values
#         # or a scaler. The bins do not have the same width
#         # for illustration, we calculate the bins the same way np.histogram would if bin was a scaler        
#         self.bins = np.linspace(self.xMin, self.xMax, self.numBins + 1)     
#            
#         # note len(bins) != len(binCounts) ie. bin is num edges = len(binCounts) + 1
#         #leftBoundary <= value < rightBoundary
#         
#         #   x   x   x   x   x
#         # [   [   [   [   [   ]
#                 
#         binCounts, retBins = np.histogram(self.x, self.bins)
#         if semiLog :
#             self.binCounts = np.log10( binCounts )            
#         else :
#             self.binCounts = binCounts
#             
#         self.retBins = retBins
#         # print("x:\n{}".format(self.x))
#         # print("bins:\n{}".format(self.bins))
#         # print("binCounts:\n{}".format(self.binCounts))
#                 
#         self._plot()
#         
#     ########################################################################
#     def _plot(self):
#         '''
#         ref: 
#             - lecture 4
#             - https://docs.scipy.org/doc/numpy/reference/generated/numpy.histogram.html#numpy.histogram
#         '''
#         # print("x\n{}".format(self.x))
#         # print("\nbins:\n{}".format(self.bins))
#         
# 
#         # print("\nbinCounts:\n{}".format(self.binCounts))
#         # print("\nretBins:\n{}".format(self.retBins))
#  
#         for i in range(0, len(self.binCounts), 1) :
#             left, bottom, width, height = self._dimensions(i)
#             rectangle=mplpatches.Rectangle( [left,bottom], width, height,
#                                        #facecolor=(128/255.0, 128/255.0, 128/255.0),
#                                        facecolor=self.color,
#                                        edgecolor='black',
#                                        linewidth=0.1,
#                                        alpha=self.alpha,
#                                        label=self.label) # 
#             self.panel.add_patch(rectangle)            
#             
#     ########################################################################
#     def _dimensions(self, i):
#         bottom = 0
#         left = self.bins[i] 
#         width = self.bins[i+1] - left
#         height = self.binCounts[i]
#         
#         #print("Histogram: left:{} bottom:{} width:{} height:{}".format(left, bottom, width, height))        
#         return (left, bottom, width, height)
#             
# ########################################################################
# class HistogramLeft(Histogram):   
#     '''
#     - bars are drawn horizontally
#     - x axis from left to right goes from positive number to zero
#     - y axis goes from top to bottom 0, positive number     
#     '''
#     def __init__(self, panel, x, numBins):
#         super(HistogramLeft, self).__init__(panel, x, numBins)
# 
#     ########################################################################
#     def _dimensions(self, i):
#         normalBottom = 0
#         normalLeft = self.bins[i] 
#         normalWidth = self.bins[i+1] - normalLeft
#         normalHeight = self.binCounts[i]
#         
#         width = normalHeight
#         height = normalWidth
#         bottom = height * i
#         left = 0 
#         #print("HistogramLeft: left:{} bottom:{} width:{} height:{}".format(left, bottom, width, height))        
#         return(left, bottom, width, height)
# 
# ########################################################################
# class HistogramRight(Histogram):   
#     '''
#     - bars are drawn horizontally
#     - x axis from left to right goes from 0 to positive number 
#     - y axis goes from top to bottom 0, positive number     
#     '''
#     def __init__(self, panel, x, numBins):
#         super(HistogramRight, self).__init__(panel, x, numBins)
# 
#     ########################################################################
#     def _dimensions(self, i):
#         normalBottom = 0
#         normalLeft = self.bins[i] 
#         normalWidth = self.bins[i+1] - normalLeft
#         normalHeight = self.binCounts[i]
#         
#         width = normalHeight
#         height = normalWidth
#         bottom = height * i
#         left = 0
#         #print("HistogramRight: left:{} bottom:{} width:{} height:{}".format(left, bottom, width, height))
#         
#         return(left, bottom, width, height)