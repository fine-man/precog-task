import numpy as np
from scipy.stats import gamma
from scipy.stats import expon
from scipy.stats import invgamma
import matplotlib.pyplot as plt
import pandas as pd

fig, ax = plt.subplots()

filepath = "small_data.csv"
df = pd.read_csv(filepath)
print(f"loaded {filepath}")
data = list(df["disposition_days"])

ax.hist(data, bins=500, density=True, ec='black', lw=0.5)
print("histogram prepared. Finding best fit curve now ...")

a = 0.5731919169613173
loc = 0.999999999999999999
scale = 145.42211799619184

x = np.linspace(gamma.ppf(0.01, a, loc, scale), gamma.ppf(0.99, a, loc, scale), 500)
ax.plot(x, gamma.pdf(x, a, loc, scale), label='gamma pdf')

print("Best fit curve prepared")
ax.legend()

ax.set_xlim(0, 500)
ax.set_ylim(0, 0.04)

ax.set_xlabel("disposition days")
ax.set_ylabel("probability density")
ax.set_title("Best Fit Probability Density Function for Disposition Days (2018)")
ax.grid(True)

plt.show()
