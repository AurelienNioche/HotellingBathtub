import numpy as np


a = np.random.random(size=(2, 10**6))
print(np.mean(np.absolute(a[0] - a[1])))