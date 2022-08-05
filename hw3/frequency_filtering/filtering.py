# For this part of the assignment, You can use inbuilt functions to compute the fourier transform
# You are welcome to use fft that are available in numpy and opencv

import numpy as np
import math


class Filtering:
    def __init__(self, image):
        """initializes the variables for frequency filtering on an input image
        takes as input:
        image: the input image
        """
        self.image = image
        self.mask = self.get_mask(image.shape)

    def get_mask(self, shape):
        """Computes a user-defined mask
        takes as input:
        shape: the shape of the mask to be generated
        rtype: a 2d numpy array with size of shape
        """
        # type = 'ILPF'
        # D_not = 23.2

        # type = 'BLPF'
        # D_not = 15
        # n = 4

        # # type = 'GLPF'
        # # D_not = 9.2
        

        # H = np.empty(shape)
        # if type == 'ILPF': #ideal lowpass filter - ILPF
        #     for u in range(shape[0]):
        #         for v in range(shape[1]):
        #             D = math.pow(math.pow(u-shape[0]/2,2)+math.pow(v-shape[1]/2,2),1/2)
        #             H[u,v] = 1 if D <= D_not else 0
        # elif type == 'BLPF': #butterworth lowpass filter - BLPF
        #     for u in range(shape[0]):
        #         for v in range(shape[1]):
        #             D = math.pow(math.pow(u-shape[0]/2,2)+math.pow(v-shape[1]/2,2),1/2)
        #             H[u,v] = 1/(1+math.pow(D/D_not,2*n))  
        # elif type == 'GLPF': #gaussian lowpass filter - GLPF
        #     sigma = D_not
        #     for u in range(shape[0]):
        #         for v in range(shape[1]):
        #             D = math.pow(math.pow(u-shape[0]/2,2)+math.pow(v-shape[1]/2,2),1/2)
        #             H[u,v] = math.exp(-1*D**2/(2*sigma**2))

        H = np.ones((512,512)) 

        #small stars ---------------------------------
        # top left
        for row in range(240, 250): # 238, 250
            for col in range(230, 240): # 228, 243
                H[row,col] = 0
        # bottom right
        for row in range(266, 275): # (263, 278)
            for col in range(274, 283): # (271, 286)
                H[row,col] = 0

        #big stars ---------------------------
        # top right
        #vertical box
        for row in range(213,248):
            for col in range(296,301):
                H[row,col] = 0
        #horizontal box
        for row in range(230, 235):
            for col in range(280, 317):
                H[row,col] = 0
                
        # for row in range(223, 238): #(223, 238)
        #     for col in range(286, 311): #(288, 313)
        #         H[row,col] = 0


        # bottom left
        #vertical box
        for row in range(265, 302):
            for col in range(211, 216):
                H[row,col] = 0
        #horizontal box
        for row in range(279, 283): # (273, 288)
            for col in range(195, 225): # (203, 227)
                H[row,col] = 0

        # for row in range(274, 288): # (273, 288)
        #     for col in range(200, 225): # (203, 227)
        #         H[row,col] = 0
        
        return H

    def post_process_image(self, image):
        """Post processing to display DFTs and IDFTs
        takes as input:
        image: the image obtained from the inverse fourier transform
        return an image with full contrast stretch
        -----------------------------------------------------
        You can perform post processing as needed. For example,
        1. You can perfrom log compression
        2. You can perfrom a full contrast stretch (fsimage)
        3. You can take negative (255 - fsimage)
        4. etc.
        """
        #1 log compression
        image = self.logCompression(image)

        #2. full contrast stretch
        return self.fullContrastStetch(image)
    
    def logCompression(self, image):
        return np.array(np.log(image), dtype=np.uint8)
    
    def fullContrastStetch(self, image):
        max = np.max(image)
        min = np.min(image)
        newImage = np.empty(image.shape)
        for i in range(image.shape[0]):
            for j in range(image.shape[1]):
                newImage[i,j] = round(image[i,j]-min)/(max-min)
        return newImage*255

    def filter(self):
        """Performs frequency filtering on an input image
        returns a filtered image, magnitude of frequency_filtering, magnitude of filtered frequency_filtering
        ----------------------------------------------------------
        You are allowed to use inbuilt functions to compute fft
        There are packages available in numpy as well as in opencv
        Note: You do not have to do zero padding as discussed in class, the inbuilt functions takes care of that
        filtered image, magnitude of frequency_filtering, magnitude of filtered frequency_filtering: Make sure all images being returned have grey scale full contrast stretch and dtype=uint8
        
        Steps:"""
        # 1. Compute the fft of the image
        F = np.fft.fft2(self.image)

        # 2. shift the fft to center the low frequencies
        sF = np.fft.fftshift(F)

        # 3. get the mask (write your code in functions provided above) the functions can be called by self.filter(shape)
        H = self.get_mask(self.image.shape)

        # 4. filter the image frequency based on the mask (Convolution theorem)
        G = H*sF

        # 5. compute the inverse shift
        sG = np.fft.ifftshift(G)

        # 6. compute the inverse fourier transform
        g = np.fft.ifft2(sG)

        # 7. compute the magnitude
        gMag = np.abs(g)

        # 8. You will need to do post processing on the magnitude and depending on the algorithm (use post_process_image to write this code)
        post_processing_gMag = self.fullContrastStetch(gMag)

        return [post_processing_gMag, self.post_process_image(np.abs(sF)), self.post_process_image(np.abs(sF))*H]
       
