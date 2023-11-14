"""
Spec compare idea

"""

# Libraries/Settings
import numpy as np
import pyqtgraph as pg
from pyqtgraph.Qt import QtGui
from matplotlib import cm
from PyQt5.QtCore import Qt
from scipy.io import wavfile
import matplotlib.pyplot as plt

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
        self.topPlot = self.win.addPlot()


        # Define bottom plot 
        self.win.nextRow()
        self.bottomPlot = self.win.addPlot()
        

    def setupPlot(self):

        self.topPlot.setLabel('bottom', text='Time [S]')
        self.topPlot.setLabel('left', text='Freq (kHz)')


        # return filterSpec, t, freqs
        self.topImg = pg.ImageItem()
        self.topPlot.addItem(self.topImg)

        self.bottomPlot.setLabel('bottom', text='Time [S]')
        self.bottomPlot.setLabel('left', text='Freq (kHz)')


        self.bottomImg = pg.ImageItem()
        self.bottomPlot.addItem(self.bottomImg)
        

        self.view_box1 = self.topImg.getViewBox()
        self.view_box2 = self.bottomImg.getViewBox()

    def twoToOne(self):



      xRange1 = self.view_box1.viewRange()[0]
      xRange2 = self.view_box2.viewRange()[0]

      if np.abs(self.currentScale - (xRange2[-1] - xRange2[0])) < .1:
        print('Done')
        return
      else:
        self.currentScale= xRange1[-1] - xRange1[0]

      yRange1 = self.view_box1.viewRange()[1]
      yRange2 = self.view_box2.viewRange()[1]

      scale1 = xRange1[-1] - xRange1[0]
      scale2 = xRange2[-1] - xRange2[0]

      center1 = (xRange1[-1] + xRange1[0])/2
      center2 = (xRange2[-1] + xRange2[0])/2

      # print(self.view_box1.viewRange())
      # Adjust the X-axis scale of the other viewbox based on the target viewbox
      # source_viewbox = self.sender()
      minIn = center1 - scale2/2
      maxIn = center1 + scale2/2
    
      self.view_box1.setXRange(minIn,maxIn, padding=0)

    def oneToTwo(self):



      xRange1 = self.view_box1.viewRange()[0]
      xRange2 = self.view_box2.viewRange()[0]

      if np.abs(self.currentScale - (xRange1[-1] - xRange1[0])) < .1:
        print('Done')
        return
      else:
        self.currentScale= xRange1[-1] - xRange1[0]

      yRange1 = self.view_box1.viewRange()[1]
      yRange2 = self.view_box2.viewRange()[1]

      scale1 = xRange1[-1] - xRange1[0]
      scale2 = xRange2[-1] - xRange2[0]

      center1 = (xRange1[-1] + xRange1[0])/2
      center2 = (xRange2[-1] + xRange2[0])/2

      # print(self.view_box1.viewRange())
      # Adjust the X-axis scale of the other viewbox based on the target viewbox
      # source_viewbox = self.sender()
      minIn = center2 - scale1/2
      maxIn = center2 + scale1/2
    
      self.view_box2.setXRange(minIn,maxIn, padding=0)



    def startLink(self):  
      # Link only the X-axis scale manually
      self.view_box1.sigXRangeChanged.connect(self.oneToTwo)
      self.view_box2.sigXRangeChanged.connect(self.twoToOne)

      self.currentScale = self.view_box1.viewRange()[0][1] - self.view_box1.viewRange()[0][0]


    def addFile(self,inputFile,location):

        rgb_array, freqs, t = self.loadWav(inputFile)
        if location == 'top':
            relevantPlot = self.topImg

        if location == 'bottom':
            relevantPlot = self.bottomImg

        relevantPlot.setImage(rgb_array)

        height,width = rgb_array.shape[0:2]

        x_start, x_end, y_start, y_end = t[0], t[-1], freqs[0]/1000, freqs[-1]/1000
        pos = [x_start, y_start]
        scale = [float(x_end - x_start) / width, float(y_end - y_start) / height]

        relevantPlot.setPos(*pos)
        tr = QtGui.QTransform()
        relevantPlot.setTransform(tr.scale(scale[0], scale[1]))
        relevantPlot.getViewBox().setLimits(yMin=y_start, yMax=y_end)
        #relevantPlot.getViewBox().setLimits(xMin=x_start, xMax=x_end)
        # Do transformations
        # standardYshape  = 10
        self.topImg.getViewBox().setLimits(yMin=y_start, yMax=y_end)
        # self.topImg.getViewBox().setLimits(yMin=0, yMax=100)


    def clear_plots(self):
        self.topPlot.clear()
        self.bottomPlot.clear()



    def keyPressEvent(self,evt):

        key = evt.key()
        oldBoutVal = self.currentBout
        oldLetterVal = self.currentLetterInd

        # Check if the left arrow key is pressed
        if key == Qt.Key_Left:
            print('left')
                

    def loadWav(self,inputFile):
      samplerate, data = wavfile.read(inputFile)
      FS = samplerate # input
      NFFT = 512
      noverlap = 450  # noverlap > NFFT/2

      # Create Spectrogram
      spectrum, freqs, t, im = plt.specgram(data, NFFT=NFFT, Fs=FS, noverlap=noverlap,cmap='jet')

      # Manual Params (can be changed)
      logThresh = 10
      afterThresh = 4

      # Take log then delete elements below another thresh after log
      filterSpec = np.log(spectrum + logThresh)
      filterSpec[np.where(filterSpec < afterThresh)] = 0

      colormap = 'jet'

      # Normalize the numeric array to the [0, 1] range
      normalized_array = (filterSpec - np.min(filterSpec)) / (np.max(filterSpec) - np.min(filterSpec))

      # Apply the colormap to the normalized array
      rgb_array = plt.cm.get_cmap(colormap)(normalized_array)

      return rgb_array, freqs, t

    def show(self):
        self.win.show()
        self.app.exec_()


# IDEA (iterate through bouts..)
if __name__ == '__main__':

    # Instantiate the plotter    
    plotter = DataPlotter()
    plotter.setupPlot()
    plotter.addFile('/Users/ethanmuchnik/Desktop/specViewer/Demo_Wav/USA5207_45107.22309894_6_30_6_11_49.wav','top')
    plotter.addFile('/Users/ethanmuchnik/Desktop/specViewer/Demo_Wav/USA5207_45107.22652648_6_30_6_17_32.wav','bottom')
    plotter.startLink()
    plotter.show()