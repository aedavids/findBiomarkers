'''
Created on Apr 12, 2020

@author: Andrew Davidson aedavids@ucsc.edu

def createPanel(fig, 
                panelWidthInInches, panelHeightInInches,
                leftRelativeSize, bottomRelativeSize):

'''
import matplotlib.pyplot as plt

########################################################################
def createPanel(fig, 
                panelWidthInInches, panelHeightInInches,
                leftRelativeSize, bottomRelativeSize):
    '''
    returns a 'panel'. I.E. a graph component we can put stuff into
    do not use a plt.subplot. it is not flexible enough
    
    we can have multiple panels
    the values of left, bottom are relative to the size of the figure. they 
    should be values between 0 and 1
    '''
    
    figWidth, figHeight = fig.get_size_inches()
    relativeWidth = panelWidthInInches / figWidth
    relativeHeight = panelHeightInInches / figHeight
    
    # left, bottom, width, and height are relative to size of figure,
    # they should be values in range [0,1] 
    retPanel = plt.axes( [leftRelativeSize, bottomRelativeSize, relativeWidth, relativeHeight])
    return retPanel