"""
2D array up/downscaling routines
"""
import numpy as np
try:
    from scipy import interpolate
    scipy_imported = True
except ImportError:
    scipy_imported = False


# Uncomment @profile to line profile with test_profile.sh
# @profile
def bilinear_interpolate_by_factor(im, factor=1.0, use_scipy=scipy_imported):
    if (np.float(factor) == np.float(1)):
        return im

    ny = im.shape[0]
    nx = im.shape[1]
    ny_new = np.ceil(ny * factor).astype('uint16')
    nx_new = np.ceil(nx * factor).astype('uint16')

    if use_scipy:
        return bilinear_interp_scipy(nx, ny, nx_new, ny_new, im)
    else:
        return bilinear_interp_numpy_only(nx, ny, nx_new, ny_new, im)


# @profile
def bilinear_interp_numpy_only(nx, ny, nx_new, ny_new, im):
    # try to deal with all numeric types
    im_datatype = im.dtype

    x = np.linspace(0, nx - 2, nx_new, dtype='float32')
    y = np.linspace(0, ny - 2, ny_new, dtype='float32')

    x0 = np.floor(x).astype('uint16').reshape(1, nx_new).repeat(ny_new, 0)
    x1 = x0 + 1
    y0 = np.floor(y).astype('uint16').reshape(ny_new, 1).repeat(nx_new, 1)
    y1 = y0 + 1

    x = x.reshape(1, nx_new).repeat(ny_new, 0)
    y = y.reshape(ny_new, 1).repeat(nx_new, 1)

    dx = x - x0
    dy = y - y0
    dxdy = dx * dy

    # im_scaled = ((x1 - x) * (y1 - y) * im[y0, x0])
    # im_scaled += ((x1 - x) * (y - y0) * im[y1, x0])
    # im_scaled += ((x - x0) * (y1 - y) * im[y0, x1])
    # im_scaled += ((x - x0) * (y - y0) * im[y1, x1])

    # slightly faster version of above
    im_scaled = ((1 - dx - dy + dxdy) * im[y0, x0])
    im_scaled += ((dy - dxdy) * im[y1, x0])
    im_scaled += ((dx - dxdy) * im[y0, x1])
    im_scaled += (dxdy * im[y1, x1])

    return im_scaled.astype(im_datatype)


# @profile
def bilinear_interp_scipy(nx, ny, nx_new, ny_new, im):

    x = np.linspace(0, nx - 1, nx, dtype='float32')
    y = np.linspace(0, ny - 1, ny, dtype='float32')

    x_new = np.linspace(0, nx - 1, nx_new, dtype='float32')
    y_new = np.linspace(0, ny - 1, ny_new, dtype='float32')

    # I've tried interp2d (linear), RegularGridInterpolator (linear), and
    # RectBivariateSpline (order=1), the last one seems to be the fastest
    interpolator = interpolate.RectBivariateSpline(y, x, im, kx=1, ky=1)

    im_new = interpolator(y_new, x_new)

    return im_new
