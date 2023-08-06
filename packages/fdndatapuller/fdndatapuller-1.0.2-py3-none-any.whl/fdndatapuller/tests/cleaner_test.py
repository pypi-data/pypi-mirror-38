from util.cleaner import cleanreview, cleantitle

def test_cleaner():
    '''test to prevent regression on title'''
    tst_str = '''Dior - SOURCILS POUDRE
POWDER EYEBROW PENCIL WITH A BRUSH AND SHARPENER'''
    assert '\n' not in cleantitle(tst_str)

    tst_str = '''Estee Lauder - Estee Lauder Resilience Lift Night Lifting/Firming
Face and Neck Creme'''
    assert '\n' not in cleantitle(tst_str)