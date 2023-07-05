from fastapi import FastAPI, Response
from fastapi.responses import HTMLResponse
from typing import Optional
import pandas as pd
import csv
import uvicorn
from fastapi.responses import RedirectResponse


app = FastAPI()

class DataReader:
    def __init__(self, csv_file):
        self.data = None
        self.load_data(csv_file)

    def load_data(self, csv_file):
        self.data = pd.read_csv(csv_file)

    def get_attribute(self, attribute):
        return self.data[attribute].unique().tolist()

# Instantiate the DataReader class with the CSV file path
mydb = DataReader('data1.csv')

# Define the root endpoint
@app.get("/", response_class=HTMLResponse)
async def docs_redirect():
    """Redirects to the docs page."""
    return RedirectResponse(url="/docs")
    

# Define the countries route
@app.get("/countries/")
async def countries():
    """Returns a list of unique countries."""
    response = mydb.get_attribute('Country')
    country={
        "success":True,
        "countries":response
    }
    return country

# Define the regions route
@app.get("/regions/")
async def regions():
    """Returns a list of unique WHO regions."""
    response = mydb.get_attribute('WHO_region')
    regions={
        "success":True,
        "countries":response
    }
    return regions

# Define the deaths route
@app.get("/deaths/")
async def deaths(country: Optional[str] = None, year: Optional[int] = None, region: Optional[str] = None):
    
    """
    This method will return a total death count or can be filtered by country , region,and year.
    
    - **Params:**
      - country (str) : A country name
      - region(str): A region name
      - year (int) : A 4 digit year
    - **Returns:**
      - (int) : The total sum based on filters (if any)

    #### Example 1:

    [http://127.0.0.1:8000/deaths/](http://127.0.0.1:8000/deaths/)

    #### Response 1:

        {
        "total_death": 6945714,
        "success": true,
        "params": {
            "country": null,
            "region": null,
            "year": null
        }
        }

    #### Example 2:

    [http://127.0.0.1:8000/deaths/?country=Nepal](http://127.0.0.1:8000/deaths/?country=Nepal)

    #### Response 2:

        {
            "total_death": 12031,
            "success": true,
            "params": {
             "country": "Nepal",
            "region": null,
            "year": null
        }
        }

    """
    response = int(mydb.data['New_deaths'].sum())
    message = f"Total number of entire deaths: {response}"

    if year is not None:
        if country is not None:
            response = int(mydb.data.loc[(pd.to_datetime(mydb.data['Date_reported']).dt.year == int(year)) & (mydb.data['Country'] == country), 'New_deaths'].sum())
            message = f"Total number of deaths in {year} for the country of {country} is {response}"
        elif region is not None:
            response = int(mydb.data.loc[(pd.to_datetime(mydb.data['Date_reported']).dt.year == int(year)) & (mydb.data['WHO_region'] == region), 'New_deaths'].sum())
            message = f"Total number of deaths in {year} for the WHO region of {region} is {response}"
        else:
            response = int(mydb.data.loc[pd.to_datetime(mydb.data['Date_reported']).dt.year == int(year), 'New_deaths'].sum())
            message = f"Total number of deaths in {year} is {response}"
    else:
        if country is not None:
            response = int(mydb.data[mydb.data['Country'] == country]['New_deaths'].sum())
            message = f"Total number of deaths in the country of {country} is {response}"
        if region is not None:
            response = int(mydb.data[mydb.data['WHO_region'] == region]['New_deaths'].sum())
            message = f"Total number of deaths in the WHO region of {region} is {response}"
    body={
        "total_death":response,
        "success":True,
        "params":{
            "country":country,
            "region":region,
            "year":year
        }
    }
    return body

# Define the cases route
@app.get("/cases/")
async def get_cases(country: Optional[str] = None, year: Optional[int] = None, region: Optional[str] = None):
    """
    This method will return a total number of cases and can be filtered by country , region,and year.
    
    - **Params:**
      - country (str) : A country name
      - region(str): A region name
      - year (int) : A 4 digit year
    - **Returns:**
      - (int) : The total sum based on filters (if any)

    #### Example 1:

    [http://127.0.0.1:8000/cases/](http://127.0.0.1:8000/cases/)

    #### Response 1:

        {
            "total_cases": 768187096,
            "success": true,
            "params": {
                 "country": null,
                "region": null,
                "year": null
            }
            }

    #### Example 2:

    [http://127.0.0.1:8000/cases/?country=India](http://127.0.0.1:8000/cases/?country=India)

    #### Response 2:

        {
            "total_cases": 44993543,
            "success": true,
            "params": {
                 "country": "India",
                "region": null,
                 "year": null
            }
            }

    """
    response = int(mydb.data['New_cases'].sum())
    message = f"Total number of entire cases: {response}"

    if year is not None:
        if country is not None:
            response = int(mydb.data.loc[(pd.to_datetime(mydb.data['Date_reported']).dt.year == int(year)) & (mydb.data['Country'] == country), 'New_cases'].sum())
            message = f"Total number of cases in {year} for the country of {country} is {response}"
        elif region is not None:
            response = int(mydb.data.loc[(pd.to_datetime(mydb.data['Date_reported']).dt.year == int(year)) & (mydb.data['WHO_region'] == region), 'New_cases'].sum())
            message = f"Total number of casaes in {year} for the WHO region of {region} is {response}"
        else:
            response = int(mydb.data.loc[pd.to_datetime(mydb.data['Date_reported']).dt.year == int(year), 'New_cases'].sum())
            message = f"Total number of cases in {year} is {response}"
    else:
        if country is not None:
            response = int(mydb.data[mydb.data['Country'] == country]['New_cases'].sum())
            message = f"Total number of cases in the country of {country} is {response}"
        if region is not None:
            response = int(mydb.data[mydb.data['WHO_region'] == region]['New_cases'].sum())
            message = f"Total number of cases in the WHO region of {region} is {response}"
    body={
        "total_cases":response,
        "success":True,
        "params":{
            "country":country,
            "region":region,
            "year":year
        }
    }
    return body

@app.get("/max_deaths/")
async def get_max_deaths(min_date: str = None, max_date: str = None):
    """
    This method will return maximum deaths and can be filtered by minimum date and maximum data
    
    - **Params:**
      - minimum date (str) : min date
      - maximum date (str): max date
      
    - **Returns:**
      - (int) : The total sum based on filters (if any)

    #### Example 1:

    [http://127.0.0.1:8000/max_deaths/](http://127.0.0.1:8000/max_deaths/)

    #### Response 1:

        {
            "data": "United States of America",
            "success": true,
            "total_death": "1127152",
             "message": "The country with the maximum deaths is United States of America with 1127152 deaths"
        }

    #### Example 2:

    [http://127.0.0.1:8000/max_deaths/?min_date=2023-05-31&max_date=2023-06-30](http://127.0.0.1:8000/max_deaths/?min_date=2023-05-31&max_date=2023-06-30)

    #### Response 2:

       {
             "data": "Brazil",
            "success": true,
             "total_death": "735",
             "message": "The country with the maximum deaths between 2023-05-31 00:00:00 and 2023-06-30 00:00:00 is Brazil with 735 deaths"
        }

    """

    mydb.data['Date_reported'] = pd.to_datetime(mydb.data['Date_reported'])

    if min_date is not None and max_date is not None:
        start_date = pd.to_datetime(min_date)
        end_date = pd.to_datetime(max_date)
        if start_date > end_date:
            start_date, end_date = end_date, start_date
        message = f"The country with the maximum deaths between {start_date} and {end_date} is"
    else:
        start_date = mydb.data['Date_reported'].min()
        end_date = mydb.data['Date_reported'].max()
        message = "The country with the maximum deaths is"

    filtered_df = mydb.data[(mydb.data['Date_reported'] >= start_date) & (mydb.data['Date_reported'] <= end_date)]
    grouped_df = filtered_df.groupby('Country')['New_deaths'].sum().reset_index()

    max_deaths_sum = grouped_df['New_deaths'].max()
    country_with_max_deaths_sum = grouped_df.loc[grouped_df['New_deaths'] == max_deaths_sum, 'Country'].values[0]

    response = {
        "data": country_with_max_deaths_sum,
        "success": True,
        "total_death": str(max_deaths_sum),
        "message": f"{message} {country_with_max_deaths_sum} with {max_deaths_sum} deaths"
    }

    return response

@app.get("/min_deaths/")
async def get_min_deaths(min_date: str = None, max_date: str = None):
    """
    This method will return the country with the minimum number of deaths within a specified date range.
    - Params:
        - min_date (str): The minimum date (format: YYYY-MM-DD)
        - max_date (str): The maximum date (format: YYYY-MM-DD)
    - Returns:
        - dict: A dictionary containing the country with the minimum deaths and the corresponding death count.

     #### Example 1:

    [http://127.0.0.1:8000/min_deaths/](http://127.0.0.1:8000/min_deaths/)

    #### Response 1:

        {
             "data": "Democratic People's Republic of Korea",
            "success": true,
            "total_min_death": "0",
            "message": "The country with the minimum deaths is Democratic People's Republic of Korea with 0 deaths"
        }

    #### Example 2:

    [http://127.0.0.1:8000/min_deaths/?min_date=2023-05-31&max_date=2023-06-30](http://127.0.0.1:8000/min_deaths/?min_date=2023-05-31&max_date=2023-06-30)

    #### Response 2:

       {
            "data": "Albania",
            "success": true,
            "Total_min_death": "0",
            "message": "The country with the minimum deaths between 2023-05-31 00:00:00 and 2023-06-30 00:00:00 is Albania with 0 deaths"
        }
    """

    mydb.data['Date_reported'] = pd.to_datetime(mydb.data['Date_reported'])

    if min_date is not None and max_date is not None:
        start_date = pd.to_datetime(min_date)
        end_date = pd.to_datetime(max_date)
        if start_date > end_date:
            start_date, end_date = end_date, start_date
        message = f"The country with the minimum deaths between {start_date} and {end_date} is"
    else:
        start_date = mydb.data['Date_reported'].min()
        end_date = mydb.data['Date_reported'].max()
        message = "The country with the minimum deaths is"

    filtered_df = mydb.data[(mydb.data['Date_reported'] >= start_date) & (mydb.data['Date_reported'] <= end_date)]
    grouped_df = filtered_df.groupby('Country')['New_deaths'].sum().reset_index()

    min_deaths_sum = grouped_df['New_deaths'].min()
    country_with_min_deaths_sum = grouped_df.loc[grouped_df['New_deaths'] == min_deaths_sum, 'Country'].values[0]

    response = {
        "data": country_with_min_deaths_sum,
        "success": True,
        "total_min_death": str(min_deaths_sum),
        "message": f"{message} {country_with_min_deaths_sum} with {min_deaths_sum} deaths"
    }

    return response

@app.get("/avg_deaths/")
async def avg_deaths():
    """
    This method will return the average number of deaths across all countries.
    - Returns:
        - dict: A dictionary containing the average number of deaths.

    #### Example 1:

    [http://127.0.0.1:8000/avg_deaths/](http://127.0.0.1:8000/avg_deaths/)

    #### Response 1:

        {
             "avg_death": 23.149139120523127,
             "success": true,
             "message": "Average number of deaths across all countries: 23.149139120523127"
        }


    """

    avg_deaths = mydb.data['New_deaths'].mean()
    response = {
        "avg_death": avg_deaths,
        "success": True,
        "message": f"Average number of deaths across all countries: {avg_deaths}"
    }

    return response






if __name__ == "__main__":

    # Run the FastAPI app using uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, log_level="debug", reload=True)