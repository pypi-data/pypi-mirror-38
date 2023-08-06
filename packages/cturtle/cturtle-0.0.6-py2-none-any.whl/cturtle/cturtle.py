# coding: utf-8

# Copyright (C) 2018 Université Clermont Auvergne, CNRS/IN2P3, LPC
# Author: Valentin NIESS (niess@in2p3.fr)
#
# Topographic Utilities for tRansporting parTicules over Long rangEs (TURTLE)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>

"""
Python/ctypes interface to the TURTLE C library
"""


__version__ = "0.0.6"


import ctypes as C
from ctypes.util import find_library
import glob
import os


__all__ = ["Ecef", "LibraryError", "Map", "RETURN_SUCCESS", "__version__"]


"""TURTLE return values"""
RETURN_SUCCESS = 0


class LibraryError(Exception):
    """A TURTLE library error"""
    pass


class _MapInfo(C.Structure):
    _fields_ = (("nx", C.c_int), ("ny", C.c_int), ("x", 2 * C.c_double),
                ("y", 2 * C.c_double), ("z", 2 * C.c_double),
                ("encoding", C.c_char_p))


class Map:
    """Encapsulation of a TURTLE map object"""

    def __init__(self, *args, **kwargs):
        self._map = C.c_void_p(None)
        if (len(args) == 1) and (len(kwargs) == 0):
            self.load(args[0])
        elif (len(kwargs) == 1) and (kwargs.keys()[0] == "path"):
            self.load(kwargs["path"])
        elif len(args) + len(kwargs) > 0:
            self.create(*args, **kwargs)

    def create(self, *args, **kwargs):
        _map_destroy(C.byref(self._map))
        if len(args) > len(_MapInfo._fields_):
            projection = args[len(_MapInfo._fields_) - 1]
        else:
            try:
                projection = kwargs["projection"]
            except KeyError:
                projection = None
        meta = _MapInfo(*args, **kwargs)
        _map_create(C.byref(self._map), meta, projection)

    def load(self, path):
        _map_destroy(C.byref(self._map))
        _map_load(C.byref(self._map), path)

    def elevation(self, x, y, check=True):
        z = C.c_double(0)
        if check:
            inside = C.c_int(0)
        else:
            inside = None
        _map_elevation(self._map, x, y, C.byref(z), C.byref(inside))
        if check and (not inside.value):
            return None
        return float(z.value)

    def node(self, ix, iy):
        x, y, z = (C.c_double(0.) for _ in xrange(3))
        _map_node(self._map, ix, iy, C.byref(x), C.byref(y), C.byref(z))
        return map(float, (x.value, y.value, z.value))


class Ecef(list):
    """Encapsulation of the ECEF conversion routines"""
    def __init__(self, x=0., y=0., z=0.):
        self[:] = (x, y, z)

    @property
    def x(self):
        return self[0]

    @x.setter
    def x(self, x):
        self[0] = x

    @property
    def y(self):
        return self[1]

    @x.setter
    def y(self, y):
        self[1] = y

    @property
    def z(self):
        return self[2]

    @z.setter
    def z(self, z):
        self[2] = z

    def from_geodetic(self, latitude, longitude, altitude):
        r = (3 * C.c_double)()
        _ecef_from_geodetic(latitude, longitude, altitude, r)
        self[:] = r
        return self

    def to_geodetic(self):
        r = (3 * C.c_double)(self[0], self[1], self[2])
        la, lo, z = (C.c_double() for _ in xrange(3))
        _ecef_to_geodetic(r, C.byref(la), C.byref(lo), C.byref(z))
        return (la.value, lo.value, z.value)

    def from_horizontal(self, latitude, longitude, azimuth, elevation):
        u = (3 * C.c_double)()
        _ecef_from_horizontal(latitude, longitude, azimuth, elevation, u)
        self[:] = u
        return self

    def to_horizontal(self, latitude, longitude):
        u = (3 * C.c_double)(self[0], self[1], self[2])
        az, el = (C.c_double() for _ in xrange(2))
        _ecef_to_horizontal(latitude, longitude, u, C.byref(az), C.byref(el))
        return (az.value, el.value)

def _initialise():
    """Load the TURTLE library and configure its ctypes interface"""
    def look_for_library_in(variable):
        """Look for the library in an environment variable"""
        env = os.getenv(variable)
        if env is None:
            return None
        for p in env.split(":"):
            p = glob.glob(os.path.join(p, "libturtle.*"))
            if p:
                return p[0]

    path = (find_library("turtle") or
            look_for_library_in("LD_LIBRARY_PATH") or
            look_for_library_in("PYTHONPATH"))
    if not path:
        raise ImportError("could not locate the TURTLE library")

    lib = C.cdll.LoadLibrary(os.path.realpath(path))

    # Configure the error handler
    @C.CFUNCTYPE(None, C.c_uint, C.c_void_p, C.c_char_p)
    def handle_error(code, function, message):
        _error_message.append(message)

    globals()["_error_message"] = []
    lib.turtle_error_handler_set(handle_error)

    def Define(function, arguments=None, result=None, encapsulate=True):
        """Helper routine for configuring a library function"""
        f = getattr(lib, "turtle" + function)
        if arguments:
            f.argtypes = arguments
        if result:
            f.restype = result
        if not encapsulate:
            globals()[function] = f
            return

        def encapsulated_library_function(*args):
            """Encapsulation of the library function with error check"""
            r = f(*args)
            if r != RETURN_SUCCESS:
                raise LibraryError(_error_message.pop())

        globals()[function] = encapsulated_library_function

    # Export the map functions
    Define("_map_create", arguments=(C.POINTER(C.c_void_p), C.POINTER(_MapInfo),
                                     C.c_char_p))
    Define("_map_destroy", arguments=(C.POINTER(C.c_void_p),),
           encapsulate=False)
    Define("_map_dump", arguments=(C.c_void_p, C.c_char_p))
    Define("_map_elevation", arguments=(C.c_void_p, C.c_double, C.c_double,
                                        C.POINTER(C.c_double),
                                        C.POINTER(C.c_int)))
    Define("_map_fill", arguments=(C.c_void_p, C.c_int, C.c_int, C.c_double))
    Define("_map_load", arguments=(C.POINTER(C.c_void_p), C.c_char_p))
    Define("_map_meta", arguments=(C.c_void_p, C.POINTER(_MapInfo),
                                   C.POINTER(C.c_char_p)),
           encapsulate=False)
    Define("_map_node", arguments=(C.c_void_p, C.c_int, C.c_int,
                                   C.POINTER(C.c_double), C.POINTER(C.c_double),
                                   C.POINTER(C.c_double)))
    Define("_map_projection", arguments=(C.c_void_p,), result=C.c_void_p,
           encapsulate=False)

    # Export the ECEF functions
    Define("_ecef_from_geodetic", arguments=(C.c_double, C.c_double, C.c_double,
                                             3 * C.c_double),
           encapsulate=False)
    Define("_ecef_to_geodetic", arguments=(3 * C.c_double,
                                           C.POINTER(C.c_double),
                                           C.POINTER(C.c_double),
                                           C.POINTER(C.c_double)),
           encapsulate=False)
    Define("_ecef_from_horizontal", arguments=(C.c_double, C.c_double,
                                               C.c_double, C.c_double,
                                               3 * C.c_double),
           encapsulate=False)
    Define("_ecef_to_horizontal", arguments=(C.c_double, C.c_double,
                                             3 * C.c_double,
                                             C.POINTER(C.c_double),
                                             C.POINTER(C.c_double)),
           encapsulate=False)

_initialise()
