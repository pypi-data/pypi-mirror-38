from test_shapes import model
import numpy
import matplotlib.pyplot as plt
from matplotlib import cm

import os
import sys
curr_path = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(curr_path))

from vtrplot.interp import bilinear_interpolate_by_factor


def test_plot():
    model_interp = bilinear_interpolate_by_factor(model, 5.5)

    plt.figure(1)
    plt.imshow(model, cmap=cm.RdBu_r)

    plt.figure(2)
    plt.imshow(model_interp, cmap=cm.RdBu_r)

    plt.show()


def test_discr():
    model_int = numpy.ceil(model * 255.0 / 4805.00).astype('uint8')
    model_int_intrp = bilinear_interpolate_by_factor(model_int, 2.5)
    model_int_intrp = model_int_intrp.astype('uint8')

    model_interp_int = bilinear_interpolate_by_factor(model, 2.5)
    model_interp_int = numpy.ceil(model_interp_int * 255.0 / 4805.00).astype('uint8')

    model_err = model_int_intrp.astype('float32') - model_interp_int.astype('float32')

    plt.figure(1)
    plt.imshow(model_err)

    plt.show()


if __name__ == "__main__":
    # test_plot()
    test_discr()
