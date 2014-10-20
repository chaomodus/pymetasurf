"""ctypes-based bindings for libmetasurf."""

version = "0.1.0"
version_info = (0,1,0)

from .metasurf import MetaSurface, UnitMetaball, MSURF_GREATER, MSURF_LESSER
from .shapes import shapes
