# File:        data_analysis.py
# Authors:     Bhavyai Gupta, Brandon Attai
# Description: Source code of the class DataAnalysis providing methods and attributes for analysis of dataframes

from custom_errors import ValueOutOfRange
from custom_errors import ValueDuplicate
import pandas as pd
import ansi_colors as color
import time
import os
import matplotlib.pyplot as plt
from launch import clear_console
import seaborn as sns


class DataAnalysis:
    """
    Class to facilitate data import, aggregation, analysis, and reporting

    Constructor:
        The constructor performs the following functions -
        - imports the data from Excel/CSV files into panda dataframes
        - merges the data together into one dataframe, indexes it, and sorts the indexes
        - add additional columns into the dataframe
        - checks the null values and data mismatches
        - exports the entire merged hierarchical dataset into excel

    Attributes:
        _unc_data
        _liv_data
        _pop_data
        _gdp_data
        _dataset

    Methods:
        _import_data(default_location, custom_location): Method to import the known files from the relative locations in the project directory
        _merge_data(): Method to merge the data from different dataframes into one dataframe
        _additional_statistics(): Method to add additional columns to the dataframe
        _check_null(): Method to check null values in the dataframe.
        export_dataset(): Method to export the entire merged hierarchical dataframe into Excel file
        print_imported_dataframes(): Method to print dataframes imported from Excel or CSV
        print_aggregate_stats(): Method to print aggregate stats for the entire dataset
        group_by_stats(): Method to print the one or several aggregate stats grouped by UN Region/UN Sub-Region ranging in years for the dataframe.
        higher_gdp_than_usa(): Method to list countries having GDP per capita than the USA
        pivot_plot(): Method using pivot table and matplotlib to compare statistics
        alt_pivot_plot(): Method to plot graphs on Population Rate, Fertility Rate, Life Expectancy, and Urban Population
        for four different countries
    """

    def __init__(self):
        print("\n" + color.yellow +
              "Please wait while the program initializes..." + color.reset)
        time.sleep(2)
        print("\n[Step 1/5] Importing data from excel and csv files")
        self._import_data("UN Population Datasets", "CustomUNData")
        print("[Step 1/5] " + color.green + "complete" + color.reset)

        print("\n[Step 2/5] Merging all data into one dataframe")
        self._merge_data()
        print("[Step 2/5] " + color.green + "complete" + color.reset)

        print("\n[Step 3/5] Adding extra columns to the entire combined dataframe")
        self._additional_statistics()
        print("\n[Step 3/5] " + color.green + "complete" + color.reset)

        print("\n[Step 4/5] Checking null values\n")
        self._check_null()
        print("\n[Step 4/5] " + color.green + "complete" + color.reset)

        print("\n[Step 5/5] Exporting entire merged hierarchical dataset into excel")
        self.export_dataset()
        print("[Step 5/5] " + color.green + "complete" + color.reset)
        input("\n\n" + color.blue +
              "Press enter to enter program menu " + color.reset)

    def _import_data(self, default_location, custom_location):
        """
        Method to import the known files from the relative locations in the project directory

            Parameters:
                default_location (str): relative path to location of provided files
                custom_location (str): relative path to location of additional files

            Returns:
                None
        """
        # Importing UN Codes dataset
        # ----------------------------------------
        self._unc_data = pd.read_excel(
            os.path.join(default_location, "UN Codes.xlsx"))

        # fixing incompatible name of "United States of America" in the "UN Codes.xlsx" file
        self._unc_data.loc[self._unc_data["Country"] ==
                           "United States", "Country"] = "United States of America"
        # ----------------------------------------

        # Importing UN Population Dataset 1
        # ----------------------------------------
        liv_data_raw = pd.read_excel(os.path.join(
            default_location, "UN Population Dataset 1.xlsx"), usecols="B:E")

        # creating temporary dataframe with Series filtered on "Population annual rate of increase (percent)"
        filter_series = "Population annual rate of increase (percent)"
        liv_data_population = liv_data_raw[liv_data_raw["Series"] == filter_series].drop(
            "Series", axis=1).rename(columns={"Value": filter_series})

        # creating temporary dataframe with Series filtered on "Total fertility rate (children per women)"
        filter_series = "Total fertility rate (children per women)"
        liv_data_fertility = liv_data_raw[liv_data_raw["Series"] == filter_series].drop(
            "Series", axis=1).rename(columns={"Value": filter_series})

        # creating temporary dataframe with Series filtered on "Life expectancy at birth for both sexes (years)"
        filter_series = "Life expectancy at birth for both sexes (years)"
        liv_data_expectancy = liv_data_raw[liv_data_raw["Series"] == filter_series].drop(
            "Series", axis=1).rename(columns={"Value": filter_series})

        # join dataframe liv_data_population and liv_data_fertility
        liv_data_temp = pd.merge(liv_data_population, liv_data_fertility, how="inner", on=[
                                 "Region/Country/Area", "Year"])

        # join dataframe liv_data_temp and liv_data_expectancy
        self._liv_data = pd.merge(liv_data_temp, liv_data_expectancy, how="inner", on=[
                                  "Region/Country/Area", "Year"])
        # ----------------------------------------

        # Importing UN Population Dataset 2
        # ----------------------------------------
        pop_data_raw = pd.read_excel(os.path.join(
            default_location, "UN Population Dataset 2.xlsx"), usecols="B:D, F")

        # creating dataframe with Series filtered on "Urban population (percent)"
        filter_series = "Urban population (percent)"
        self._pop_data = pop_data_raw[pop_data_raw["Series"] == filter_series].drop(
            "Series", axis=1).rename(columns={"Value": filter_series}).reset_index(drop=True)
        # ----------------------------------------

        # Importing UN GDP Data
        # ----------------------------------------
        gdp_data_raw = pd.read_csv(os.path.join(custom_location, "UNGDPData.csv"), usecols=[
                                   "Region/Country/Area", "Year", "Series", "Value"])

        # creating dataframe with Series filtered on "Urban population (percent)"
        filter_series = "GDP per capita (US dollars)"
        self._gdp_data = gdp_data_raw[gdp_data_raw["Series"] == filter_series].drop(
            "Series", axis=1).rename(columns={"Value": filter_series}).reset_index(drop=True)
        # ----------------------------------------

    def _merge_data(self):
        """
        Method to merge the data from different dataframes into one dataframe

            Parameters:
                none

            Returns:
                None
        """
        # merging "UN Codes" and "UN Population Dataset 1" into dataset_temp
        dataset_temp = pd.merge(self._unc_data, self._liv_data, how="left", left_on="Country",
                                right_on="Region/Country/Area").drop("Region/Country/Area", axis=1)

        # merging dataset_temp and "UN Population Dataset 2" into dataset_temp
        dataset_temp = pd.merge(dataset_temp, self._pop_data, how="left", left_on=[
                                "Country", "Year"], right_on=["Region/Country/Area", "Year"]).drop("Region/Country/Area", axis=1)

        # merging dataset_temp and "UN GDP Data" into dataset
        self._dataset = pd.merge(dataset_temp, self._gdp_data, how="left", left_on=[
                                 "Country", "Year"], right_on=["Region/Country/Area", "Year"]).drop("Region/Country/Area", axis=1)

        # create the index on Region, Sub-Region and Country
        self._dataset.set_index(
            ["UN Region", "UN Sub-Region", "Country"], inplace=True)

        # sort the indexes
        self._dataset.sort_index(inplace=True)

        # dropping the null values
        self._dataset.dropna(inplace=True)

    def _additional_statistics(self):
        """
        Method to add additional columns to the dataframe

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

        usa = "United States of America"

        # get the GDP for United States
        us_gdp_capita = self._dataset.loc[idx[:, :, usa],
                                          idx["Year", "GDP per capita (US dollars)"]]
        us_gdp_capita.reset_index(drop=True, inplace=True)

        # get all the different years in the self._dataset for the "United States of America"
        different_years = self._dataset.loc[idx[:, :, usa], idx["Year"]]

        # loop to fill the values in the column
        for y in different_years:
            # fetch the gdp of US for "Year" = y
            us_gdp_capita_y = float(
                us_gdp_capita[us_gdp_capita["Year"] == y]["GDP per capita (US dollars)"])

            # for the "Year" = y, calculate GDP per capita wrt USA = GDP per capita / GDP per capita of USA
            self._dataset.loc[idx[self._dataset["Year"] == y], idx["GDP per capita wrt USA"]
                              ] = self._dataset.loc[idx[self._dataset["Year"] == y], idx["GDP per capita (US dollars)"]] / us_gdp_capita_y

        # printing what column has been added - to make it easy for TAs
        print("\nAdded column \'GDP per capita wrt USA\' to the dataset")
        # ----------------------------------------

        # Extra column 2
        # ----------------------------------------
        # Column to compare the Ratio of Urban Population to GDP per Capita

        self._dataset.insert(5, "Ratio of Urban Population to GDP per Capita",
                             self._dataset['Urban population (percent)'] / self._dataset['GDP per capita (US dollars)'])

        print("Added column \'Ratio of Urban Population to GDP per capita\' to the dataset")
        # ----------------------------------------

        # Extra column 3
        # ----------------------------------------
        # Column to compare the Ratio of Annual Rate of Population Increase to GDP per Capita

        self._dataset.insert(6, "Ratio of Annual Rate of Population Increase to GDP per Capita",
                             self._dataset['Population annual rate of increase (percent)'] / self._dataset['GDP per capita (US dollars)'])

        print("Added column \'Ratio of Annual Rate of Population Increase to GDP per Capita\' to the dataset")
        # ----------------------------------------

    def _check_null(self):
        """
        Method to check null values in the dataframe.

            Parameters:
                none

            Returns:
                None
        """
        print(self._dataset.isnull().any())

    def export_dataset(self):
        """
        Method to export the entire merged hierarchical dataframe into Excel files with default filename

            Parameters:
                none

            Returns:
                None
        """
        try:
            self._dataset.to_excel("Export UN Data.xlsx",
                                   index=True, header=True)
            print("\nFile \'Export UN Data.xlsx\' created\n")

        except Exception as e:
            print("\n" + color.red + "An exception occurred during export. Please check the below message and try again" + color.reset + "\n")
            print(e)

    def print_imported_dataframes(self):
        """
        Method to print dataframes imported from Excel or CSV

            Parameters:
                none

            Returns:
                None
        """
        print("\n\n" + color.green + "UN Codes dataframe" + color.reset + "\n")
        print(self._unc_data)

        print("\n\n" + color.green +
              "UN Life Expectancy and Fertility dataframe" + color.reset + "\n")
        print(self._liv_data)

        print("\n\n" + color.green +
              "UN Urban Population dataframe" + color.reset + "\n")
        print(self._pop_data)

        print("\n\n" + color.green +
              "UN Gross Domestic Product dataframe" + color.reset + "\n")
        print(self._gdp_data)

    def print_aggregate_stats(self):
        """
        Method to print aggregate stats for the entire dataset

            Parameters:
                none

            Returns:
                None
        """
        print("\n" + color.green +
              "Aggregate statistics for the entire dataset" + color.reset + "\n")
        print(self._dataset.describe())

    def group_by_stats(self):
        """
        Method to print the one or several aggregate stats grouped by UN Region/UN Sub-Region ranging in years for the dataframe.

            Parameters:
                none

            Returns:
                None
        """
        clear_console()

        print("\n" + color.yellow +
              "Sub Menu: Aggregation stats grouped by UN Region/UN Sub-Region" + color.reset)

        while(True):
            try:
                print("\n" + color.magenta +
                      "[Q1] How do you want to get aggregate stats? By \"UN Region\" or By \"UN Sub-Region\"" + color.reset)
                choice_region_type = input(
                    "\nEnter either \"UN Region\" or \"UN Sub-Region\" (without the quotes): ")

                if choice_region_type == "UN Region" or choice_region_type == "UN Sub-Region":
                    break

                else:
                    raise ValueOutOfRange(
                        "This option is not supported. Please choose a valid menu option")

            except ValueOutOfRange as e:
                print("\n" + color.red + str(e) + color.reset)

        # here we have got choice_region_type

        while(True):
            try:
                print("\n" + color.magenta + "[Q2] Which data column you want the aggregate stats for?" +
                      color.reset + "\n\nPlease enter one of the below possible options (dont enter leading hypen):\n")

                for col in range(1, self._dataset.columns.size):
                    print(" - " + self._dataset.columns[col])

                choice_column = input("\nEnter your choice: ")

                if choice_column in self._dataset.columns and choice_column != "Year":
                    break

                else:
                    raise ValueOutOfRange(
                        "This option is not supported. Please choose a valid menu option")

            except ValueOutOfRange as e:
                print("\n" + color.red + str(e) + color.reset)

        # now we have got choice_region_type and choice_column

        while(True):
            try:
                print("\n" + color.magenta + "[Q3] What aggregate stats you want?" + color.reset +
                      "\n\nPlease enter one of the below possible options (dont enter leading hypen):\n")

                available_stat = ["mean", "median", "min", "max", "all"]

                for col in range(0, len(available_stat)):
                    print(" - " + available_stat[col])

                choice_stat = input("\nEnter your choice: ")

                if choice_stat not in available_stat:
                    raise ValueOutOfRange(
                        "This option is not supported. Please choose a valid menu option")

                elif choice_stat == "all":
                    # changing to what "all" actually stands for
                    choice_stat = ["mean", "median", "min", "max"]
                    break

                else:
                    break

            except ValueOutOfRange as e:
                print("\n" + color.red + str(e) + color.reset)

        # now we have got all three choice_region_type, choice_column, and choice_stat. So running the aggregate
        print("\n" + color.green + "Here are the requested stats" + color.reset + "\n")
        print(self._dataset.groupby([choice_region_type, "Year"])[
              choice_column].aggregate(choice_stat).unstack())

    def higher_gdp_than_usa(self):
        """
        Method to show use of additional column "GDP per capita wrt USA". This method lists the
        countries that have had higher GDP per capita than the USA, and the years in which
        the said figure was higher

            Parameters:
                none

            Returns:
                None
        """
        higher_gdp = self._dataset[self._dataset["GDP per capita wrt USA"] > 1].reset_index(
        )

        print("\n" + color.green + "Showing list of countries that have had higher GDP per capita than USA and in what year" + color.reset + "\n")
        higher_gdp = higher_gdp[["Country", "Year"]
                                ].sort_values(by=["Country", "Year"])
        print(higher_gdp.to_string(index=False))

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
                country_choice = input(
                    "\n" + color.magenta + "Please enter the Country you would like to compare: " + color.reset)
                try:
                    pivot_df1 = pivot_df.pivot_table(
                        'Population annual rate of increase (percent)', index='Year', columns='Country').loc[:, country_choice]
                    break
                except KeyError:
                    print(
                        color.red + "Invalid country name, please try again!" + color.reset)
            except KeyError:
                print(color.red +
                      "Invalid country name, please try again!" + color.reset)

        # Create multiple pivot tables to be superimposed on the plot.
        pivot_df2 = pivot_df.pivot_table(
            'Total fertility rate (children per women)', index='Year', columns='Country').loc[:, country_choice]
        pivot_df3 = pivot_df.pivot_table(
            'Life expectancy at birth for both sexes (years)', index='Year', columns='Country').loc[:, country_choice]

        # Superimplose the plots
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

    def alt_pivot_plot(self):
        """
        Method to plot graphs on Population Rate, Fertility Rate, Life Expectancy, and Urban Population
        for four different countries

            Parameters:
                none

            Returns:
                None
        """
        clear_console()

        print("\n" + color.yellow +
              "Sub Menu: Plotting graphs using pivot table" + color.reset)
        print("\nWe will print compare four countries on the basis of -")
        print(" - Population annual rate of increase (percent)")
        print(" - Total fertility rate (children per women)")
        print(" - Life expectancy at birth for both sexes (years)")
        print(" - Urban population (percent)")

        print("\n" + color.magenta +
              "Please enter four unique countries, one at a time. eg. United States of America" + color.reset + "\n")
        countries = []

        for i in range(0, 4):
            while(True):
                try:
                    choice_country = input("Enter country " + str(i+1) + " : ")

                    # if its a valid country
                    if(choice_country in self._dataset.index.get_level_values(2).values):
                        # now check if its not already added
                        if(choice_country not in countries):
                            countries.append(choice_country)
                            i = i + 1
                            break

                        # oops, user tried to re-enter a country
                        else:
                            raise ValueDuplicate(
                                "You have already entered this country. Please enter a different country")

                    # if its an invalid country
                    else:
                        raise ValueOutOfRange(
                            "This is not a valid country. Please enter a valid country")

                except ValueOutOfRange as e:
                    print("\n" + color.red + str(e) + color.reset + "\n")

                except ValueDuplicate as e:
                    print("\n" + color.red + str(e) + color.reset + "\n")

        # sort the list countries
        countries.sort()

        # now we have got four different countries, lets plot the graphs

        # creating IndexSlice object
        idx = pd.IndexSlice

        # get a subset of dataframe with only four countries and required columns
        subset = self._dataset.loc[idx[:, :, countries, idx[:]]]

        # choose only the required columns from the subset
        subset = subset.loc[idx[:], idx["Year", "Population annual rate of increase (percent)", "Total fertility rate (children per women)",
                                        "Life expectancy at birth for both sexes (years)", "Urban population (percent)"]]

        # creating pivot table
        pivot_data = subset.pivot_table(index="Year", columns="Country")

        # printing pivot table
        print("\n" + color.green +
              "Pivot table for the above countries" + color.reset + "\n")
        print(pivot_data)

        # creating plots
        fig = plt.figure(1)
        fig.set_size_inches(20, 10)
        fig.suptitle("Comparison of countries")

        (axs0, axs1) = fig.subplots(2, 2)

        # plot for Population annual rate of increase (percent)
        axs0[0].set_title("Population annual rate of increase (percent)")
        axs0[0].set(xlabel="Year", ylabel="Percentage")
        axs0[0].plot(
            pivot_data.loc[:, idx["Population annual rate of increase (percent)"]])
        axs0[0].legend(countries, loc="upper right")

        # plot for Total fertility rate (children per women)
        axs0[1].set_title("Total fertility rate (children per women)")
        axs0[1].set(xlabel="Year", ylabel="Children per women")
        axs0[1].plot(
            pivot_data.loc[:, idx["Total fertility rate (children per women)"]])
        axs0[1].legend(countries, loc="upper right")

        # plot for Life expectancy at birth for both sexes (years)
        axs1[0].set_title("Life expectancy at birth for both sexes (years)")
        axs1[0].set(xlabel="Year", ylabel="Years")
        axs1[0].plot(
            pivot_data.loc[:, idx["Life expectancy at birth for both sexes (years)"]])
        axs1[0].legend(countries, loc="upper right")

        # plot for Urban population (percent)
        axs1[1].set_title("Urban population (percent)")
        axs1[1].set(xlabel="Year", ylabel="Percentage")
        axs1[1].plot(pivot_data.loc[:, idx["Urban population (percent)"]])
        axs1[1].legend(countries, loc="upper right")

        # save the plot in project directory
        fig.savefig("Plots.png", dpi=100)
        print("\n\nPlot saved as \'Plots.png\'")

        show_now = input("\n" + color.magenta +
                         "Do you want see the plot now? Enter y/Y for yes: " + color.reset)

        if(show_now == "y" or show_now == "Y"):
            plt.show()
            return

        else:
            return
