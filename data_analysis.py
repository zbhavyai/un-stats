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
        - indexes the dataframe
        - sorts the data depending on the index
        - checks the null values and data mismatches

    Attributes:
        _unc_data
        _liv_data
        _pop_data
        _edu_data
        _gdp_data
        _net_data

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
        Method to manually confirm the import of data from Excel

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
