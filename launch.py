# File:        launch.py
# Authors:     Bhavyai Gupta, Brandon Attai
# Description: Source Code to control the execution flow for the Project

import ansi_colors as color
from custom_errors import ValueOutOfRange
import data_analysis as da
import time
import os


def clear_console():
    """Function to clear the console

        Parameters:
            none

        Returns:
            None
    """
    print("\033\143")


def splash_message():
    """
    Function to display the welcome message to the program, and opens up the VT mode
    by bug (https://bugs.python.org/issue30075) for windows default console for ANSI
    sequence to work. This function intends to be run only once at program startup.

        Parameters:
            none

        Returns:
            None
    """
    os.system("")

    clear_console()

    print(color.magenta)
    print("--------------------------")
    print(" Welcome to UN Statistics")
    print("--------------------------")
    print(color.reset, end="")

    # show the splash screen for 1.5 seconds and then clear again
    time.sleep(1.5)

    clear_console()


def program_menu():
    """
    Function to control the flow the whole program by displaying the menu
    and navigation throughtout according to the user input

        Parameters:
            none

        Returns:
            None
    """
    # creating object of class DataAnalysis
    analysis = da.DataAnalysis()

    # loop to keep printing the menu until Exit
    while(True):
        # clear the console everytime menu is printed
        clear_console()

        print("\n" + color.yellow + "Program menu" + color.reset)
        # generic options
        print("\n[1] Print the imported datasets")
        print("\n[2] Re-export the entire merged hierarchical dataset into Excel")
        print("\n[3] Print aggregate stats for the entire dataset")

        # data specific options
        print(
            "\n[4] Print aggregation stats grouped by UN Region/UN Sub-Region and available years")
        print(
            "\n[5] Print the list of countries that have higher GDP per capita than USA, and the year")
        print(
            "\n[6] Show plot of Population Increase, Total Fertility Rate and Life Expectancy for a country")

        print("\n[0] Exit")

        # loop to get valid choice from the user
        while(True):
            try:
                choice = int(input("\nPlease enter the menu option number: "))

                if choice < 0 or choice > 6:
                    raise ValueOutOfRange(
                        "This option is not supported. Please choose a valid menu option")

                elif choice == 0:
                    print("\nBye!\n")
                    return

                else:
                    break

            except ValueError as e:
                print("\n" + color.red +
                      "Please enter a valid menu option" + color.reset)

            except ValueOutOfRange as e:
                print("\n" + color.red + str(e) + color.reset)

        # after getting a valid option from the user, perform the requested option

        if choice == 1:
            analysis.print_imported_dataframes()
            input("\n" + color.blue +
                  "Press enter to return to the menu " + color.reset)

        elif choice == 2:
            analysis.export_dataset()
            input("\n" + color.blue +
                  "Press enter to return to the menu " + color.reset)

        elif choice == 3:
            analysis.print_aggregate_stats()
            input("\n" + color.blue +
                  "Press enter to return to the menu " + color.reset)

        elif choice == 4:
            analysis.group_by_stats()
            input("\n" + color.blue +
                  "Press enter to return to the menu " + color.reset)

        elif choice == 5:
            analysis.higher_gdp_than_usa()
            input("\n" + color.blue +
                  "Press enter to return to the menu " + color.reset)

        else:  # choice == 6:
            # analysis.pivot_plot()
            analysis.alt_pivot_plot()
            input("\n" + color.blue +
                  "Press enter to return to the menu " + color.reset)


if __name__ == '__main__':
    splash_message()
    program_menu()
