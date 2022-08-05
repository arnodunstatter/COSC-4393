# For this part of the assignment, please implement your own code for all computations,
# Do not use inbuilt functions like fft from either numpy, opencv or other libraries
import numpy as np
import math


class Dft:
    def __init__(self):
        pass

    def eulersRule(self, u,i,N,v,j,M=None,sign=-1):
        if M==None: M=N
        pi = math.pi
        c = 1j #complex number
        x = 2*pi*((u*i/N)+(v*j/M))
        return math.cos(x)+sign*c*math.sin(x)

    def forward_transform(self, matrix):
        """Computes the forward Fourier transform of the input matrix
        takes as input:
        matrix: a 2d matrix
        returns a complex matrix representing fourier transform"""
        f = matrix
        N,M = f.shape
        F = np.zeros((N,M), complex)
        for u in range(N):
            for v in range(M):
                F[u,v] = sum([sum([f[i,j]*self.eulersRule(u,i,N,v,j,M) for j in range(M)]) for i in range(N)])
        return F

    def inverse_transform(self, matrix):
        """Computes the inverse Fourier transform of the input matrix
        You can implement the inverse transform formula with or without the normalizing factor.
        Both formulas are accepted.
        takes as input:
        matrix: a 2d matrix (DFT) usually complex
        returns a complex matrix representing the inverse fourier transform"""
        F = matrix
        N,M = F.shape
        f = np.zeros((N,M), complex)
        for i in range(N):
            for j in range(M):
                f[i,j] = sum([sum([F[u,v]*self.eulersRule(i,u,N,j,v,M, sign=1) for v in range(M)]) for u in range(N)])
        return f*1/N*1/M
    

    def magnitude(self, matrix):
        """Computes the magnitude of the input matrix (iDFT)
        takes as input:
        matrix: a 2d matrix
        returns a matrix representing magnitude of the complex matrix"""
        F=matrix
        N,M = F.shape
        mag = np.zeros((N,M))
        for i in range(N):
            for j in range(M):
                mag[i,j] = float(math.sqrt(F[i,j].real**2+F[i,j].imag**2))
        #mag_compressed_unit8 = np.array(np.log(mag), dtype=np.uint8)
        return mag #_compressed_unit8