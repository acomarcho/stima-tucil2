import numpy as np

def isPointLEThanPoint(p1, p2):
  '''
    p1 dan p2 adalah list [x, y]
    p1 dikatakan <= p2 jika
    p1.x < p2.x atau p1.x = p2.x dan p1.y <= p2.y
  '''
  if (p1[0] < p2[0]):
    return True
  elif (p1[0] > p2[0]):
    return False
  else:
    return p1[1] <= p2[1]

def isPointGEThanPoint(p1, p2):
  '''
    p1 dan p2 adalah list [x, y]
    p1 dikatakan >= p2 jika
    p1.x > p2.x atau p1.x = p2.x dan p1.y >= p2.y
  '''
  if (p1[0] > p2[0]):
    return True
  elif (p1[0] < p2[0]):
    return False
  else:
    return p1[1] >= p2[1]

def partition(bucket, start, end):
  '''
    Implementasi partisi titik-titik pada bucket
    menggunakan metode quicksort.
    Mengembalikan index akhir dari partisi pertama.
  '''
  pivot = bucket[(start + end) // 2]
  p = start
  q = end
  while (True):
    # Cari lokasi yang benar untuk p
    while (not isPointGEThanPoint(bucket[p], pivot)):
      p += 1
    # Cari lokasi yang benar untuk q
    while (not isPointLEThanPoint(bucket[q], pivot)):
      q -= 1
    # Apabila p < q, lakukan swap
    if (p < q):
      tmp = bucket[p]
      bucket[p] = bucket[q]
      bucket[q] = tmp
      # Lanjutkan iterasi untuk p += 1 dan q -= 1
      p += 1
      q -= 1
    else:
      # Looping berakhir
      break
  return q

def sortBucket(bucket, start, end):
  '''
    Implementasi quicksort pada bucket.
  '''
  if (start < end):
    # Sorting hanya dilakukan jika start < end
    k = partition(bucket, start, end)
    sortBucket(bucket, start, k)
    sortBucket(bucket, k + 1, end)

def isPointAboveLine(p1, p2, p):
  '''
    Mengecek apakah p ada di atas p1p2
    Dengan dasar persamaan
    y = mx + c => c = y - mx
    apakah y0 > m*x0 + c?
  '''
  if (p2[0] != p1[0]):
    m = (p2[1] - p1[1]) / (p2[0] - p1[0])
    c = p1[1] - m * p1[0]
    return p[1] > m*p[0] + c
  else:
    return False

def isPointBelowLine(p1, p2, p):
  '''
    Mengecek apakah p ada di atas p1p2
    Dengan dasar persamaan
    y = mx + c => c = y - mx
    apakah y0 < m*x0 + c?
  '''
  if (p2[0] != p1[0]):
    m = (p2[1] - p1[1]) / (p2[0] - p1[0])
    c = p1[1] - m * p1[0]
    return p[1] < m*p[0] + c
  else:
    return False

def dividePointsByLine(p1, p2, bucket):
  '''
    Mengembalikan tupel (s1, s2)
    di mana s1 adalah titik-titik pada bucket yang berada di atas garis p1p2
    dan s2 adalah titik-titik pada bucket yang berada di bawah garis p1p2
  '''
  s1 = []
  s2 = []
  for p in bucket:
    if isPointAboveLine(p1, p2, p):
      s1.append(p)
    elif isPointBelowLine(p1, p2, p):
      s2.append(p)
  return (s1, s2)

def getDistanceToLine(p1, p2, p):
  '''
    Mencari jarak dari titik p ke garis p1p2
  '''
  # Bentuk persamaan garis Ax + By + C = 0
  A = p1[1] - p2[1]
  B = p2[0] - p1[0]
  C = p1[0]*p2[1] - p2[0]*p1[1]
  return (abs(A*p[0] + B*p[1] + C))/((A ** 2 + B ** 2) ** (1/2))

def convexHullAbove(p1, p2, s, hullPairs):
  '''
    Algoritma convex hull untuk daerah atas
  '''
  if (len(s) > 0):
    # Cari titik terjauh terhadap garis p1p2 dari s
    maxDist = None
    maxP = None
    maxPIdx = None
    for i, p in enumerate(s):
      if maxDist == None:
        maxDist = getDistanceToLine(p1, p2, p)
        maxP = p
        maxPIdx = i
      else:
        if (getDistanceToLine(p1, p2, p) > maxDist):
          maxDist = getDistanceToLine(p1, p2, p)
          maxP = p
          maxPIdx = i
    # Hapus dari s
    s.pop(maxPIdx)
    # Bagi daerah untuk diconquer secara rekursif
    above1, below1 = dividePointsByLine(p1, maxP, s)
    above2, below2 = dividePointsByLine(p2, maxP, s)
    # Penambahan ke hullPairs jika ada daerah yang kosong
    if len(above1) == 0:
      hullPairs.append([p1, maxP])
    if len(above2) == 0:
      hullPairs.append([p2, maxP])
    # Conquer
    convexHullAbove(p1, maxP, above1, hullPairs)
    convexHullAbove(p2, maxP, above2, hullPairs)

def convexHullBelow(p1, p2, s, hullPairs):
  '''
    Algoritma convex hull untuk daerah bawah
  '''
  if (len(s) > 0):
    # Cari titik terjauh terhadap garis p1p2 dari s
    maxDist = None
    maxP = None
    maxPIdx = None
    for i, p in enumerate(s):
      if maxDist == None:
        maxDist = getDistanceToLine(p1, p2, p)
        maxP = p
        maxPIdx = i
      else:
        if (getDistanceToLine(p1, p2, p) > maxDist):
          maxDist = getDistanceToLine(p1, p2, p)
          maxP = p
          maxPIdx = i
    # Hapus dari s
    s.pop(maxPIdx)
    # Bagi daerah untuk diconquer secara rekursif
    above1, below1 = dividePointsByLine(p1, maxP, s)
    above2, below2 = dividePointsByLine(p2, maxP, s)
    # Penambahan ke hullPairs jika ada daerah yang kosong
    if len(below1) == 0:
      hullPairs.append([p1, maxP])
    if len(below2) == 0:
      hullPairs.append([p2, maxP])
    # Conquer
    convexHullBelow(p1, maxP, below1, hullPairs)
    convexHullBelow(p2, maxP, below2, hullPairs)

def ConvexHull(bucket):
  '''
    Mengembalikan hullPairs, yaitu list of [point1, point2]
    di mana point1 dan point2 sendiri merupakan list [x, y]
    untuk nantinya diplot.
  '''
  myBucket = bucket.tolist()
  hullPairs = []
  # Kasus 'sederhana' yaitu di bucket hanya ada satu atau dua titik.
  # Dalam kasus ini, cukup hubungkan dua garis tersebut.
  if len(myBucket) == 1:
    return [[myBucket[0], myBucket[0]]]
  if len(bucket) == 2:
    return [[myBucket[0], myBucket[1]]]
  # Dalam realisasinya, perlu melakukan sorting dahulu terhadap bucket.
  # Bucket diurutkan berdasarkan absis menaik, jika absis sama, berdasarkan ordinat menaik.
  # Implementasinya menggunakan quickSort sendiri.
  sortBucket(myBucket, 0, len(myBucket) - 1)
  # Masukkan titik pertama dan titik terakhir ke dalam hullPairs
  p1 = myBucket[0]; pn = myBucket[-1]
  # Hapus dari titik-titik yang ada
  myBucket.pop(0); myBucket.pop(-1)
  # Bagi menjadi dua daerah: s1 (titik-titik di atas garis) dan s2 (titik-titik di bawah garis)
  s1, s2 = dividePointsByLine(p1, pn, myBucket)
  # Bila ada satu daerah yang kosong, maka masukkan pair ke dalam hullPairs
  if len(s1) == 0 or len(s2) == 0:
    hullPairs.append([p1, pn])
  # Kerjakan dengan divide and conquer
  convexHullAbove(p1, pn, s1, hullPairs)
  convexHullBelow(p1, pn, s2, hullPairs)
  return hullPairs
