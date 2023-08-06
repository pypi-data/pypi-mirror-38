import datetime
import logging

import ee
import pytest

import openet.ndvi as ndvi_et
import openet.ndvi.utils as utils


SCENE_ID = 'LC08_042035_20150713'
SCENE_DT = datetime.datetime.strptime(SCENE_ID[-8:], '%Y%m%d')
SCENE_DATE = SCENE_DT.strftime('%Y-%m-%d')
SCENE_DOY = int(SCENE_DT.strftime('%j'))


# Should these be test fixtures instead?
# I'm not sure how to make them fixtures and allow input parameters
def toa_image(red=0.2, nir=0.7, bt=300):
    """Construct a fake Landsat 8 TOA image with renamed bands"""
    return ee.Image.constant([red, nir, bt])\
        .rename(['red', 'nir', 'lst']) \
        .setMulti({
            'system:time_start': ee.Date(SCENE_DATE).millis(),
            'k1_constant': ee.Number(607.76),
            'k2_constant': ee.Number(1260.56)})


def default_image(ndvi=0.8):
    # First construct a fake 'prepped' input image
    return ee.Image.constant([ndvi]).rename(['ndvi']) \
        .setMulti({
            'system:index': SCENE_ID,
            'system:time_start': ee.Date(SCENE_DATE).millis(),
    })


def test_ee_init():
    """Check that Earth Engine was initialized"""
    assert ee.Number(1).getInfo() == 1


def test_Image_default_parameters():
    n = ndvi_et.Image(default_image())
    assert n._m == 1.25
    assert n._b == 0


# Todo: Break these up into separate functions?
def test_Image_calculated_properties():
    n = ndvi_et.Image(default_image())
    assert n._time_start.getInfo() == ee.Date(SCENE_DATE).millis().getInfo()
    # assert n._scene_id.getInfo() == SCENE_ID
    # assert n._wrs2_tile.getInfo() == 'p{}r{}'.format(
    #     SCENE_ID.split('_')[1][:3], SCENE_ID.split('_')[1][3:])


# def test_Image_date_properties():
#     n = ndvi_et.Image(default_image())
#     assert n._date.getInfo()['value'] == utils.millis(SCENE_DT)
#     assert n._year.getInfo() == int(SCENE_DATE.split('-')[0])
#     assert n._month.getInfo() == int(SCENE_DATE.split('-')[1])
#     assert n._start_date.getInfo()['value'] == utils.millis(SCENE_DT)
#     assert n._end_date.getInfo()['value'] == utils.millis(
#         SCENE_DT + datetime.timedelta(days=1))
#     assert n._doy.getInfo() == SCENE_DOY


# def test_Image_scene_id_property():
#     """Test that the system:index from a merged collection is parsed"""
#     input_img = default_image()
#     n = ndvi_et.Image(input_img.set('system:index', '1_2_' + SCENE_ID))
#     assert n._scene_id.getInfo() == SCENE_ID


# Test the static methods of the class first
# Do these need to be inside the TestClass?
@pytest.mark.parametrize(
    'red, nir, expected',
    [
        [0.2, 9.0 / 55, -0.1],
        [0.2, 0.2,  0.0],
        [0.1, 11.0 / 90,  0.1],
        [0.2, 0.3, 0.2],
        [0.1, 13.0 / 70, 0.3],
        [0.3, 0.7, 0.4],
        [0.2, 0.6, 0.5],
        [0.2, 0.8, 0.6],
        [0.1, 17.0 / 30, 0.7],
    ]
)
def test_Image_ndvi_calculation(red, nir, expected, tol=0.000001):
    toa = toa_image(red=red, nir=nir)
    output = utils.constant_image_value(ndvi_et.Image._ndvi(toa))
    # logging.debug('\n  Target values: {}'.format(expected))
    # logging.debug('  Output values: {}'.format(output))
    assert abs(output - expected) <= tol


def test_Image_ndvi_band_name():
    output = ndvi_et.Image._ndvi(toa_image()).getInfo()['bands'][0]['id']
    assert output == 'ndvi'


@pytest.mark.parametrize(
    # Todo: Test defaults by passing None
    'ndvi, m, b, expected',
    [
        [0.8, 1.25, 0, 1.0],
        [0.8, 1.0, 0, 0.8],
        [0.8, 1.0, 0.2, 1.0],
        [0.0, 1.25, 0, 0.0],
        [0.8, None, None, 1.0],
    ]
)
def test_Image_etf(ndvi, m, b, expected, tol=0.0001):
    input_args = {'image': default_image(ndvi=ndvi)}
    if m is not None:
        input_args['m'] = m
    if b is not None:
        input_args['b'] = b
    output_img = ndvi_et.Image(**input_args).etf
    output = utils.constant_image_value(ee.Image(output_img))

    # For some ETf tests, returning None is the correct result
    if output is None and expected is None:
        assert True
    else:
        assert abs(output - expected) <= tol


def test_Image_etf_band_name():
    output = ndvi_et.Image(default_image()).etf.getInfo()['bands'][0]['id']
    assert output == 'etf'


def test_Image_etf_properties(tol=0.0001):
    """Test if properties are set on the ETf image"""
    etf_img = ndvi_et.Image(default_image()).etf
    output = etf_img.getInfo()['properties']
    assert output['system:index'] == SCENE_ID
    assert output['system:time_start'] == ee.Date(SCENE_DATE).millis().getInfo()


# How should these @classmethods be tested?
def test_Image_from_landsat_c1_toa_default_image():
    """Test that the classmethod is returning a class object"""
    output = ndvi_et.Image.from_landsat_c1_toa(toa_image())
    assert type(output) == type(ndvi_et.Image(default_image()))


@pytest.mark.parametrize(
    'image_id',
    [
        'LANDSAT/LC08/C01/T1_RT_TOA/LC08_044033_20170716',
        'LANDSAT/LC08/C01/T1_TOA/LC08_044033_20170716',
        'LANDSAT/LE07/C01/T1_RT_TOA/LE07_044033_20170708',
        'LANDSAT/LE07/C01/T1_TOA/LE07_044033_20170708',
        'LANDSAT/LT05/C01/T1_TOA/LT05_044033_20110716',
    ]
)
def test_Image_from_landsat_c1_toa_landsat_image(image_id):
    """Test instantiating the class from a real Landsat images"""
    output = ndvi_et.Image.from_landsat_c1_toa(ee.Image(image_id)).ndvi.getInfo()
    assert output['properties']['system:index'] == image_id.split('/')[-1]


def test_Image_from_landsat_c1_toa_exception():
    """Test instantiating the class for an invalid image ID"""
    with pytest.raises(Exception):
        ndvi_et.Image.from_landsat_c1_toa(ee.Image('DEADBEEF'))._index.getInfo()


def test_Image_from_landsat_c1_sr_default_image():
    """Test that the classmethod is returning a class object"""
    output = ndvi_et.Image.from_landsat_c1_sr(toa_image())
    assert type(output) == type(ndvi_et.Image(default_image()))


@pytest.mark.parametrize(
    'image_id',
    [
        # 'LANDSAT/LC08/C01/T1_RT_SR/LC08_044033_20170716',
        'LANDSAT/LC08/C01/T1_SR/LC08_044033_20170716',
        # 'LANDSAT/LE07/C01/T1_RT_SR/LE07_044033_20170708',
        'LANDSAT/LE07/C01/T1_SR/LE07_044033_20170708',
        'LANDSAT/LT05/C01/T1_SR/LT05_044033_20110716',
    ]
)
def test_Image_from_landsat_c1_sr_landsat_image(image_id):
    """Test instantiating the class from a real Landsat images"""
    output = ndvi_et.Image.from_landsat_c1_sr(ee.Image(image_id)).ndvi.getInfo()
    assert output['properties']['system:index'] == image_id.split('/')[-1]


def test_Image_from_landsat_c1_sr_exception():
    """Test instantiating the class for an invalid image ID"""
    with pytest.raises(Exception):
        ndvi_et.Image.from_landsat_c1_sr(ee.Image('DEADBEEF'))._index.getInfo()


def test_Image_from_sentinel2_toa_default_image():
    """Test that the classmethod is returning a class object"""
    output = ndvi_et.Image.from_sentinel2_toa(toa_image())
    assert type(output) == type(ndvi_et.Image(default_image()))


@pytest.mark.parametrize(
    'image_id',
    [
        'COPERNICUS/S2/20170510T184921_20170510T185915_T10SFJ',
    ]
)
def test_Image_from_sentinel2_toa_sentinel_image(image_id):
    """Test instantiating the class from a real Landsat images"""
    output = ndvi_et.Image.from_sentinel2_toa(ee.Image(image_id)).ndvi.getInfo()
    assert output['properties']['system:index'] == image_id.split('/')[-1]


def test_Image_from_sentinel2_toa_exception():
    """Test instantiating the class for an invalid image ID"""
    with pytest.raises(Exception):
        ndvi_et.Image.from_sentinel2_toa(ee.Image('DEADBEEF'))._index.getInfo()