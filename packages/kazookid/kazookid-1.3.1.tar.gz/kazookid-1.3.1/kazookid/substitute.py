class Substitute(object):

    '''
    Substitutes are can be used to provide or verify
    direct and indirect input and output of objects
    during testing.

    See: http://xunitpatterns.com/

    Test Spy
    ========

    Test Spies capture indirect output
    http://xunitpatterns.com/Test%20Spy.html

    # Check if a method was called

        from kazookid import Substitute

        def test_spy():
            engine = Substitute()
            game = Game(engine)
            game.run()
            assert_true(engine.render.was_called)

    # Check on parameters

        def test_spy():
            engine = Substitute()
            game = Game(engine)
            game.run()
            assert_true(engine.render.was_called_with(time))


    Test Stub
    =========

    Stubs feed indirect input into the System under Test
    http://xunitpatterns.com/Test%20Stub.html

    # To provide indirect input:

        substitute.value = 5

        substitute.method.returns(1)

        substitute.method.raises(Exception)
    '''

    def __init__(self):
        self._calls = {}
        self._config = {}
        self._iterator = Iterator()

    def __getattr__(self, name):
        if name == 'yields':
            return self._iterator

        config = self.__dict__['_config']
        call = Call(name=name, parent=self)
        config[name] = config.get(name, call)
        return config[name]

    def __iter__(self):
        return self._iterator.__iter__()


class Context(Substitute):

    def __enter__(self, *args, **kwargs):
        return self

    def __exit__(self, *args, **kwargs):
        pass


class Call(object):
    '''
    Intercepts a call or method on a substitute object
    '''

    def __init__(self, name, parent):
        self.name = name
        self.parent = parent
        self.return_value = None
        self.exception = None

    def __call__(self, *args, **kwargs):
        if self.exception:
            raise self.exception()

        # Calls are registered by
        # appending the arguments passed to this method
        # to the substitute
        self.parent._calls.setdefault(self.name, []).append((args, kwargs))

        try:
            return self.return_value[0]
        except:
            return None

    def _number_of_calls(self):
        '''
        Returns how many times this call was invoked
        '''
        return len(self.parent._calls.get(self.name, []))

    def _unpack(self, items):
        '''
        Convenience method: If a collection contains only a singular item,
        that item is returned instead of the list, e.g.:
        self._unpack([1]) --> 1
        self._unpack((1,)) --> 1
        self._unpack([1,2,3]) --> [1,2,3]
        '''
        return items[-1] if len(items) == 1 else items

    @property
    def args(self):
        '''
        Returns the arguments this call was invoked with.
        '''

        # Arguments are stored internally in tuples with (args, kwargs)
        # For convenience, if only one argument was passed,
        # this single argument is unwrapped from the tuple and returned.

        calls = self.parent._calls.get(self.name, [])

        # Unpack, if single call
        if len(calls) == 1:
            args, kwargs = calls[-1]
            return self._unpack(args)

        # Return all recorded arguments
        return [self._unpack(args) for args, kwargs in calls]

    def raises(self, exception):
        '''
        Configure this call to raise an exeption
        '''
        self.exception = exception

    def returns(self, *args, **kwargs):
        '''
        Configure this call to return some data
        '''
        self.return_value = args

    @property
    def was_called(self):
        '''
        Returns whether this call was invoked at least once.
        '''
        return self._number_of_calls() > 0

    def was_called_times(self, times):
        '''
        Returns whether this call was invoked exactly ```times```.
        '''
        return self._number_of_calls() == times

    def was_called_with(self, *args, **kwargs):
        '''
        Returns whether this call was invoked with these ```arguments```.
        '''
        args = self._unpack(args)
        return (args == self.args) or (args in self.args)


class Iterator(object):

    def __init__(self):
        self._items = []

    def __iter__(self):
        return self._items.__iter__()

    def __call__(self, items):
        self._items = items
