from taro.data.scrapers import get_armed_conflicts


def test_success(): 
        assert get_armed_conflicts() != None, 'Scraping not successfull!'
        
def test_keys():
    assert list(get_armed_conflicts()[0].keys()) == ['name', 'country', 'cum_fat']
        