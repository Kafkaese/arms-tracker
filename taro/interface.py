from taro.data.scrapers import get_armed_conflicts, get_conflict_belligerents
from taro.data.database import create_write_dict_db

def run_scraper():
    # scrape all conflicts
    conflicts = get_armed_conflicts()
    
    # scrape belligerent information for all conflicts
    results = [get_conflict_belligerents(conflict['url']) for conflict in conflicts]
    
    print(conflicts)
    # dump conflicts into database
    create_write_dict_db('conflicts', conflicts)