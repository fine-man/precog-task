import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from fitter import Fitter, get_common_distributions, get_distributions

dataset = pd.read_csv("data.csv")

sns.set_style('white')
sns.set_context('paper', font_scale=2)

sns.displot(data=dataset, x="disposition_days", kind="hist", bins=10000, aspect=1.5)
disposition_days = dataset["disposition_days"].values

good_distributations = ['betaprime', 'invgamma'] + get_common_distributions()

f = Fitter(disposition_days, xmin=0, xmax=500, distributions=['invgamma'])
#['invgamma', 'betaprime', 'gamma', 'chi2']

#['gamma', 'lognorm', 'beta', 'burr', 'norm']

f.fit()
print(f.summary())
print(f.get_best(method='sumsquare_error'))
plt.show()
