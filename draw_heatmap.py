# -*- coding: utf-8 -*-
"""
Created on Mon May 21 10:29:53 2018

@author: USER
"""
from matplotlib import cm 
import matplotlib.pyplot as plt
   
def heatmap(data,ylabels,wight):  
    #cmap=cm.Blues      
    cmap=cm.get_cmap('rainbow',1000)  
    figure=plt.figure(facecolor='w',figsize=(20,(wight*0.2)))  
    ax=figure.add_subplot(1,1,1,position=[0.1,0.15,0.8,0.8])  
    ax.set_yticks(range(len(ylabels)))  
    ax.set_yticklabels(ylabels,fontsize=8)    
    vmax=data[0][0]  
    vmin=data[0][0]  
    for i in data:  
        for j in i:  
            if j>vmax:  
                vmax=j  
            if j<vmin:  
                vmin=j  
    map=ax.imshow(data,interpolation='nearest',cmap=cmap,aspect='auto',vmin=vmin,vmax=vmax)  
    cb=plt.colorbar(mappable=map,cax=None,ax=None,shrink=0.7)  
    cb.set_clim(1, 30)
    plt.show()