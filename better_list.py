import ctypes
from pprint import pprint


Py_ssize_t = ctypes.c_int64 if hasattr(ctypes.pythonapi, 'Py_InitModule4_64') else ctypes.c_int


class PyObject(ctypes.Structure):
    pass


PyObject._fields_ = [
    ('ob_refcnt', Py_ssize_t),
    ('ob_type', ctypes.POINTER(PyObject))
]


class Proxy(PyObject):
    _fields_ = [
        ('dict', ctypes.POINTER(PyObject)),
    ]

"""
This is a bunch of jank in order to build the structure:
ob_refcnt - Py_ssize_t
ob_type   - *PyObject
dict      - *PyObject
At the same time it bootstraps the notion of a PyObject
"""


def shimmed(class_):
    # Pulling these boys into the scope
    name = class_.__name__
    target = class_.__dict__

    # Weird introspection to find the ctypes version of the dict attribute on the class_
    proxy_dict = Proxy.from_address(id(target))
    namespace = {}

    # Ghetto work around, by inserting the proxy's dict into the `namespace` (heh),
    #  it is coerced into a python representation of its underlying py_object.
    ctypes.pythonapi.PyDict_SetItem(
        ctypes.py_object(namespace),
        ctypes.py_object(name),
        proxy_dict.dict
    )

    # This is just returning the 'py_object' version of proxy_dict.dict we inserted above ^
    return namespace[name]


def apply_shim(class_, attribute, value):

    # Crack the class open
    help = shimmed(class_)

    # Get the old value
    old = help.get(attribute, None)

    # Stab the new value in
    help[attribute] = value

    return old


def bins(self, bin_size):
    return [self[lower_bound:lower_bound + bin_size] for 
            lower_bound in range(0, len(self), bin_size)]

def chunks(self, *args):
    delims = [0, *args, len(self)]
    return [self[lb: ub] for lb, ub in ((delims[i], delims[i+1]) for i in range(len(delims) - 1))]

apply_shim(list, 'bins', bins)
apply_shim(list, 'chunks', chunks)

