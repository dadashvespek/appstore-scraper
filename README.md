# Google Play Store Scraper
This is a Python script that scrapes data from the Google Play Store related to user-defined keywords. The script collects data on the name, developer, rating, reviews, installs, last updated, and whether the app contains ads or has in-app purchases. The script also collects the URLs for the recommended apps for each app. The data is stored in a pandas dataframe and written to a data file.

## Installation
To use the script, you need to have Python 3 installed along with the required libraries, including requests, BeautifulSoup, and pandas. You can install these libraries using pip, the package installer for Python. To install requests, BeautifulSoup, and pandas, run the following command in your terminal:

```
pip install -r requirements.txt
```
You will also need to create a custom module called context_words.py, which should contain a list of keywords related to the app category. This module should be placed in the same directory as the script.

## Usage
To run the script, you need to define a list of keywords in the keywords variable. Then, you call the main() function with the list of keywords as an argument. The script will loop through each keyword and collect data for all the related apps. The resulting data will be stored in a file called data.csv in the same directory as the script.
