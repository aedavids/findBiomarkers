'''
Created on Apr 12, 2020

@author: Andrew Davidson aedavids@ucsc.edu

def addLegend(panel, colorMapTuples, labels, alpha=1)

def createPanel(fig, 
                panelWidthInInches, panelHeightInInches,
                leftRelativeSize, bottomRelativeSize):

def fancyBarGraph(panel, barHeights, barNames=None, xticksIndicies=None, 
                  RGBTuple=(180, 180, 180), alpha=1)
'''
import matplotlib.pyplot as plt
import matplotlib.patches as mplpatches

########################################################################
def addLegend(panel, colorMapTuples, labels, alpha=1):
    '''
    places legend in upper left corner 
    
    arguments:
        panel: type axes
        
        colorMapTuples:
            example : [ (255, 0, 0), (231, 23, 120) ]
        
        labels:
            list of strings
            
        alpha:
            0 <= value <=1
    
    returns:
        the panel argument
    '''
    colors = []
    for ct in colorMapTuples:
        r,g,b = ct
        colors.append( (r/255,g/255,b/255) )
    handles = [ mplpatches.Rectangle((0,0),1,1,color=c, alpha=alpha) for c in colors ]
    panel.legend(handles, labels)
    
    return panel

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

########################################################################
def fancyBarGraph(panel, barHeights, barNames=None, xticksIndicies=None, 
                  RGBTuple=(180, 180, 180), alpha=1):
    '''
    plots a bar graph wiht optional xtick labels. The labels are rotated 90 degrees
    
    Use case:
    plot a bar graph showing the number of example in each category
    Y axis shows the count values. 
    x axis shows bar for each category
    
    arguments:
        panel: 
            object of type axes
        
        barHeights:
            array like list of values
        
        barNames: 
            narray like list of bar names. E.G. category names
            
            default=None
            
        xticksIndicies:
            identifies the bars you want xtick names for
            array like list of index into barNames.
            
            default=None
            
        RGBTuple=(180, 180, 180)
        
        alpha=1        

    
    returns: 
        panel object of type axes
    '''
    xIdx = range(len(barNames))
    color = list([v/255.0 for v in RGBTuple])
    panel.bar(xIdx, barHeights, color=color, alpha=alpha)
    
    # rotate x labels
    # https://stackoverflow.com/a/52724092
    if xticksIndicies:
        panel.set_xticks(xticksIndicies)
        tickNames = barNames[xticksIndicies]
        panel.set_xticklabels(tickNames, rotation=90, fontsize=8)

    
    return panel

