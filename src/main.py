import pandas as pd
import matplotlib.pyplot as plt
from sklearn import datasets
irisData = datasets.load_iris()
wineData = datasets.load_wine()
breastCancerData = datasets.load_breast_cancer()
import matplotlib.pyplot as plt
from myConvexHull import ConvexHull

# Minta input dataset
print("Pilih dataset yang ingin Anda gunakan!")
print("1. Dataset Iris")
print("2. Dataset Wine")
print("3. Dataset Breast Cancer")
while (True):
  n = int(input("Pilihan Anda: "))
  if (n >= 1 and n <= 3):
    break

# Set data sesuai input
data = None
if n == 1:
  data = irisData
elif n == 2:
  data = wineData
elif n == 3:
  data = breastCancerData

# Minta input x dan y
x = None; y = None
print("Pilih nomor fitur untuk nilai x dan y!")
for i in range(len(data.feature_names)):
  print(f'{i}. {data.feature_names[i]}')
while (True):
  x = int(input("Nomor fitur sebagai nilai x: "))
  if (x >= 0 and x < len(data.feature_names)):
    break
while (True):
  y = int(input("Nomor fitur sebagai nilai y: "))
  if (y >= 0 and y < len(data.feature_names)):
    break

# Tunjukkan head dari dataset
print("5 data pertama pada dataset yang Anda pilih:")
df = pd.DataFrame(data.data, columns=data.feature_names)
df['Target'] = pd.DataFrame(data.target)
print(df.head())

# Cetak convex hull
plt.figure(figsize = (10, 6))
colors = ['salmon', 'green', 'plum', 'aquamarine', 'grey', 'purple', 'azure', 'indigo', 'red', 'beige', 'ivory', 'aqua']
plt.title(f'{data.feature_names[y]} vs {data.feature_names[x]}')
plt.xlabel(data.feature_names[x])
plt.ylabel(data.feature_names[y])
for i in range(len(data.target_names)):
  bucket = df[df['Target'] == i]
  bucket = bucket.iloc[:,[x,y]].values
  hull = ConvexHull(bucket)
  plt.scatter(bucket[:, 0], bucket[:, 1], label=data.target_names[i], c=colors[i])
  for pair in hull:
    plt.plot([pair[0][0], pair[1][0]], [pair[0][1], pair[1][1]], colors[i])
plt.legend()
plt.show()