"""
Class for pyqtgraph GUI - Ethan (gardner Lab)

Requires: pyqtgraph, PyQt5,numpy, matplotlib

"""

# Libraries/Settings
import numpy as np
import pyqtgraph as pg
from pyqtgraph.Qt import QtGui
from matplotlib import cm
# -------------

class DataPlotter:
    def __init__(self):


        # Setup main window/layout
        pg.setConfigOptions(imageAxisOrder='row-major')
        self.app = pg.mkQApp()
        self.win = pg.GraphicsLayoutWidget()
        self.win.setWindowTitle('Embedding Analysis')

        # Define Top plot (ready for iamge)
        self.topPlot = self.win.addPlot(title="")
        self.img = pg.ImageItem()
        self.topPlot.addItem(self.img)

        # Define bottom plot 
        self.win.nextRow()
        self.bottomPlot = self.win.addPlot(colspan=2)


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

        self.img.hoverEvent = image_hover_event

    def update(self):
        minX, maxX = self.region.getRegion()
        findIndices = np.where(np.logical_and(self.rel_times > minX, self.rel_times < maxX))[0]
    
        self.newScatter.setData(pos = self.emb[findIndices,:])


    def accept_embedding(self,embedding,rel_times):

        self.emb = embedding
        self.rel_times = rel_times


        self.cmap = cm.get_cmap('hsv')
        norm_times = np.arange(self.emb.shape[0])/self.emb.shape[0]
        colors = self.cmap(norm_times) * 255
        print(colors)
        self.defaultColors = colors.copy()
        self.scatter = pg.ScatterPlotItem(pos=embedding, size=5, brush=colors)
        self.bottomPlot.addItem(self.scatter)
        
        self.newScatter = pg.ScatterPlotItem(pos=embedding[0:10,:], size=5, brush=pg.mkBrush(255, 255, 255, 200))
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

        # Add ROI
        self.region = pg.LinearRegionItem(values=(0, self.rel_times[-1] / 10))
        self.region.setZValue(10)

        
        self.region.sigRegionChanged.connect(self.update)
        self.topPlot.addItem(self.region)

    def show(self):
        self.win.show()
        self.app.exec_()

if __name__ == '__main__':

    # Load your data
    file_path = '/Users/ethanmuchnik/Desktop/OHSU/Results/workingOHSU-M1-S100.npz'
    A = np.load(file_path)
    rawSpk = A['rawSpk']
    spk_emb = A['spk_emb']
    start_times = A['start_times']
    
    # Instantiate the plotter    
    plotter = DataPlotter()

    # feed it image array (numpy)
    plotter.accept_image_array(rawSpk)
    # feed it (N by 2) embedding and length N list of times associated with each point
    plotter.accept_embedding(spk_emb,start_times)

    # Show
    plotter.show()
