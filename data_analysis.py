# File:        data_analysis.py
# Authors:     Bhavyai Gupta, Brandon Attai
# Description: Source code of the class DataAnalysis

from custom_errors import ValueOutOfRange
import pandas as pd
import ansi_colors as color
import time
import os
import matplotlib.pyplot as plt
import seaborn as sns


class DataAnalysis:
    """
    Class to facilitate data import, aggregation, analysis, and reporting

    Constructor:
        The constructor performs the following functions -
        - imports the data from Excel/CSV files into panda dataframes
        - merges the data together into one dataframe
        - indexes the dataframe and sorts depending on the index
        - checks the null values and data mismatches
        - exports the entire merged hierarchical dataset into excel

    Attributes:
        _unc_data
        _liv_data
        _pop_data
        _gdp_data
        _dataset

    Methods:
        _import_data(default_location, custom_location)
        print_imported_dataframes()
        _merge_data()
        export_dataset()
        check_null()
        print_aggregate_stats()
        additional_statistics()
        pivot_plot()
    """

    def __init__(self):
        print("\n" + color.yellow + "Please wait while the program initializes..." + color.reset)
        time.sleep(2)
        print("\n[Step 1/5] Importing data from excel and csv files")
        self._import_data("UN Population Datasets", "CustomUNData")
        print("[Step 1/5] " + color.green + "complete" + color.reset)

        print("\n[Step 2/5] Merging all data into one dataframe")
        self._merge_data()
        print("[Step 2/5] " + color.green + "complete" + color.reset)

        print("\n[Step 3/5] Checking null values\n")
        self.check_null()
        print("\n[Step 3/5] " + color.green + "complete" + color.reset)

        print("\n[Step 4/5] Adding extra columns to the entire combined dataframe")
        self._additional_statistics()
        print("\n[Step 4/5] " + color.green + "complete" + color.reset)

        print("\n[Step 5/5] Exporting entire merged hierarchical dataset into excel")
        self.export_dataset()
        print("[Step 5/5] " + color.green + "complete" + color.reset)
        input("\n\n" + color.blue + "Press enter to enter program menu " + color.reset)



    def _import_data(self, default_location, custom_location):
        """
        Method to import the known files from the relation location in the project directory

            Parameters:
                location (str): relative path where the data is stored

            Returns:
                None
        """
        # Importing UN Codes dataset
        # ----------------------------------------
        self._unc_data = pd.read_excel(os.path.join(default_location, "UN Codes.xlsx"))

        # fixing incompatible name of "United States of America" in the "UN Codes.xlsx" file
        self._unc_data.loc[self._unc_data["Country"] == "United States", "Country"] = "United States of America"
        # ----------------------------------------


        # Importing UN Population Dataset 1
        # ----------------------------------------
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
        # ----------------------------------------


        # Importing UN Population Dataset 2
        # ----------------------------------------
        pop_data_raw = pd.read_excel(os.path.join(default_location, "UN Population Dataset 2.xlsx"), usecols="B:D, F")

        # creating dataframe with Series filtered on "Urban population (percent)"
        filter_series = "Urban population (percent)"
        self._pop_data = pop_data_raw[pop_data_raw["Series"] == filter_series].drop("Series", axis=1).rename(columns={"Value": filter_series}).reset_index(drop=True)
        # ----------------------------------------


        # Importing UN GDP Data
        # ----------------------------------------
        gdp_data_raw = pd.read_csv(os.path.join(custom_location, "UNGDPData.csv"), usecols=["Region/Country/Area", "Year", "Series", "Value"])

        # creating dataframe with Series filtered on "Urban population (percent)"
        filter_series = "GDP per capita (US dollars)"
        self._gdp_data = gdp_data_raw[gdp_data_raw["Series"] == filter_series].drop("Series", axis=1).rename(columns={"Value": filter_series}).reset_index(drop=True)
        # ----------------------------------------



    def print_imported_dataframes(self):
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



    def export_dataset(self):
        """
        Method to export the entire merged hierarchical dataframe into Excel files with default filename

            Parameters:
                none

            Returns:
                None
        """
        try:
            self._dataset.to_excel("Export UN Data.xlsx", index = True, header = True)
            print("File \'Export UN Data.xlsx\' created")

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
        print(self._dataset.isnull().any())



    def print_aggregate_stats(self):
        """
        Method to print aggregate stats for the entire dataset

            Parameters:
                none

            Returns:
                None
        """
        print("\n" + color.magenta + "Aggregate statistics for the entire dataset" + color.reset + "\n")
        print(self._dataset.describe())



    def group_by_stats(self):
        """
        Method using the groupby function to show the averages for a specific field
        for all Sub-Regions ranging in years for the dataset.

            Parameters:
                none

            Returns:
                None
        """
        year_analysis = self._dataset['Year']
        year_analysis = year_analysis.astype(str)
        year_analysis.name = 'Year'

        while(True):
            try:
                choice = input("\n" + color.magenta + """Please enter the name of the data that you would like to see the average quinquennial stats for.
                                \nThe options are: """ + color.reset +"""
                                \n1) """ +self._dataset.columns[1] +"""
                                \n2) """ +self._dataset.columns[2] +"""
                                \n3) """ +self._dataset.columns[3] +"""
                                \n4) """ +self._dataset.columns[4] +"""
                                \n5) """ + self._dataset.columns[5] + """
                                \nEnter here: """ + "\n")

                if choice not in self._dataset.columns:
                    raise ValueOutOfRange("This option is not supported. Please choose a valid menu option")

                else:
                    break

            except ValueError as e:
                print("\n" + color.red + "Please enter a valid menu option" + color.reset)

            except ValueOutOfRange as e:
                print("\n" + color.red + str(e) + color.reset)

            except KeyboardInterrupt as e:
                print("\n\nYou pressed Ctrl+C. Bye!\n")
                return

        print(self._dataset.groupby(['UN Sub-Region',year_analysis])[choice].mean().unstack())



    def _additional_statistics(self):
        """
        Method adding two columns to the dataset.

            Parameters:
                none

            Returns:
                None
        """
        # creating IndexSlice object
        idx = pd.IndexSlice

        # Extra column 1
        # ----------------------------------------
        # Adding extra column "GDP per capita wrt USA", which is ratio of "GDP per capita (US dollars)" of the country and "GDP per capita (US dollars)" of the "United States of America"

        # get the GDP for United States
        us_gdp_capita = self._dataset.loc[idx[:, :, "United States of America"], idx["Year", "GDP per capita (US dollars)"]]
        us_gdp_capita.reset_index(drop=True, inplace=True)

        # get all the different years in the self._dataset for the "United States of America"
        different_years = self._dataset.loc[idx[:, :, "United States of America"], idx["Year"]]

        # loop to fill the values in the column
        for y in different_years:
            # fetch the gdp of US for "Year" = y
            us_gdp_capita_y = float(us_gdp_capita[us_gdp_capita["Year"] == y]["GDP per capita (US dollars)"])

            # for the "Year" = y, calculate GDP per capita wrt USA = GDP per capita / GDP per capita of USA
            self._dataset.loc[idx[self._dataset["Year"] == y], idx["GDP per capita wrt USA"]] = self._dataset.loc[idx[self._dataset["Year"] == y], idx["GDP per capita (US dollars)"]] / us_gdp_capita_y

        # printing what column has been added - to make it easy for TAs
        print("\nAdded column \'GDP per capita wrt USA\' to the dataset")
        # ----------------------------------------


        # Extra column 2
        # ----------------------------------------
        # Column to compare the Ratio of Urban Population to GDP per Capita

        self._dataset.insert(5, "Ratio of Urban Population to GDP per Capita", \
            self._dataset['Urban population (percent)'] / self._dataset['GDP per capita (US dollars)'])

        print("Added column \'Ratio of Urban Population to GDP per capita\' to the dataset")
        # ----------------------------------------


        # Extra column 3
        # ----------------------------------------
        # Column to compare the Ratio of Annual Rate of Population Increase to GDP per Capita

        self._dataset.insert(6, "Ratio of Annual Rate of Population Increase to GDP per Capita", \
            self._dataset['Population annual rate of increase (percent)'] / self._dataset['GDP per capita (US dollars)'])

        print("Added column \'Ratio of Annual Rate of Population Increase to GDP per Capita\' to the dataset")
        # ----------------------------------------



    def pivot_plot(self):
        """
        Method using pivot table and matplotlib to compare statistics.

            Parameters:
                none

            Returns:
                None
        """
        pivot_df = self._dataset.reset_index(level=['Country'])
        while(True):
            try:
                country_choice = input("\n" + color.magenta + "Please enter the Country you would like to compare: "+ color.reset)
                try:
                    pivot_df1 = pivot_df.pivot_table('Population annual rate of increase (percent)', index = 'Year', columns= 'Country').loc[:,country_choice]
                    break
                except KeyError:
                    print(color.red + "Invalid country name, please try again!" + color.reset)
            except KeyError:
                print(color.red + "Invalid country name, please try again!" + color.reset)

        # Create multiple pivot tables to be superimposed on the plot.
        pivot_df2 = pivot_df.pivot_table('Total fertility rate (children per women)', index='Year', columns='Country').loc[:,country_choice]
        pivot_df3 = pivot_df.pivot_table('Life expectancy at birth for both sexes (years)', index='Year', columns='Country').loc[:,country_choice]

        #Superimplose the plots
        pivot_df1.plot()
        pivot_df2.plot()
        pivot_df3.plot()
        plt.xlabel("Year")
        plt.ylabel("Value")
        plt.title("""Comparison of Life Population annual rate of increase (percent) to
                    \nTotal fertility rate (children per women) to
                    \nLife expectancy at birth for both sexes (years)
                    \nfor Country: {0}""".format(country_choice))
        plt.legend()
        plt.show()
