from .solver import polymer_reaction, units_react, clean_polymer


def test_units_react():
    assert units_react('C', 'c')
    assert units_react('z', 'Z')
    assert not units_react('C', 'C')
    assert not units_react('s', 's')
    assert not units_react('a', 'Z')
    assert not units_react('a', 'z')
    assert not units_react('A', 'z')


def test_polymer_reaction():
    polymer = 'dabAcCaCBAcCcaDA'
    assert polymer_reaction(polymer) == 'dabCBAcaDA'


def test_clean_polymer():
    test_polymer = 'dabAcCaCBAcCcaDA'
    options_to_test = [
        ('a', 'dbcCCBcCcD'),
        ('B', 'daAcCaCAcCcaDA'),
        ('c', 'dabAaBAaDA'),
        ('D', 'abAcCaCBAcCcaA'),
    ]

    for unit_to_clean, expected_polymer in options_to_test:
        assert clean_polymer(test_polymer, unit_to_clean)
