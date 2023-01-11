import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt
import pandas as pd


df = pd.read_csv("data.csv")
data = list(df["disposition_days"])

# Fit a normal distribution to the data:
mu, std = norm.fit(data)

# Plot the histogram.
plt.hist(data, bins=100, density=True, alpha=0.6, color='g')

# Plot the PDF.
xmin, xmax = (0, 500)
#xmin, xmax = plt.xlim()
print(xmin, xmax)
x = np.linspace(xmin, xmax, 100)
p = norm.pdf(x, mu, std)
plt.plot(x, p, 'k', linewidth=2)
title = "Fit results: mu = %.2f,  std = %.2f" % (mu, std)
plt.title(title)
plt.show()
