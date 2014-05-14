import unittest

from nose.tools import raises

from uni.assertions import AssertionSet, AssertionFailed


class TestScannerCheck(unittest.TestCase):

    querylist = [
        {'$exists': 'moocow'},
        {'age': {'$lt': 50}},
        {'cowtype': 'huge'}
    ]

    def test_scanner_check(self):
        with AssertionSet(self.querylist) as scanner:
            scanner.check({'moocow': True})
            scanner.check({'age': 300})
            scanner.check({'age': 3})
            scanner.check({'cowtype': 'wee'})
            scanner.check({'cowtype': 'huge'})
        self.assertTrue(scanner.success)

    def test_scanner_check_false(self):
        with AssertionSet(self.querylist) as scanner:
            scanner.check({'moocow': True})
            scanner.check({'age': 300})
            scanner.check({'cowtype': 'wee'})
        self.assertFalse(scanner.success)

    @raises(AssertionFailed)
    def test_scanner_check_raises(self):
        with AssertionSet(self.querylist, raise_failure=True) as scanner:
            scanner.check({'moocow': True})
            scanner.check({'age': 300})
            scanner.check({'cowtype': 'wee'})
        self.assertTrue(scanner.success)

    def test_scanner_check_all(self):
        scanner = AssertionSet(self.querylist)
        datalist = [
            {'moocow': True},
            {'age': 300},
            {'age': 3},
            {'cowtype': 'wee'},
            {'cowtype': 'huge'}]
        self.assertTrue(scanner.check_all(datalist))

    def test_scanner_check_all_false(self):
        scanner = AssertionSet(self.querylist)
        datalist = [
            {'moocow': True},
            {'age': 300},
            {'cowtype': 'wee'}]
        self.assertFalse(scanner.check_all(datalist))

    @raises(AssertionFailed)
    def test_scanner_check_all_raises(self):
        scanner = AssertionSet(self.querylist, raise_failure=True)
        datalist = [
            {'moocow': True},
            {'age': 300},
            {'cowtype': 'wee'}]
        scanner.check_all(datalist)
