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

        self.setupPlot()
        

    def setupPlot(self):
        self.win = pg.GraphicsLayoutWidget()
        self.win.setWindowTitle('Embedding Analysis')
        self.win.keyPressEvent = self.keyPressEvent


        # Define Top plot (ready for iamge)
        self.topPlot = self.win.addPlot(title="")
        self.img = pg.ImageItem()
        self.topPlot.addItem(self.img)

        # Define bottom plot 
        self.win.nextRow()
        self.middlePlot = self.win.addPlot()
        self.imgSpec = pg.ImageItem()
        self.middlePlot.addItem(self.imgSpec)


        # Define bottom plot 
        self.win.nextRow()
        self.bottomPlot = self.win.addPlot()


    # Change to general one day?
    def set_spec(self,image_array_spec):

        self.image_array_spec = image_array_spec
        self.imgSpec.setImage(image_array_spec)
        

    def accept_image_array(self,image_array):
        
        self.image_array = image_array
        self.img.setImage(image_array)
        

        def image_hover_event(event):
            if event.isExit():
                self.topPlot.setTitle("")
                return
            pos = event.pos()
            i, j = pos.y(), pos.x()
            i = int(np.clip(i, 0, self.image_array.shape[0] - 1))
            j = int(np.clip(j, 0, self.image_array.shape[1] - 1))
            val = self.image_array[i, j]
            ppos = self.img.mapToParent(pos)
            x, y = ppos.x(), ppos.y()
            self.topPlot.setTitle("pos: (%0.1f, %0.1f)  pixel: (%d, %d)  value: %.3g" % (x, y, i, j, val))

        #Disabled
        #self.img.hoverEvent = image_hover_event

    def update(self):
        rgn = self.region.getRegion()
        findIndices = np.where(np.logical_and(self.rel_times > rgn[0], self.rel_times < rgn[1]))[0]
    
        self.newScatter.setData(pos = self.emb[findIndices,:])



        self.bottomPlot.setXRange(np.min(self.emb[:,0]) - 1, np.max(self.emb[:,0] + 1), padding=0)
        self.bottomPlot.setYRange(np.min(self.emb[:,1]) - 1, np.max(self.emb[:,1] + 1), padding=0)

        self.region2.setRegion(rgn)


    def update2(self):
        rgn = self.region2.getRegion()
        self.region.setRegion(rgn)






    def accept_embedding(self,embedding,rel_times,repeat = False):

        if repeat == True:
            self.bottomPlot.clear()

        self.emb = embedding
        self.rel_times = rel_times


        self.cmap = cm.get_cmap('hsv')
        norm_times = np.arange(self.emb.shape[0])/self.emb.shape[0]
        colors = self.cmap(norm_times) * 255
        print(colors)
        self.defaultColors = colors.copy()
        self.scatter = pg.ScatterPlotItem(pos=embedding, size=5, brush=colors)
        self.bottomPlot.addItem(self.scatter)
        
        self.newScatter = pg.ScatterPlotItem(pos=embedding[0:10,:], size=10, brush=pg.mkBrush(255, 255, 255, 200))
        self.bottomPlot.addItem(self.newScatter)

        # Scale img 
        height,width = self.image_array.shape

        x_start, x_end, y_start, y_end = 0, rel_times[-1], 0, height
        pos = [x_start, y_start]
        scale = [float(x_end - x_start) / width, float(y_end - y_start) / height]

        self.img.setPos(*pos)
        tr = QtGui.QTransform()
        self.img.setTransform(tr.scale(scale[0], scale[1]))
        self.topPlot.getViewBox().setLimits(yMin=y_start, yMax=y_end)
        self.topPlot.getViewBox().setLimits(xMin=x_start, xMax=x_end)


        # SCALE IMG 2 todo: functionalize

        # Scale img 
        height,width = self.image_array_spec.shape

        x_start, x_end, y_start, y_end = 0, rel_times[-1], 0, height
        pos = [x_start, y_start]
        scale = [float(x_end - x_start) / width, float(y_end - y_start) / height]

        self.imgSpec.setPos(*pos)
        tr = QtGui.QTransform()
        self.imgSpec.setTransform(tr.scale(scale[0], scale[1]))
        self.middlePlot.getViewBox().setLimits(yMin=y_start, yMax=y_end)
        self.middlePlot.getViewBox().setLimits(xMin=x_start, xMax=x_end)



        # Add ROI
        if repeat == False:
            self.region = pg.LinearRegionItem(values=(0, self.rel_times[-1] / 10))
            self.region.setZValue(10)

            
            self.region.sigRegionChanged.connect(self.update)
            self.topPlot.addItem(self.region)


            # ADD ROI2 todo

            self.region2 = pg.LinearRegionItem(values=(0, self.rel_times[-1] / 10))
            self.region2.setZValue(10)
            self.region2.sigRegionChanged.connect(self.update2)

            self.middlePlot.addItem(self.region2)


        # consider where 

        self.bottomPlot.setXRange(np.min(self.emb[:,0]) - 1, np.max(self.emb[:,0] + 1), padding=0)
        self.bottomPlot.setYRange(np.min(self.emb[:,1]) - 1, np.max(self.emb[:,1] + 1), padding=0)


    def keyPressEvent(self,evt):

        key = evt.key()

        # Check if the left arrow key is pressed
        if key == Qt.Key_Left:
            self.currentBout += -1 
                    # Check if the left arrow key is pressed
        if key == Qt.Key_Right:
            self.currentBout += 1 

        self.plot_file(self.currentBout,repeat = True)
        self.topPlot.setTitle(f'Embedding Analysis for bout {self.currentBout}')


    def accept_folder(self,path):
        self.workingFolder = path 
        self.currentBout = 1 #change later
        self.plot_file(self.currentBout)



    def plot_file(self,boutNum,repeat = False):
        print('plotting bout ',boutNum)
        filePath = f'{self.workingFolder}/bout{boutNum}.npz'
        A = np.load(filePath)
        rawSpk = A['rawSpk']
        spk_emb = A['spk_emb']
        start_times = A['start_times']
    
        filterSpec = A['filterSpec']

        plotter.accept_image_array(rawSpk)
        plotter.set_spec(filterSpec)

        # feed it (N by 2) embedding and length N list of times associated with each point
        plotter.accept_embedding(spk_emb,start_times,repeat = repeat)



    def show(self):
        self.win.show()
        self.app.exec_()


# IDEA (iterate through bouts..)
if __name__ == '__main__':

    # Load your data
    file_path = 'working.npz'
    A = np.load(file_path)
    rawSpk = A['rawSpk']
    spk_emb = A['spk_emb']
    start_times = A['start_times']
    
    filterSpec = A['filterSpec']


    # Instantiate the plotter    
    plotter = DataPlotter()

    plotter.accept_folder('Results2')
    # Show
    plotter.show()
