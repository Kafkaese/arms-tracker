from taro.data.scrapers import get_conflict_belligerents

def test_example():
    assert  get_conflict_belligerents('https://en.wikipedia.org/wiki/Ethiopian_civil_conflict_(2018%E2%80%93present)') == ['Ethiopia', 'Eritrea', 'UFEFCF', 'Sudan', 'Al-Qaeda']