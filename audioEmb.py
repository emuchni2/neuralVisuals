"""
Code to plot just an audio/behavioral and embedding

"""

# Libraries/Settings
import numpy as np
import pyqtgraph as pg
from pyqtgraph.Qt import QtGui
from matplotlib import cm
from PyQt5.QtCore import Qt

# -------------

class DataPlotter:
    def __init__(self):


        # Setup main window/layout
        pg.setConfigOptions(imageAxisOrder='row-major')
        self.app = pg.mkQApp()


        # Instantiate window
        self.win = pg.GraphicsLayoutWidget()
        self.win.setWindowTitle('Embedding Analysis')

        # Behave plot
        self.behavePlot = self.win.addPlot()


        # Define bottom plot 
        self.win.nextRow()
        self.embPlot = self.win.addPlot()


        self.setupPlot()
        

    def setupPlot(self):

        # Setup behave plot for img
        self.imgBehave = pg.ImageItem()
        self.behavePlot.addItem(self.imgBehave)
        self.behavePlot.hideAxis('left')
        # self.behavePlot.hideAxis('bottom')


        # Setup emb plot
        self.embPlot.hideAxis('left')
        self.embPlot.hideAxis('bottom')

    def clear_plots(self):
        self.embPlot.clear()
        self.behavePlot.clear()


    # Change to general one day?
    def set_behavioral_image(self,image_array):

        self.behave_array = image_array
        self.imgBehave.setImage(self.behave_array)
     

    def update(self):
        rgn = self.region.getRegion()

        findIndices = np.where(np.logical_and(self.startEndTimes[0,:] > rgn[0], self.startEndTimes[1,:] < rgn[1]))[0]
    
        self.newScatter.setData(pos = self.emb[findIndices,:])



        self.embPlot.setXRange(np.min(self.emb[:,0]) - 1, np.max(self.emb[:,0] + 1), padding=0)
        self.embPlot.setYRange(np.min(self.emb[:,1]) - 1, np.max(self.emb[:,1] + 1), padding=0)






    def accept_embedding(self,embedding,startEndTimes):

        self.emb = embedding
        self.startEndTimes = startEndTimes


        self.cmap = cm.get_cmap('hsv')
        norm_times = np.arange(self.emb.shape[0])/self.emb.shape[0]
        colors = self.cmap(norm_times) * 255
        self.defaultColors = colors.copy()
        self.scatter = pg.ScatterPlotItem(pos=embedding, size=5, brush=colors)
        self.embPlot.addItem(self.scatter)
        
        self.newScatter = pg.ScatterPlotItem(pos=embedding[0:10,:], size=10, brush=pg.mkBrush(255, 255, 255, 200))
        self.embPlot.addItem(self.newScatter)


        # Scale imgBehave 
        height,width = self.behave_array.shape

        x_start, x_end, y_start, y_end = 0, self.startEndTimes[1,-1], 0, height
        pos = [x_start, y_start]
        scale = [float(x_end - x_start) / width, float(y_end - y_start) / height]

        self.imgBehave.setPos(*pos)
        tr = QtGui.QTransform()
        self.imgBehave.setTransform(tr.scale(scale[0], scale[1]))
        self.behavePlot.getViewBox().setLimits(yMin=y_start, yMax=y_end)
        self.behavePlot.getViewBox().setLimits(xMin=x_start, xMax=x_end)

        print(self.startEndTimes)
        self.region = pg.LinearRegionItem(values=(0, self.startEndTimes[0,-1] / 10))
        self.region.setZValue(10)

        
        self.region.sigRegionChanged.connect(self.update)

        self.behavePlot.addItem(self.region)


        # consider where 

        self.embPlot.setXRange(np.min(self.emb[:,0]) - 1, np.max(self.emb[:,0] + 1), padding=0)
        self.embPlot.setYRange(np.min(self.emb[:,1]) - 1, np.max(self.emb[:,1] + 1), padding=0)




    def plot_file(self,filePath):

        self.clear_plots()
        self.setupPlot()

        A = np.load(filePath)

        self.startEndTimes = A['embStartEnd']
        plotter.set_behavioral_image(A['behavioralArr'])

        # feed it (N by 2) embedding and length N list of times associated with each point
        plotter.accept_embedding(A['embVals'],A['embStartEnd'])



    def show(self):
        self.win.show()
        self.app.exec_()


# IDEA (iterate through bouts..)
if __name__ == '__main__':

    # Instantiate the plotter    
    plotter = DataPlotter()

    # Accept folder of data
    #plotter.accept_folder('SortedResults/B119-Jul28')
    plotter.plot_file('demoCanary/exampleData.npz')


    # Show
    plotter.show()
