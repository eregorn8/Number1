# -*- coding: utf-8 -*-
"""
Created on Mon Dec 28 13:02:01 2015

@author: Jonathan
"""

import numpy as np
import matplotlib.pyplot as plt
plt.clf()
N = 100;
# Lets do some tests. Make a random velocity field
#  Which is fourier smoothed...

vx = np.random.rand(N,N)-.5
vy = np.random.rand(N,N)-.5

vx_f = np.fft.fft2(vx)
vy_f = np.fft.fft2(vy)



# Make the Mask
mwidth = .5
dx,dy = np.meshgrid(np.linspace(-1,1,N),np.linspace(-1,1,N))
msk = np.exp(-(N/mwidth)*(dx**2 + dy**2))

vx = np.real(np.fft.ifft2(vx_f*np.fft.fftshift(msk)))
vy = np.real(np.fft.ifft2(vy_f*np.fft.fftshift(msk)))


vx = 0*np.sin(dx*10) + np.sin(dy*10)
vy = 0*np.cos(dy*10) + np.cos(dx*10)

# Calculate derivitive via F.T.




