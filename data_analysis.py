# File:        data_analysis.py
# Authors:     Bhavyai Gupta, Brandon Attai
# Description: Source code of the class DataAnalysis

import pandas as pd
import ansi_colors as color
import os


class DataAnalysis:
    """
    Class to facilitate data import, aggregation, analysis, and reporting

    Constructor:
        The constructor performs the following functions -
        - imports the data from Excel/CSV files into panda dataframes
        - merges the data together into one dataframe
        - indexes the dataframe and sorts depending on the index
        - checks the null values and data mismatches

    Attributes:
        _unc_data
        _liv_data
        _pop_data
        _edu_data
        _gdp_data
        _net_data
        _dataset

    Methods:
        _import_data
    """

    def __init__(self):
        self._import_data("UN Population Datasets", "CustomUNData")



    def _import_data(self, default_location, custom_location):
        """
        Method to import the known files from the relation location in the project directory

            Parameters:
                location (str): relative path where the data is stored

            Returns:
                None
        """

        self._unc_data = pd.read_excel(os.path.join(default_location, "UN Codes.xlsx"))
        self._liv_data = pd.read_excel(os.path.join(default_location, "UN Population Dataset 1.xlsx"))
        self._pop_data = pd.read_excel(os.path.join(default_location, "UN Population Dataset 2.xlsx"))
        self._edu_data = pd.read_csv(os.path.join(custom_location, "UNEducationData.csv"))
        self._gdp_data = pd.read_csv(os.path.join(custom_location, "UNGDPData.csv"))
        self._net_data = pd.read_csv(os.path.join(custom_location, "UNInternetData.csv"))


    def print_imported(self):
        """
        Method to print the imported data from Excel or CSV

            Parameters:
                none

            Returns:
                None
        """

        print("\n\n" + color.green + "UN Code dataframe" + color.reset + "\n")
        print(self._unc_data)

        print("\n\n" + color.green + "UN Life Expectancy and Fertility dataframe" + color.reset + "\n")
        print(self._liv_data)

        print("\n\n" + color.green + "UN Population dataframe" + color.reset + "\n")
        print(self._pop_data)

        print("\n\n" + color.green + "UN Education dataframe" + color.reset + "\n")
        print(self._edu_data)

        print("\n\n" + color.green + "UN Gross Domestic Product dataframe" + color.reset + "\n")
        print(self._gdp_data)

        print("\n\n" + color.green + "UN Internet Usage dataframe" + color.reset + "\n")
        print(self._net_data)


    def merge_data(self):
        """
        Method to merge the data from different dataframes into one dataframe

            Parameters:
                none

            Returns:
                None
        """
        # First merge for UN Codes and Education Data filter by Tertiary Education
        merged1 = pd.merge(self._unc_data,self._edu_data, how='outer',left_on='Country',right_on='Region/Country/Area')
        merged1 = merged1.drop(['Region/Country/Area', 'UN Sub-Region'], axis=1).dropna()
        merged1 = merged1[merged1['Series'].str.contains('tertiary')]

        # Second merge for Merge1 and Life Data filter by Fertility Rate
        merged2 = pd.merge(merged1, self._liv_data, how = 'inner', left_on = ['Country', 'Year'], right_on = ['Region/Country/Area','Year'])
        merged2 = merged2[merged2['Series_y'].str.contains('fertility')]
        merged2 = merged2.drop(['Code','Region/Country/Area'],axis =1)
        merged2 = merged2.rename(columns = {'Series_x':'Tertiary Enrollment', 'Series_y':'Fertility Rate', 'Value_x':'Enrollment (Thousands)', 'Value_y': 'Rate'})

        # Third merge for Merge2 and GDP Data filter by GDP Per Capita
        merged3 = pd.merge(merged2, self._gdp_data, how = 'inner', left_on = ['Country', 'Year'], right_on = ['Region/Country/Area','Year'])
        merged3 = merged3.drop(['Code','Region/Country/Area', 'Footnotes', 'Source'],axis =1)
        merged3 = merged3.rename(columns = {'Series': 'GDP per Capita', 'Value':'GDP Value'})
        merged3 = merged3[merged3['GDP per Capita'].str.contains('per capita')]

        # Fourth merge for Merge3 and Internet Data
        merged4 = pd.merge(merged3, self._net_data, how = 'inner', left_on = ['Country', 'Year'], right_on = ['Region/Country/Area','Year'])
        merged4 = merged4.drop(['Code','Region/Country/Area', 'Footnotes', 'Source'],axis =1)
        merged4 = merged4.rename(columns = {'Series': 'Internet Users (%)', 'Value' : 'Percentage'})

        # Fifth merge for Merge4 and Population Data filter by Urban Population
        merged5 = pd.merge(merged4, self._pop_data, how = 'inner', left_on = ['Country', 'Year'], right_on = ['Region/Country/Area','Year'])
        merged5 = merged5.drop(['Code','Region/Country/Area', 'Capital City'],axis =1)
        merged5 = merged5.rename(columns = {'Series': 'Urban Population (%)', 'Value' : 'Percentage 2'})
        merged5 = merged5[merged5['Urban Population (%)'].str.contains('Urban')]

        # Create multi-indexed dataframe and sort it
        self._dataset = merged5.set_index(['UN Region', 'Country'])
        self._dataset.sort_index()
