# File:        launch.py
# Authors:     Bhavyai Gupta, Brandon Attai
# Description: Source Code to display the menu for the Project

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

    # show the splash screen for 1 second and then clear again
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
        print("\n[4] Print stats for relation between Life Expectancy and Urbanization")
        print("\n[5] Print stats for relation between Tertiary Education in all countries")
        print("\n[6] Print stats for relation between Fertility and Literacy")
        print("\n[7] Print stats for relation between Urbanization and Fertility")

        print("\n[0] Exit")

        # loop to get valid choice from the user
        while(True):
            try:
                choice = int(input("\nPlease enter the menu option number: "))

                if choice < 0 or choice > 7:
                    raise ValueOutOfRange("This option is not supported. Please choose a valid menu option")

                elif choice == 0:
                    print("\nBye!\n")
                    return

                else:
                    break

            except ValueError as e:
                print("\n" + color.red + "Please enter a valid menu option" + color.reset)

            except ValueOutOfRange as e:
                print("\n" + color.red + str(e) + color.reset)

            except KeyboardInterrupt as e:
                print("\n\nYou pressed Ctrl+C. Bye!\n")
                return


        # after getting a valid option from the user, perform the requested option

        if choice == 1:
            analysis.print_imported()
            input("\n" + color.blue + "Press enter to return to the menu " + color.reset)

        elif choice == 2:
            analysis.export_dataset()
            input("\n" + color.blue + "Press enter to return to the menu " + color.reset)

        elif choice == 3:
            analysis.aggregate_stats()
            input("\n" + color.blue + "Press enter to return to the menu " + color.reset)

        elif choice == 4:
            # call function for Urbanization and Fertility
            input("\n" + color.blue + "Press enter to return to the menu " + color.reset)

        elif choice == 5:
            # call function for stats for Life Expectancy and Urbanization
            input("\n" + color.blue + "Press enter to return to the menu " + color.reset)

        elif choice == 6:
            # call function for stats for Tertiary Education
            input("\n" + color.blue + "Press enter to return to the menu " + color.reset)

        else: # choice == 7
            # call function for stats for Fertility and Literacy
            input("\n" + color.blue + "Press enter to return to the menu " + color.reset)



if __name__ == '__main__':
    splash_message()
    program_menu()
