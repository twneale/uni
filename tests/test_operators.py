from nose.tools import raises

import uni


class TestComparison:

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
        assert uni.check(spec, self.checkable)

    def test_in_false(self):
        spec  = {
            'species': {
                '$in': ['cow', 'pig']
                }
            }
        assert not uni.check(spec, self.checkable)

    def test_nin(self):
        spec  = {
            'species': {
                '$nin': ['cow', 'pig', 'bunny']
                }
            }
        assert uni.check(spec, self.checkable)

    def test_nin_false(self):
        spec  = {
            'species': {
                '$nin': ['cow', 'pig', 't-rex']
                }
            }
        assert not uni.check(spec, self.checkable)

    def test_gte_eq(self):
        spec  = {
            'uni': {
                'age': {
                    '$gte': 3
                    }
                }
            }
        assert uni.check(spec, self.checkable)

    def test_gte_gt(self) :
        spec  = {
            'uni': {
                'age': {
                    '$gte': 2
                    }
                }
            }
        assert uni.check(spec, self.checkable)

    def test_gte_false(self):
        spec  = {
            'uni': {
                'age': {
                    '$gte': 4
                    }
                }
            }
        assert not uni.check(spec, self.checkable)

    def test_gt(self):
        spec  = {
            'uni': {
                'age': {
                    '$gt': 2
                    }
                }
            }
        assert uni.check(spec, self.checkable)

    def test_gt_false(self):
        spec  = {
            'uni': {
                'age': {
                    '$gt': 4
                    }
                }
            }
        assert not uni.check(spec, self.checkable)

    def test_lte_eq(self):
        spec  = {
            'uni': {
                'age': {
                    '$lte': 3
                    }
                }
            }
        assert uni.check(spec, self.checkable)

    def test_lte_lt(self):
        spec  = {
            'uni': {
                'age': {
                    '$lte': 4
                    }
                }
            }
        assert uni.check(spec, self.checkable)

    def test_lte_false(self):
        spec  = {
            'uni': {
                'age': {
                    '$lt': 2
                    }
                }
            }
        assert not uni.check(spec, self.checkable)

    def test_lt(self):
        spec  = {
            'uni': {
                'age': {
                    '$lt': 4
                    }
                }
            }
        assert uni.check(spec, self.checkable)

    def test_lt_false(self):
        spec  = {
            'uni': {
                'age': {
                    '$gt': 3
                    }
                }
            }
        assert not uni.check(spec, self.checkable)

    def test_ne(self):
        spec  = {
            'uni': {
                'age': {
                    '$ne': 2
                    }
                }
            }
        assert uni.check(spec, self.checkable)

    def test_ne_false(self):
        spec  = {
            'uni': {
                'age': {
                    '$ne': 3
                    }
                }
            }
        assert not uni.check(spec, self.checkable)


class TestLogical:

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
        assert uni.check(spec, self.checkable)

    def test_or_false(self):
        spec  = {
            '$or': [
                {'uni.age': {'$ne': 3}},
                {'species': {
                    '$in': ['cow', 'pig', 'bunny']}
                    },
                ]
            }
        assert not uni.check(spec, self.checkable)

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
        assert uni.check(spec, self.checkable)

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
        assert not uni.check(spec, self.checkable)

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
        assert uni.check(spec, self.checkable)

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
        assert not uni.check(spec, self.checkable)


class TestEvaluation:

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
        assert uni.check(spec, self.checkable)

    def test_type_false(self):
        spec  = {
            'uni.age': {
                '$type': 'unicode'
                }
            }
        assert not uni.check(spec, self.checkable)

    def test_exists(self):
        spec  = {
            'uni.age': {
                '$exists': True,
                }
            }
        assert uni.check(spec, self.checkable)

    def test_exists_false(self):
        spec  = {
            'uni.cow': {
                '$exists': False,
                }
            }
        assert uni.check(spec, self.checkable)

    @raises(uni.InvalidQuery)
    def test_exists_false(self):
        spec  = {
            '$exists': 'uni.cow',
            }
        assert uni.check(spec, self.checkable)


class TestArray:

    checkable = {
        'species': range(10),
        }

    def test_all(self):
        spec  = {
            'species': {
                '$all': [1, 2, 3],
                }
            }
        assert uni.check(spec, self.checkable)

    def test_all_false(self):
        spec  = {
            'species': {
                '$all': ['cow', 2, 3],
                }
            }
        assert not uni.check(spec, self.checkable)


class TestPathEval:

    checkable = {
        'type': str,
        'cow': {
            'size': 'extrabig',
            },
        'types': [str, object],
        }

    def test_getattr(self):
        spec  = {'type.__name__': 'str'}
        assert uni.check(spec, self.checkable)

    def test_getattr_false(self):
        spec  = {'type.__name__': {'$ne': 'list'}}
        assert uni.check(spec, self.checkable)

    def test_getitem(self):
        spec  = {'cow.size': 'extrabig'}
        assert uni.check(spec, self.checkable)

    def test_getitem_false(self):
        spec  = {'cow.size': {'$ne': 'tiny'}}
        assert uni.check(spec, self.checkable)

    def test_index_getattr(self):
        spec  = {'types.0.__name__': 'str'}
        assert uni.check(spec, self.checkable)

    def test_index_getattr_false(self):
        spec  = {'types.1.__name__': {'$ne': 'dict'}}
        assert uni.check(spec, self.checkable)
