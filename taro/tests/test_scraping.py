from taro.data.scrapers import get_armed_conflicts
from taro.data.scrapers import get_conflict_belligerents


def test_conflicts_success(): 
        assert get_armed_conflicts() != None, 'Scraping not successfull!'
        
def test_conflicts_keys():
        assert list(get_armed_conflicts()[0].keys()) == ['name', 'country', 'url', 'cum_fat']
        

def test_belligerent_ethiopia_example():
    expected_output = [{'name': 'Ethiopia', 'url': 'https://en.wikipedia.org//wiki/Ethiopia'},
                        {'name': 'Eritrea', 'url': 'https://en.wikipedia.org//wiki/Eritrea'},
                        {'name': 'UFEFCF',
                            'url': 'https://en.wikipedia.org//wiki/United_Front_of_Ethiopian_Federalist_and_Confederalist_Forces'},
                        {'name': 'Sudan', 'url': 'https://en.wikipedia.org//wiki/Sudan'},
                        {'name': 'Al-Qaeda', 'url': 'https://en.wikipedia.org//wiki/Al-Qaeda'}]


    assert  get_conflict_belligerents('https://en.wikipedia.org/wiki/Ethiopian_civil_conflict_(2018%E2%80%93present)') == expected_output
    
def test_full_call_first_example():
    res = get_armed_conflicts()
    bel = get_conflict_belligerents(res[0]['url'])
    expectec_output = [{'name': 'State Administration Council', 'url': 'https://en.wikipedia.org//wiki/State_Administration_Council'}, 
                       {'name': 'National Unity Government', 'url': 'https://en.wikipedia.org//wiki/National_Unity_Government_of_Myanmar'}]
    assert bel == expectec_output
    
def test_all_conflicts():
    conflicts = get_armed_conflicts()
    results = [get_conflict_belligerents(conflict['url'], write_logs=True) for conflict in conflicts]
    
    assert [] not in results

if __name__ == "__main__":
    print(test_all_conflicts())