# Visualization Tools

Python based visualization tools for low dimensional embeddings of spectral and neural data 

## **Spectrogram Viewer** 
Quick tool for visual comparison of two 'Wav' files 



![image](https://github.com/emuchni2/neuralVisuals/assets/85625059/94162dd3-e187-40c8-988f-dcbe13954e9a)

Dependencies: matplotlib, pyqtgraph, PyQt5, scipy, numpy

Run viewer.py or import DataPlotter class and run the following commands

```python
plotter = DataPlotter()
plotter.setupPlot()
plotter.addFile('/Users/ethanmuchnik/Desktop/specViewer/Demo_Wav/USA5207_45107.22309894_6_30_6_11_49.wav','top')
plotter.addFile('/Users/ethanmuchnik/Desktop/specViewer/Demo_Wav/USA5207_45107.22652648_6_30_6_17_32.wav','bottom')
plotter.startLink()
plotter.show()
```

## **Neural Embedding Scroller**
Traverse neural, behavioral, and low dimensional data
**Dependencies:**: matplotlib, pyqtgraph, PyQt5, numpy

Run improvedGUI.py or import DataPlotter class and run the following commands

```python
# Instantiate the plotter    
plotter = DataPlotter()

# Accept folder of data
plotter.accept_folder('/Users/ethanmuchnik/Desktop/Series_GUI/SortedResults/Pk146-Jul28')

# Show
plotter.show()
```
![image](https://github.com/emuchni2/neuralVisuals/assets/85625059/f5c6871f-6c12-4026-b0a3-05cc8a2c88b0)



## **Audio Embedding Selection Tool**

**Dependencies:**: matplotlib, pyqtgraph, PyQt5, numpy

**Inputs:**

npz file with:

- 'embVals' : N by 2 array of x,y values for low dimensional embedding
- 'embStartEnd' : 2 by N array of start,end times for each of the N slices
- 'behavioralArr': Np array of spectrogram (must be representative of the time bounded by the first start and last end of embStartEnd)

<img src="https://github.com/emuchni2/neuralVisuals/assets/85625059/4cd190a7-2a69-44f6-98d3-722ef7b6bd22" alt="Neural Embedding Scroller" width="600" height="400">

```python
app = QApplication([])
# Instantiate the plotter    
plotter = DataPlotter()
# Accept file of data
plotter.plot_file('/Users/ethanmuchnik/Downloads/demoCanaryLarge3.npz')
plotter.addROI()
# Show
plotter.show()
```

## **Plotting Techniques/Ideas**

Pixelated UMAP 
![image](https://github.com/emuchni2/neuralVisuals/assets/85625059/91a05a0d-c717-48be-b42b-f2fda3467e9f)

## **Contact**
- Ethan Muchnik (Gardner Lab)
- ethan.k.muchnik@gmail.com
