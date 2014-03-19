import unittest

import uni


class TestComparison(unittest.TestCase):

    checkable = {
        'species': 't-rex',
        'uni': {
            'age': 3,
            }
        }

    def test_in(self):
        spec  = {
            'species': {
                '$in': ['cow', 'pig', 't-rex']
                }
            }
        result = uni.check(spec, self.checkable)
        self.assertTrue(result)

    def test_in_false(self):
        spec  = {
            'species': {
                '$in': ['cow', 'pig']
                }
            }
        result = uni.check(spec, self.checkable)
        self.assertFalse(result)

    def test_nin(self):
        spec  = {
            'species': {
                '$nin': ['cow', 'pig', 'bunny']
                }
            }
        result = uni.check(spec, self.checkable)
        self.assertTrue(result, True)

    def test_nin_false(self):
        spec  = {
            'species': {
                '$nin': ['cow', 'pig', 't-rex']
                }
            }
        result = uni.check(spec, self.checkable)
        self.assertFalse(result, True)

    def test_gte_eq(self):
        spec  = {
            'uni': {
                'age': {
                    '$gte': 3
                    }
                }
            }
        result = uni.check(spec, self.checkable)
        self.assertTrue(result)

    def test_gte_gt(self) :
        spec  = {
            'uni': {
                'age': {
                    '$gte': 2
                    }
                }
            }
        result = uni.check(spec, self.checkable)
        self.assertTrue(result)

    def test_gte_false(self):
        spec  = {
            'uni': {
                'age': {
                    '$gte': 4
                    }
                }
            }
        result = uni.check(spec, self.checkable)
        self.assertFalse(result)

    def test_gt(self):
        spec  = {
            'uni': {
                'age': {
                    '$gt': 2
                    }
                }
            }
        result = uni.check(spec, self.checkable)
        self.assertTrue(result, True)

    def test_gt_false(self):
        spec  = {
            'uni': {
                'age': {
                    '$gt': 4
                    }
                }
            }
        result = uni.check(spec, self.checkable)
        self.assertFalse(result, True)

    def test_lte_eq(self):
        spec  = {
            'uni': {
                'age': {
                    '$lte': 3
                    }
                }
            }
        result = uni.check(spec, self.checkable)
        self.assertTrue(result, True)

    def test_lte_lt(self):
        spec  = {
            'uni': {
                'age': {
                    '$lte': 4
                    }
                }
            }
        result = uni.check(spec, self.checkable)
        self.assertTrue(result, True)

    def test_lte_false(self):
        spec  = {
            'uni': {
                'age': {
                    '$lt': 2
                    }
                }
            }
        result = uni.check(spec, self.checkable)
        self.assertFalse(result, True)

    def test_lt(self):
        spec  = {
            'uni': {
                'age': {
                    '$lt': 4
                    }
                }
            }
        result = uni.check(spec, self.checkable)
        self.assertTrue(result, True)

    def test_lt_false(self):
        spec  = {
            'uni': {
                'age': {
                    '$gt': 3
                    }
                }
            }
        result = uni.check(spec, self.checkable)
        self.assertFalse(result, True)

    def test_ne(self):
        spec  = {
            'uni': {
                'age': {
                    '$ne': 2
                    }
                }
            }
        result = uni.check(spec, self.checkable)
        self.assertTrue(result, True)

    def test_ne_false(self):
        spec  = {
            'uni': {
                'age': {
                    '$ne': 3
                    }
                }
            }
        result = uni.check(spec, self.checkable)
        self.assertFalse(result, True)


class TestLogical(unittest.TestCase):

    checkable = {
        'species': 't-rex',
        'uni': {
            'age': 3,
            },
        'info': {
            'unicorns_are_real': True,
            'unicorns_that_exist': ['uni', "uni's brother"]
            }
        }

    def test_or(self):
        spec  = {
            '$or': [
                {'uni.age': {'$ne': 3}},
                {'species': {
                    '$in': ['cow', 'pig', 't-rex']}
                    },
                ]
            }
        result = uni.check(spec, self.checkable)
        self.assertTrue(result, True)

    def test_or_false(self):
        spec  = {
            '$or': [
                {'uni.age': {'$ne': 3}},
                {'species': {
                    '$in': ['cow', 'pig', 'bunny']}
                    },
                ]
            }
        result = uni.check(spec, self.checkable)
        self.assertFalse(result, True)

    def test_any(self):
        spec  = {
            '$or': [
                {'uni.age': {'$ne': 3}},
                {'species': {
                    '$in': ['cow', 'pig', 't-rex']}
                    },
                {'info.unicorns_are_real': True},
                {'info.unicorns_that_exist': 'cowcorn'},
                ]
            }
        result = uni.check(spec, self.checkable)
        self.assertTrue(result, True)

    def test_any_false(self):
        spec  = {
            '$or': [
                {'uni.age': {'$ne': 3}},
                {'species': {
                    '$in': ['cow', 'pig']}
                    },
                {'info.unicorns_are_real': False},
                {'info.unicorns_that_exist': 'cowcorn'},
                ]
            }
        result = uni.check(spec, self.checkable)
        self.assertFalse(result, True)

    def test_and(self):
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
        self.assertTrue(result, True)

    def test_and_false(self):
        spec  = {
            '$and': [
                {'uni.age': {'$ne': 3}},
                {'species': {
                    '$in': ['cow', 'pig']}
                    },
                {'info.unicorns_are_real': False},
                {'info.unicorns_that_exist': 'cowcorn'},
                ]
            }
        result = uni.check(spec, self.checkable)
        self.assertFalse(result, True)


class TestEvaluation(unittest.TestCase):

    checkable = {
        'species': 't-rex',
        'uni': {
            'age': 3,
            },
        'info': {
            'unicorns_are_real': True,
            'unicorns_that_exist': ['uni', "uni's brother"]
            }
        }

    def test_type(self):
        spec  = {
            'uni.age': {
                '$type': 'int'
                }
            }
        result = uni.check(spec, self.checkable)
        self.assertTrue(result, True)

    def test_type_false(self):
        spec  = {
            'uni.age': {
                '$type': 'unicode'
                }
            }
        result = uni.check(spec, self.checkable)
        self.assertFalse(result, True)

    def test_exists(self):
        spec  = {
            'uni.age': {
                '$exists': True,
                }
            }
        result = uni.check(spec, self.checkable)
        self.assertTrue(result, True)

    def test_type_false(self):
        spec  = {
            'uni.age': {
                '$exists': False,
                }
            }
        result = uni.check(spec, self.checkable)
        self.assertFalse(result, True)


class TestArray(unittest.TestCase):

    checkable = {
        'species': range(10),
        }

    def test_all(self):
        spec  = {
            'species': {
                '$all': [1, 2, 3],
                }
            }
        result = uni.check(spec, self.checkable)
        self.assertTrue(result, True)

    def test_all_false(self):
        spec  = {
            'species': {
                '$all': ['cow', 2, 3],
                }
            }
        result = uni.check(spec, self.checkable)
        self.assertFalse(result, True)
