from test_shapes import model
from skimage.transform import rescale

import os
import sys
curr_path = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(curr_path))

from vtrplot.interp import bilinear_interpolate_by_factor


@profile
def normal_interp():
    bilinear_interpolate_by_factor(model, 5.5)


@profile
def integer_interp():
    model_int = (model * 255.0 / 4805.00).astype('uint8')
    model_int_intrp = bilinear_interpolate_by_factor(model_int, 5.5)


@profile
def skimage_interp():
    model_scaled = model / 4805.0
    # default is bilinear mode
    rescale(model_scaled, 5.5)


if __name__ == "__main__":
    normal_interp()
    integer_interp()
    skimage_interp()
