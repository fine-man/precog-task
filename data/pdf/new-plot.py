import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import norm


# Fit Gaussian distribution and plot
sns.distplot(data, fit=norm, kde=False)
