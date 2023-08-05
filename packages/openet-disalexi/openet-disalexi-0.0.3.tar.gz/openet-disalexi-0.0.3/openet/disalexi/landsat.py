import ee


class Landsat(object):
    """"""
    def __init__(self, toa_image):
        """Initialize a Landsat Collection 1 image

        Parameters
        ----------
        toa_image : ee.Image
            Landsat 5/7/8 Collection 1 TOA image
            (i.e. from the "LANDSAT/X/C01/T1_TOA" collection)

        """
        self.toa_image = toa_image

        # Use the SPACECRAFT_ID property identify each Landsat type
        self.spacecraft_id = ee.String(self.toa_image.get('SPACECRAFT_ID'))

        # Rename bands to generic names
        input_bands = ee.Dictionary({
            'LANDSAT_5': ['B1', 'B2', 'B3', 'B4', 'B5', 'B7', 'B6', 'BQA'],
            'LANDSAT_7': ['B1', 'B2', 'B3', 'B4', 'B5', 'B7', 'B6_VCID_1', 'BQA'],
            'LANDSAT_8': ['B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B10', 'BQA']})
        output_bands = [
            'blue', 'green', 'red', 'nir', 'swir1', 'swir2', 'lst', 'bqa']

        # Rename thermal band "k" coefficients to generic names
        input_k1 = ee.Dictionary({
            'LANDSAT_5': 'K1_CONSTANT_BAND_6',
            'LANDSAT_7': 'K1_CONSTANT_BAND_6_VCID_1',
            'LANDSAT_8': 'K1_CONSTANT_BAND_10'})
        input_k2 = ee.Dictionary({
            'LANDSAT_5': 'K2_CONSTANT_BAND_6',
            'LANDSAT_7': 'K2_CONSTANT_BAND_6_VCID_1',
            'LANDSAT_8': 'K2_CONSTANT_BAND_10'})
        output_k1 = self.toa_image.get(input_k1.get(self.spacecraft_id))
        output_k2 = self.toa_image.get(input_k2.get(self.spacecraft_id))

        self.input_image = ee.Image(self.toa_image) \
            .select(input_bands.get(self.spacecraft_id), output_bands) \
            .set('k1_constant', ee.Number(output_k1)) \
            .set('k2_constant', ee.Number(output_k2))

    def prep(self):
        """Return an image with the bands/products needed to run EE DisALEXI

        Parameters
        ----------
        self.toa_image : ee.Image

        Returns
        -------
        prep_image : ee.Image

        """
        self.prep_image = ee.Image([
            self._get_albedo(),
            self._get_bqa_cfmask(),
            self._get_lai(),
            self._get_lst(),
            # self.input_image.select(['lst']),
            self._get_ndvi()])
        self.prep_image = ee.Image(self.prep_image.setMulti({
            'SCENE_ID': self.toa_image.get('system:index'),
            'system:time_start': self.toa_image.get('system:time_start')}))
        return self.prep_image

        # The cloud mask could be applied here
        # mask_img = self.prep_image.select('cfmask').eq(0)
        # return self.prep_image.updateMask(mask_img)

    def _get_albedo(self):
        """Compute total shortwave broadband albedo following [Liang2001]

        The Python code had the following line and comment:
            "bands = [1, 3, 4, 5, 7]  # dont use blue"
        IDL code and [Liang2001] indicate that the green band is not used.
        Coefficients were derived for Landsat 7 ETM+, but were found to be
            "suitable" to Landsat 4/5 TM also.

        Parameters
        ----------
        self.input_image : ee.Image

        Returns
        -------
        albedo : ee.Image

        References
        ----------
        .. [Liang2001] Shunlin Liang (2001),
            Narrowband to broadband conversions of land surface albedo -
            I Algorithms, Remote Sensing of Environment,
            Volume 76, Issue2, Pages 213-238,
            http://doi.org/10.1016/S0034-4257(00)00205-4
        """
        bands = ['blue', 'red', 'nir', 'swir1', 'swir2']
        coef = [0.356, 0.130, 0.373, 0.085, 0.072]
        return ee.Image(self.input_image).select(bands) \
            .multiply(coef) \
            .reduce(ee.Reducer.sum()) \
            .subtract(0.0018) \
            .rename(['albedo'])

    def _get_bqa_cfmask(self):
        """Extract CFmask from Landsat Collection 1 BQA band

        https://landsat.usgs.gov/collectionqualityband

        Confidence values
        00 = "Not Determined" = Algorithm did not determine the status of this condition
        01 = "No" = Algorithm has low to no confidence that this condition exists
            (0-33 percent confidence)
        10 = "Maybe" = Algorithm has medium confidence that this condition exists
            (34-66 percent confidence)
        11 = "Yes" = Algorithm has high confidence that this condition exists
            (67-100 percent confidence


        Parameters
        ----------
        self.input_image : ee.Image

        Returns
        -------
        cfmask : ee.Image

        """
        bqa_image = self.input_image.select(['bqa'])

        def getQABits(bqa_image, start, end, newName):
            """
            From Tyler's function
            https://ee-api.appspot.com/#97ab9a8f694b28128a5a5ca2e2df7841
            """
            pattern = 0
            for i in range(start, end + 1):
                pattern += int(2 ** i)
            return bqa_image.select([0], [newName]) \
                .bitwise_and(pattern).right_shift(start)

        # Extract the various masks from the QA band
        fill_mask = getQABits(bqa_image, 0, 0, 'designated_fill')
        # drop_mask = getQABits(bqa_image, 1, 1, 'dropped_pixel')
        # Landsat 8 only
        # terrain_mask = getQABits(bqa_image, 1, 1, 'terrain_occlusion')
        # saturation_mask = getQABits(
        #     bqa_image, 2, 3, 'saturation_confidence').gte(2)
        # cloud_mask = getQABits(bqa_image, 4, 4, 'cloud')
        cloud_mask = getQABits(bqa_image, 5, 6, 'cloud_confidence').gte(2)
        shadow_mask = getQABits(bqa_image, 7, 8, 'shadow_confidence').gte(3)
        snow_mask = getQABits(bqa_image, 9, 10, 'snow_confidence').gte(3)
        # Landsat 8 only
        # cirrus_mask = getQABits(bqa_image, 11, 12, 'cirrus_confidence').gte(3)

        # Convert masks to old style Fmask values
        # 0 - Clear land
        # 1 - Clear water
        # 2 - Cloud shadow
        # 3 - Snow
        # 4 - Cloud
        return fill_mask \
            .add(shadow_mask.multiply(2)) \
            .add(snow_mask.multiply(3)) \
            .add(cloud_mask.multiply(4)) \
            .rename(['cfmask'])

    def _get_lai(self):
        """Compute LAI using METRIC NDVI / LAI empirical equation

        Parameters
        ----------
        self.input_image : ee.Image

        Returns
        -------
        lai : ee.Image

        """
        ndvi = self.input_image.normalizedDifference(['nir', 'red']) \
            .rename(['lai'])
        return ndvi.pow(3).multiply(7.0).clamp(0, 6)

    def _emissivity(self):
        """METRIC narrowband emissivity"""
        lai = self._get_lai()
        ndvi = self._get_ndvi()
        # Initial values are for NDVI > 0 and LAI <= 3
        return lai.divide(300).add(0.97) \
            .where(ndvi.lte(0), 0.99) \
            .where(ndvi.gt(0).And(lai.gt(3)), 0.98)

    def _get_lst(self):
        """Compute emissivity corrected land surface temperature (LST)
        from brightness temperature.

        Note, the coefficients were derived from a small number of scenes in
        southern Idaho [Allen2007] and may not be appropriate for other areas.

        Parameters
        ----------
        self.input_image : ee.Image

        Returns
        -------
        lst : ee.Image

        References
        ----------
        .. [ALlen2007a] R. Allen, M. Tasumi, R. Trezza (2007),
            Satellite-Based Energy Balance for Mapping Evapotranspiration with
            Internalized Calibration (METRIC) Model,
            Journal of Irrigation and Drainage Engineering, Vol 133(4),
            http://dx.doi.org/10.1061/(ASCE)0733-9437(2007)133:4(380)

        """
        # Get properties from image
        k1 = ee.Number(self.input_image.get('k1_constant'))
        k2 = ee.Number(self.input_image.get('k2_constant'))

        ts_brightness = self.input_image.select(['lst'])
        emissivity = self._emissivity()

        # First back out radiance from brightness temperature
        # Then recalculate emissivity corrected Ts
        thermal_rad_toa = ts_brightness.expression(
            'k1 / (exp(k2 / ts_brightness) - 1)',
            {'ts_brightness': ts_brightness, 'k1': k1, 'k2': k2})

        # tnb = 0.866   # narrow band transmissivity of air
        # rp = 0.91     # path radiance
        # rsky = 1.32   # narrow band clear sky downward thermal radiation
        rc = thermal_rad_toa.expression(
            '((thermal_rad_toa - rp) / tnb) - ((1. - emiss) * rsky)',
            {
                'thermal_rad_toa': thermal_rad_toa,
                'emiss': emissivity,
                'rp': 0.91, 'tnb': 0.866, 'rsky': 1.32})
        lst = rc.expression(
            'k2 / log(emiss * k1 / rc + 1)',
            {'emiss': emissivity, 'rc': rc, 'k1': k1, 'k2': k2})

        return lst.rename(['lst'])

    def _get_ndvi(self):
        """Compute NDVI

        Parameters
        ----------
        self.input_image : ee.Image

        Returns
        -------
        ndvi : ee.Image

        """
        return self.input_image.normalizedDifference(['nir', 'red']) \
            .rename(['ndvi'])
