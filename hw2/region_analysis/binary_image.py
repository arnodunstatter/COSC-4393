import cv2
class BinaryImage:
    def __init__(self):
        pass

    def compute_histogram(self, image):
        """Computes the histogram of the input image
        takes as input:
        image: a grey scale image
        returns a histogram as a list"""

        hist = [0]*256
        for row in range(image.shape[0]):
            for col in range(image.shape[1]):
                hist[image[row][col]] += 1

        return hist

    def find_otsu_threshold(self, hist):
        """analyses a histogram it to find the otsu's threshold assuming that the input hstogram is bimodal histogram
        takes as input
        hist: a bimodal histogram
        returns: an optimal threshold value (otsu's threshold)"""
        def w(start,end): #both are inclusive
            #let's get our divisor, totalPixels
            totalPixels = sum(hist)
            #now let's get our w (the sum of probabilities) to return
            w = 0
            for i in range(start,end+1):
                w += hist[i]/totalPixels
            return w

        def var(section): #section is an array representing a section of the historgram
            variance = 0
            n = sum(section)
            mean = sum([i*section[i] for i in range(len(section))])/n #computes the mean of a histogram, assuming lowest values of the hist are between 0 and len(hist)-1
            for i in range(len(section)):
                variance += ((i - mean)**2)*section[i]
            return variance/n

        threshold = 0
        best = None
        for t in range(0,256): #t is the proposed intensity threshold
            try:
                wsicv = w(0,t)*var(hist[:t+1])+w(t+1,255)*var(hist[t+1:]) #Weighted Sum of Intra-class Variance
            except: pass
            else:
                if best is None or best > wsicv:
                    threshold, best = t, wsicv

        return threshold

    def binarize(self, image):
        """Comptues the binary image of the the input image based on histogram analysis and thresholding
        take as input
        image: an grey scale image
        returns: a binary image"""
        # I don't want to edit the signature or the dip_hw2_region_analysis.py file, so i'm just going to call the relevant functions in here
        hist = self.compute_histogram(image)
        threshold = self.find_otsu_threshold(hist)
        bin_img = image.copy()
        for row in range(image.shape[0]):
            for col in range(image.shape[1]):
                if bin_img[row][col] <= threshold: bin_img[row][col] = 0
                else: bin_img[row][col] = 255
        return bin_img


