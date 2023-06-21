from get_weather import asyncGetWeather

import time                                             # needed for the sleep function
import json
from bs4 import BeautifulSoup                           # used to parse the HTML
from selenium import webdriver                          # used to render the web page
from seleniumwire import webdriver                      
from selenium.webdriver.chrome.service import Service   # Service is only needed for ChromeDriverManager


import functools                                        # used to create a print function that flushes the buffer
flushprint = functools.partial(print, flush=True)       # create a print function that flushes the buffer immediately

""" 
Description:
    This is an example gui that allows you to enter the appropriate parameters to get the weather from wunderground.
TODO:
    - You will need to change the text input boxes to drop down boxes and add the appropriate values to the drop down boxes.
    - For example the month drop down box should have the values 1-12.
    - The day drop down box should have the values 1-31.
    - The year drop down box should have the values ??-2023.
    - The filter drop down box should have the values 'daily', 'weekly', 'monthly'.
"""
import PySimpleGUI as sg      

def currentDate(returnType='tuple'):
    """ Get the current date and return it as a tuple, list, or dictionary.
    Args:
        returnType (str): The type of object to return.  Valid values are 'tuple', 'list', or 'dict'.
    """
    from datetime import datetime
    if returnType == 'tuple':
        return (datetime.now().month, datetime.now().day, datetime.now().year)
    elif returnType == 'list':
        return [datetime.now().month, datetime.now().day, datetime.now().year]

    return {
        'day':datetime.now().day,
        'month':datetime.now().month,
        'year':datetime.now().year
    }

def get_icao_codes_from_json(json_file):
    icao_codes = []
    
    with open(json_file) as file:
        data = json.load(file)
        
        for entry in data:
            icao_code = entry.get("icao")
            if icao_code:
                icao_codes.append(icao_code)
    
    return icao_codes

def buildWeatherURL(month=None, day=None, year=None, airport=None, filter=None):
    """ A gui to pass parameters to get the weather from the web.
    Args:
        month (int): The month to get the weather for.
        day (int): The day to get the weather for.
        year (int): The year to get the weather for.
    Returns:
        Should return a URL like this, but replace the month, day, and year, filter, and airport with the values passed in.
        https://www.wunderground.com/history/daily/KCHO/date/2020-12-31
    """
    current_month,current_day,current_year = currentDate('tuple')
    
    if not month:
        month = current_month
    if not day:
        day = current_day
    if not year:
        year = current_year
    
    # Create the gui's layout using text boxes that allow for user input without checking for valid input
    layout = [
         [sg.Text('Month')], [sg.Combo(list(range(1, 13)), default_value=month)],
         [sg.Text('Day')], [sg.Combo(list(range(1, 32)), default_value=day)],
         [sg.Text('Year')], [sg.Combo(list(range(2000, 2024)), default_value=year)],
        [sg.Text('Code')],[sg.Combo(get_icao_codes_from_json("/Users/nirupavardhan/Projects/4883-softwareTools-Lingareddy/assignments/A07/airports-better.json"))],
        [sg.Text('Daily / Weekly / Monthly')],[sg.Combo(["daily","weekly","monthly"])],
        [sg.Submit(), sg.Cancel()]
    ]      

    window = sg.Window('Get The Weather', layout)    

    event, values = window.read()
    window.close()
        
    month = values[0]
    day = values[1]
    year = values[2]
    code = values[3]
    filter = values[4]

    return month,day,year,code,filter
    # return the URL to pass to wunderground to get appropriate weather data

if __name__=='__main__':
    month,day,year,code,filter = buildWeatherURL()
    url = f'http://www.wunderground.com/history/{filter}/{code}/date/{year}-{month}-{day}'
    print(url)
    # get the page source HTML from the URL
    page = asyncGetWeather(url)

    # parse the HTML
    soup = BeautifulSoup(page, 'html.parser')
    data=[]
    datahead=[]
    # find the appropriate tag that contains the weather data
    history = soup.find('lib-city-history-observation')
    # print(history)
    for row in history:
        if row:
            cellsHead = row.find_all('th')
            datahead = [cell.get_text(strip=True) for cell in cellsHead]
            #datahead.append(data_row)
            tbody=row.find('tbody')
            cells = tbody.find_all('tr')
            for tr in cells:
                data_row_td=[]
                for td in tr.find_all('td'):
                    data_row_td.append(td.get_text(strip=True) )
                data.append(data_row_td)
    print("+++++++",data)
    print("-------",datahead)
    history = soup.find('lib-city-history-observation')

    # # print the parsed HTML
    # print(history.prettify())

    layout = [
        [sg.Table(values=data, headings=datahead, auto_size_columns=True,
                   justification='left')],
        [sg.OK()]
    ]
    
    window = sg.Window('Weather Data', layout)
    event, _ = window.read()
    window.close()