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
        _import_data(default_location, custom_location)
        print_imported()
        _merge_data()
    """

    def __init__(self):
        self._import_data("UN Population Datasets", "CustomUNData")
        self._merge_data()



    def _import_data(self, default_location, custom_location):
        """
        Method to import the known files from the relation location in the project directory

            Parameters:
                location (str): relative path where the data is stored

            Returns:
                None
        """
        # import the UN Codes data, as is
        self._unc_data = pd.read_excel(os.path.join(default_location, "UN Codes.xlsx"))

        # import specific columns from the UN Population Dataset 1
        liv_data_raw = pd.read_excel(os.path.join(default_location, "UN Population Dataset 1.xlsx"), usecols="B:E")

        # creating temporary dataframe with Series filtered on "Population annual rate of increase (percent)"
        filter_series = "Population annual rate of increase (percent)"
        liv_data_population = liv_data_raw[liv_data_raw["Series"] == filter_series].drop("Series", axis=1).rename(columns={"Value": filter_series})

        # creating temporary dataframe with Series filtered on "Total fertility rate (children per women)"
        filter_series = "Total fertility rate (children per women)"
        liv_data_fertility = liv_data_raw[liv_data_raw["Series"] == filter_series].drop("Series", axis=1).rename(columns={"Value": filter_series})

        # creating temporary dataframe with Series filtered on "Life expectancy at birth for both sexes (years)"
        filter_series = "Life expectancy at birth for both sexes (years)"
        liv_data_expectancy = liv_data_raw[liv_data_raw["Series"] == filter_series].drop("Series", axis=1).rename(columns={"Value": filter_series})

        # join dataframe liv_data_population and liv_data_fertility
        liv_data_temp = pd.merge(liv_data_population, liv_data_fertility, how="inner", on=["Region/Country/Area", "Year"])

        # join dataframe liv_data_temp and liv_data_expectancy
        self._liv_data = pd.merge(liv_data_temp, liv_data_expectancy, how="inner", on=["Region/Country/Area", "Year"])

        # import specific columns from from the UN Population Dataset 2
        pop_data_raw = pd.read_excel(os.path.join(default_location, "UN Population Dataset 2.xlsx"), usecols="B:D, F")

        # creating dataframe with Series filtered on "Urban population (percent)"
        filter_series = "Urban population (percent)"
        self._pop_data = pop_data_raw[pop_data_raw["Series"] == filter_series].drop("Series", axis=1).rename(columns={"Value": filter_series}).reset_index(drop=True)

        # import specific columns from from the UN GDP Data
        gdp_data_raw = pd.read_csv(os.path.join(custom_location, "UNGDPData.csv"), usecols=["Region/Country/Area", "Year", "Series", "Value"])

        # creating dataframe with Series filtered on "Urban population (percent)"
        filter_series = "GDP per capita (US dollars)"
        self._gdp_data = gdp_data_raw[gdp_data_raw["Series"] == filter_series].drop("Series", axis=1).rename(columns={"Value": filter_series}).reset_index(drop=True)



    def print_imported(self):
        """
        Method to print the imported data from Excel or CSV

            Parameters:
                none

            Returns:
                None
        """
        print("\n\n" + color.magenta + "UN Codes dataframe" + color.reset + "\n")
        print(self._unc_data)

        print("\n\n" + color.magenta + "UN Life Expectancy and Fertility dataframe" + color.reset + "\n")
        print(self._liv_data)

        print("\n\n" + color.magenta + "UN Urban Population dataframe" + color.reset + "\n")
        print(self._pop_data)

        print("\n\n" + color.magenta + "UN Gross Domestic Product dataframe" + color.reset + "\n")
        print(self._gdp_data)



    def _merge_data(self):
        """
        Method to merge the data from different dataframes into one dataframe

            Parameters:
                none

            Returns:
                None
        """
        # merging "UN Codes" and "UN Population Dataset 1" into dataset_temp
        dataset_temp = pd.merge(self._unc_data, self._liv_data, how="left", left_on="Country", right_on="Region/Country/Area").drop("Region/Country/Area", axis=1)

        # merging dataset_temp and "UN Population Dataset 2" into dataset_temp
        dataset_temp = pd.merge(dataset_temp, self._pop_data, how="left", left_on=["Country", "Year"], right_on=["Region/Country/Area", "Year"]).drop("Region/Country/Area", axis=1)

        # merging dataset_temp and "UN GDP Data" into dataset
        self._dataset = pd.merge(dataset_temp, self._gdp_data, how="left", left_on=["Country", "Year"], right_on=["Region/Country/Area", "Year"]).drop("Region/Country/Area", axis=1)

        # create the index on Region, Sub-Region and Country
        self._dataset.set_index(["UN Region", "UN Sub-Region", "Country"], inplace=True)

        # sort the indexes
        self._dataset.sort_index(inplace=True)

        # dropping the null values
        self._dataset.dropna(inplace=True)



    def export_datasets(self):
        """
        Method to export all the dataframes into Excel files with default filenames

            Parameters:
                none

            Returns:
                None
        """
        try:
            self._unc_data.to_excel("Export UN Codes.xlsx", index=True, header=True)
            print("\n" + color.magenta + "File \'Export UN Codes.xlsx\' created" + color.reset)
            self._liv_data.to_excel("Export UN Population Dataset 1.xlsx", index=True, header=True)
            print("\n" + color.magenta + "File \'Export UN Population Dataset 1.xlsx\' created" + color.reset)
            self._pop_data.to_excel("Export UN Population Dataset 2.xlsx", index=True, header=True)
            print("\n" + color.magenta + "File \'Export UN Population Dataset 2.xlsx\' created" + color.reset)
            self._gdp_data.to_excel("Export UN GDP Dataset.xlsx", index=True, header=True)
            print("\n" + color.magenta + "File \'Export UN GDP Dataset.xlsx\' created" + color.reset)
            self._dataset.to_excel("Export UN Data.xlsx", index = True, header = True)
            print("\n" + color.magenta + "File \'Export UN Data.xlsx\' created" + color.reset)

        except Exception as e:
            print("\n" + color.red + "An exception occurred during export. Please check the below message and try again" + color.reset + "\n")
            print(e)



    def check_null(self):
        """
        Method to check null values in the dataset.

            Parameters:
                none

            Returns:
                None
        """
        print("\n" + color.magenta + "Checking null values" + color.reset)
        print(self._dataset.isnull().any())



    def aggregate_stats(self):
        """
        Method to print aggregate stats for the entire dataset

            Parameters:
                none

            Returns:
                None
        """
        print("\n" + color.magenta + "Aggregate statistics for the entire dataset" + color.reset + "\n")
        print(self._dataset.describe())