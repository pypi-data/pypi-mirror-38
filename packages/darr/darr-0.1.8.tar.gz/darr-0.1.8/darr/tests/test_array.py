import os
import unittest
from pathlib import Path
import warnings

import numpy as np
from numpy.testing import assert_equal, assert_array_equal

from darr.array import asarray, create_array, numtypes, Array, \
    truncate_array, BaseDataDir, delete_array, AppendDataError
from .utils import tempdir


def assert_array_identical(x, y):
    assert_array_equal(x, y)
    assert_equal(x.dtype, y.dtype)
    assert_equal(x.shape, y.shape)

def check_arrayequaltoasarray(ndarray):
    """Tests if asarray creates an array of same shape and dtype and same
    contents as input."""
    with tempdir() as dirname:
        dar = asarray(path=dirname, array=ndarray, overwrite=True)
        assert_array_equal(dar[:], ndarray)
        assert_equal(dar.dtype, ndarray.dtype)
        assert_equal(dar.shape, ndarray.shape)

def check_arrayequaltocreatearray(ndarray, shape, dtype=None, chunklen=None):
    with tempdir() as dirname:
        dar = create_array(path=dirname, shape=shape,
                           dtype=dtype, chunklen=chunklen,
                           overwrite=True)
        if dtype is not None:
            ndarray = ndarray.astype(dtype)
        assert_array_identical(ndarray, dar[:])

class AsArray(unittest.TestCase):

    def test_onedimensional(self):
        ndarray = np.arange(24)
        check_arrayequaltoasarray(ndarray)

    def test_twodimensional(self):
        ndarray = np.arange(24).reshape(12, 2)
        check_arrayequaltoasarray(ndarray)

    def test_threedimensional(self):
        ndarray = np.arange(24).reshape(4, 2, 3)
        check_arrayequaltoasarray(ndarray)

    def test_numericdtypes(self):
        dtypes = numtypes.keys()
        for dtype in dtypes:
            ndarray = np.arange(24, dtype=dtype)
            check_arrayequaltoasarray(ndarray)

    def test_fortranorder(self):
        ndarray = np.asarray(np.arange(24, dtype='float64'), order='F')
        check_arrayequaltoasarray(ndarray)

    def test_corder(self):
        ndarray = np.asarray(np.arange(24, dtype='float64'), order='C')
        check_arrayequaltoasarray(ndarray)

    def test_littleendian(self):
        ndarray = np.arange(24, dtype='<f4')
        check_arrayequaltoasarray(ndarray)

    def test_bigendian(self):
        ndarray = np.arange(24, dtype='>f4')
        check_arrayequaltoasarray(ndarray)

    def test_emptyarray(self):
        ndarray = np.zeros(0, dtype='float64')
        check_arrayequaltocreatearray(ndarray=ndarray, shape=(0,),
                                      dtype='float64')

    def test_emptyarraydifferentdtype(self):
        ndarray = np.zeros(0, dtype='float64')
        check_arrayequaltocreatearray(ndarray=ndarray, shape=(0,),
                                      dtype='int64')

    def test_overwritearray(self):
        with tempdir() as dirname:
            a = np.zeros((5,), dtype='float64')
            dar = asarray(path=dirname, array=a, overwrite=True)
            b = np.ones((4,2), dtype='uint8')
            dar = asarray(path=dirname, array=b, overwrite=True)
            assert_array_identical(dar[:], b)

    def test_writingsmallerchunks(self):
        with tempdir() as dirname:
            a = np.arange(1024, dtype='int64').reshape(2,-1)
            dar = asarray(path=dirname, array=a, chunklen=4, overwrite=True)
            assert_equal(a, dar[:])
            dar = asarray(path=dirname, array=a, chunklen=5, overwrite=True)
            assert_equal(a, dar[:])

    def test_writinglargerthanlenchunks(self):
        with tempdir() as dirname:
            a = np.arange(1024, dtype='int64').reshape(2, -1)
            dar = asarray(path=dirname, array=a, chunklen=4096, overwrite=True)
            assert_equal(a, dar[:])


class CreateDiskArray(unittest.TestCase):

    def test_zerosfloat64default(self):
        shape = (12,)
        ndarray = np.zeros(shape, dtype='float64')
        check_arrayequaltocreatearray(ndarray=ndarray, shape=shape)

    def test_twodimensional(self):
        shape = (12, 2)
        ndarray = np.zeros(shape, dtype='float64')
        check_arrayequaltocreatearray(ndarray=ndarray, shape=shape)

    def test_threedimensional(self):
        shape = (4, 2, 3)
        ndarray = np.zeros(shape, dtype='float64')
        check_arrayequaltocreatearray(ndarray=ndarray, shape=shape)

    # split out manually?
    def test_numericdtypes(self):
        dtypes = numtypes.keys()
        for dtype in dtypes:
            ndarray = np.zeros(24, dtype=dtype)
            check_arrayequaltocreatearray(ndarray=ndarray, shape=(24,),
                                          dtype=dtype)

    def test_chunked(self):
        ndarray = np.zeros(12, dtype='float64')
        for chunklen in (1, 5, 6, 11, 12, 13):
            check_arrayequaltocreatearray(ndarray=ndarray, shape=(12,),
                                          chunklen=chunklen)
        ndarray = np.zeros(13, dtype='float64')
        for chunklen in (1, 6, 7, 12, 13, 14):
            check_arrayequaltocreatearray(ndarray=ndarray, shape=(13,),
                                          chunklen=chunklen)

    def test_chunkedthreedimensional(self):
        ndarray = np.zeros((12,3,7), dtype='float64')
        for chunklen in (1, 5, 6, 11, 12, 13):
            check_arrayequaltocreatearray(ndarray=ndarray, shape=(12, 3, 7),
                                          chunklen=chunklen*21)
        ndarray = np.zeros((13,3,7), dtype='float64')
        for chunklen in (1, 6, 7, 12, 13, 14):
            check_arrayequaltocreatearray(ndarray=ndarray, shape=(13, 3, 7),
                                          chunklen=chunklen*21)

    def test_toosmallchunklen(self):
        ndarray = np.zeros((12, 3, 7), dtype='float64')
        check_arrayequaltocreatearray(ndarray=ndarray, shape=(12, 3, 7),
                                      chunklen=1)

    def test_emptyarray(self):
        ndarray = np.zeros((0,3,7), dtype='float64')
        check_arrayequaltocreatearray(ndarray=ndarray, shape=(0, 3, 7),
                                      chunklen=1)


class TestArray(unittest.TestCase):

    def test_instantiatefromexistingpath(self):
        with tempdir() as dirname:
            dar = create_array(path=dirname, shape=(12,),
                               dtype='int64', overwrite=True)
            dar = Array(path=dirname)

    def test_instantiatefromnonexistingpath(self):
        with tempdir() as dirname:
            dar = create_array(path=dirname, shape=(12,),
                               dtype='int64', overwrite=True)
        with self.assertRaises(OSError):
            Array(path=dirname)

    def test_setvalues(self):
        with tempdir() as dirname:
            dar = create_array(path=dirname, shape=(12,), fill=0,
                               dtype='int64', overwrite=True)
            assert_equal(dar[2:4],[0,0])
            dar[2:4] = 1
            assert_equal(dar[2:4], [1,1])

    def test_currentchecksumsnometadata(self):
        with tempdir() as dirname:
            dar = create_array(path=dirname, shape=(12,), fill=0,
                               dtype='int64', overwrite=True)
            s = set(dar.currentchecksums)
            assert_equal({'README.txt', 'arraydescription.json',
                    'arrayvalues.bin'}, s)

    def test_currentchecksumsmetadata(self):
        with tempdir() as dirname:
            dar = create_array(path=dirname, shape=(12,), fill=0,
                               dtype='int64', metadata={'a':1}, overwrite=True)
            s = set(dar.currentchecksums)
            assert_equal({'README.txt', 'arraydescription.json',
                          'arrayvalues.bin', 'metadata.json'}, s)

    def test_str(self):
        with tempdir() as dirname:
            dar = create_array(path=dirname, shape=(2,), fill=0,
                               dtype='int64', overwrite=True)
            assert_equal(str(dar),'[0 0]')

    def test_repr(self):
        with tempdir() as dirname:
            dar = create_array(path=dirname, shape=(2,), fill=0,
                               dtype='int64', overwrite=True)
            # linux and windows have different numpy memmap reprs...
            assert_equal(repr(dar)[:18], 'darr array ([0, 0]')

    def test_setaccessmode(self):
        with tempdir() as dirname:
            dar = create_array(path=dirname, shape=(2,), fill=0,
                               dtype='int64', overwrite=True, accessmode='r')
            self.assertEqual(dar.accessmode, 'r')
            dar.accessmode = 'r+'
            self.assertEqual(dar.accessmode, 'r+')
            self.assertRaises(ValueError, setattr, dar, 'accessmode', 'w')
            self.assertRaises(ValueError, setattr, dar, 'accessmode', 'a')

    def test_itemsize(self):
        with tempdir() as dirname:
            dar = create_array(path=dirname, shape=(2,), fill=0,
                               dtype='int64', overwrite=True)
            assert_equal(dar.itemsize, 8)

    def test_nbytes(self):
        with tempdir() as dirname:
            dar = create_array(path=dirname, shape=(2,), fill=0,
                               dtype='int64', overwrite=True)
            assert_equal(dar.nbytes, 2*8)

    def test_mb(self):
        with tempdir() as dirname:
            dar = create_array(path=dirname, shape=(2,), fill=0,
                               dtype='int64', overwrite=True)
            assert_equal(dar.mb, 2*8/1e6)

    def test_mb(self):
        with tempdir() as dirname:
            dar = create_array(path=dirname, shape=(2,), fill=0,
                               dtype='int64', overwrite=True)
            assert_equal(dar.mb, 2*8/1e6)

    def test_size(self):
        with tempdir() as dirname:
            dar = create_array(path=dirname, shape=(2,2), fill=0,
                               dtype='int64', overwrite=True)
            assert_equal(dar.size, 4)


class TestReadArrayDescr(unittest.TestCase):

    def test_arrayinfomissingfile(self):
        with tempdir() as dirname:
            dar = create_array(path=dirname, shape=(2,), fill=0,
                               dtype='int64', overwrite=True)
            dar._arraydescrpath.unlink()
            self.assertRaises(FileNotFoundError, Array, dar.path)

    def test_arrayinfonewerversionfile(self):
        with tempdir() as dirname:
            dar = create_array(path=dirname, shape=(2,), fill=0,
                               dtype='int64', overwrite=True)
            arrayinfo = dar._arrayinfo.copy()
            vs = f"1{arrayinfo['darrversion']}"
            arrayinfo['darrversion'] = vs
            dar._write_jsondict(dar._arraydescrfilename, arrayinfo,
                                overwrite=True)
            self.assertWarns(UserWarning, Array, dar.path)

    def test_arrayinfowrongshapetype(self):
        with tempdir() as dirname:
            dar = create_array(path=dirname, shape=(2,), fill=0,
                               dtype='int64', overwrite=True)
            arrayinfo = dar._arrayinfo.copy()
            arrayinfo['shape'] = ['a', 3]
            dar._write_jsondict(dar._arraydescrfilename, arrayinfo,
                                overwrite=True)
            self.assertRaises(TypeError, Array, dar.path)

    def test_arrayinfowrongorder(self):
        with tempdir() as dirname:
            dar = create_array(path=dirname, shape=(2,), fill=0,
                               dtype='int64', overwrite=True)
            arrayinfo = dar._arrayinfo.copy()
            arrayinfo['arrayorder'] = 'D'
            dar._write_jsondict(dar._arraydescrfilename, arrayinfo,
                                overwrite=True)
            self.assertRaises(ValueError, Array, dar.path)
            arrayinfo['arrayorder'] = '[D]'
            dar._write_jsondict(dar._arraydescrfilename, arrayinfo,
                                overwrite=True)
            self.assertRaises(Exception, Array, dar.path)


class TestConsistency(unittest.TestCase):

    def test_consistencyself(self):
        with tempdir() as dirname:
            dar = create_array(path=dirname, shape=(2,), fill=0,
                               dtype='int64', overwrite=True)
            arrayinfo = dar._arrayinfo.copy()
            arrayinfo['shape'] = (3,)
            dar._write_jsondict(dar._arraydescrfilename, arrayinfo,
                                overwrite=True)
            self.assertRaises(ValueError, dar._check_consistency)

    def test_consistencywrongshape(self):
        with tempdir() as dirname:
            dar = create_array(path=dirname, shape=(2,), fill=0,
                               dtype='int64', overwrite=True)
            arrayinfo = dar._arrayinfo.copy()
            arrayinfo['shape'] = (3,)
            dar._write_jsondict(dar._arraydescrfilename, arrayinfo,
                                overwrite=True)
            self.assertRaises(ValueError, Array, dar.path)

    def test_consistencywrongitemsize(self):
        with tempdir() as dirname:
            dar = create_array(path=dirname, shape=(2,), fill=0,
                               dtype='int64', overwrite=True)
            arrayinfo = dar._arrayinfo.copy()
            arrayinfo['numtype'] = 'int32'
            dar._write_jsondict(dar._arraydescrfilename, arrayinfo,
                                overwrite=True)
            self.assertRaises(ValueError, Array, dar.path)


class IterView(unittest.TestCase):

    def test_defaultparams_fit(self):
        with tempdir() as dirname:
            dar = create_array(path=dirname, shape=(12,),
                               dtype='int64', overwrite=True)
            l = [c for c in dar.iterview(chunklen=2)]
            assert_equal(len(l), 6)
            assert_array_equal(np.concatenate(l), dar[:])
            del l # otherwise file is still in use and may not be removed
            del dar

    def test_remainderfalse_fit(self):
        with tempdir() as dirname:
            dar = create_array(path=dirname, shape=(12,),
                               dtype='int64', overwrite=True)
            l = [c for c in dar.iterview(chunklen=2, include_remainder=False)]
            assert_equal(len(l), 6)
            assert_array_equal(np.concatenate(l), dar[:])
            del l # otherwise file is still in use and may not be removed
            del dar

    def test_defaultparams_nofit(self):
        with tempdir() as dirname:
            dar = create_array(path=dirname, shape=(13,),
                               dtype='int64', overwrite=True)
            l = [c for c in dar.iterview(chunklen=2)]
            assert_equal(len(l), 7)
            assert_array_equal(np.concatenate(l), dar[:])
            del l # otherwise file is still in use and may not be removed
            del dar

    def test_remainderfalse_nofit(self):
        with tempdir() as dirname:
            dar = create_array(path=dirname, shape=(13,),
                               dtype='int64', overwrite=True)
            l = [c for c in
                 dar.iterview(chunklen=2, include_remainder=False)]
            assert_equal(len(l), 6)
            assert_array_equal(np.concatenate(l), dar[:12])
            del l # otherwise file is still in use and may not be removed
            del dar


class AppendData(unittest.TestCase):

    def test_appendnumber(self):
        with tempdir() as dirname:
            dar = create_array(path=dirname, shape=(2,),
                               dtype='int64', overwrite=True)
            dar.append(1)
            assert_array_equal(np.array([0, 0, 1], dtype='int64'), dar[:])

    def test_appendlist1d(self):
        with tempdir() as dirname:
            dar = create_array(path=dirname, shape=(2,),
                               dtype='int64', overwrite=True)
            dar.append([1,2])
            dar.append([3])
            assert_array_equal(np.array([0,0,1,2,3], dtype='int64'), dar[:])

    def test_appendlist2d(self):
        with tempdir() as dirname:
            dar = create_array(path=dirname, shape=(2, 3),
                               dtype='int64', overwrite=True)
            dar.append([[1,2,3]])
            dar.append([[1,2,3],[4,5,6]])
            assert_array_equal(np.array([[0,0,0],[0,0,0],[1,2,3],[1,2,3],
                                         [4, 5, 6]], dtype='int64'), dar[:])

    def test_appendtoempty1d(self):
        with tempdir() as dirname:
            dar = create_array(path=dirname, shape=(0,),
                               dtype='int64', overwrite=True)
            dar.append([1, 2, 3])
            assert_array_equal(np.array([1, 2, 3], dtype='int64'), dar[:])

    def test_appendtoempty2d(self):
        with tempdir() as dirname:
            dar = create_array(path=dirname, shape=(0, 2),
                               dtype='int64', overwrite=True)
            dar.append([[1,2]])
            dar.append([[1,2],[3,4]])
            assert_array_equal(np.array([[1,2],[1,2],[3,4]], dtype='int64'),
            dar[:])

    def test_appendempty1d(self):
        with tempdir() as dirname:
            dar = create_array(path=dirname, shape=(1,),
                               dtype='int64', overwrite=True)
            dar.append([])
            assert_array_equal(np.array([0], dtype='int64'), dar[:])

    def test_appendempty2d(self):
        with tempdir() as dirname:
            dar = create_array(path=dirname, shape=(1, 2),
                               dtype='int64', overwrite=True)
            dar.append(np.zeros((0,2), dtype='int64'))
            assert_array_equal(np.array([[0,0]], dtype='int64'), dar[:])

    def test_appendemptytoempty1d(self):
        with tempdir() as dirname:
            dar = create_array(path=dirname, shape=(0,),
                               dtype='int64', overwrite=True)
            dar.append([])
            assert_array_equal(np.array([], dtype='int64'), dar[:])

    def test_appendemptytoempty2d(self):
        with tempdir() as dirname:
            dar = create_array(path=dirname, shape=(0, 2),
                               dtype='int64', overwrite=True)
            dar.append(np.zeros((0, 2), dtype='int64'))
            assert_array_equal(np.zeros((0,2), dtype='int64'), dar[:])

    def test_appenddataerror(self):
        def testiter():
            yield [1, 2, 3]
            yield [4, 5, 6]
            raise ValueError
        g = (f for f in testiter())
        with tempdir() as dirname:
            dar = create_array(path=dirname, shape=(2,),
                               dtype='int64', overwrite=True)
            self.assertRaises(AppendDataError, dar.iterappend, g)
            assert_equal(dar[:], [0,0,1,2,3,4,5,6])

    def test_appendwrongshape(self):
        with tempdir() as dirname:
            dar = create_array(path=dirname, shape=(2,3),
                               dtype='int64', overwrite=True)
            ar = [[3,4]]
            self.assertRaises(AppendDataError, dar.append, ar)

    def test_appendreadonlyarray(self):
        with tempdir() as dirname:
            dar = create_array(path=dirname, shape=(2,),
                               dtype='int64', overwrite=True, accessmode='r')
            ar = [3, 4]
            self.assertRaises(OSError, dar.append, ar)

    def test_iterappendnoniterable(self):
        with tempdir() as dirname:
            dar = create_array(path=dirname, shape=(2,),
                               dtype='int64', overwrite=True)
            ar = 3
            self.assertRaises(TypeError, dar.iterappend, ar)

class TestIterView(unittest.TestCase):

    def test_iterviewstartindextoohigh(self):
        with tempdir() as dirname:
            dar = create_array(path=dirname, shape=(10,),
                               dtype='int64', overwrite=True)
            with self.assertRaises(ValueError):
                chunks = [f for f in dar.iterview(chunklen=2, startindex=5, \
                                                  endindex=2)]

    def test_iterviewendindextoohigh(self):
        with tempdir() as dirname:
            dar = create_array(path=dirname, shape=(5,),
                               dtype='int64', overwrite=True)
            with self.assertRaises(ValueError):
                chunks = [f for f in dar.iterview(chunklen=2, startindex=1, \
                                                  endindex=8)]


class MetaData(unittest.TestCase):

    def test_createwithmetadata(self):
        with tempdir() as dirname:
            md = {'fs':20000, 'x': 33.3}
            dar = create_array(path=dirname, shape=(0, 2),
                               dtype='int64', metadata=md, overwrite=True)
            assert_equal(dict(dar.metadata), md)

    def test_getmetadata(self):
        with tempdir() as dirname:
            md = {'fs': 20000, 'x': 33.3}
            dar = create_array(path=dirname, shape=(0, 2),
                               dtype='int64', metadata=md, overwrite=True)
            self.assertEqual(dar.metadata.get('fs'), 20000)

    def test_metadatavalues(self):
        with tempdir() as dirname:
            md = {'fs': 20000, 'x': 33.3}
            dar = create_array(path=dirname, shape=(0, 2),
                               dtype='int64', metadata=md, overwrite=True)
            self.assertEqual(set(dar.metadata.values()), {20000,33.3})


    def test_changemetadata(self):
        with tempdir() as dirname:
            md = {'fs': 20000, 'x': 33.3}
            dar = create_array(path=dirname, shape=(0, 2),
                               dtype='int64', metadata=md, overwrite=True)
            dar.metadata['fs'] = 40000
            assert_equal(dict(dar.metadata), {'fs': 40000, 'x': 33.3})
            dar.metadata.update({'x': 34.4})
            assert_equal(dict(dar.metadata), {'fs': 40000, 'x': 34.4})

    def test_popmetadata(self):
        with tempdir() as dirname:
            md = {'fs': 20000, 'x': 33.3}
            dar = create_array(path=dirname, shape=(0, 2),
                               dtype='int64', metadata=md, overwrite=True)
            dar.metadata.pop('x')
            assert_equal(dict(dar.metadata), {'fs': 20000})
            dar.metadata.pop('fs')
            assert_equal(dict(dar.metadata), {})

    def test_popitmemetadata(self):
        with tempdir() as dirname:
            md = {'fs': 20000, 'x': 33.3}
            dar = create_array(path=dirname, shape=(0, 2),
                               dtype='int64', metadata=md, overwrite=True)
            k, v = dar.metadata.popitem()
            keys = dar.metadata.keys()
            assert k not in keys
            k, v = dar.metadata.popitem()
            assert not dar._metadata.path.exists()

    def test_metadataaccessmodereadwrite(self):
        with tempdir() as dirname:
            md = {'fs': 20000, 'x': 33.3}
            dar = create_array(path=dirname, shape=(0, 2),
                               dtype='int64', metadata=md, overwrite=True,
                               accessmode='r+')
            self.assertEqual(dar.metadata.accessmode, 'r+')
            dar.metadata['x'] = 22.2

    def test_metadataaccessmodereadonly(self):
        with tempdir() as dirname:
            md = {'fs': 20000, 'x': 33.3}
            dar = create_array(path=dirname, shape=(0, 2),
                               dtype='int64', metadata=md, overwrite=True,
                               accessmode='r')
            self.assertEqual(dar.metadata.accessmode, 'r')
            self.assertRaises(OSError, dar.metadata.popitem)
            self.assertRaises(OSError, dar.metadata.pop)
            self.assertRaises(OSError, dar.metadata.update, {'a': 3})

    def test_setaccessmode(self):
        with tempdir() as dirname:
            dar = create_array(path=dirname, shape=(2,), fill=0,
                               dtype='int64', overwrite=True, accessmode='r')
            self.assertEqual(dar.metadata.accessmode, 'r')
            dar.metadata.accessmode = 'r+'
            self.assertEqual(dar.metadata.accessmode, 'r+')
            self.assertRaises(ValueError, setattr, dar.metadata, 'accessmode',
                              'w')
            self.assertRaises(ValueError, setattr, dar.metadata, 'accessmode',
                              'a')

    def test_delitem(self):
        with tempdir() as dirname:
            md = {'fs': 20000, 'x': 33.3}
            dar = create_array(path=dirname, shape=(0, 2),
                               dtype='int64', metadata=md, overwrite=True,
                               accessmode='r+')
            del dar.metadata['x']
            self.assertEqual(dict(dar.metadata), {'fs': 20000})

    def test_metadatarepr(self):
        with tempdir() as dirname:
            md = {'a': 1}
            dar = create_array(path=dirname, shape=(0, 2),
                               dtype='int64', metadata=md, overwrite=True,
                               accessmode='r+')
            self.assertEqual(repr(dar.metadata), "{'a': 1}")


class TestOpenFile(unittest.TestCase):

    def test_openfile(self):
        with tempdir() as dirname:
            dar = create_array(path=dirname, shape=(0, 2), dtype='int64',
                               overwrite=True, accessmode='r+')
            with dar.open_file('notes.txt', 'a') as f:
                f.write('test\n')
            path = dar.path / 'notes.txt'
            self.assertEqual(path.exists(), True)

    def test_openfileprotectedfiles(self):
        with tempdir() as dirname:
            dar = create_array(path=dirname, shape=(0, 2), dtype='int64',
                               overwrite=True, accessmode='r+')
            for fn in dar._filenames:
                with self.assertRaises(OSError):
                    with dar.open_file(fn, 'a') as f:
                        f.write('test\n')



class TruncateData(unittest.TestCase):

    def test_truncate1d(self):
        with tempdir() as dirname:
            a = np.array([0,1,2,3,4], dtype='int64')
            dar = asarray(path=dirname, array=a, overwrite=True,
                          accessmode='r+')
            assert_equal(a, dar[:])
            truncate_array(dar, 2)
            assert_equal(a[:2], dar[:])


class DeleteArray(unittest.TestCase):

    def test_simpledeletearray(self):
        with tempdir() as dirname:
            dalpath = Path(dirname).joinpath('temp.dal')
            dar = create_array(path=dalpath, shape=(0, 2), dtype='int64')
            delete_array(dar)
            assert_equal(len(os.listdir(dirname)), 0)

    def test_simpledeletearraypath(self):
        with tempdir() as dirname:
            dalpath = Path(dirname).joinpath('temp.dal')
            dar = create_array(path=dalpath, shape=(0, 2), dtype='int64')
            delete_array(dalpath)
            assert_equal(len(os.listdir(dirname)), 0)

    def test_donotdeletenondarrfile(self):
        with tempdir() as dirname:
            dalpath = Path(dirname).joinpath('temp.dal')
            dar = create_array(path=dalpath, shape=(0, 2), dtype='int64')
            dar._write_jsondict('test.json', {'a': 1})
            testpath = dar._path.joinpath('test.json')
            self.assertRaises(OSError, delete_array, dar)
            self.assertEqual(testpath.exists(), True)

class TestMd5Checksums(unittest.TestCase):

    def test_storemd5checksums(self):
        with tempdir() as dirname:
            dar = create_array(path=dirname, shape=(2, 2), dtype='int64',
                               overwrite=True)
            cs = dar.store_md5checksums()
            scs = dar.storedmd5checksums
            self.assertEqual(scs, cs)
            ccs = dar.currentchecksums
            self.assertEqual(scs, cs)

    def test_assertmd5checksumsvalues(self):
        with tempdir() as dirname:
            dar = create_array(path=dirname, shape=(2, 2), dtype='int64',
                               overwrite=True)
            self.assertRaises(FileNotFoundError, dar.assert_md5checksums)
            scs = dar.store_md5checksums()
            ccs = dar.currentchecksums
            self.assertEqual(scs, ccs)
            dar[0] = 1
            self.assertRaises(ValueError, dar.assert_md5checksums)
            scs = dar.store_md5checksums()
            ccs = dar.currentchecksums
            self.assertEqual(scs, ccs)


class TestBaseDataDir(unittest.TestCase):

    def test_writejsondictcorrectinput(self):
        with tempdir() as dirname:
            bd = BaseDataDir(dirname)
            bd._write_jsondict('test1.json', {'a': 1})

    def test_writejsondictincorrectinput(self):
        with tempdir() as dirname:
            bd = BaseDataDir(dirname)
            with self.assertRaises(TypeError):
                bd._write_jsondict('test1.json', 3)
            with self.assertRaises(TypeError):
                bd._write_jsondict('test1.json', 'a')

    def test_updatejsondictcorrect(self):
        with tempdir() as dirname:
            bd = BaseDataDir(dirname)
            bd._write_jsondict('test1.json', {'a': 1})
            bd._update_jsondict('test1.json', {'a': 2, 'b':3})

    def test_readjsondict(self):
        with tempdir() as dirname:
            bd = BaseDataDir(dirname)
            wd = {'a': 1, 'b': [1,2,3], 'c': 'k'}
            bd._write_jsondict('test1.json', wd)
            rd = bd._read_jsondict('test1.json')
            assert_equal(wd, rd)

    def test_readjsondictrequiredkeypresent(self):
        with tempdir() as dirname:
            bd = BaseDataDir(dirname)
            wd = {'a': 1, 'b': [1,2,3], 'c': 'k'}
            bd._write_jsondict('test1.json', wd)
            rd = bd._read_jsondict('test1.json', requiredkeys=('a', 'c'))
            assert_equal(wd, rd)

    def test_readjsondictrequiredkeynotpresent(self):
        with tempdir() as dirname:
            bd = BaseDataDir(dirname)
            wd = {'a': 1, 'b': [1,2,3], 'c': 'k'}
            bd._write_jsondict('test1.json', wd)
            self.assertRaises(ValueError, bd._read_jsondict, 'test1.json',
                              requiredkeys=('a', 'd'))

    def test_readjsondictnotdict(self):
        with tempdir() as dirname:
            bd = BaseDataDir(dirname)
            wd = {'a': 1, 'b': [1, 2, 3], 'c': 'k'}
            bd._write_jsonfile('test1.json', [1,2,3])
            self.assertRaises(TypeError, bd._read_jsondict, 'test1.json')



if __name__ == '__main__':
    unittest.main()