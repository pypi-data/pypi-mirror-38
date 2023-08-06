import json 
import urllib 
import pandas as pd
from datetime import *
import re
import itertools
import functions as fn 


        
def checkCountry(country):       
    if type(country) is str:
        linkAPI = 'http://api.tradingeconomics.com/country/' + urllib.quote(country)
    else:
        multiCountry = ",".join(country)
        linkAPI = 'http://api.tradingeconomics.com/country/' + urllib.quote(multiCountry)
    return linkAPI
    
    
def checkIndic(indicators, linkAPI):       
    if type(indicators) is str:
        linkAPI = linkAPI + '/' + urllib.quote(indicators)
    else:
        multiIndic = ",".join(indicators)
        linkAPI = linkAPI + '/' + urllib.quote(multiIndic)
    return linkAPI

 
def getResults(webResults, country):
        names = ['country', 'category', 'latestvalue', 'latestvaluedate', 'source', 'unit', 'categorygroup', 'frequency', 'previousvalue', 'previousvaluedate']
        names2 = ['Country', 'Category','LatestValue', 'LatestValueDate',  'Source', 'Unit', 'CategoryGroup', 'Frequency', 'PreviousValue', 'PreviousValueDate']
        maindf = pd.DataFrame()  
        for i in range(len(names)):
            names[i] = [d[names2[i]]  for d in webResults]
            maindf = pd.concat([maindf, pd.DataFrame(names[i], columns = [names2[i]])], axis = 1) 
        maindf['Country'] =  maindf['Country'].map(lambda x: x.strip())
        return maindf    

          
def getIndicatorData(country = None, indicators = None, output_type = None, credentials = None):
    """
    Return a list of all indicators, indicators by country or country-indicator pair.
    =================================================================================

    Parameters:
    -----------
    country: string or list.
             String for one country information. List of strings for 
             several countrys, for example country = ['country_name', 'country_name'].
    indicators: string or list.
             String for one indicator. List of strings for several indicators, for example 
             indicators = 'indicator_name' or 
             indicators = ['indicator_name', 'indicator_name']
    output_type: string.
             'dict'(default) for dictionary format output, 'df' for data frame,
             'raw' for list of dictionaries directly from the web. 
    credentials: string.
             User's credentials.

    Notes
    -----
    All parameters are optional. Without parameters a list of all indicators will be provided. 
    Without credentials default information will be provided.

    Example
    -------
    getIndicatorData(country = 'United States', indicators = 'Imports', output_type = 'df')

    getIndicatorData(country = ['United States', 'Portugal'], indicators = ['Imports','Exports'])
    """
    if country == None:
        linkAPI = 'http://api.tradingeconomics.com/indicators/'
    else:
        linkAPI = checkCountry(country)
    if indicators == None:
        linkAPI = linkAPI
    else:
        linkAPI = checkIndic(indicators, linkAPI)
    if credentials == None:
        credentials = 'guest:guest'
    else:
        fn.credCheck(credentials)
    linkAPI = linkAPI + '?c=' + credentials
    webResults = json.load(urllib.urlopen(linkAPI))
    if country == None:
        print ('Without country indication only a list of available indicators will be returned...')
        category = [d['Category'] for d in webResults]       
        category_group = [d['CategoryGroup'] for d in webResults]
        output = {'Category': category, 'CategoryGroup': category_group}
    else:
        maindf = getResults(webResults, country)    
        if output_type == None or output_type =='dict':
            output = fn.out_type(maindf)
        elif output_type == 'df': 
            output = maindf
        elif output_type == 'raw':
            output = webResults
        else:
            raise ValueError ('output_type options : df for data frame, dict(defoult) for dictionary by country, raw for results directly from web.')      
    return output
  