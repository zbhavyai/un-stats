import numpy as np
import pandas as pd
import os 

print('hello')
print(os.getcwd())
codes = pd.read_excel('UN Codes.xlsx')
pop_data1 = pd.read_excel('UN Population Dataset 1.xlsx')
pop_data2 = pd.read_excel('UN Population Dataset 2.xlsx')

display('codes.head()', 'pop_data1.head()', 'pop_data2.head()')