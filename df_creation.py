import numpy as np
import pandas as pd
import os


def df_creation():
    """
    Function to create a dataframe based using .xlsx or .csv files. 

        Parameters: 
            None

        Returns:
            None
    """
    print(os.getcwd()) #Print current working directory to ensure files can be read (temporary)

    codes = pd.read_excel('UNCodes.xlsx')
    life_data = pd.read_excel('UNPopulationDataset1.xlsx')
    pop_data = pd.read_excel('UNPopulationDataset2.xlsx')
    edu_data = pd.read_csv('UNEducationData.csv')
    gdp_data = pd.read_csv('UNGDPData.csv')
    internet_data = pd.read_csv('UNInternetData.csv')

    # First merge for UN Codes and Education Data filter by Tertiary Education
    merged1 = pd.merge(codes,edu_data, how='outer',left_on='Country',
        right_on='Region/Country/Area')
    merged1 = merged1.drop(['Region/Country/Area', 'UN Sub-Region'], axis=1).dropna()
    merged1 = merged1[merged1['Series'].str.contains('tertiary')]

    # Second merge for Merge1 and Life Data filter by Fertility Rate
    merged2 = pd.merge(merged1, life_data, how = 'inner', left_on = ['Country', 'Year'],
                   right_on = ['Region/Country/Area','Year'])
    merged2 = merged2[merged2['Series_y'].str.contains('fertility')]
    merged2 = merged2.drop(['Code','Region/Country/Area'],axis =1)
    merged2 = merged2.rename(columns = {'Series_x':'Tertiary Enrollment', 'Series_y':'Fertility Rate',
                        'Value_x':'Enrollment (Thousands)', 'Value_y': 'Rate'})

    # Third merge for Merge2 and GDP Data filter by GDP Per Capita
    merged3 = pd.merge(merged2, gdp_data, how = 'inner', left_on = ['Country', 'Year'],
                   right_on = ['Region/Country/Area','Year'])
    merged3 = merged3.drop(['Code','Region/Country/Area', 'Footnotes', 'Source'],axis =1)
    merged3 = merged3.rename(columns = {'Series': 'GDP per Capita', 'Value':'GDP Value'})
    merged3 = merged3[merged3['GDP per Capita'].str.contains('per capita')]

    # Fourth merge for Merge3 and Internet Data
    merged4 = pd.merge(merged3, internet_data, how = 'inner', left_on = ['Country', 'Year'],
                   right_on = ['Region/Country/Area','Year'])
    merged4 = merged4.drop(['Code','Region/Country/Area', 'Footnotes', 'Source'],axis =1)
    merged4 = merged4.rename(columns = {'Series': 'Internet Users (%)', 'Value' : 'Percentage'})

    # Fifth merge for Merge4 and Population Data filter by Urban Population
    merged5 = pd.merge(merged4, pop_data, how = 'inner', left_on = ['Country', 'Year'],
                   right_on = ['Region/Country/Area','Year'])
    merged5 = merged5.drop(['Code','Region/Country/Area', 'Capital City'],axis =1)
    merged5 = merged5.rename(columns = {'Series': 'Urban Population (%)', 'Value' : 'Percentage 2'})
    merged5 = merged5[merged5['Urban Population (%)'].str.contains('Urban')]

    # Create dataframe multi-indexd
    dataset = merged4.set_index(['UN Region', 'Country'])
    print(dataset.head())

    return dataset

df_creation()



    

