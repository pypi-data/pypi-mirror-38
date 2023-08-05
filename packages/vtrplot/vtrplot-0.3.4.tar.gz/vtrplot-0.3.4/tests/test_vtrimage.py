import time
import os

import sys
curr_path = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(curr_path))

from vtrplot import vtr_image


filedir = os.path.join(curr_path, 'test_files')

# Test Cases
# -------------------------------------------------

# # small 2D (~130ms)
threeD = False
vtr_filename = 'test.vtr'
png_filename = 'test.png'

# normal-ish 3D (~160ms loading all into mem, ~150ms memmap)
# threeD = True
# vtr_filename = 'test_small3D.vtr'
# png_filename = 'test_small3D.png'

# # # large-ish 3D (~380ms loading all into mem, ~ 160ms memmap)
# threeD = True
# vtr_filename = 'test_large3D.vtr'
# png_filename = 'test_large3D.png'

colorbar_name = 'colorbar.png'

# ------------------------------------------------


times = 1
# times = 10

start = time.time()
for _ in range(times):
    m = vtr_image.VTRImage(os.path.join(filedir, vtr_filename))
    if threeD:
        # print m.to_pngfile(os.path.join(filedir, png_filename), slice_dim=3, slice=1, min_val=1526.0438, max_val=1550)
        # print m.to_pngfile(os.path.join(filedir, png_filename), slice_dim=3, slice=90, min_range=30)
        # print m.to_pngfile(os.path.join(filedir, png_filename), palette="L1colour", slice_dim=2, slice=50)
        print m.to_pngfile(os.path.join(filedir, png_filename), palette="L1colour", scale_factor=1, slice_dim=2, slice=50)
        # print m.to_pngfile(os.path.join(filedir, png_filename), slice_dim=2, slice=80)
    else:
        print m.to_pngfile(os.path.join(filedir, png_filename), palette="viridis")
        # print m.to_pngfile(os.path.join(filedir, png_filename), palette="viridis", min_val=-1500, max_val=3000)
end = time.time()

print("Ran {:d} times, elapsed time {:.2f} ms".format(times, (end - start) * 1000.0 / times))



start = time.time()
for _ in range(10):
    vtr_image.palettebar_to_png(os.path.join(filedir, colorbar_name))
end = time.time()

print("palettebar_to_png finished in {:.2f} ms".format((end - start) * 1000.0 / times))
