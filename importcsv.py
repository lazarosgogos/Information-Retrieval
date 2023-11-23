# -*- coding: utf-8 -*-
"""
Created on Sun Nov 19 10:38:37 2023

@author: KoEle
"""
import pandas as pd 

def opencsv(filename):
    return pd.read_csv(filename, delimiter=',', header='infer')
    
def writetodisk(dataset, filename):
    dataset.to_csv(filename, index=False)