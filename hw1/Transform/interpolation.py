class interpolation:

    def linear_interpolation(self,x,x1,I_x1,x2,I_x2):
        """Computes the linear interpolation value at some iD location x between two 1D points (Pt1 and Pt2).
        
        There are no arguments defined in the function definition on purpose. It is left upto the student to define any requierd arguments.
        Please change the signature of the function and add the arguments based on your implementation.
        
        The function ideally takes two 1D points Pt1 and Pt2, and their intensitites I(Pt1), I(Pt2).
        return the interpolated intensity value (I(x)) at location x """

        # Write your code for linear interpolation here
        # I_x = m*x + b
        #             b = I_x1 - m*x1
        # I_x2 = m*x2 +   I_x1 - m*x1 = m(x2-x1) + I_x1
        # m = (I_x2 - I_x1)/(x2 - x1)

        # m = (I_x2 - I_x1)/(x2 - x1)
        # b = I_x1 - m*x1
        # return m*x + b

        #return I_x1 + (I_x2-I_x1)*((x-x1)/(x2-x1))
        return I_x1*(x2-x)/(x2-x1) + I_x2*(x-x1)/(x2-x1)

    def bilinear_interpolation(self,p,p1,I_p1,p2,I_p2,p3,I_p3,p4,I_p4):

        """Computes the bi linear interpolation value at some 2D location x between four 2D points (Pt1, Pt2, Pt3, and Pt4).
        
        There are no arguments defined in the function definition on purpose. It is left upto the student to define any requierd arguments.
        Please change the signature of the function and add the arguments based on your implementation.
        
        The function ideally takes four 2D points Pt1, Pt2, Pt3, and Pt4, and their intensitites I(Pt1), I(Pt2), I(Pt3), and I(Pt4).
        return the interpolated intensity value (I(x)) at location x """

        # Write your code for bilinear interpolation here
        # Recall that bilinear interpolation performs linear interpolation three times
        # Please reuse or call linear interpolation method three times by passing the appropriate parameters to compute this task
        
        y = p[1] #input for our first set of interpolations
        Itop = self.linear_interpolation(y,p1[1],I_p1,p2[1],I_p2) #Itop as a function of the x coord
        Ibot = self.linear_interpolation(y,p3[1],I_p3,p4[1],I_p4) #Ibot as a function of the x coord
        x = p[0]
        I = self.linear_interpolation(x,p1[0],Itop,p3[0],Ibot) #I as a function of the y coord and (implicitly) as a function of the x coord
        return I

