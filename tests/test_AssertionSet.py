from nose.tools import raises

from uni import AssertionSet, AssertionFailed


class TestAssertionSet:

    querylist = [
        ({'name': 'Thom'}, {'age': 34}),
        ({'name': 'Mr. B'}, {'age': {'$lt': 5}}),
        ({'cowtype': {'$exists': True}}, {'cowsize': 'huge'})
    ]

    def test_assertionset_check(self):
        with AssertionSet(self.querylist) as scanner:
            scanner.check({'name': 'Mr. B', 'age': 4, 'cute': True})
            scanner.check({'name': 'Thom', 'age': 34, 'cute': False})
            scanner.check({'cowtype': 'heffer', 'cowsize': 'huge'})
        assert scanner.success

    def test_assertionset_check_false(self):
        with AssertionSet(self.querylist) as scanner:
            scanner.check({'name': 'Thom', 'age': 33, 'cute': False})
        assert not scanner.success

    @raises(AssertionFailed)
    def test_assertionset_check_raises(self):
        with AssertionSet(self.querylist, raise_failure=True) as scanner:
            scanner.check({'name': 'Mr. B', 'age': 6, 'cute': True})
        assert scanner.success

    def test_assertionset_check_all(self):
        scanner = AssertionSet(self.querylist)
        datalist = [
            {'name': 'Mr. B', 'age': 4, 'cute': True},
            {'name': 'Thom', 'age': 34, 'cute': False},
            {'cowtype': 'heffer', 'cowsize': 'huge'},]
        assert scanner.check_all(datalist)

    def test_assertionset_check_all_false(self):
        scanner = AssertionSet(self.querylist)
        datalist = [
            {'name': 'Mr. B', 'age': 4, 'cute': True},
            {'name': 'Thom', 'age': 34, 'cute': False},
            {'cowtype': 'heffer', 'cowsize': 'tiny'},]
        assert not scanner.check_all(datalist)

    @raises(AssertionFailed)
    def test_assertionset_check_all_raises(self):
        scanner = AssertionSet(self.querylist, raise_failure=True)
        datalist = [
            {'name': 'Mr. B', 'age': 4, 'cute': True},
            {'name': 'Thom', 'age': 34, 'cute': False},
            {'cowtype': 'heffer', 'cowsize': 'tiny'},]
        scanner.check_all(datalist)
