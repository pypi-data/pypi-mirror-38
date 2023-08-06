from nd.io.convert_ import assemble_complex, disassemble_complex
from nd.testing import generate_test_dataset
from xarray.testing import assert_identical as xr_assert_identical
from xarray.testing import assert_equal as xr_assert_equal
from numpy.testing import assert_equal
import numpy as np


def test_disassemble_complex():
    # Create complex dataset
    ds = generate_test_dataset(var=['b', 'c'])
    dims = tuple(ds.dims.keys())
    shape = tuple(ds.dims.values())
    complex_data = np.random.rand(*shape) + 1j * np.random.rand(*shape)
    ds['a'] = (dims, complex_data)
    # Check that disassembling into reals works as expected
    ds_real = disassemble_complex(ds)
    assert_equal(set(ds_real.data_vars), {'a__re', 'a__im', 'b', 'c'})
    xr_assert_equal(ds['a'].real, ds_real['a__re'])
    xr_assert_equal(ds['a'].imag, ds_real['a__im'])


def test_assemble_complex():
    # Create real dataset with real and imag part
    ds = generate_test_dataset(var=['a__im', 'a__re', 'b', 'c'])
    # Check that assembling into complex works
    ds_complex = assemble_complex(ds)
    assert_equal(set(ds_complex.data_vars), {'a', 'b', 'c'})
    xr_assert_equal(ds_complex['a'].real, ds['a__re'])
    xr_assert_equal(ds_complex['a'].imag, ds['a__im'])


def test_assemble_and_dissassemble_complex():
    ds_orig = generate_test_dataset(var=['a__im', 'a__re', 'b', 'c'])
    ds_complex = assemble_complex(ds_orig)
    ds_real = disassemble_complex(ds_complex)
    xr_assert_identical(ds_orig, ds_real)


def test_add_time():
    pass


def test_dualpol_to_complex():
    pass


def test_generate_covariance_matrix():
    pass


def test_compact_to_complex():
    pass
