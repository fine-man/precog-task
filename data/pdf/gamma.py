import numpy as np
from scipy.stats import gamma
import matplotlib.pyplot as plt
import pandas as pd

fig, ax = plt.subplots()

df = pd.read_csv("small_data.csv")
data = list(df["disposition_days"])
ax.hist(data, bins=250, density=True, ec='black', lw=0.5)

a = 0.6413976857345591
loc = 0.999999999999999999
scale = 103.82470434943471

x = np.linspace(gamma.ppf(0.01, a, loc, scale), gamma.ppf(0.99, a, loc, scale), 500)
print(x)
ax.plot(x, gamma.pdf(x, a, loc, scale), label='gamma pdf')
ax.legend()

ax.set_xlim(0, 500)
ax.set_ylim(0, 0.035)

ax.set_xlabel("disposition days")
ax.set_ylabel("probability density")
ax.set_title("Probability Density function for disposition days")
ax.grid(True)

plt.show()
