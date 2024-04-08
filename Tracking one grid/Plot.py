import numpy as np
import matplotlib.pyplot as plt
 
file = []
file = (open("res.txt", "r")) #Endre filnavn så det stemmer med data fil
data = file.read().splitlines()
 
x,y,xn,yn = [],[],[],[]
 
for i in data:
    broken = i.split(",")
    xn = broken[0]
    x.append(float(xn))
    yn = broken[1]
    y.append(float(yn))
 
for i in range(len(x)):
    plt.plot(x[i],y[i],"o")
 
plt.grid()
plt.show()
 
file = []
file = (open("./Results/res2.txt", "r")) #Endre filnavn så det stemmer med data fil
data = file.read().splitlines()
 
x,y,xn,yn = [],[],[],[]
 
for i in data:
    broken = i.split(",")
    xn = broken[0]
    x.append(float(xn))
    yn = broken[1]
    y.append(float(yn))
 
for i in range(len(x)):
    plt.plot(x[i],y[i],"o")
 
plt.grid()
plt.show()