import matplotlib.pyplot as plt
from scipy.interpolate import KroghInterpolator
import numpy as np

x=range(-20,20)
y=[]
for i in x:
    y.append((i**2)+25)

x=x[1::5]
y=y[1::5]

f=KroghInterpolator(x,y)
xfine=np.arange(min(x),max(x),.5)
yfine=f(xfine)

val_interp=min(yfine)
print (val_interp)

plt.scatter(x,y)
plt.plot(xfine, yfine)
plt.show()
