import numpy as np
import pandas as pd
import pickle
import matplotlib.pyplot as plt

# used for plotting random distributions (uses matplotlib underneath)
import seaborn as sns

# for fitting probability distributions to data
from fitter import Fitter, get_common_distributions, get_distributions

state_code = 26 # state code for Delhi

# loading the dataset
filename = f"./csv-files/days_{state_code}.csv"
dataset = pd.read_csv(filename)
print("loaded data.csv")

# paramter file
par_file = "parameter.pkl"

# filename to save the final png
save_filename = "./images/test.png"

# setting up the plot
sns.set_style('white')
sns.set_context('paper', font_scale=2)

# plotting the histogram
sns.displot(data=dataset, x="disposition_days", kind="hist", bins=500, aspect=1.5)

# finding the best fit curve
disposition_days = dataset["disposition_days"].values
good_distributations = ['betaprime', 'invgamma'] + get_common_distributions()

f = Fitter(disposition_days, timeout=120,
           distributions=['gamma'])

f.fit()
print(f.summary())
parameter_dict = f.get_best(method='sumsquare_error')

# writing the paramters to a file
with open(par_file, 'wb') as f:
    pickle.dump(parameter_dict, f)

print(parameter_dict)
print(f"saved parameters of best fit curve to {par_file}")
plt.savefig(save_filename)
print(f"saved the figure {save_filename}")
