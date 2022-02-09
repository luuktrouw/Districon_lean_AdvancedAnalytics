import numpy as np
import matplotlib.pyplot as plt


a = np.random.normal(3,1,10000000)


plt.hist(a, bins=5000)
plt.show()