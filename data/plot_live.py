import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.animation import FuncAnimation


df = pd.read_csv('data/07.17.2023/16.28.csv')


#line1 = ax.scatter(df['Desired Position: x (m)'], df['Desired Position: x (m)')
#line2 = ax.scatter(df['Actual Position: x (m)'],df['Actual Position: y (m)'])
#line3 = ax.scatter(df['Fish Position: x (m)'], df['Fish Position: y (m)'])

dt = 0.005
n=20
L = 1
particles=np.zeros(n,dtype=[("position", float , 2),
                           ("velocity", float ,2),
                           ("force", float ,2),
                           ("size", float , 1)])

particles["position"]=np.random.uniform(0,L,(n,2));
particles["velocity"]=np.zeros((n,2));
particles["size"]=0.5*np.ones(n);

fig = plt.figure(figsize=(7,7))
ax = plt.axes(xlim=(0,L),ylim=(0,L))
scatter=ax.scatter(particles["position"][:,0], particles["position"][:,1])

def update(frame_number):
   particles["force"]=np.random.uniform(-2,2.,(n,2));
   particles["velocity"] = particles["velocity"] + particles["force"]*dt
   particles["position"] = particles["position"] + particles["velocity"]*dt

   particles["position"] = particles["position"]%L
   scatter.set_offsets(particles["position"])
   return scatter,

anim = FuncAnimation(fig, update, interval=10)
plt.show()