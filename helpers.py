"""

Helper Functions 

"""
import numpy as np
import matplotlib.pyplot as plt


def colorScaler(inputEmbedding,metric = 'time', colormap = 'hsv',customSeries = None):

	N = inputEmbedding.shape[0] 

	if N < 4:
		print('Warning, small embedding dimension to plot')

	if metric == 'time':
		array = np.linspace(0, 1, N)
		cmap = plt.get_cmap(colormap)  # Get the desired colormap
		rgbArray = cmap(array)[:, :3] 

	if metric == 'RGB':
		print('fail')




	return rgbArray
