from .interpolation import interpolation
import math
import numpy as np

class Geometric:
    def __init__(self):
        pass

    def forward_rotate(self, image, theta):
        """Computes the forward rotated image by an angle theta
                image: input image
                theta: angle to rotate the image by (in radians)
                return the rotated image"""
        # 1. Compute Rotation matrix
        def counterClockwise(p,theta): #the basic operation
            x,y = p[0],p[1]
            return (math.cos(theta)*x - math.sin(theta)*y , math.sin(theta)*x+math.cos(theta)*y)

        # 2. Rotate Corners
        #first get new positions of four corners and use to calculate new size
        rows, cols = image.shape
        originalCorners = [(row,col) for row in (0,rows) for col in (0,cols)]
        newCorners = [counterClockwise(p,theta) for p in originalCorners]
        minX = min(newCorners,key=lambda p:p[0])[0]
        maxX = max(newCorners,key=lambda p:p[0])[0]
        Rrows =  int(maxX - minX)
        minY = min(newCorners,key=lambda p:p[1])[1]
        maxY = max(newCorners,key=lambda p:p[1])[1]
        Rcols = int(maxY - minY)
    
        # 3. Create Rotated Image, R of size (rows,cols)
        R = np.empty((Rrows,Rcols)) #black background

        # 4. Fill in R from values in image
        for row in range(rows):
            for col in range(cols):
                Rrow, Rcol = counterClockwise((row,col),theta)
                Rrow, Rcol = int(Rrow-minX), int(Rcol-minY)
                if Rrow < Rrows and Rcol < Rcols:
                    R[Rrow,Rcol] = image[row,col]
        return R

    def reverse_rotation(self, rotated_image, theta, origin, original_shape):
        """Computes the reverse rotated image by an angle theta
                rotated_image: the rotated image from previous step
                theta: angle to rotate the image by (in radians)
                Origin: origin of the original image with respect to the rotated image
                Original shape: shape of the orginal image
                return the original image"""
        # 1. Compute inverse rotation matrix
        def clockwise(p, theta):
            x,y = p[0],p[1]
            return (math.cos(theta)*x + math.sin(theta)*y , -math.sin(theta)*x+math.cos(theta)*y)

        # 2. Create image I of original shape
        I = np.empty(original_shape)

        # 3. For Rrow,Rcol in rotated image calculate location with respect to origin
        R = rotated_image
        for Rrow in range(rotated_image.shape[0]):
            for Rcol in range(rotated_image.shape[1]):

                r = Rrow - origin[0]
                c = Rcol - origin[1]
                row, col = clockwise((r,c),theta)
                row,col = int(row),int(col)

                #print(Rrow,Rcol,"->",r,c,"->",row,col)
                if row > -1 and row < 256 and col > -1 and col < 256:
                    I[int(row),int(col)] = R[Rrow,Rcol]
        return I
        
    def rotate(self, image, theta, interpolation_type):
        """Computes the forward rotated image by an angle theta using interpolation
                image: the input image
                theta: angle to rotate the image by (in radians)
                interpolation_type: type of interpolation to use (nearest_neighbor, bilinear)
                return the original image"""
        # class inputError(BaseException):
        #     print(f"rotate received interpolation_type='{interpolation_type}' which is not acceptable.")
        #     print("please fix the code such that interpolatin_type receives either 'nearest_neighbor' or 'bilinear'")
        # if interpolation_type != "nearest_neighbor" and interpolation_type != "bilinear":
        #     raise(inputError)
        if "bilinear"==interpolation_type:
            interpolater = interpolation()
        # 1. Compute Rotation matrix
        def counterClockwise(p,theta): #the basic operation
            x,y = p[0],p[1]
            return (math.cos(theta)*x - math.sin(theta)*y , math.sin(theta)*x+math.cos(theta)*y)

        # 2. Compute the Inverse Rotation matrix
        def clockwise(p, theta):
            x,y = p[0],p[1]
            return (math.cos(theta)*x + math.sin(theta)*y , -math.sin(theta)*x+math.cos(theta)*y)

        # 3. Compute size of the rotated image
        numRows, numCols = image.shape
        originalCorners = [(row,col) for row in (0,numRows) for col in (0,numCols)]
        newCorners = [counterClockwise(p,theta) for p in originalCorners]
        minX = min(newCorners,key=lambda p:p[0])[0]
        maxX = max(newCorners,key=lambda p:p[0])[0]
        numRrows =  int(maxX - minX)
        minY = min(newCorners,key=lambda p:p[1])[1]
        maxY = max(newCorners,key=lambda p:p[1])[1]
        numRcols = int(maxY - minY)

        # 4. Create rotated image, R, of size (numRows, numCols)
        R = np.zeros((numRrows,numRcols))
        # 5. Calculate location O with respect to N
        O = (-minX,-minY) # where minX and minY are computed from the 4 newCorners

        # 6. For Rrow,Rcol in R - i.e. for i'_N, j'_N in R
        for Rrow in range(R.shape[0]):
            for Rcol in range(R.shape[1]):
        #       6.1 Calculate location with respect to origin
                r,c = Rrow-O[0],Rcol-O[1] ############################################# he did -O in the notes but this seemed wrong to me. If yours bugs, try -O instead
        #       6.2 Compute inverse rotation on (r,c) to get row,col
                row,col = clockwise((r,c),theta)
                row,col = row,col
                if 0 < row < 255 and 0 < col < 255:
                    if interpolation_type == "nearest_neighbor":
                        R[Rrow,Rcol]=image[(int(row),int(col))]           
                    elif interpolation_type == "bilinear":
                    #       6.3 Bilinear interpolation
                    #           6.3.1 Find four nearest neighbors to (row,col)
                        # p1 = (row-1,col-1)
                        # p2 = (row-1,col+1)
                        # p3 = (row+1,col-1)
                        # p4 = (row+1,col+1)
                        p1 = (math.floor(row),math.floor(col))
                        p2 = (math.floor(row),math.ceil(col))
                        p3 = (math.ceil(row),math.floor(col))
                        p4 = (math.ceil(row),math.ceil(col))
                        R[Rrow,Rcol] = interpolater.bilinear_interpolation((row,col),p1,image[p1],p2,image[p2],p3,image[p3],p4,image[p4])



        #nan appraoch
        #                 if isinstance(row,int) and isinstance(col,int):
        #                     R[Rrow,R] = image[row,col]
        #                 else:
        #                     R[Rrow,Rcol] = np.NaN
        # # 6.3.2 Obtain bi-linear interpolated value b
        # if interpolation_type == "bilinear": 
        #     for Rrow in range(R.shape[0]):
        #         for Rcol in range(r.shape[1]):
        #             if np.isnan(R[Rrow,Rcol]):

        # 6.3.3 R(Rrow,Rcol) = b


        return R


