import re
import operator

import dispatcher


class UnhandledOperatorError(Exception):
    pass


class InvalidKeypath(Exception):
    pass


class SpecChecker(dispatcher.Mixin):
    '''Is testing for minimal pattern matching, so should
    evaluate lazily and bail.
    '''

    # -----------------------------------------------------------------------
    # Top-level checking functions.
    # -----------------------------------------------------------------------
    def path_getitem(self, obj, keypath):
        segs = keypath.split('.')
        this = obj
        for seg in segs:
            if isinstance(this, dict):
                this = this[seg]
                continue
            if isinstance(this, (list, tuple)):
                if seg.isdigit():
                    this = this[int(seg)]
                else:
                    msg = '''
                        Got invalid segment %r in keypath %r for
                       type %r in object %r.'''
                    msg = re.sub(r'\s+', ' ', msg)
                    args = (seg, keypath, type(this), this)
                    raise InvalidKeypath(msg % args)
                continue
        return this

    def check(self, spec, data):
        path_getitem = self.path_getitem
        for keypath, specvalue in spec.items():
            if keypath.startswith('$'):
                optext = keypath
                checkable = data
                args = (optext, specvalue, checkable)
                generator = self.dispatch_operator(*args)
            else:
                checkable = path_getitem(data, keypath)
                generator = self.dispatch_literal(specvalue, checkable)
            for result in generator:
                if not result:
                    return False
        return True

    # -----------------------------------------------------------------------
    # Functions for evaluating query literals.
    # -----------------------------------------------------------------------
    dispatch_literal = dispatcher.Mixin.dispatch

    def handle_literal(self, val, checkable):
        '''This one's tricky...check for equality,
        then for contains.
        '''
        if val == checkable:
            yield True
            return
        else:
            try:
                yield val in checkable
                return
            except TypeError:
                pass
        yield False

    handle_basestring = handle_bool = handle_literal
    handle_int = handle_float = handle_long = handle_literal
    handle_NoneType = handle_literal

    def handle_dict(self, dicty, checkable):
        for key, query in dicty.items():
            if key.startswith('$'):
                optext = key
                args = (optext, query, checkable)
                for result in self.dispatch_operator(*args):
                    yield result
            else:
                result = self.check({key: query}, checkable)
                yield result

    def handle_list(self, listy, checkable):
        yield listy == checkable

    handle_set = handle_tuple = handle_list

    # -----------------------------------------------------------------------
    # Functions for evaluating query operators.
    # -----------------------------------------------------------------------
    UnhandledOperatorError = UnhandledOperatorError

    op_funcs = {

        # Comparison.
        '$in': lambda item, array: item in array,
        '$gte': operator.ge,
        '$gt': operator.gt,
        '$lt': operator.lt,
        '$lte': operator.le,
        '$ne': lambda a, b: a != b,
        '$nin': lambda item, array: item not in array,
        '$all': lambda a, b: set(b).issubset(set(a)),
    }

    def dispatch_operator(self, optext, spec, checkable):

        # Try handle with builtin operators.
        if optext in self.op_funcs:
            args = (optext, spec, checkable)
            for result in self.handle_operator(*args):
                yield result
            return

        # Fall back to class-level double-dispatch.
        optext = optext.lstrip('$')
        try:
            method = self.dispatch_data[optext]
        except KeyError:
            raise self.DispatchError('No method found: %r' % spec)
        results = method(spec, checkable)
        if isinstance(results, self.gentype):
            for result in results:
                yield result
            return
        else:
            yield results
            return

        # If none found, complain.
        msg = 'Encountered unhandled operator: %r' % optext
        raise self.UnhandledOperatorError(msg)

    def handle_operator(self, optext, spec, checkable):
        op = self.op_funcs[optext]
        yield op(checkable, spec)

    def handle_and(self, listy, checkable):
        for spec in listy:
            if not self.check(spec, checkable):
                return False
        return True

    def handle_any(self, listy, checkable):
        for spec in listy:
            if self.check(spec, checkable):
                return True

    handle_or = handle_any

    def handle_nor(self, listy, checkable):
        for spec in listy:
            if self.check(spec, checkable):
                return False

    handle_none = handle_nor

    def handle_not(self, spec, checkable):
        return not self.check(spec, checkable)

    def handle_type(self, spec, checkable):
        checkable_type = type(checkable)
        if checkable_type == spec:
            return True
        elif checkable_type.__name__ == spec:
            return True
        else:
            return False

    def handle_isinstance(self, spec, checkable):
        '''This will have to wait until dynamic loading
        in the dispatcher module is functionalized better.
        '''
        raise NotImplemented()

    def handle_subclass(self, spec, checkable):
        '''This will have to wait until dynamic loading
        in the dispatcher module is functionalized better.
        '''
        raise NotImplemented()

    def handle_exists(self, spec, checkable):
        '''The implementation of this one is weird. By the time
        the {'$exists': True} spec gets to the dispatched
        handler, the key presumably exists.

        So we just parrot the assertion the spec makes. If it
        asserts the key exists, we return True. If it asserts
        the key doesn't exist, we return False, because that
        can't be true.
        '''
        return spec


def check(spec, data, checker=SpecChecker()):
    return checker.check(spec, data)
