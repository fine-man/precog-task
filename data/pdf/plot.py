import pandas as pd
from scipy.stats import norm
import numpy as np

df = pd.read_csv("data.csv")
data = list(df["disposition_days"])

# Fit a normal distribution to the data:
mu, std = norm.fit(data)
print(mu, std)

"""
# Plot the histogram.
plt.hist(data, bins=100, density=True, alpha=0.6, color='g')

# Plot the PDF.
xmin, xmax = plt.xlim()
x = np.linspace(xmin, xmax, 100)
p = norm.pdf(x, mu, std)
plt.plot(x, p, 'k', linewidth=2)
title = "Fit results: mu = %.2f,  std = %.2f" % (mu, std)
plt.title(title)

plt.show()
"""
