import os.path
import numpy as np
from png import Writer as pngWriter
from math import sqrt

from .sliced_models import SlicedModel_VTR, SlicedModel_SEGY
from .interp import bilinear_interpolate_by_factor
from .color_mappings import default_mapping, swatch


# default target size to around 1.0 million elements
# (generally produces PNG files ~200kB)
target_size = 1000000


class VTRImage(object):
    """
    Augments SliceModel with plots from slices
    """

    def __init__(self, file_name):
        _, file_ext = os.path.splitext(file_name)
        if file_ext == ".vtr":
            self.model = SlicedModel_VTR(file_name)
        elif file_ext == ".sgy" or file_ext == ".segy":
            self.model = SlicedModel_SEGY(file_name)
        else:
            raise ValueError('unrecognized file extension')

    # @profile
    def _normalize_to_unit(self, input_array):
        """
        Normalizes an NDarray into values of range [0.0, 1.0]

        Warning: Assumes no NaN values in the image
        """
        input_array = np.asanyarray(input_array)

        if self.min_val is None:
            self.min_val = input_array.min()

        if self.max_val is None:
            self.max_val = input_array.max()
            if (self.min_range is not None) and \
               (abs(self.max_val - self.min_val) < abs(self.min_range)):
                self.max_val = self.min_val + self.min_range

        input_array -= self.min_val
        input_array /= (self.max_val - self.min_val)
        return input_array

    # @profile
    def _quantize_to_N(self, xa, N=256):
        N = int(N)

        # Calculations with native byteorder are faster, and avoid a
        # bug that otherwise can occur with putmask when the last
        # argument is a numpy scalar.
        if not xa.dtype.isnative:
            xa = xa.byteswap().newbyteorder()

        # Treat 1.0 as slightly less than 1.
        vals = np.array([1, 0], dtype=xa.dtype)
        almost_one = np.nextafter(*vals)
        np.copyto(xa, almost_one, where=xa == 1.0)
        # The following clip is fast, and prevents possible
        # conversion of large positive values to negative integers.

        xa *= N
        np.clip(xa, -1, N, out=xa)

        # ensure that all 'under' values will still have negative
        # value after casting to int
        np.copyto(xa, -1, where=xa < 0.0)
        xa = xa.astype(int)

        # once more, ensure clipped values are set to the bounds
        np.copyto(xa, N - 1, where=xa > N - 1)
        np.copyto(xa, 0, where=xa < 0)

        if (N <= 256):
            xa = xa.astype(np.uint8)

        return xa

    # @profile
    def to_image(self, model_propID=0, slice_dim=2, slice=-1, scale_factor=-1):
        """
        converts a model slice to an 8-bit RGBA pixelmap

        `slice_dim` is the dimension to slice over (FW3D Keyfile order, depth is 3)

        `slice` is the slice index (starts at 1), throws an error if not set when in 3D

        if scale_factor=-1, it uses the global `target_size` varibale to set the sacling
        factor to be equal to that number of elements
        """
        model_slice = self.model.slice_along_dim(model_propID, slice_dim, slice, transpose=True)

        if (scale_factor == -1):
            slice_size = model_slice.shape[0] * model_slice.shape[1]
            scale_factor = sqrt(target_size / float(slice_size))
            # if smaller than 1, don't scale it
            scale_factor = max(1, scale_factor)
        resampled_array = bilinear_interpolate_by_factor(model_slice, scale_factor)

        # normalize array
        resampled_array = self._normalize_to_unit(resampled_array)

        # discretize to uint8 for image
        # rgba_array = self.to_rgba(resampled_array, bytes=True)
        discretized_array = self._quantize_to_N(resampled_array, N=256)
        return discretized_array

    # @profile
    def to_pngfile(self, filename, model_propID=0, slice_dim=2, slice=-1, scale_factor=-1,
                   palette=None, min_val=None, max_val=None, min_range=None):
        """
        writes a model slice to a PNG image file

        `slice_dim` is the dimension to slice over (FW3D Keyfile order, depth is 3)

        `slice` is the slice index (starts at 1), throws an error if not set when in 3D

        if scale_factor=-1, it uses the global `target_size` varibale to set the sacling
        factor to be equal to that number of elements
        """
        # rgba_array = self.to_image(model_propID=model_propID, slice_dim=slice_dim,
        #                            slice=slice, scale_factor=-1)
        # discarding alpha produces smaller PNG files
        # rgba_array = rgba_array[:, :, 0:3]
        # width = rgba_array.shape[1]
        # height = rgba_array.shape[0]
        # rgba_array = rgba_array.reshape(rgba_array.shape[0], rgba_array.shape[1] * 3)

        if (not palette) or (not (palette in swatch)):
            palette = default_mapping

        self.min_val = min_val
        self.max_val = max_val
        self.min_range = min_range

        discretized_image = self.to_image(model_propID=model_propID, slice_dim=slice_dim,
                                          slice=slice, scale_factor=scale_factor)
        width = discretized_image.shape[1]
        height = discretized_image.shape[0]
        with open(filename, 'wb') as f:
            w = pngWriter(width=width, height=height, palette=swatch[palette],
                          alpha=False, bitdepth=8, compression=-1, filter_type=0)
            w.write(f, discretized_image)

        return (self.min_val, self.max_val)

    def to_floatfile(self, filename, model_propID=0, slice_dim=2, slice=-1):
        """
        writes a model slice to a Float32 binary file

        `slice_dim` is the dimension to slice over (FW3D Keyfile order, depth is 3)

        `slice` is the slice index (starts at 1), throws an error if not set when in 3D

        if scale_factor=-1, it uses the global `target_size` varibale to set the sacling
        factor to be equal to that number of elements

        the binary file written this way does not have its axes transposed (i.e., fastest is depth)
        """

        model_slice = self.model.slice_along_dim(model_propID, slice_dim, slice, transpose=False)
        model_slice.tofile(filename, sep="")


def palettebar_to_png(filename, palette=None):
    if (not palette) or (not (palette in swatch)):
        palette = default_mapping
    # assumes 8-bit depth colormapping
    N = 256
    array = np.asarray(range(N), dtype='uint8')
    array = array.reshape((1,N)).transpose()

    with open(filename, 'wb') as f:
        w = pngWriter(width=1, height=N, palette=swatch[palette],
                      alpha=False, bitdepth=8, compression=-1, filter_type=0)
        w.write(f, array)
