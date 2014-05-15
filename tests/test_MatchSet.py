from nose.tools import raises

from uni import MatchSet, MatchSetFailed


class TestMatchSet:

    querylist = [
        {'moocow': {'$exists': True}},
        {'age': {'$lt': 50}},
        {'cowtype': 'huge'}
    ]

    def test_matchset_check(self):
        with MatchSet(self.querylist) as scanner:
            scanner.check({'moocow': True})
            scanner.check({'age': 300})
            scanner.check({'age': 3})
            scanner.check({'cowtype': 'wee'})
            scanner.check({'cowtype': 'huge'})
        assert scanner.success

    def test_matchset_check_false(self):
        with MatchSet(self.querylist) as scanner:
            scanner.check({'moocow': True})
            scanner.check({'age': 300})
            scanner.check({'cowtype': 'wee'})
        assert not scanner.success

    @raises(MatchSetFailed)
    def test_matchset_check_raises(self):
        with MatchSet(self.querylist, raise_failure=True) as scanner:
            scanner.check({'moocow': True})
            scanner.check({'age': 300})
            scanner.check({'cowtype': 'wee'})
        assert scanner.success

    def test_matchset_check_all(self):
        scanner = MatchSet(self.querylist)
        datalist = [
            {'moocow': True},
            {'age': 300},
            {'age': 3},
            {'cowtype': 'wee'},
            {'cowtype': 'huge'}]
        assert scanner.check_all(datalist)

    def test_matchset_check_all_false(self):
        scanner = MatchSet(self.querylist)
        datalist = [
            {'moocow': True},
            {'age': 300},
            {'cowtype': 'wee'}]
        assert not scanner.check_all(datalist)

    @raises(MatchSetFailed)
    def test_matchset_check_all_raises(self):
        scanner = MatchSet(self.querylist, raise_failure=True)
        datalist = [
            {'moocow': True},
            {'age': 300},
            {'cowtype': 'wee'}]
        scanner.check_all(datalist)
