import numpy as np

class Rle:
    def __init__(self):
        pass

    def encode_image(self,binary_image):
        """
        Compress the image
        takes as input:
        image: binary_image
        returns run length code
        """
        rle_code = []
        runCount = 0
        last = 255 # because we assume white to start with here we also must assume white to start with in decode
        for row in range(binary_image.shape[0]):
            for col in range(binary_image.shape[1]):
                if binary_image[row][col] == last:
                    runCount += 1
                else:
                    rle_code.append(runCount)
                    runCount = 1
                    last = binary_image[row][col]
        return rle_code

    def decode_image(self, rle_code, height, width):
        """
        Get original image from the rle_code
        takes as input:
        rle_code: the run length code to be decoded
        Height, width: height and width of the original image
        returns decoded binary image
        """
        bw = [0,255] #black and white
        i = True # start with white because we assumed we start with white in encode
        n = 0 #index for rle_code
        bin_im = np.array([[None]*width]*height)
        for row in range(bin_im.shape[0]):
            for col in range(bin_im.shape[1]):
                if rle_code[n] == 0:
                    n += 1
                    i = not i
                bin_im[row][col] = bw[i]
                if n < len(rle_code)-1: rle_code[n] -= 1
        bin_im = np.array(bin_im, np.uint8)

        return bin_im  # replace zeros with image reconstructed from rle_Code





        




