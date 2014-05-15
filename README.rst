

Test mongo-style queries on arbitrary python objects
====================================================

[![Build Status](https://travis-ci.org/opencivicdata/python-opencivicdata.svg?branch=master)](https://travis-ci.org/opencivicdata/python-opencivicdata)
[![Coverage Status](https://coveralls.io/repos/opencivicdata/python-opencivicdata/badge.png?branch=master)](https://coveralls.io/r/opencivicdata/python-opencivicdata?branch=master)
[![Latest Version](https://pypip.in/version/opencivicdata/badge.png)](https://pypi.python.org/pypi/opencivicdata/)
[![Download Format](https://pypip.in/format/opencivicdata/badge.png)](https://pypi.python.org/pypi/opencivicdata/)

    import uni

    data = {
        'species': 't-rex',
        'uni': {
            'age': 3,
            },
        'info': {
            'unicorns_are_real': True,
            'unicorns_that_exist': ['uni', "uni's brother"]
            }
        }

    spec  = {
        '$and': [
            {'uni.age': {'$ne': 4}},
            {'species': {
                '$in': ['cow', 'pig', 't-rex']}
                },
            {'info.unicorns_are_real': True},
            {'info.unicorns_that_exist': 'uni'},
            ]
        }

    result = uni.check(spec, self.checkable)
    print(result)  # True!


Test a stream of python objects agaist a suite of assertions
============================================================

    import uni

    querylist = [
        {'$exists': 'moocow'},
        {'age': {'$lt': 50}},
        {'cowtype': 'huge'}
    ]

    with uni.AssertionSet(self.querylist) as scanner:
        scanner.check({'moocow': True})
        scanner.check({'age': 300})
        scanner.check({'age': 3})
        scanner.check({'cowtype': 'wee'})
        scanner.check({'cowtype': 'huge'})

    print(scanner.success)  # True!
