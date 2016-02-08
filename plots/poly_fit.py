from numpy.polynomial import Polynomial
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
import sys

try:
    num = float(sys.argv[1])
    num = np.clip(num, 2.6, 42)
except:
    num = 42

x = np.array([2.6, 16.4, 20.9, 24.6, 26.7,
            29.5, 32, 33.85, 35.5, 36.5, 42])
y = np.array([0, 4, 8, 12, 16,
            20, 24, 28, 32, 36, 40])

p = Polynomial.fit(x, y, 2)
plt.plot(*p.linspace(), linewidth=1.5)
plt.plot(x, y, 'ro')
conv = interp1d(*p.linspace())
print np.clip(conv(num), 0, 40)
plt.title('$Least\,squares\,fitting\,of\,power$\n$measurement,\,based\,on\,error$')
plt.xlabel('$Measured\,power\,(W)$')
plt.ylabel('$Expected\,power\,(W)$')
plt.show()
