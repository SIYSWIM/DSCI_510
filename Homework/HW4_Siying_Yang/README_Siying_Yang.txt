DSCI 510 Homework 4: Data Collection

Project Description
This project aims to scrap FIPS code for all states and counties across the United States and use them to access PM 2.5 data from 2011 to 2019. Finally, after manully downloading Emergency Department Visits for Asthma from 2011 to 2019 datasets across the U.S. within the time range, the project iterates all files together and appends all asthma data into one file.

Prerequisites
Before running the Jupyter Notebook, please make sure to install the following libraries:
	•	pandas
	•	time
	•	requests
	•	beautifulsoup4
	•	os
You can install these libraries using pip. For example, run the following command in your terminal:
pip install pandas time requests beautifulsoup4

Files
************
Please keep the original files’ name as some may be the input format for the program, and some may be the output files as the program automatically names.
************
	• HW4_Siying_Yang.ipynb
	• sample datasets:
		⁃ example_states_counties.csv
		⁃ example_pmdata.csv
		⁃ example_asthmadata.csv
	• full datasets
		⁃ states_county_FIPS.csv
		⁃ pmdata_all.csv
		⁃ asthma_all.csv
	• files for program processing
		⁃ pmdata_county.csv
		⁃ asthma folder
	• CurrentProjectPlan(modify)_Siying_Yang.pdf
	• Maintainability_Extensibility_Siying_Yang.pdf
	• README_Siying_Yang.rtf (with read-friendly text style)
	• README_Siying_Yang.txt (as requested)
	• README_Illustration_Siying_Yang.pdf (Flow Chart for the Program Codes)

Guideline for Notebook Cells
 The Jupyter Notebook consists of two parts:
	•	Example functions for data collection and an open test for output with at least 5 entries.
	•	Full programs for each collection, necessary pre-processing steps, and output files are provided.
Please run the cells step by step in each part.

Sample Code Explanation
This repository contains sample programs for retrieving and processing FIPS codes for states and counties as well as data on PM 2.5 pollutants by county and year using the EPA's Air Quality System API. Also, a sample output for downloaded asthma data is provided.
Getting Started
Install required packages in Prerequisites
Description and Usage
example_FIPScode: contains functions for retrieving and processing FIPS codes for states and counties.
	⁃	example_statecode(): retrieves a pandas dataframe of FIPS codes for states.
	⁃	example_countycode(df): retrieves a pandas dataframe of FIPS codes for counties. Requires the output from example_statecode() as an input.

example_PMdata: contains function for retrieving data on PM 2.5 pollutants by county and year using the EPA's Air Quality System API.
	⁃	example_PMdata(email, key, years, pollutant, df): retrieves a pandas dataframe of PM 2.5 pollutant data by county and year using the EPA's Air Quality System API. 
	▪	email: string - the email address used to register the API key
	▪	key: string - the API key obtained from the CDC website
	▪	years: list - a list of integers representing the years to query PM 2.5 data for
	▪	pollutant: string - a string representing the pollutant to query PM 2.5 data for (e.g., '88101’, for more parameters, please see details on the official website)
	▪	dataframe: the output pandas DataFrame from example_FIPScode() that contains the FIPS code for states and counties
example_asthma: contains an asthma(df) function to output 5 sample entries for downloaded asthma data.
	▪	df: a CSV file for asthma data
Output
	•	example_states_counties.csv: a CSV file containing FIPS codes for states and counties.
	•	example_PMdata.csv: a CSV file containing data on PM 2.5 pollutants by county and year.
	•	example_asthmadata.csv: a CSV file containing data on ED visits for asthma by counties and year

FIPS Code Program: FIPScode
This program scrapes FIPS codes for all states and counties in the United States from the Wikipedia page "Federal Information Processing Standard state code". The program outputs a CSV file with the state and county FIPS codes.
Getting Started
Install required packages in Prerequisites
How to Use
1. Run the program with functions
	⁃	statecode()
	This function scrapes the state table from the Wikipedia page and returns a pandas dataframe with the following columns:
	⁃	State Name
	⁃	Alpha Code
	⁃	State FIPS Code
	⁃	county_link

	⁃	countycode(links)
	This function needs a parameter from the output of the statecode() function, which is a series of links for counties’ pages, and takes a list of county links and scrapes the county tables from the Wikipedia pages. It returns a pandas dataframe with the following columns:
	⁃	county_link
	⁃	County Name
	⁃	County FIPS Code

	⁃	FIPScode
	This variable merges the state and county dataframes based on county_link and drops unnecessary columns. It renames columns and outputs the final dataframe to a CSV file.

2. The program will scrape data from the Wikipedia page and create a CSV file with the FIPS codes.
3. The output CSV file will be named "states_county_FIPS.csv" and will contain the following columns:
	▪	State Name
	▪	Alpha Code
	▪	State FIPS Code
	▪	County Name
	▪	County FIPS Code

PM 2.5 Data Program: PMdata
This Python program queries the United States Environmental Protection Agency (EPA) Air Quality System (AQS) to collect annual PM 2.5 concentration data for counties across multiple states in the United States. The program outputs a CSV file with each county’s maximum annual PM 2.5 concentration in the given time range.
Getting Started
Install required packages in Prerequisites, downloaded CSV of FIPScode output file as the pre-processing program requires.
******
Note that the sample program differs from the full program, as the sample program does not read a file for input but only reads dataframe from the previous step. 
When directly web scrapping from Wikipedia, all FIPS codes are formatted as a string, and when stored in a CSV, the codes are in numeric type. The full programs are run separately for extensibility, so each progress will generate a CSV for the following data scraping and integration and needs a pre-processing step.
******
How to Use
1. Run the program in a Python environment.
	⁃	format_county_code(), format_state_code()
	These formatting functions ensure that the FIPS codes for counties and states are properly formatted for API queries.
	⁃	query_api(email, key, years, pollutant, dataframe) with following parameters:
	▪	email: email address used to register the AQS API key.
	▪	key: the AQS API key.
	▪	years: a list of years within which to query PM 2.5 data.
	▪	pollutant: the AQS parameter code for PM 2.5.
	▪	dataframe: a data frame from the previous formatting functions with FIPS codes grouped by states
	The query_api() function requires a CSV file of states_county_FIPS.csv from FIPScode, and outputs a pandas DataFrame containing annual PM 2.5 concentration data for each county in the states that are available for asthma data from 2011 to 2019.

2. The program will output a CSV file named pmdata_all.csv containing each county’s maximum annual PM 2.5 concentration in the given time range in the working directory.

Asthma ED visits Data Program: AsthmaData
This program is designed to combine data from downloaded multiple CSV files containing asthma emergency department visit data, clean and format the data, and output a single CSV file with the cleaned data.
Getting Started
Install required packages in Prerequisites, and download asthma folders to the current path as the program requires input files.
How to Use
Run the program to generate a single CSV file called asthma_all.csv containing all the data.
The file has the following columns:
	▪	State FIPS Code
	▪	State Name
	▪	County FIPS Code
	▪	County Name
	▪	Year
	▪	EDvisit
Limitations
This program assumes that all input files have the same column headers and format. If this is not the case, the program may not work correctly. *****Please do not change the files’ format.
Additionally, the program assumes that all input files are located in a directory called asthma in the same directory as the program file. If this is not the case, the program cannot find the input files. *****Please download the asthma folder and put it in the same path as the jupyter notebook.


Further Analysis (Not included in Jupyter Notebook)
Combine output files from PMdata and AsthmaData for correlational analysis.
Using PMdata and AsthmaData separately for visualization.

Authors
	•	Siying Yang

Acknowledgments
	•	EPA's Air Quality System API
	•	Pandas
	•	Requests
	•	Beautiful Soup
	•	CDC National Environmental Public Health Tracking Network
