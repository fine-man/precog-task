import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt
import pandas as pd


df = pd.read_csv("small_data.csv")
data = list(df["disposition_days"])

# Fit a normal distribution to the data:
mu, std = norm.fit(data)

fig, ax = plt.subplots()

# Plot the histogram.
ax.hist(data, bins=1000, density=True, alpha=0.6, color='g')
ax.set_xlabel("Mean decision days")
ax.set_ylabel("Probability Density")

# Plot the PDF.
xmin, xmax = (0, 500)
#xmin, xmax = plt.xlim()
print(xmin, xmax)
x = np.linspace(xmin, xmax, 100)
p = norm.pdf(x, mu, std)
ax.plot(x, p, 'k', linewidth=2)
title = "Fit results: mu = %.2f,  std = %.2f" % (mu, std)
ax.set_title(title)

plt.show()
