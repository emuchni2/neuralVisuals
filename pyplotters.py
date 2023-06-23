
# Matplotlib based plotters 

from helpers import *

'''

Code to create a pixelated UMAP image
-Add advanced colorization methods, or write wrapper/function
-Generalize Label Text
'''
def pixelatedUMAP(inputEmbedding,imageSize = 500,mode = 'averaging',boundary = .5):

	# Obtain X and Y coordinates
	x = inputEmbedding[:,0]
	y = inputEmbedding[:,1]

	# Set X and Y ranges of output image
	range_min_x, range_max_x = np.min(x) - boundary, np.max(x) + boundary  
	range_min_y, range_max_y = np.min(y) - boundary, np.max(y) + boundary

	# Reference function to colorize
	colors = colorScaler(inputEmbedding,'time')

	# Create an empty image grid
	image = np.zeros((imageSize, imageSize, 3))
	imageCount = np.zeros((imageSize, imageSize, 3))

	# Scale and shift the coordinates to match the image grid
	scaled_x = (x - range_min_x) / (range_max_x - range_min_x) * imageSize
	scaled_y = (y - range_min_y) / (range_max_y - range_min_y) * imageSize

	# Iterate over points and add colors to the image
	for xi, yi, color in zip(scaled_x, scaled_y, colors):
		xi, yi = int(xi), int(yi)
		image[xi - 1, yi - 1, :] += color  # Verify indexing
		imageCount[xi - 1, yi - 1, :] += 1 

	if mode == 'averaging':
		image = image/imageCount

	plt.imshow(image, origin='lower', extent=[range_min_x, range_max_x, range_min_y, range_max_y])
	plt.xlabel('UMAP Embedding Dim1')
	plt.ylabel('UMAP Embedding Dim1')
	plt.title('UMAP Embedding -- Pixelated')

def threePlotter(inputEmbedding):

	minIndex = 0 
	maxIndex = 5000

	manualTimeCorrection = 5/1000 #150 --> 200HZ and a step of one --> each slice moves 1/200 = 5ms
	time = np.arange(maxIndex - minIndex) * manualTimeCorrection # ADD TIME... better

	# spkToColors = rescale_array(spk_emb)

	
	# Generate some random data
	x = inputEmbedding[minIndex:maxIndex,0]
	y = inputEmbedding[minIndex:maxIndex,1]
	z = time
	#color = spkToColors[minIndex:maxIndex,:]

	# Create a 3D scatter plot
	fig = plt.figure(facecolor='white')
	ax = fig.add_subplot(111, projection='3d')
	scatter = ax.scatter(x, y, z, cmap='viridis') #, c=color

	# Add a colorbar
	#cbar = fig.colorbar(scatter)
	#cbar.set_label('Spike Embedding')

	# Set labels for each axis
	ax.set_xlabel('UMAP Embedding Dim1')
	ax.set_ylabel('UMAP Embedding Dim1')
	ax.set_zlabel('Time [S]')





if __name__ == '__main__':

	# embeddingPath = '/Users/ethanmuchnik/Desktop/SuperData/results/B119/splitsA-standardAttemptA-UMAP.npz'
	# embedding = np.load(embeddingPath)['spk_emb']
	# pixelatedUMAP(embedding,imageSize = 500,mode = 'additive')
	# plt.show()

	embeddingPath = '/Users/ethanmuchnik/Desktop/SuperData/results/B119/splitsA-standardAttemptA-UMAP.npz'
	embedding = np.load(embeddingPath)['spk_emb']
	threePlotter(embedding)
	plt.show()


