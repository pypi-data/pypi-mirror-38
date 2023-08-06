import ee

import openet.interp


def lazy_property(fn):
    """Decorator that makes a property lazy-evaluated

    https://stevenloria.com/lazy-properties/
    """
    attr_name = '_lazy_' + fn.__name__

    @property
    def _lazy_property(self):
        if not hasattr(self, attr_name):
            setattr(self, attr_name, fn(self))
        return getattr(self, attr_name)
    return _lazy_property


# TODO: Make this into a Collection class
def collection(
        variable,
        collections,
        start_date,
        end_date,
        t_interval,
        geometry,
        **kwargs
    ):
    """Earth Engine based NDVI ET Image Collection

    Parameters
    ----------
    variable : str
        Variable to compute.
    collections : list
        GEE satellite image collection IDs.
    start_date : str
        ISO format inclusive start date (i.e. YYYY-MM-DD).
    end_date : str
        ISO format exclusive end date (i.e. YYYY-MM-DD).
    t_interval : {'daily', 'monthly', 'annual', 'overpass'}
        Time interval over which to interpolate and aggregate values.
        Selecting 'overpass' will return values only for the overpass dates.
    geometry : ee.Geometry
        The geometry object will be used to filter the input collections.
    kwargs : dict

    """

    # Should this be a global (or Collection class property)
    landsat_c1_toa_collections = [
        'LANDSAT/LC08/C01/T1_RT_TOA',
        'LANDSAT/LE07/C01/T1_RT_TOA',
        'LANDSAT/LC08/C01/T1_TOA',
        'LANDSAT/LE07/C01/T1_TOA',
        'LANDSAT/LT05/C01/T1_TOA',
    ]
    sentinel2_toa_collections = [
        'COPERNICUS/S2',
    ]

    # Test whether the requested variable is supported
    # Force variable to be lowercase for now
    variable = variable.lower()
    if variable.lower() not in dir(Image):
        raise ValueError('unsupported variable: {}'.format(variable))

    # Build the variable image collection
    variable_coll = ee.ImageCollection([])
    for coll_id in collections:
        if coll_id in landsat_c1_toa_collections:
            def compute(image):
                model_obj = Image.from_landsat_c1_toa(
                    toa_image=ee.Image(image))
                return ee.Image(getattr(model_obj, variable))
        elif coll_id in sentinel2_toa_collections:
            def compute(image):
                model_obj = Image.from_sentinel2_toa(
                    toa_image=ee.Image(image))
                return ee.Image(getattr(model_obj, variable))
        else:
            raise ValueError('unsupported collection: {}'.format(coll_id))

        var_coll = ee.ImageCollection(coll_id)\
            .filterDate(start_date, end_date)\
            .filterBounds(geometry)\
            .map(compute)

        # TODO: Apply additional filter parameters from kwargs
        #   (like CLOUD_COVER_LAND for Landsat)
        # .filterMetadata() \

        variable_coll = variable_coll.merge(var_coll)

    # Interpolate/aggregate to t_interval
    # TODO: Test whether the requested variable can/should be interpolated
    # TODO: Only load ET reference collection if interpolating ET
    # TODO: Get reference ET collection ID and band name from kwargs
    # TODO:   or accept an ee.ImageCollection directly
    # TODO: Get interp_days and interp_type from kwargs
    # TODO: Add aggregation functions to return other timesteps

    # Hardcoding to GRIDMET for now
    et_reference_coll = ee.ImageCollection('IDAHO_EPSCOR/GRIDMET')\
        .select(['etr'])\
        .filterDate(start_date, end_date)

    # Interpolate to a daily timestep
    interp_coll = openet.interp.daily_et(
        et_reference_coll, variable_coll, interp_days=32, interp_type='linear')

    # Return the daily collection
    return interp_coll


class Image():
    """GEE based model for computing ET fraction as a linear function of NDVI"""

    def __init__(
            self,
            image,
            m=1.25,
            b=0.0,
            **kwargs
            ):
        """Construct a generic NDVI based ET Image

        Parameters
        ----------
        image : ee.Image
            Must have bands: "ndvi"
        m : float, optional
            Slope (the default is 1.25).
        b : float, optional
            Offset (the default is 0.0).
        kwargs :

        Notes
        -----
        ETf = m * NDVI + b

        """
        input_image = ee.Image(image)
        self.ndvi = input_image.select(['ndvi'])
        self._m = m
        self._b = b

        # Copy system properties
        self._index = input_image.get('system:index')
        self._time_start = input_image.get('system:time_start')

    @lazy_property
    def etf(self):
        """Compute ETf"""
        etf = ee.Image(self.ndvi) \
            .multiply(self._m).add(self._b) \
            .setMulti({
                'system:index': self._index,
                'system:time_start': self._time_start})
        return ee.Image(etf).rename(['etf'])

    @classmethod
    def from_landsat_c1_toa(cls, toa_image, **kwargs):
        """Constructs an NDVI-ET Image instance from a Landsat TOA image

        Parameters
        ----------
        toa_image : ee.Image
            A raw Landsat Collection 1 TOA image.

        Returns
        -------
        Image

        """
        toa_image = ee.Image(toa_image)

        # Use the SPACECRAFT_ID property identify each Landsat type
        spacecraft_id = ee.String(toa_image.get('SPACECRAFT_ID'))

        # Rename bands to generic names
        input_bands = ee.Dictionary({
            'LANDSAT_5': ['B1', 'B2', 'B3', 'B4', 'B5', 'B7', 'B6', 'BQA'],
            'LANDSAT_7': ['B1', 'B2', 'B3', 'B4', 'B5', 'B7', 'B6_VCID_1', 'BQA'],
            'LANDSAT_8': ['B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B10', 'BQA'],
        })
        output_bands = ['blue', 'green', 'red', 'nir', 'swir1', 'swir2', 'lst',
                        'BQA']
        prep_image = toa_image.select(input_bands.get(spacecraft_id),
                                      output_bands)

        # Build the input image
        # Eventually send the BQA band or a cloud mask through also
        input_image = ee.Image([
            cls._ndvi(prep_image)
        ])

        # Apply the cloud mask and add properties
        input_image = input_image \
            .updateMask(openet.common.landsat_c1_toa_cloud_mask(toa_image)) \
            .setMulti({
                'system:index': toa_image.get('system:index'),
                'system:time_start': toa_image.get('system:time_start')
            })

        # Instantiate the class
        return cls(input_image, **kwargs)

    @classmethod
    def from_landsat_c1_sr(cls, sr_image, **kwargs):
        """Constructs an NDVI-ET Image instance from a Landsat SR image

        Parameters
        ----------
        sr_image : ee.Image
            A raw Landsat Collection 1 SR image.

        Returns
        -------
        Image

        """
        sr_image = ee.Image(sr_image)

        # Use the SATELLITE property identify each Landsat type
        spacecraft_id = ee.String(sr_image.get('SATELLITE'))

        # Rename bands to generic names
        input_bands = ee.Dictionary({
            'LANDSAT_5': ['B1', 'B2', 'B3', 'B4', 'B5', 'B7', 'B6', 'pixel_qa'],
            'LANDSAT_7': ['B1', 'B2', 'B3', 'B4', 'B5', 'B7', 'B6', 'pixel_qa'],
            'LANDSAT_8': ['B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B10', 'pixel_qa'],
        })
        output_bands = ['blue', 'green', 'red', 'nir', 'swir1', 'swir2', 'lst',
                        'pixel_qa']
        prep_image = sr_image.select(input_bands.get(spacecraft_id),
                                     output_bands)

        # Build the input image
        # Eventually send the BQA band or a cloud mask through also
        input_image = ee.Image([
            cls._ndvi(prep_image)
        ])

        # Apply the cloud mask and add properties
        input_image = input_image \
            .updateMask(openet.common.landsat_c1_sr_cloud_mask(sr_image)) \
            .setMulti({
                'system:index': sr_image.get('system:index'),
                'system:time_start': sr_image.get('system:time_start')
            })

        # Instantiate the class
        return cls(input_image, **kwargs)

    @classmethod
    def from_sentinel2_toa(cls, toa_image, **kwargs):
        """Constructs an NDVI-ET Image instance from a Sentinel 2 TOA image

        Parameters
        ----------
        toa_image : ee.Image
            A raw Sentinel 21 TOA image.

        Returns
        -------
        Image

        """
        toa_image = ee.Image(toa_image)

        # Don't distinguish between Sentinel-2 A and B for now
        # Rename bands to generic names
        # Scale bands to 0-1 (from 0-10000)
        input_bands = ['B2', 'B3', 'B4', 'B8', 'B11', 'B12', 'QA60']
        output_bands = ['blue', 'green', 'red', 'nir', 'swir1', 'swir2', 'QA60']
        prep_image = toa_image \
            .select(input_bands, output_bands) \
            .divide(10000.0)

        # Build the input image
        # Eventually send the BQA band or a cloud mask through also
        input_image = ee.Image([
            cls._ndvi(prep_image)
        ])

        # Apply the cloud mask and add properties
        input_image = input_image \
            .updateMask(openet.common.sentinel2_toa_cloud_mask(toa_image)) \
            .setMulti({
                'system:index': toa_image.get('system:index'),
                'system:time_start': toa_image.get('system:time_start')
            })

        # Instantiate the class
        return cls(input_image, **kwargs)

    @staticmethod
    def _ndvi(toa_image):
        """Compute NDVI

        Parameters
        ----------
        toa_image : ee.Image
            Renamed TOA image with 'nir' and 'red bands.

        Returns
        -------
        ee.Image

        """
        return ee.Image(toa_image).normalizedDifference(['nir', 'red']) \
            .rename(['ndvi'])
