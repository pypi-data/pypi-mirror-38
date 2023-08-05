# Sliced models from VTR and SEGY files

from vtrtool import VTRModel
import segyio
from segyio import TraceField
import numpy as np


class SlicedModel_VTR(VTRModel):
    # sliced model from a VTR file

    def __init__(self, file_name, use_memmap=True):
        super(SlicedModel_VTR, self).__init__(file_name, use_memmap=use_memmap)

    def __valid_dim_index(self, dim):
        return (dim == int(dim)) and (dim > 0) and (dim <= self.num_dimensions)

    def __valid_slice_for_dim(self, dim, slice):
        return (slice == int(slice)) and (slice > 0) and (slice <= self.shape[dim - 1])

    # @profile
    def slice_along_dim(self, propID, dim, slice, transpose=False):

        def transpose_if_needed(x):
            if transpose:
                return x.transpose()
            else:
                return x

        if (self.num_dimensions == 1):
            raise Exception('slice_along_dim can only be called for 2D or 3D models')

        if (self.num_dimensions == 2):
            # simply ignore slicing and use the whole model
            return transpose_if_needed(self.arrays[propID].copy())

        # Assum 3D model from this point on

        if not(self.__valid_dim_index(dim)):
            raise Exception('invalid slicing dimension dim')

        if not(self.__valid_slice_for_dim(dim, slice)):
            raise Exception('invalid slice index')

        if (dim == 3):
            model_slice = self.arrays[propID][:, :, slice]
        elif (dim == 2):
            model_slice = self.arrays[propID][:, slice, :]
        elif (dim == 1):
            model_slice = self.arrays[propID][slice, :, :]
        else:
            raise Exception('invalid dimension to slice over')

        # read slice memmap into memory for more compute-intensive tasks
        model_slice = model_slice.copy()

        # the transpose make sure that depth ends up being vertical axis
        # when slicing over 1st and 2nd dimension
        return transpose_if_needed(np.squeeze(model_slice))


class SlicedModel_SEGY(object):
    # sliced model from a SEGY file, using segyio

    def __init__(self, file_name, use_memmap=False):
        # open in unstructured mode as this does minimal pre-parsing of headers
        f = segyio.open(file_name, mode="r", strict=False, ignore_geometry=True)

        # determine what headers to use for inline/crosslines
        # there are two main candidates: SourceX/SourceY and Inline3D/Crossline3D
        # additionally we use reciever/group and cdp X/Y headers as fallbacks
        got_correct_headers = False

        last_sourceX = f.header[-1].get(TraceField.SourceX)
        last_sourceY = f.header[-1].get(TraceField.SourceY)

        last_inline3d = f.header[-1].get(TraceField.INLINE_3D)
        last_xline3d = f.header[-1].get(TraceField.CROSSLINE_3D)

        last_recieverX = f.header[-1].get(TraceField.GroupX)
        last_recieverY = f.header[-1].get(TraceField.GroupY)

        last_cdpX = f.header[-1].get(TraceField.CDP_X)
        last_cdpY = f.header[-1].get(TraceField.CDP_Y)

        trace_count = f.tracecount

        if trace_count <= 1:
            raise ValueError('SlicedModel does not yet work on 1D models')

        # check to see whether any of the above headers are valid, and gives consistent trace count

        if last_sourceX > 0 or last_sourceY > 0:
            try:
                # read segy file using these headers for inline/xline sorting and see if trace count is consistent
                f = segyio.open(file_name, mode="r", iline=TraceField.SourceX, xline=TraceField.SourceY)
                if len(f.ilines) * len(f.xlines) == trace_count:
                    got_correct_headers = True
                    self.used_headers="source"
            except Exception as e:
                pass

        if not got_correct_headers and (last_inline3d > 0 or last_xline3d > 0):
            try:
                f = segyio.open(file_name, mode="r", iline=TraceField.INLINE_3D, xline=TraceField.CROSSLINE_3D)
                if len(f.ilines) * len(f.xlines) == trace_count:
                    got_correct_headers = True
                    self.used_headers="inline3d"
            except Exception as e:
                pass

        if not got_correct_headers and (last_recieverX > 0 or last_recieverY > 0):
            try:
                f = segyio.open(file_name, mode="r", iline=TraceField.GroupX, xline=TraceField.GroupY)
                if len(f.ilines) * len(f.xlines) == trace_count:
                    got_correct_headers = True
                    self.used_headers="group"
            except Exception as e:
                pass

        if not got_correct_headers and (last_cdpX > 0 or last_cdpY > 0):
            try:
                f = segyio.open(file_name, mode="r", iline=TraceField.CDP_X, xline=TraceField.CDP_Y)
                if len(f.ilines) * len(f.xlines) == trace_count:
                    got_correct_headers = True
                    self.used_headers="cdp"
            except Exception as e:
                pass

        if not got_correct_headers:
            raise ValueError('cannot determine a good inline/crossline header pair for the SEGY file')

        # try to memmap
        self.use_memmap = use_memmap
        if use_memmap:
            f.mmap()  # activate mmap mode; failure is silent

        # set object properties and determine some basic geometry stuff
        self.segyio_handle = f
        self.file = file_name
        if len(f.xlines) == 1:
            self.num_dimensions = 2
            self.model_array_2d = f.xline[0].copy()  # load whole model into memory if 2D
            self.shape = (len(f.xlines), len(f.samples))
        elif len(f.ilines) == 1:
            self.num_dimensions = 2
            self.model_array_2d = f.iline[0].copy()  # load whole model into memory if 2D
            self.shape = (len(f.xlines), len(f.samples))
        else:
            self.num_dimensions = 3
            self.shape = (len(f.ilines), len(f.xlines), len(f.samples))

    def __valid_dim_index(self, dim):
        return (dim == int(dim)) and (dim > 0) and (dim <= self.num_dimensions)

    def __valid_slice_for_dim(self, dim, slice):
        return (slice == int(slice)) and (slice > 0) and (slice <= self.shape[dim - 1])

    # @profile
    def slice_along_dim(self, propID, dim, slice, transpose=False):

        def transpose_if_needed(x):
            if transpose:
                return x.transpose()
            else:
                return x

        if (self.num_dimensions == 1):
            raise Exception('slice_along_dim can only be called for 2D or 3D models')

        if (self.num_dimensions == 2):
            # simply ignore slicing and use the whole model
            return transpose_if_needed(self.model_array_2d)

        # Assum 3D model from this point on

        if not(self.__valid_dim_index(dim)):
            raise Exception('invalid slicing dimension dim')

        if not(self.__valid_slice_for_dim(dim, slice)):
            raise Exception('invalid slice index')

        if (dim == 3):
            model_slice = self.segyio_handle.depth_slice[slice].reshape((self.shape[1], self.shape[0])).transpose()
        elif (dim == 2):
            model_slice = self.segyio_handle.xline[self.segyio_handle.xlines[slice]]
        elif (dim == 1):
            model_slice = self.segyio_handle.iline[self.segyio_handle.ilines[slice]]
        else:
            raise Exception('invalid dimension to slice over')

        # read slice memmap into memory for more compute-intensive tasks
        model_slice = model_slice.copy()

        # the transpose make sure that depth ends up being vertical axis
        # when slicing over 1st and 2nd dimension
        return transpose_if_needed(model_slice)
