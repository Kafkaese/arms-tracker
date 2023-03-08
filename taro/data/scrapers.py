from bs4 import BeautifulSoup
import requests as re

def get_armed_conflicts():
    res = re.get('https://en.wikipedia.org/wiki/List_of_ongoing_armed_conflicts').content

    soup = BeautifulSoup(res, 'html.parser')

    
    # Tables are classed by numbe of combat related deaths
    #table_numbers = ['10000','1000', '100']
    
    # First 4 tables contain the data 
    tables =soup.find_all('table')[:3]


    
if __name__ == "__main__":
    get_armed_conflicts()