#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  3 11:25:57 2019

@author: gather3
"""
import pandas as pd
import folium
from folium import plugins

import plotly.graph_objects as go

class Statistics():
    def __init__(self,dataset, columns):
        self.data = dataset
        self.columns = columns
        
        
    def generateStats(self):
        return self.data.describe()
    
class Map():
    def __init__(self, dataset, colour = 0, legend = 0, labels = 0, hoverData = 0, location = (None, None)):
        self.map = folium.Map(tiles='Stamen Terrain')
        self.data = dataset
        self.colour = colour
        self.legend = legend
        self.labels = labels
        self.hoverData = hoverData
        self.location = location
        
    def createMap(self):
        mc = plugins.MarkerCluster()
        
        for index, location in self.data.iterrows():
            mc.add_child(folium.Marker([location['latitude'], location['longitude']])).add_to(self.map)
            
        self.map.save('test.html')
        return self.map
# Still have to update this map for django         
class Plot():
    def __init__(self, dataset, xLabel, yLabel, color = None, hover = list(), labels = dict()):
        self.data = dataset
        self.xLabel = xLabel
        self.yLabel = yLabel
        self.color = color
        self.hover = hover
        self.labels = labels
        
    # =============================================================================
    # # Create plotly functions to generate the graphs
    # =============================================================================

    # General plot
    def __str__(self):
        return f'x Label: {self.xLabel}'+ "\n" + f'y Label: {self.yLabel}' + "\n" + \
    f'Color: {self.color}' +"\n" + f'Hover: {self.hover}' +"\n" + f'Labels: {self.labels}'
    
    def plot_all(self, function):
        try:
            for df in self.data:
                self.__plot(self.data,function, self.xLabel, self.yLabel, self.color, self.hover, self.labels)
        except ValueError as e:
            print(e)
            print(f'Showing only the ones that mathces the requirement')
            pass
    
    def __plot(self, df, function, x_label,y_label, color = 'Team', hover = (), labels = {}):
        
        fig = go.Figure()
        
        fig.add_trace(function(x=file[x_label], y = file[y_label]))
        fig.write_image("fig1.png")
        
    def plotByIndex(self, index, function):
        self.__plot(self.data[index], self.xLabel,self.yLabel,self.color,self.hover, self.labels)
        


if __name__ == '__main__':
    
    file = pd.read_csv("Risk_Toilets_Final.csv")
    m = Map(file)
    
    m.createMap()
    
    p = Plot(file, 'storage_ty', 'last_clean')
    
    p.plot_all(go.Bar)