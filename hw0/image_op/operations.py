import numpy as np
import cv2


class Operation:

    def __init__(self):
        pass

    def merge(self, image_left, image_right, column):
        """
        Merge image_left and image_right at column (column)
        
        image_left: the input image 1
        image_right: the input image 2
        column: column at which the images should be merged

        returns the merged image at column
        """
        
        # add your code here

        merged = np.zeros(image_left.shape) #350 rows, 340 columns, with columns as subarrays in the rows
        for r in range(image_left.shape[0]):
            for c in range(image_left.shape[1]):
                if c < column: #use left image
                    merged[r][c] = image_left[r][c]
                else: #use right image
                    merged[r][c] = image_right[r][c]

        # Please do not change the structure
        return merged  # Currently the original image is returned, please replace this with the merged image

    def intensity_scaling(self, input_image, column, alpha, beta):
        """
        Scale your image intensity.

        input_image: the input image
        column: image column at which left section ends
        alpha: left half scaling constant
        beta: right half scaling constant

        return: output_image
        """
        # add your code here
        output_image = np.zeros(input_image.shape)  # 350 rows, 340 columns, with columns as subarrays in the rows
        for r in range(input_image.shape[0]):
            for c in range(input_image.shape[1]):
                if c < column:  # use left image
                    output_image[r][c] = input_image[r][c]*alpha
                else:  # use right image
                    output_image[r][c] = input_image[r][c]*beta
        # Please do not change the structure
        return output_image  # Currently the input image is returned, please replace this with the intensity scaled image

    def centralize_pixel(self, input_image, column):
        """
        Centralize your pixels (do not use np.mean)

        input_image: the input image
        column: image column at which left section ends

        return: output_image
        """

        # add your code here

        # first let's compute the offsets
        int_sum_left, int_sum_right = 0, 0
        left_count, right_count = 0, 0
        for r in range(input_image.shape[0]):
            for c in range(input_image.shape[1]):
                if c < column:  # use left image
                    int_sum_left += input_image[r][c]
                    left_count += 1
                else:  # use right image
                    int_sum_right += input_image[r][c]
                    right_count += 1
        #we don't want divide by 0 errors
        if left_count > 0:
            offset_left = 128 - (int_sum_left/left_count)
        else:
            offset_left = 0
        if right_count > 0:
            offset_right = 128 - (int_sum_right/right_count)
        else:
            offset_right = 0


        output_image = np.zeros(input_image.shape)  # 350 rows, 340 columns, with columns as subarrays in the rows
        for r in range(input_image.shape[0]):
            for c in range(input_image.shape[1]):
                if c < column:  # use left image
                    output_image[r][c] = input_image[r][c] + offset_left
                else:  # use right image
                    output_image[r][c] = input_image[r][c] + offset_right

        return output_image   # Currently the input image is returned, please replace this with the centralized image
