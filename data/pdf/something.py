import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats
import math

mu = 85.68
sigma = 118.53
x = np.linspace(mu - 3*sigma, mu + 3*sigma, 100)
plt.plot(x, stats.norm.pdf(x, mu, sigma))
plt.show()
