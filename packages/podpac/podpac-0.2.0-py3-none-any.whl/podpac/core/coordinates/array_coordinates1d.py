"""
One-Dimensional Coordinates: Array
"""


from __future__ import division, unicode_literals, print_function, absolute_import

import copy
from collections import OrderedDict

import numpy as np
import traitlets as tl
from collections import OrderedDict

# from podpac.core.utils import cached_property, clear_cache
from podpac.core.coordinates.utils import make_coord_value, make_coord_array, add_coord
from podpac.core.coordinates.coordinates1d import Coordinates1d

class ArrayCoordinates1d(Coordinates1d):
    """
    A basic array of coordinates. Not guaranteed to be sorted, unique, or uniformly-spaced.

    Attributes
    ----------
    coords : np.ndarray
        Input coordinate array. Values must all be the same type.
        Numerical values are converted to floats, and datetime values are converted to np.datetime64.

    See Also
    --------
    UniformCoordinates1d : sorted, uniformly-spaced coordinates defined by a start, stop, and step.

    """

    coords = tl.Instance(np.ndarray)

    def __init__(self, coords=[], **kwargs):
        """
        Initialize coords from an array.

        Parameters
        ----------
        coords : array-like
            coordinate values.
        **kwargs
            Description
        """

        coords = make_coord_array(coords)
        super(ArrayCoordinates1d, self).__init__(coords=coords, **kwargs)

    @tl.validate('coords')
    def _validate_coords(self, d):
        val = d['value']
        if val.ndim != 1:
            raise ValueError("Invalid coords (ndim='%d', must be ndim=1" % val.ndim)
        if val.dtype != float and not np.issubdtype(val.dtype, np.datetime64):
            raise ValueError("Invalid coords (dtype='%s', must be np.float64 or np.datetime64)")
        return val

    @tl.observe('coords')
    def _observe_coords(self, change):
        # clear_cache(self, change, ['bounds', 'coordinates'])

        val = self.coords
        if val.size == 0:
            self.set_trait('is_monotonic', None)
            self.set_trait('is_descending', None)
            self.set_trait('is_uniform', None)
        elif val.size == 1:
            self.set_trait('is_monotonic', True)
            self.set_trait('is_descending', None)
            self.set_trait('is_uniform', True)
        else:
            deltas = (val[1:] - val[:-1]).astype(float) * (val[1] - val[0]).astype(float)
            if np.any(deltas <= 0):
                self.set_trait('is_monotonic', False)
                self.set_trait('is_descending', None)
                self.set_trait('is_uniform', False)
            else:
                self.set_trait('is_monotonic', True)
                self.set_trait('is_descending', self.coords[1] < self.coords[0])
                self.set_trait('is_uniform', np.allclose(deltas, deltas[0]))

    # ------------------------------------------------------------------------------------------------------------------
    # Alternate Constructors
    # ------------------------------------------------------------------------------------------------------------------

    @classmethod
    def from_xarray(cls, x, **kwargs):
        return cls(x.data, name=x.name)

    @classmethod
    def from_definition(cls, d):
        coords = d.pop('values')
        return cls(coords, **d)

    def copy(self, **kwargs):
        properties = self.properties
        properties.update(kwargs)
        return ArrayCoordinates1d(self.coords, **properties)

    # ------------------------------------------------------------------------------------------------------------------
    # standard methods, array-like
    # ------------------------------------------------------------------------------------------------------------------

    def __len__(self):
        return self.size

    def __getitem__(self, index):
        coords = self.coords[index]
        return ArrayCoordinates1d(coords, **self.properties)

    # ------------------------------------------------------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------------------------------------------------------

    @property
    def coordinates(self):
        """ Coordinate values. """

        # get coordinates and ensure read-only array with correct dtype
        coordinates = self.coords.copy()
        coordinates.setflags(write=False)
        return coordinates

    @property
    def size(self):
        ''' Number of coordinates. '''
        return self.coords.size

    @property
    def dtype(self):
        if self.size == 0:
            return None
        elif self.coords.dtype == float:
            return float
        elif np.issubdtype(self.coords.dtype, np.datetime64):
            return np.datetime64
        else:
            raise ValueError("Invalid coords dtype '%s'" % self.coords.dtype)

    @property
    def bounds(self):
        """ Coordinate bounds. """

        # TODO are we sure this can't be a tuple?

        if self.size == 0:
            lo, hi = np.nan, np.nan
        elif self.is_monotonic:
            lo, hi = sorted([self.coords[0], self.coords[-1]])
        elif self.dtype is np.datetime64:
            lo, hi = np.min(self.coords), np.max(self.coords)
        else:
            lo, hi = np.nanmin(self.coords), np.nanmax(self.coords)

        # read-only array with the correct dtype
        bounds = np.array([lo, hi], dtype=self.dtype)
        bounds.setflags(write=False)
        return bounds

    @property
    def area_bounds(self):
        # point ctypes, just use bounds
        if self.ctype == 'point':
            return self.bounds

        # segment ctypes, with explicit extents
        if self.extents is not None:
            return self.extents

        # segment ctypes, calculated
        if self.size == 0:
            lo, hi = np.nan, np.nan
        elif self.size == 1:
            lo, hi = self.coords[0], self.coords[0]
        elif self.ctype == 'midpoint':
            lo = add_coord(self.coords[0], -(self.coords[ 1] - self.coords[ 0]) / 2.)
            hi = add_coord(self.coords[-1], (self.coords[-1] - self.coords[-2]) / 2.)
        elif (self.ctype == 'left' and not self.is_descending) or (self.ctype == 'right' and self.is_descending):
            lo = self.coords[0]
            hi = add_coord(self.coords[-1], (self.coords[-1] - self.coords[-2]))
        else:
            lo = add_coord(self.coords[0], -(self.coords[ 1] - self.coords[ 0]))
            hi = self.coords[-1]

        if self.is_descending:
            lo, hi = hi, lo

        # read-only array with the correct dtype
        area_bounds = np.array([lo, hi], dtype=self.dtype)
        area_bounds.setflags(write=False)
        return area_bounds

    @property
    def definition(self):
        d = OrderedDict()
        if self.dtype == float:
            d['values'] = self.coords.tolist()
        else:
            d['values'] = self.coords.astype('str').tolist()
        d.update(self.properties)
        return d

    # ------------------------------------------------------------------------------------------------------------------
    # Methods
    # ------------------------------------------------------------------------------------------------------------------

    def select(self, bounds, outer=False, return_indices=False):
        bounds = make_coord_value(bounds[0]), make_coord_value(bounds[1])

        # empty
        if self.size == 0:
            return self._select_empty(return_indices)

        # full
        if self.bounds[0] >= bounds[0] and self.bounds[1] <= bounds[1]:
            return self._select_full(return_indices)

        # none
        if self.area_bounds[0] > bounds[1] or self.area_bounds[1] < bounds[0]:
            return self._select_empty(return_indices)

        if not outer:
            gt = self.coordinates >= bounds[0]
            lt = self.coordinates <= bounds[1]
            I = np.where(gt & lt)[0]

        elif self.is_monotonic:
            gt = np.where(self.coords >= bounds[0])[0]
            lt = np.where(self.coords <= bounds[1])[0]
            if self.is_descending:
                lt, gt = gt, lt
            start = max(0, gt[0]-1)
            stop = min(self.size-1, lt[-1]+1)
            I = slice(start, stop+1)

        else:
            raise NotImplementedError("select outer=True is not yet supported for non-monotonic coordinates")

        c = ArrayCoordinates1d(self.coords[I], **self.properties)
        if return_indices:
            return c, I
        else:
            return c
