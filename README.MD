# UN Stats

## What is it

A mini data science project to process the UN Population and GDP data based on user inputs using NumPy/Pandas and display the statistics using Matplotlib

Below datasets are used in the project

+ [UN Region, Sub-Region and Country](https://data.un.org/_Docs/SYB/CSV/SYB63_1_202105_Population,%20Surface%20Area%20and%20Density.csv)

+ [Population Growth, Fertility, Life Expectancy and Mortality](https://data.un.org/_Docs/SYB/CSV/SYB62_246_201907_Population%20Growth,%20Fertility%20and%20Mortality%20Indicators.csv)

+ [Population in the Capital City, Urban and Rural Areas](https://data.un.org/_Docs/SYB/CSV/SYB61_253_Population%20Growth%20Rates%20in%20Urban%20areas%20and%20Capital%20cities.csv)

+ [GDP and GDP per Capita](https://data.un.org/_Docs/SYB/CSV/SYB63_230_202009_GDP%20and%20GDP%20Per%20Capita.csv)



### Course Instructor

[Dr. Emily Marasco](https://schulich.ucalgary.ca/contacts/emily-marasco)



### Group Members

[Bhavyai Gupta (myself)](https://github.com/zbhavyai)

[Brandon Attai](https://github.com/b-attai)



## Features

+ Decide what data statistics you want by the use of menu options

+ Print stats for the entire dataset or for a subset of data

+ Compare countries on various statistics and plot the graphs



## Dependencies

+ numpy 1.20.3

+ pandas 1.2.4

+ matplotlib 3.4.2

+ openpyxl 3.0.7



## How to use

+ Run the `launch.py` file

   ```python
   python launch.py
   ```

+ Follow the onscreen instructions



## Screenshots

+ Launching the program

   ![Screenshots/01_How_To_Start.png](Screenshots/01_How_To_Start.png)


+ Initial checks by the program

   ![Screenshots/02_Program_Reporting_Initial_Checks.png](Screenshots/02_Program_Reporting_Initial_Checks.png)


+ Program Menu

   ![Screenshots/03_Program_Menu.png](Screenshots/03_Program_Menu.png)


+ Menu Option 1: Print Dataframes

   ![Screenshots/04_Menu_Option_1_Print_Dataframes_Part_1.png](Screenshots/04_Menu_Option_1_Print_Dataframes_Part_1.png)

   ![Screenshots/05_Menu_Option_1_Print_Dataframes_Part_2.png](Screenshots/05_Menu_Option_1_Print_Dataframes_Part_2.png)


+ Menu Option 2: ReExporting Dataframe

   ![Screenshots/06_Menu_Option_2_ReExporting_Dataframe.png](Screenshots/06_Menu_Option_2_ReExporting_Dataframe.png)


+ Menu Option 3: Aggregate Stats for entire dataset

   ![Screenshots/07_Menu_Option_3_Aggregate_Stats.png](Screenshots/07_Menu_Option_3_Aggregate_Stats.png)


+ Menu Option 4: Aggregate Stats for subset of data

   ![Screenshots/08_Menu_Option_4_GroupBy_Part_1.png](Screenshots/08_Menu_Option_4_GroupBy_Part_1.png)

   ![Screenshots/09_Menu_Option_4_GroupBy_Part_2.png](Screenshots/09_Menu_Option_4_GroupBy_Part_2.png)


+ Menu Option 5: Countries with higher GDP per capita than USA

   ![Screenshots/10_Menu_Option_5_Additional_Column.png](Screenshots/10_Menu_Option_5_Additional_Column.png)


+ Comparing four distinct countries on various statistics

   ![Screenshots/11_Menu_Option_6_Pivot_Table.png](Screenshots/11_Menu_Option_6_Pivot_Table.png)

   ![Screenshots/12_Menu_Option_6_Plots.png](Screenshots/12_Menu_Option_6_Plots.png)


+ Exiting the program

   ![Screenshots/13_Menu_Option_0_Exit.png](Screenshots/13_Menu_Option_0_Exit.png)
