# EXPERIMENTAL! This code is still experimental, and is probably going to
# change

from pathlib import Path
from contextlib import contextmanager

import numpy as np
from ._version import get_versions

from .array import BaseDataDir, Array, MetaData, asarray, \
    create_basedir, check_accessmode, delete_array, create_array

__all__ = ['RaggedArray', 'asraggedarray', 'create_raggedarray',
           'delete_raggedarray']

class RaggedArray(BaseDataDir):
    """
    Disk-based sequence of arrays that may have a variable length in maximally
    one dimension.

    """
    _valuesdirname = 'values'
    _indicesdirname = 'indices'
    _version = '0.1.0'
    _metadatafilename = 'metadata.json'
    _readmefilename = 'README.txt'
    _filenames = {_valuesdirname, _indicesdirname,
                  _readmefilename, _metadatafilename} | BaseDataDir._filenames
    _formatversion = get_versions()['version']
    def __init__(self, path, accessmode='r'):
        BaseDataDir.__init__(self, path=path)
        self._accessmode = check_accessmode(accessmode)
        self._valuespath = self.path.joinpath(self._valuesdirname)
        self._indicespath = self.path.joinpath(self._indicesdirname)
        self._values = Array(self._valuespath, accessmode=self._accessmode)
        self._indices = Array(self._indicespath, accessmode=self._accessmode)
        self._metadata = MetaData(self._path.joinpath(self._metadatafilename),
                                  accessmode=accessmode)

    @property
    def accessmode(self):
        """
        Set data access mode of metadata.

        Parameters
        ----------
        accessmode: {'r', 'r+'}, default 'r'
            File access mode of the data. `r` means read-only, `r+`
            means read-write.

        """
        return self._accessmode

    @accessmode.setter
    def accessmode(self, value):
        self._accessmode = check_accessmode(value)
        self._metadata.accessmode = value

    @property
    def dtype(self):
        """Numpy data type of the array values.

        """
        return self._values._dtype

    @property
    def atom(self):
        """Dimensions of the non-variable axes of the arrays.

        """
        return tuple(self._values._shape[1:])

    @property
    def narrays(self):
        """Numpy data type of the array values.

        """
        return self._indices.shape[0]

    @property
    def metadata(self):
        """
        Dictionary of meta data.

        """
        return self._metadata

    @property
    def mb(self):
        """Size in megabytes of the data array.

        """
        return self._values._mb #+ self._indices._mb

    @property
    def size(self):
        """Total number of values in the data array.

        """
        return self._values._size


    def __getitem__(self, item):
        if not np.issubdtype(type(item), np.integer):
            raise TypeError("Only integers can be used for indexing " \
                            "darraylists, which '{}' is not".format(item))
        index = slice(*self._indices[item])
        return self._values[index]

    def __len__(self):
        return self._indices.shape[0]

    def append(self, array):
        size = len(array)
        endindex = self._values.shape[0]
        self._values.append(np.asarray(array, dtype=self.dtype))
        self._indices.append([[endindex, endindex + size]])

    def copy(self, path, accessmode='r', overwrite=False):
        arrayiterable = (self[i] for i in range(len(self)))
        metadata = dict(self.metadata)
        return asraggedarray(path=path, arrayiterable=arrayiterable,
                             dtype=self.dtype, metadata=metadata,
                             accessmode=accessmode, overwrite=overwrite)

    @contextmanager
    def _view(self, accessmode=None):
        with self._indices.view(accessmode=accessmode) as iv,\
             self._values.view(accessmode=accessmode) as vv:
            yield iv, vv

    @contextmanager
    def iterview(self, startindex=0, endindex=None, stepsize=1,
                 accessmode=None):
        if endindex is None:
            endindex = self.narrays
        with self._view(accessmode=accessmode):
            for i in range(startindex, endindex, stepsize):
                return self[i]



# FIXME empty arrayiterable
def asraggedarray(path, arrayiterable, dtype=None, metadata=None,
                  accessmode='r+', overwrite=False):
    path = Path(path)
    if not hasattr(arrayiterable, 'next'):
        arrayiterable = (a for a in arrayiterable)
    bd = create_basedir(path=path, overwrite=overwrite)
    firstarray = np.asarray(next(arrayiterable), dtype=dtype)
    dtype = firstarray.dtype
    valuespath = bd.path.joinpath(RaggedArray._valuesdirname)
    indicespath = bd.path.joinpath(RaggedArray._indicesdirname)
    valuesda = asarray(path=valuespath, array=firstarray, dtype=dtype,
                       accessmode='r+', overwrite=overwrite)
    firstindices = [[0, len(firstarray)]]
    indicesda = asarray(path=indicespath, array=firstindices,
                        dtype=np.int64, accessmode='r+',
                        overwrite=overwrite)
    valueslen = firstindices[0][1]
    indiceslen = 1
    with valuesda._open_array(accessmode='r+') as (vv, vfd), \
         indicesda._open_array(accessmode='r+') as (iv, ifd):
        for array in arrayiterable:
            lenincreasevalues = valuesda._append(array, fd=vfd)
            starti, endi = valueslen, valueslen + lenincreasevalues
            lenincreaseindices = indicesda._append([[starti, endi]], fd=ifd)
            valueslen += lenincreasevalues
            indiceslen += lenincreaseindices
    valuesda._update_len(lenincrease=valueslen-firstindices[0][1])
    valuesda._update_readmetxt()
    indicesda._update_len(lenincrease=indiceslen-1)
    indicesda._update_readmetxt()

    metadatapath = path.joinpath(Array._metadatafilename)
    if metadata is not None:
        bd._write_jsondict(filename=Array._metadatafilename,
                           d=metadata, overwrite=overwrite)
    elif metadatapath.exists():  # no metadata but file exists, remove it
        metadatapath.unlink()
    bd._write_txt(RaggedArray._readmefilename, readmetxt)
    return RaggedArray(path=path, accessmode=accessmode)


def create_raggedarray(path, atom=(), dtype='float64', metadata=None,
                       accessmode='r+', overwrite=False):
    if not hasattr(atom, '__len__'):
        raise TypeError(f'shape "{atom}" is not a sequence of dimensions.\n'
                        f'If you want just a list of 1-dimensional arrays, '
                        f'use "()"')
    shape = [0] + list(atom)
    ar = np.zeros(shape, dtype=dtype)
    dal = asraggedarray(path=path, arrayiterable=[ar], metadata=metadata,
                        accessmode=accessmode, overwrite=overwrite)
    # the current ragged array has one element, which is an empty array
    # but we want an empty ragged array => we should get rid of the indices
    create_array(path=dal._indicespath, shape=(0,2), dtype=np.int64,
                 overwrite=True)
    return RaggedArray(dal.path, accessmode=accessmode)







readmetxt = """Disk-based storage of ragged arrays
               ===================================

This directory is a data store for numeric ragged arrays. This is a sequence
of arrays that may have variable lengths in maximally one of their dimensions.

There are two subdirectories, each containing an array stored in a simple 
format that should be easy to read. To do so, see the README's in these 
directories.

The subdirectory 'values' holds the actual numerical data, where arrays are 
simply appended along their variable length dimension (first axis).

The subdirectory 'indices' holds 2D array data that represent the first 
axis start and end indices (counting from 0) to read corresponding arrays 
in the list.

So to read the n-th array in the list, read the nt-h start and end indices 
from the indices array ('starti, endi = indices[n]') and use these to read the 
array data from the values array (array = values[starti:endi]).


"""


def delete_raggedarray(rar):
    """
    Delete Darr ragged array data from disk.

    Parameters
    ----------
    path: path to data directory

    """
    try:
        if not isinstance(rar, RaggedArray):
            dal = RaggedArray(rar)
    except:
        raise TypeError(f"'{dal}' not recognized as a Darr array list")

    for fn in rar._filenames:
        path = rar.path.joinpath(fn)
        if path.exists() and not path.is_dir():
            path.unlink()
    delete_array(rar._values)
    delete_array(rar._indices)
    try:
        rar._path.rmdir()
    except OSError as error:
        message = f"Error: could not fully delete Darr array list directory " \
                  f"'{rar.path}'. It may contain additional files that are " \
                  f"not part of the darr. If so, these should be removed " \
                  f"manually."
        raise OSError(message) from error