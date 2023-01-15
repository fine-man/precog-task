import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# used for plotting random distributions (uses matplotlib underneath)
import seaborn as sns

# for fitting probability distributions to data
from fitter import Fitter, get_common_distributions, get_distributions

dataset = pd.read_csv("small_data.csv")
print("loaded data.csv")

sns.set_style('white')
sns.set_context('paper', font_scale=2)

sns.displot(data=dataset, x="disposition_days", kind="hist", bins=250, aspect=1.5)

disposition_days = dataset["disposition_days"].values

good_distributations = ['betaprime', 'invgamma'] + get_common_distributions()

f = Fitter(disposition_days, timeout=120,
           distributions=get_common_distributions())

#['invgamma', 'betaprime', 'gamma', 'chi2']
#['gamma', 'lognorm', 'beta', 'burr', 'norm']

f.fit()
print(f.summary())
print(f.get_best(method='sumsquare_error'))

plt.savefig("test.png")
