
import pandas as pd
import numpy as np
import csv
import matplotlib.pyplot as plt

# referenced: https://www.tutorialspoint.com/how-to-plot-csv-data-using-matplotlib-and-pandas-in-python on 6/12/23
#              https://www.statology.org/pandas-plot-multiple-series/ on 6/13/23
#              https://stackoverflow.com/questions/44970881/matplotlib-multiple-scatter-subplots-with-shared-colour-bar

## Choose CSV file to read for plotting
df = pd.read_csv('data/backup07.21.2023/10.59.csv') # read csv file from data folder. Ex: 'data/06.13.2023/13.17.csv' reads the 13.17.csv file from the 06.13.2023 subfolder inside data folder
# print(df['Desired Position: y (m)'])
# for col in df.columns:
#     print(col)

print(df)


t = [pos for pos in df['robot states']]   

# print(t)
# print(len(t))
# print(type(t[0]))
# print(t[0])

'''
for object in t:
    print('break')
    print(object)
'''

    
