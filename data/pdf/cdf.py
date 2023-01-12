import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv("data.csv")
dataset = df["disposition_days"].values
n = len(dataset)

x = np.sort(dataset)
y = np.arange(n)/float(n)

plt.xlabel('x-axis')
plt.ylabel('y-axis')

plt.title('CDF using sorting the data')
plt.plot(x, y, marker='o')
plt.show()
