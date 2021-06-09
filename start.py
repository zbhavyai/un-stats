import pandas as pd


# step 1 import datasets into dataframe
dataset_un_codes = r'UN Population Datasets/UN Codes.xlsx'
dataset_growth_stats = r'UN Population Datasets/UN Population Dataset 1.xlsx'
dataset_growth_cities = r'UN Population Datasets/UN Population Dataset 2.xlsx'


# step 1.1 check the import
print(pd.read_excel(dataset_un_codes))
print(pd.read_excel(dataset_growth_stats))
print(pd.read_excel(dataset_growth_cities))


# step 2 merge the datasets



