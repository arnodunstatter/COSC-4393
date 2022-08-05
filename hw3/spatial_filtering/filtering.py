import numpy as np
import math

class Filtering:

    def __init__(self, image):
        self.image = image

    def imageStdDev(self):
        mean = sum([sum([self.image[row][col] for col in range(self.image.shape[1])]) for row in range(self.image.shape[0])])/(self.image.shape[0]*self.image.shape[1])
        return math.sqrt(sum([sum([math.pow(self.image[row][col] - mean,2) for col in range(self.image.shape[1])]) for row in range(self.image.shape[0])])/(self.image.shape[0]*self.image.shape[1]))

    def get_gaussian_filter(self):
        """Initialzes/Computes and returns a 5X5 Gaussian filter"""
        G = np.zeros((5,5))
        sigma_squared = math.pow(self.imageStdDev(), 2)
        pi = math.pi
        for row in range(G.shape[0]):
            for col in range(G.shape[1]):
                G[row][col] = (1/(2*pi*sigma_squared))*math.exp((-1/2)*(1/sigma_squared)*(row**2+col**2))
        return G/sum([sum([G[i][j] for j in range(G.shape[1]) for i in range(G.shape[0])])])

    def get_laplacian_filter(self):
        """Initialzes and returns a 3X3 Laplacian filter"""
        return np.array([
            [-1,-1,-1],
            [-1, 8,-1],
            [-1,-1,-1]
        ])

    def pad(self, mask):
        rowOffset = int(mask.shape[0]/2) # int() is the same as math.floor() here because the shape will always consist of non-negative integers
        newN = 2*rowOffset + self.image.shape[0]
        colOffset = int(mask.shape[1]/2)
        newM = 2*colOffset + self.image.shape[1]
        padded = np.zeros((newN,newM))
        for i in range(self.image.shape[0]):
            for j in range(self.image.shape[1]):
                padded[i+rowOffset][j+colOffset] = self.image[i][j]
        return padded
    
    def unpad(self, padded_image, mask):
        rowOffset = int(mask.shape[0]/2) # int() is the same as math.floor() here because the shape will always consist of non-negative integers
        colOffset = int(mask.shape[1]/2)
        unpadded = np.empty(self.image.shape)
        for i in range(self.image.shape[0]):
            for j in range(self.image.shape[1]):
                unpadded[i][j] = padded_image[i+rowOffset][j+colOffset]
        return unpadded
        

    def convolution(self, mask):
        # mask rotation 
        rotated_mask = np.array([row[::-1] for row in mask[::-1]])
        # padding
        padded = self.pad(mask)
        # sliding window sum of products
        convolved = np.zeros(padded.shape)
        rowOffset = int(mask.shape[0]/2) # int() is the same as math.floor() here because the shape will always consist of non-negative integers
        colOffset = int(mask.shape[1]/2)
        for i in range(padded.shape[0]-2*rowOffset):
            for j in range(padded.shape[1]-2*colOffset):
                window = np.array([row[j:j+mask.shape[1]] for row in padded[i:i+mask.shape[0]]]) 
                convolved[i+rowOffset][j+colOffset] = sum([sum([rotated_mask[r,c]*window[r,c] for c in range(mask.shape[1])]) for r in range(mask.shape[0])])
        return self.unpad(convolved, mask)

    def filter(self, filter_name):
        """Perform filtering on the image using the specified filter, and returns a filtered image
            takes as input:
            filter_name: a string, specifying the type of filter to use ["gaussian", laplacian"]
            return type: a 2d numpy array
                """
        if 'laplacian' != filter_name != 'gaussian':
            print("Invalid filter name passed to spatial_filtering/filter.py's filter()")
            exit()
        # figure out which filter we're using
        mask = self.get_gaussian_filter() if filter_name == 'gaussian' else self.get_laplacian_filter() 
        # perform convolution (mask rotation, padding, sliding window sum of products, unpadding)
        filter = self.convolution(mask)
        # add result to original image and return the sum
        return (self.image+filter)/2 if filter_name == 'gaussian' else self.image+filter

