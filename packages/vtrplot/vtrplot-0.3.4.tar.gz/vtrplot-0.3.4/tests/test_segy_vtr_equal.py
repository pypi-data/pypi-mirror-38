import time
import os
import hashlib

import sys
curr_path = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(curr_path))

from vtrplot import vtr_image


filedir = os.path.join(curr_path, 'test_files', 'segy_vtr_equal')

# Test Cases
# -------------------------------------------------

threeD = False
vtr_filename = 'test2D-vp.vtr'
segy_filename = 'test2D-vp.sgy'


# threeD = False
# vtr_filename = 'test2D-zero-centered.vtr'
# segy_filename = 'test2D-zero-centered.sgy'


# threeD = False
# vtr_filename = 'from_seisspace_2D.vtr'
# segy_filename = 'from_seisspace_2D.sgy'

# threeD = True
# vtr_filename = 'test3D-vp.vtr'
# segy_filename = 'test3D-vp.sgy'

# threeD = True
# vtr_filename = 'from_seisspace_3D.vtr'
# segy_filename = 'from_seisspace_3D.sgy'

# threeD = True
# vtr_filename = 'old_segyprep_3D.vtr'
# segy_filename = 'old_segyprep_3D.sgy'


# ------------------------------------------------


vtr_png_filename = vtr_filename + '.png'
segy_png_filename = segy_filename + '.png'

times = 1
# times = 10

if threeD:
    # args = {"palette": "L1colour", 'scale_factor': 2.5, 'slice_dim': 1, 'slice': 510}  # nx1
    # args = {"palette": "L1colour", 'scale_factor': 2.5, 'slice_dim': 2, 'slice': 40}  # nx2
    args = {"palette": "L1colour", 'scale_factor': 2.5, 'slice_dim': 3, 'slice': 80}  # nx3 = depth
else:
    args = {"palette": "L1colour"}

start = time.time()
for _ in range(times):
    m_vtr = vtr_image.VTRImage(os.path.join(filedir, vtr_filename))
    print m_vtr.to_pngfile(os.path.join(filedir, vtr_filename + '.png'), **args)
end = time.time()
print("Ran VTR {:d} times, elapsed time per iter {:.2f} ms".format(times, (end - start) * 1000.0 / times))


start = time.time()
for _ in range(times):
    m_segy = vtr_image.VTRImage(os.path.join(filedir, segy_filename))
    print m_segy.to_pngfile(os.path.join(filedir, segy_filename + '.png'), **args)
end = time.time()
print("Ran SEGY {:d} times, elapsed time per iter {:.2f} ms".format(times, (end - start) * 1000.0 / times))

with open(os.path.join(filedir, vtr_filename + '.png'), "rb") as vtrpng:
    print "VTR png file hash:"
    print hashlib.md5(vtrpng.read()).hexdigest()

    with open(os.path.join(filedir, segy_filename + '.png'), "rb") as segypng:
        print "SEGY png file hash:"
        print hashlib.md5(segypng.read()).hexdigest()
