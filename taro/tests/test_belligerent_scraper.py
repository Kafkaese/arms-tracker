from taro.data.scrapers import get_conflict_belligerents

def test_example():
    expected_output = [{'name': 'Ethiopia', 'url': 'https://en.wikipedia.org//wiki/Ethiopia'},
                        {'name': 'Eritrea', 'url': 'https://en.wikipedia.org//wiki/Eritrea'},
                        {'name': 'UFEFCF',
                            'url': 'https://en.wikipedia.org//wiki/United_Front_of_Ethiopian_Federalist_and_Confederalist_Forces'},
                        {'name': 'Sudan', 'url': 'https://en.wikipedia.org//wiki/Sudan'},
                        {'name': 'Al-Qaeda', 'url': 'https://en.wikipedia.org//wiki/Al-Qaeda'}]


    assert  get_conflict_belligerents('https://en.wikipedia.org/wiki/Ethiopian_civil_conflict_(2018%E2%80%93present)') == expected_output