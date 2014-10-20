"""The guts of pymetasurf. Basically MetaSurface implements the bindings using ctypes. C library loading occurs on module import."""

# Written by Cas Rusnov <rusnovn@gmail.com>

import ctypes
import sys

MSURF_GREATER = 1
MSURF_LESSER = 0

DEBUG=False

# needs porting
_lib_msurf = ctypes.cdll.LoadLibrary('libmetasurf.so.0')

class metasurface(ctypes.Structure):
    pass

_msurf_create = _lib_msurf.msurf_create
_msurf_free = _lib_msurf.msurf_free
_msurf_inside = _lib_msurf.msurf_inside
_msurf_eval_func = _lib_msurf.msurf_eval_func
_msurf_vertex_func = _lib_msurf.msurf_vertex_func
_msurf_normal_func = _lib_msurf.msurf_normal_func
_msurf_bounds = _lib_msurf.msurf_bounds
_msurf_resolution = _lib_msurf.msurf_resolution
_msurf_threshold = _lib_msurf.msurf_threshold
_msurf_polygonize = _lib_msurf.msurf_polygonize

msurf_func = ctypes.CFUNCTYPE(ctypes.c_float, ctypes.c_float, ctypes.c_float, ctypes.c_float)
msurf_cb_func = ctypes.CFUNCTYPE(None, ctypes.c_float, ctypes.c_float, ctypes.c_float)

class MetaSurface(object):
    """Represents one metasurface object. Maps its callbacks into the metasurface library (which operates via callbacks).

    This object is intended to be subclassed, and the eval_callback implemented. eval_callback returns a 1 if a particular point contains a voxel
    or a 0 if it does not."""

    def __init__(self):
        self._metasurface = ctypes.cast(_msurf_create(),ctypes.POINTER(metasurface));
        self.tri_list = list()
        self.normal_list = list()
        self._vx_cb = msurf_cb_func(self.vertex_callback)
        _msurf_vertex_func(self._metasurface, self._vx_cb)
        self._nm_cb = msurf_cb_func(self.normal_callback)
        _msurf_normal_func(self._metasurface, self._nm_cb)
        self._ev_cb = msurf_func(self.eval_callback)
        _msurf_eval_func(self._metasurface, self._ev_cb)

    def vertex_callback(self, x, y, z):
        """Called for each vertex created by metasurface. The vertexes are nominally in triangle strips."""
        DEBUG and sys.stderr.write('vertex_callback\n')
        self.tri_list.append((x,y,z))

    def normal_callback(self, x, y, z):
        """Called for each vertex normal created by metasurface. Map directly to the triangle list."""
        DEBUG and sys.stderr.write('normal_callback\n')
        self.normal_list.append((x,y,z))

    def eval_callback(self, x, y, z):
        """Called for each point in space that metasurface desires to test. Intended to be implemented by subclasses.

        Should return a 0 for not inside of a voxel, 1 for inside of voxel (default returns 0)."""
        DEBUG and sys.stderr.write('eval_callback\n')
        return 0

    def set_inside(self, inside):
        """Changes the inside/outside sense inside of metasurface."""
        DEBUG and sys.stderr.write('set_inside\n')
        _msurf_inside(self._metasurface, ctypes.c_int(inside))

    def set_bounds(self, xmin, ymin, zmin, xmax, ymax, zmax):
        """Set the bounding box which metasurface searches for voxels in."""
        DEBUG and sys.stderr.write('set_bounds\n')
        _msurf_bounds(self._metasurface, ctypes.c_float(xmin), ctypes.c_float(ymin), ctypes.c_float(zmin), ctypes.c_float(xmax), ctypes.c_float(ymax), ctypes.c_float(zmax))

    def set_resolution(self, xres, yres, zres):
        """Set the density that metasurface searches for voxels in."""
        DEBUG and sys.stderr.write('set_resolution\n')
        _msurf_resolution(self._metasurface, ctypes.c_int(xres), ctypes.c_int(yres), ctypes.c_int(zres))

    def set_threshold(self, thresh):
        DEBUG and sys.stderr.write('set_threshold\n')
        _msurf_threshold(self._metasurface, ctypes.c_float(thresh))

    def polygonize(self):
        DEBUG and sys.stderr.write('polygonize\n')
        self.tri_list = list()
        self.normal_list = list()
        _msurf_polygonize(self._metasurface)

    def __del__(self):
        _msurf_free(self._metasurface)

class UnitMetaball(MetaSurface):
    """This is a simple 1 unit metaball implemented as a child of MetaSurface."""
    def __init__(self):
        MetaSurface.__init__(self)
        self.set_inside(MSURF_LESSER)
	self.set_bounds(-1.1, -1.1, -1.1, 1.1, 1.1, 1.1);

    def eval_callback(self, x, y, z):
        return (x * x + y * y + z * z) - 1.0;
