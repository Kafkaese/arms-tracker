from bs4 import BeautifulSoup
import requests as re
from os import path

def get_armed_conflicts() -> list:
    res = re.get('https://en.wikipedia.org/wiki/List_of_ongoing_armed_conflicts').content

    soup = BeautifulSoup(res, 'html.parser')

    
    # Tables are classed by numbe of combat related deaths
    #table_numbers = ['10000','1000', '100']
    
    # First 4 tables contain the data 
    tables =soup.find_all('table')[:4]

    conflicts = []
    
    #Iterate over conflict tables
    for table in tables:
        
        #extract conflicts as rows. Skip header by starting at tbody (does not work)

        conflict_rows = table.find('tbody').find_all('tr')
        for conflict in conflict_rows[1:]:

            # Get row
            row = conflict.find_all('td')
            
            # Get conflict name
            name = row[1].find('a').text
            
            # Get conflict url 
            url = row[1].find('a')['href']
            
            # Get country name
            country = row[3].find('a').text
            
            # Get cumulative fatalities
            cum_fat = row[4].find('span').text + ' ' + row[4].text
            
            # Build dictionary
            conflicts.append({'name': name, 'country': country, 'url': 'https://en.wikipedia.org/' + url, 'cum_fat': cum_fat})
        
    return conflicts
    
def get_conflict_belligerents(url: str, write_logs=False) -> list:
    
    # Path for logs if enabled
    if write_logs:
        logs_path = path.join(path.dirname(__file__),"..", "..", "logs", "data_scrapers_get_conflict_belligerents")
    
    # Get soup
    result = re.get(url)
    soup = BeautifulSoup(result.content, 'html.parser')
    
    ## Get table rows with all belligerents
    
    # Header text is either Belligerents or Combatants or Parties to the civil conflict
    header = soup.find('th', string="Belligerents")
    if header == None:
        header = soup.find('th', string="Combatants")
    if header == None:
        header = soup.find('th', string="Parties to the civil conflict")
    if header == None:
        if write_logs:
            with open(logs_path, 'a') as logs:
                logs.write(f"!FAILED:{url}:header")
        
        return []
  
    parties = header.parent.find_next_sibling(header.parent.name).find_all('td')

    # Extract countries from parties
    belligerents = []
    for party in parties:
        
        for country in party.find_all('p'):
            try:
                country_info = country.find('a')
                belligerents.append({'name': country_info.text, 'url': 'https://en.wikipedia.org/' + country_info['href']})
                
                if write_logs:
                    with open(logs_path, 'a') as logs:
                        logs.write(f"SUCCESS:{url}:{country_info.text}\n")
            except:
                
                if write_logs:
                    with open(logs_path, 'a') as logs:
                        logs.write(f"!FAILED:{url}:'{country}'")
                
    

    return belligerents
