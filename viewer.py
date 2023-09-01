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

    def addFile(self,inputFile,location):

        rgb_array  = self.loadWav(inputFile)
        if location == 'top':
            self.topImg.setImage(rgb_array)

        if location == 'bottom':
            self.bottomImg.setImage(rgb_array)


        # Do transformations
        standardYshape  = 10
        self.topImg.getViewBox().setLimits(yMin=0, yMax=100)
        self.topImg.getViewBox().setLimits(yMin=0, yMax=100)


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

      return rgb_array

    def show(self):
        self.win.show()
        self.app.exec_()


# IDEA (iterate through bouts..)
if __name__ == '__main__':

    # Instantiate the plotter    
    plotter = DataPlotter()
    plotter.setupPlot()
    plotter.addFile('Demo_Wav/USA5207_45107.22309894_6_30_6_11_49.wav','top')
    plotter.addFile('Demo_Wav/USA5207_45107.22652648_6_30_6_17_32.wav','bottom')

    plotter.show()