from __future__ import print_function, division

from bitarray import bitarray as sub_bitarray

from six import with_metaclass


class FromFactoryer(type):
    def __getattribute__(cls, attr):
        if attr.startswith("from") and hasattr(getattr(cls(), attr, None), '__call__'):
            def wrapped(*args, **kwargs):
                bit = cls()
                getattr(bit, attr)(*args, **kwargs)
                return bit

            return wrapped
            # Default behaviour
        return super(FromFactoryer, cls).__getattribute__(attr)


class bitarray(with_metaclass(FromFactoryer, sub_bitarray)):
    pass
