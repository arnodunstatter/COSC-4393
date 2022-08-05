
import math
import numpy as np

class Filtering:

    def __init__(self, image, filter_name, filter_size, var = None):
        """initializes the variables of spatial filtering on an input image
        takes as input:
        image: the noisy input image
        filter_name: the name of the filter to use
        filter_size: integer value of the size of the fitler
        global_var: noise variance to be used in the Local noise reduction filter
        S_max: Maximum allowed size of the window that is used in adaptive median filter
        """

        self.image = image

        if filter_name == 'arithmetic_mean':
            self.filter = self.get_arithmetic_mean
        elif filter_name == 'geometric_mean':
            self.filter = self.get_geometric_mean
        if filter_name == 'local_noise':
            self.filter = self.get_local_noise
        elif filter_name == 'median':
            self.filter = self.get_median
        elif filter_name == 'adaptive_median':
            self.filter = self.get_adaptive_median

        self.filter_size = filter_size
        self.global_var = var
        self.S_max = 15

    def get_arithmetic_mean(self, roi, pos=None):
        """Computes the arithmetic mean of the input roi
        takes as input:
        roi: region of interest (a 2D numpy array of intensity values)
        returns the arithmetic mean value of the roi"""
        roi = [x for x in roi.reshape(-1) if x!=0]
        return sum(roi)/len(roi)


    def get_geometric_mean(self, roi, pos=None): #Generally achieves smoothing comparable to the artihmetic mean filter but it tends to lose less image detail in the process
        def prod(array):
            returnMe = 1
            for i in array:
                returnMe *= i
            return returnMe
        """Computes the geometric mean for the input roi
        takes as input:
        roi: region of interest (a 2D numpy array of intensity values)
        returns the geometric mean value of the roi"""
        roi = [x for x in roi.reshape(-1) if x!=0]
        return prod(roi)**(1/(len(roi)))


    def get_local_noise(self, roi, pos=None): ###############################################################################################################################################
        """Computes the local noise reduction value
        takes as input:
        roi: region of interest (a 2D numpy array of intensity values)
        returns the local noise reduction value of the roi"""
        x,y = roi.shape[0]//2, roi.shape[1]//2

        local_mean = sum(roi.reshape(-1))/(roi.shape[0]*roi.shape[1])
        local_var = sum([(i-local_mean)**2 for i in roi.reshape(-1)])/(roi.shape[0]*roi.shape[1])

        return roi[x,y]-((self.global_var**2)/(local_var**2))*(roi[x,y]-local_mean)

    def get_median(self, roi, pos=None):
        """Computes the median for the input roi
        takes as input:
        roi: region of interest (a 2D numpy array of intensity values)
        returns the median value of the roi"""
        return sorted(roi.reshape(-1))[len(roi.reshape(-1))//2]


    def get_adaptive_median(self, roi, pos=None): ###############################################################################################################################################
        """Use this function to implment the adaptive median.
        It is left up to the student to define the input to this function and call it as needed. Feel free to create
        additional functions as needed.
        roi: region of interest (a 2D numpy array of intensity values)
        """        
        def stage_A(roi, pos):
            z_min = min(roi.reshape(-1))
            z_max = max(roi.reshape(-1))
            z_med = self.get_median(roi)
            x,y = pos
            z_xy = self.image[x,y]
            S_max = self.S_max
            shape = list(roi.shape)
            
            a1 = z_med-z_min
            a2 = z_med-z_max

            if a1>0 and a2<0:# then Stage B
                return stage_B(roi, pos)
            else:
                if shape[0] > shape[1]:
                    shape[1] += 2
                else:
                    shape[0] += 2
                
                if shape[0]*shape[1] <= S_max:
                    #new_roi = self.image[x-shape[0]//2:x+shape[0]//2 +1, y-shape[1]//2:y+shape[1]//2 +1]
                    new_roi = np.empty(shape)
                    for row in range(shape[0]):
                        for col in range(shape[1]):
                            if row+x-shape[0]//2 not in range(self.image.shape[0]) or col+y-shape[1]//2 not in range(self.image.shape[1]): # need more padding
                                new_roi[row,col] = 0
                            else:
                                new_roi[row,col] = self.image[row+x-shape[0]//2, col+y-shape[1]//2]
                    return stage_A(new_roi, pos)
                else: 
                    return z_med    
        
        def stage_B(roi, pos):
            z_min = min(roi.reshape(-1))
            z_max = max(roi.reshape(-1))
            z_med = self.get_median(roi)
            x,y = pos
            z_xy = self.image[x,y]
            S_max = self.S_max
            shape = list(roi.shape)

            b1 = z_xy-z_min
            b2 = z_xy-z_max
            
            if b1>0 and b2<0:
                return z_xy
            else:
                return z_med
    
        return stage_A(roi,pos)
    


    def filtering(self): ###############################################################################################################################################
        """performs filtering on an image containing gaussian or salt & pepper noise
        returns the denoised image
        ----------------------------------------------------------
        Note: Here when we perform filtering we are not doing convolution.
        For every pixel in the image, we select a neighborhood of values defined by the kernal and apply a mathematical
        operation for all the elements within the kernel. For example, mean, median and etc.

        Note: You can create extra functions as needed. For example if you feel that it is easier to create a new function for
        the adaptive median filter as it has two stages, you are welcome to do that.
        For the adaptive median filter assume that S_max (maximum allowed size of the window) is 15
        """
        
        #1. add the necesssary zero padding to the noisy image, that way we have sufficient values to perform the operations
        #    on the pixels at the image corners. The number of rows and columns of zero padding is defined by the kernel size
        pad = self.filter_size//2
        padded_image = np.zeros((self.image.shape[0]+2*pad, self.image.shape[1]+2*pad))
        padded_image[pad:-pad, pad:-pad] = self.image
        self.image = padded_image

        #2. Iterate through the image and every pixel (i,j) gather the neighbors defined by the kernel into a list (or any data structure)
        #3. Pass these values to one of the filters that will compute the necessary mathematical operations (mean, median, etc.)
        #4. Save the results at (i,j) in the ouput image.

        #2,3,4:
        # for every pixel in the image, (i,j) gather the nieghbors into a numpy array, pass these values to the filter and save the result at (i,j)
        for i in range(pad, self.image.shape[0]-pad):
            for j in range(pad, self.image.shape[1]-pad):
                roi = self.image[i-pad:i+pad+1, j-pad:j+pad+1]
                self.image[i,j] = self.filter(roi, (i,j))

        #5. unpad
        self.image = self.image[pad:-pad, pad:-pad]

        #6. return the output image               
        return self.image

