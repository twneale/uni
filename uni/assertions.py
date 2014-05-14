from uni.checker import check


class AssertionFailed(Exception):
    pass


class AssertionSet:

    def __init__(self, querylist, raise_failure=False):
        self.querylist = list(querylist)
        self.success = None
        self.raise_failure = raise_failure

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.finalize()

    def check(self, obj):
        for query in self.querylist:
            match = check(query, obj)
            if match:
                self.querylist.remove(query)
                return

    def check_all(self, obj_list):
        for obj in obj_list:
            for query in self.querylist:
                if check(query, obj):
                    self.querylist.remove(query)
                    break
        return self.finalize()

    def finalize(self):
        if self.querylist:
            self.success = False
            if self.raise_failure:
                msg = "%d queries didn't match any data"
                raise AssertionFailed(msg)
        else:
            self.success = True
        return self.success