"""
Code to plot just an audio/behavioral and embedding

"""

# Libraries/Settings
import numpy as np
import pyqtgraph as pg
from pyqtgraph.Qt import QtGui
from matplotlib import cm
from PyQt5.QtCore import Qt
import numpy as np
from PyQt5.QtCore import QPointF
import matplotlib.pyplot as plt
# -------------
from pyqtgraph import DateAxisItem, AxisItem, QtCore

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
class DataPlotter(QWidget):
    def __init__(self):
        QWidget.__init__(self) # TODO? parent needed? #awkward


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
        
        self.win.scene().sigMouseClicked.connect(self.update2)    

        self.additionList = []
        self.additionCount = 0.05


    def setupPlot(self):

        # Setup behave plot for img
        self.imgBehave = pg.ImageItem()
        self.behavePlot.addItem(self.imgBehave)
        self.behavePlot.hideAxis('left')
        # self.behavePlot.hideAxis('bottom')


        # # Setup emb plot
        # self.embPlot.hideAxis('left')
        # self.embPlot.hideAxis('bottom')

    def clear_plots(self):
        self.embPlot.clear()
        self.behavePlot.clear()


    # Change to general one day?
    def set_behavioral_image(self,image_array,**kwargs):
        print('replot')


        self.behave_array = image_array
        # if 'addition' in kwargs.keys():
        #     self.imgBehave.setImage(self.behave_array + kwargs['addition'])
        # else:
        #     self.imgBehave.setImage(self.behave_array)
            # self.imgBehave.setImage(np.stack([self.behave_array] * 3, axis=-1))

        filterSpec = image_array
        # Normalize the numeric array to the [0, 1] range
        normalized_array = (filterSpec - np.min(filterSpec)) / (np.max(filterSpec) - np.min(filterSpec))

        # Apply the colormap to the normalized array

        rgb_array = plt.cm.get_cmap('inferno')(normalized_array)
        rgb_add = np.zeros_like(image_array)

        if 'addition' in kwargs.keys():
            relList = kwargs['addition']
            for img in relList:
                rgb_add += img 

        rgb_add1 = plt.cm.get_cmap('hsv')(rgb_add)
        rgb_add1[rgb_add == 0] = 0

        self.imgBehave.setImage(rgb_array + rgb_add1)


    def update(self):
        rgn = self.region.getRegion()

        findIndices = np.where(np.logical_and(self.startEndTimes[0,:] > rgn[0], self.startEndTimes[1,:] < rgn[1]))[0]
    
        self.newScatter.setData(pos = self.emb[findIndices,:])



        self.embPlot.setXRange(np.min(self.emb[:,0]) - 1, np.max(self.emb[:,0] + 1), padding=0)
        self.embPlot.setYRange(np.min(self.emb[:,1]) - 1, np.max(self.emb[:,1] + 1), padding=0)





    # Load the embedding and start times into scatter plot
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

        self.embMaxX = np.max(self.emb[:,0])
        self.embMaxY = np.max(self.emb[:,1])


        self.embMinX = np.min(self.emb[:,0])
        self.embMinY = np.min(self.emb[:,1])

        self.embPlot.setXRange(self.embMinX - 1, self.embMaxX + 1, padding=0)
        self.embPlot.setYRange(self.embMinY - 1, self.embMaxY + 1, padding=0)




    def plot_file(self,filePath):

        self.clear_plots()
        self.setupPlot()

        A = np.load(filePath)

        self.startEndTimes = A['embStartEnd']
        plotter.set_behavioral_image(A['behavioralArr'])

        # feed it (N by 2) embedding and length N list of times associated with each point
        plotter.accept_embedding(A['embVals'],A['embStartEnd'])

    def addROI(self):
        self.r1 = pg.EllipseROI([0, 0], [self.embMaxX/5, self.embMaxY/5], pen=(3,9))
        # r2a = pg.PolyLineROI([[0,0], [0,self.embMaxY/5], [self.embMaxX/5,self.embMaxY/5], [self.embMaxX/5,0]], closed=True)
        self.embPlot.addItem(self.r1)

        #self.r1.sigRegionChanged.connect(self.update2)

    # Manage key press events
    def keyPressEvent(self,evt):
        print('key is ',evt.key())

        if evt.key() == 65: # stick with numbers for now
            self.update()

    def update2(self):
        print('called')
        ellipse_size = self.r1.size()
        ellipse_center = self.r1.pos() + ellipse_size/2

        try:
            self.outCircles = np.vstack((self.outCircles,np.array([ellipse_center[0],ellipse_center[1],ellipse_size[0],ellipse_size[1]])))
        except:
            self.outCircles = np.array([ellipse_center[0],ellipse_center[1],ellipse_size[0],ellipse_size[1]])

        print(self.outCircles)
        np.savez('bounds.npz',bounds = self.outCircles)
        # Print the center and size
        print("Ellipse Center:", ellipse_center)
        print("Ellipse Size:", ellipse_size)
        # print(self.r1)
        print(ellipse_size[0])

        #manual distnace
        bound = np.square(self.emb[:,0] - ellipse_center[0])/np.square(ellipse_size[0]/2) +  np.square(self.emb[:,1] - ellipse_center[1])/np.square(ellipse_size[1]/2)
        indices_in_roi = np.where(bound < 1)[0]





        # # points_in_roi = [QPointF(x, y) for x, y in self.emb if self.r1.contains(QPointF(x, y))]
        # # print(points_in_roi)
        # print('does it contian 0,0')
        # if self.r1.contains(QPointF(0,0)):
        #     print('yes')

        # # indices_in_roi = [pt for pt in self.emb if roiShape.contains(pt)]
        # # print(roiShape.pos())
        # indices_in_roi = [index for index, (x, y) in enumerate(self.emb) if self.r1.contains(QPointF(x, y))]
        # print(indices_in_roi)
        # # print(indices_in_roi)
        # # print(self.emb.shape)

        tempImg = self.behave_array.copy()*0
        presumedTime = np.linspace(self.startEndTimes[0,0],self.startEndTimes[1,-1],num = tempImg.shape[1])
        print(presumedTime)
        print(self.startEndTimes.shape)
        print(self.behave_array.shape)


        for index in indices_in_roi:

            mask = (presumedTime < self.startEndTimes[1,index]) & (presumedTime > self.startEndTimes[0,index])
            relPlace = np.where(mask)[0]
            tempImg[:,relPlace] = self.additionCount
            print(self.additionCount)

        self.additionList.append(tempImg)
        self.additionCount += .05

        self.set_behavioral_image(self.behave_array,addition = self.additionList)


        # self.newScatter.setData(pos = self.emb[indices_in_roi,:])



        # self.embPlot.setXRange(np.min(self.emb[:,0]) - 1, np.max(self.emb[:,0] + 1), padding=0)
        # self.embPlot.setYRange(np.min(self.emb[:,1]) - 1, np.max(self.emb[:,1] + 1), padding=0)






    def show(self):
        self.win.show()
        self.app.exec_()


# IDEA (iterate through bouts..)
if __name__ == '__main__':
    app = QApplication([])

    # Instantiate the plotter    
    plotter = DataPlotter()

    # Accept folder of data
    #plotter.accept_folder('SortedResults/B119-Jul28')
    #/Users/ethanmuchnik/Desktop/Series_GUI/SortedResults/Pk146-Jul28/1B.npz
    #plotter.plot_file('/Users/ethanmuchnik/Desktop/Series_GUI/SortedResults/Pk146-Jul28/1B.npz')
    plotter.plot_file('/Users/ethanmuchnik/Downloads/demoCanaryLarge3.npz')
    # plotter.plot_file('working.npz')

    plotter.addROI()

    # Show
    plotter.show()

