#!/usr/bin/env python3
import pickle
import io

class IllegalObject(Exception):
    '''Exception raised when an illegal object is being unpickled'''

class UnpicklerFromFunction(object):

    class _UnpicklerFromFunction(pickle.Unpickler):
        def __init__(self, filter: callable, *args, **kargs):
            super().__init__(*args, **kargs)
            self.filter = filter

        def find_class(self, module: str, name: str):
            if self.filter(module, name):
                return self.find_class(module, name)
            raise IllegalObject('%s.%s is not allowed' % (module, name))

    def __init__(self, filter: callable):
        self.filter = filter

    def load(self, *args, **kargs):
        return self._UnpicklerFromFunction(self.filter, *args, **kargs).load()

    def loads(self, data, *args, **kargs):
        fd_like = io.BytesIO(data)
        return self.load(fd_like, *args, **kargs)
