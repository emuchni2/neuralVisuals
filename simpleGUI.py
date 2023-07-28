"""
Class for pyqtgraph GUI - Ethan (gardner Lab)

Requires: pyqtgraph, PyQt5,numpy, matplotlib

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
        self.win.keyPressEvent = self.keyPressEvent


        # Define Top plot (ready for iamge)
        self.neuroPlot = self.win.addPlot(title="")



        # Define bottom plot 
        self.win.nextRow()
        self.behavePlot = self.win.addPlot()


        # Define bottom plot 
        self.win.nextRow()
        self.embPlot = self.win.addPlot()

        self.setupPlot()
        

    def setupPlot(self):

        self.imgNeuro = pg.ImageItem()
        self.neuroPlot.addItem(self.imgNeuro)

        self.neuroPlot.hideAxis('bottom')
        self.neuroPlot.setLabel('left', text='Neuron #')

        # Add scale Line

        


        self.imgBehave = pg.ImageItem()
        self.behavePlot.addItem(self.imgBehave)
        self.behavePlot.setLabel('bottom', text='Time (S)')
        self.behavePlot.setLabel('left', text='Freq (not to scale)')
        #self.behavePlot.hideAxis('left')


        # Optional X-Link
        self.behavePlot.setXLink(self.neuroPlot)                                                                     



        self.embPlot.hideAxis('left')
        self.embPlot.hideAxis('bottom')

    def clear_plots(self):
        self.neuroPlot.clear()
        self.embPlot.clear()
        self.behavePlot.clear()


    # Change to general one day?
    def set_behavioral_image(self,image_array):

        self.behave_array = image_array
        self.imgBehave.setImage(self.behave_array)
        

    def set_neural_image(self,image_array):
        
        self.neural_array = image_array
        self.imgNeuro.setImage(self.neural_array)
        

        def image_hover_event(event):
            if event.isExit():
                self.neuroPlot.setTitle("")
                return
            pos = event.pos()
            i, j = pos.y(), pos.x()
            i = int(np.clip(i, 0, self.image_array.shape[0] - 1))
            j = int(np.clip(j, 0, self.image_array.shape[1] - 1))
            val = self.image_array[i, j]
            ppos = self.img.mapToParent(pos)
            x, y = ppos.x(), ppos.y()
            self.neuroPlot.setTitle("pos: (%0.1f, %0.1f)  pixel: (%d, %d)  value: %.3g" % (x, y, i, j, val))

        #Disabled
        #self.img.hoverEvent = image_hover_event

        # Add a finite line segment in bold red
        #windowSec - self.startEndTimes[0,0]

        # for displaying the slices
        SE = self.startEndTimes
        print(SE.shape)
        #line_item = pg.PlotDataItem(x=SE[0,:], y=0*SE[0,:], pen=pg.mkPen('r', width=1), symbol='o', symbolPen='r', symbolBrush='r', size= 5,connect=False)
        line_item = pg.PlotDataItem(x=[SE[0,1],SE[1,1]], y=[0,0],pen=pg.mkPen('r', width=1))
        self.neuroPlot.addItem(line_item)

        print('Plotted X as ', [SE[0,1],SE[1,1]])

    def update(self):
        rgn = self.region.getRegion()

        findIndices = np.where(np.logical_and(self.startEndTimes[0,:] > rgn[0], self.startEndTimes[1,:] < rgn[1]))[0]
    
        self.newScatter.setData(pos = self.emb[findIndices,:])



        self.embPlot.setXRange(np.min(self.emb[:,0]) - 1, np.max(self.emb[:,0] + 1), padding=0)
        self.embPlot.setYRange(np.min(self.emb[:,1]) - 1, np.max(self.emb[:,1] + 1), padding=0)

        self.region2.setRegion(rgn)


    def update2(self):
        rgn = self.region2.getRegion()
        self.region.setRegion(rgn)






    def accept_embedding(self,embedding,startEndTimes,repeat = False):

        if repeat == True:
            self.embPlot.clear()

        self.emb = embedding
        self.startEndTimes = startEndTimes
        print('shape')
        print(startEndTimes.shape)  


        self.cmap = cm.get_cmap('hsv')
        norm_times = np.arange(self.emb.shape[0])/self.emb.shape[0]
        colors = self.cmap(norm_times) * 255
        print(colors)
        self.defaultColors = colors.copy()
        self.scatter = pg.ScatterPlotItem(pos=embedding, size=5, brush=colors)
        self.embPlot.addItem(self.scatter)
        
        self.newScatter = pg.ScatterPlotItem(pos=embedding[0:10,:], size=10, brush=pg.mkBrush(255, 255, 255, 200))
        self.embPlot.addItem(self.newScatter)

        # Scale imgNeuro 
        height,width = self.neural_array.shape

        x_start, x_end, y_start, y_end = 0, self.startEndTimes[1,-1], 0, height
        pos = [x_start, y_start]
        scale = [float(x_end - x_start) / width, float(y_end - y_start) / height]

        self.imgNeuro.setPos(*pos)
        tr = QtGui.QTransform()
        self.imgNeuro.setTransform(tr.scale(scale[0], scale[1]))
        self.neuroPlot.getViewBox().setLimits(yMin=y_start, yMax=y_end)
        self.neuroPlot.getViewBox().setLimits(xMin=x_start, xMax=x_end)


        # SCALE IMG 2 todo: functionalize

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



        # Add ROI
        if repeat == False:
            self.region = pg.LinearRegionItem(values=(0, self.startEndTimes[0,-1] / 10))
            self.region.setZValue(10)

            
            self.region.sigRegionChanged.connect(self.update)
            self.neuroPlot.addItem(self.region)


            # ADD ROI2 todo

            self.region2 = pg.LinearRegionItem(values=(0, self.startEndTimes[0,-1] / 10))
            self.region2.setZValue(10)
            self.region2.sigRegionChanged.connect(self.update2)

            self.behavePlot.addItem(self.region2)


        # consider where 

        self.embPlot.setXRange(np.min(self.emb[:,0]) - 1, np.max(self.emb[:,0] + 1), padding=0)
        self.embPlot.setYRange(np.min(self.emb[:,1]) - 1, np.max(self.emb[:,1] + 1), padding=0)


    def keyPressEvent(self,evt):

        key = evt.key()
        oldBoutVal = self.currentBout
        oldLetterVal = self.currentLetterInd


        # Check if the left arrow key is pressed
        if key == Qt.Key_Left:
            self.currentBout += -1 
                    # Check if the left arrow key is pressed
        if key == Qt.Key_Right:
            self.currentBout += 1 

        if key == Qt.Key_Down:
            self.currentLetterInd += -1 
                    # Check if the left arrow key is pressed
        if key == Qt.Key_Up:
            self.currentLetterInd += 1 

        settingsLetter = self.letterArr[self.currentLetterInd]

        try:
            self.plot_file(repeat = False)

            # TD = dict(zip(self.param_arr[0,:], self.param_arr[1,:])) 
            # RF = TD['roundingFactor']
            # WS = TD['window_size']
            # SS = TD['step_size']
            # M = TD['metric']
            # TAO = TD['time_const']
            # Bird = TD['Bird']

            # self.paramText = f'Rounding Factor = {RF},  Window Pixels = {WS},  Step Pixels = {SS},  Distance Metric = {M},  Smoothing Tao = {TAO}'

            # self.neuroPlot.setTitle(f'{Bird} Bout: {self.currentBout}{settingsLetter} with params: {self.paramText}')



        except:
            self.currentBout = oldBoutVal
            self.currentLetterInd = oldLetterVal 
            self.plot_file(repeat = False)
            #FIX....


    def accept_folder(self,path):
        self.workingFolder = path 
        self.currentBout = 1
        self.currentLetterInd = 0 
        self.letterArr = ['A','B','C','D']
        self.currentLetter = self.letterArr[self.currentLetterInd]
        self.plot_file()



    def plot_file(self,fileName,repeat = False):

        # self.clear_plots()
        # self.setupPlot()

        # settingsLetter = self.letterArr[self.currentLetterInd]
        # filePath = f'{self.workingFolder}/{self.currentBout}{settingsLetter}.npz'
        A = np.load(fileName)

        self.startEndTimes = A['embStartEnd']
        plotter.set_neural_image(A['neuroArr'])
        plotter.set_behavioral_image(A['behavioralArr'])

        # feed it (N by 2) embedding and length N list of times associated with each point
        plotter.accept_embedding(A['embVals'],A['embStartEnd'],repeat = repeat)

        #self.param_arr = A['paramArr']



    def show(self):
        self.win.show()
        self.app.exec_()


# IDEA (iterate through bouts..)
if __name__ == '__main__':

    # Instantiate the plotter    
    plotter = DataPlotter()

    # Accept folder of data
    plotter.plot_file('SortedResults/Pk146-Jul28/1A.npz')

    # Show
    plotter.show()
