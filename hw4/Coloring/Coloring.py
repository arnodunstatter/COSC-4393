import math
import numpy as np
class Coloring:
    
    def getColor(self, val, slices):
            center = slices[len(slices)//2]
            if center[0] <= val < center[1]:
                return center[2]
            elif val < center[0]:
                return self.getColor(val, slices[:len(slices)//2])
            else: #val >= center[1]
                return self.getColor(val, slices[len(slices)//2:])

    def intensity_slicing(self, image, n_slices):
        '''
       Convert greyscale image to color image using color slicing technique.
       takes as input:
       image: the grayscale input image
       n_slices: number of slices
       '''
        

        # 1. Split the exising dynamic range (0, k-1) using n slices (creates n+1 intervals)
        maxI = np.max(image)
        minI = np.min(image)
        sliceLength = (maxI - minI) / n_slices
        slices = [[low,low+sliceLength,None] for low in np.arange(minI, maxI+1, sliceLength)]   
        
        # 2. Randomly assign a color to each interval
        for slice in slices:
            color = np.random.randint(0,256,3)
            slice[2] = color

        # 3. Create and output color image
        color_image = np.empty((image.shape[0], image.shape[1], 3))

        # 4. Iterate through the image and assign colors to the color image based on which interval the intensity belongs to
        for i in range(image.shape[0]):
            for j in range(image.shape[1]):
                #print(image[i,j])
                color_image[i,j] = self.getColor(image[i,j], slices)

        # 5. return colored image
        return color_image

    def color_transformation(self, image, n_slices, theta):
        '''
        Convert greyscale image to color image using color transformation technique.
        takes as input:
        image:  grayscale input image
        colors: color array containing RGB values
        theta: (phase_red, phase,_green, phase_blue) a tuple with phase values for (r, g, b) 
        '''
        # 1. Split the exising dynamic range (0, k-1) using n slices (creates n+1 intervals)
        maxI = np.max(image)
        minI = np.min(image)
        sliceLength = (maxI - minI) / n_slices
        slices = [[low,low+sliceLength,None] for low in np.arange(minI, maxI+1, sliceLength)]  
        
        # 2. create red values for each slice using 255*sin(slice + theta[0])
        #       similarly create green and blue using 255*sin(slice + theta[1]), 255*sin(slice + theta[2])
        for slice in slices:
            middle = (slice[0] + slice[1])/2
            r = 255*math.sin(middle + theta[0])
            g = 255*math.sin(middle + theta[1])
            b = 255*math.sin(middle + theta[2])
            slice[2] = (r,g,b)

        # 3. Create and output color image
        color_image = np.empty((image.shape[0], image.shape[1], 3))

        # 4. Iterate through the image and assign colors to the color image based on which interval the intensity belongs to
        for i in range(image.shape[0]):
            for j in range(image.shape[1]):
                #print(image[i,j])
                color_image[i,j] = self.getColor(image[i,j], slices)

        # 5. return colored image
        return color_image



        

