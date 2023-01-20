import numpy as np
from scipy.stats import gamma
from scipy.stats import expon
from scipy.stats import invgamma
import matplotlib.pyplot as plt
import pandas as pd
import pickle

fig, ax = plt.subplots()

year = 26 # state code for Delhi

filepath = f"./csv-files/days_{year}.csv"

# parameters file
par_file = "parameter.pkl"

save_filepath = "./images/pdf.png"

# loading the dataset for histogram
df = pd.read_csv(filepath)
print(f"loaded {filepath}")
data = list(df["disposition_days"])

# plotting the histogram
ax.hist(data, bins=500, density=True, ec='black', lw=0.5)
print("histogram prepared. Finding best fit curve now ...")

# reading the parameter
with open(par_file, "rb") as f:
    par_dict = pickle.load(f)

par_dict = par_dict['gamma']
a = par_dict['a']
loc = par_dict['loc']
scale = par_dict['scale']

x = np.linspace(gamma.ppf(0.01, a, loc, scale), gamma.ppf(0.99, a, loc, scale), 500)
ax.plot(x, gamma.pdf(x, a, loc, scale), label='gamma pdf')

print("Best fit curve prepared")
ax.legend()

ax.set_xlim(0, 500)
ax.set_ylim(0, 0.04)

ax.set_xlabel("Disposition Days")
ax.set_ylabel("Probability Density")
ax.set_title("Best Fit Probability Density Function for Disposition Days of all {year} Cases")
ax.grid(True)

# showing the plot and saving it to a file
#plt.savefig(save_filepath)
#print(f"Best fit curve graph has been saved to {save_filepath}")
plt.show()
