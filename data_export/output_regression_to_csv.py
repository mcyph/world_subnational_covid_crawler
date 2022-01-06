import numpy.polynomial.polynomial as poly
import pandas as pd
import numpy as np

import matplotlib.pyplot as plt

df = pd.DataFrame([[i for i in range(2000,2018)],
[23.0,27.5,46.0,56.0,64.8,71.2,80.2,98.0,113.0,155.8,414.0,2297.8,3628.4,16187.8,25197.8,42987.8,77555.5,130631.9]])
df = df.T
df.columns = ['Year', 'Values']
df['Year'] = df['Year'].astype(int)
df['Values'] = df['Values'].astype(int)
no_of_predictions = 5


X = np.array(df.Year, dtype = float)
y = np.array(df.Values, dtype = float)
Z = [2019,2020,2021,2022]
coefs = poly.polyfit(X, y, 4)
X_new = np.linspace(X[0], X[-1]+no_of_predictions, num=len(X)+no_of_predictions)
ffit = poly.polyval(X_new, coefs)
pred = poly.polyval(Z, coefs)
predictions = pd.DataFrame(Z,pred)
print(predictions)
plt.plot(X, y, 'ro', label="Original data")
plt.plot(X_new, ffit, label = "Fitted data")
plt.legend(loc='upper left')
plt.show()
