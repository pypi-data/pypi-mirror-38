import ee

from . import tseb_utils
from . import utils


def tseb_pt(T_air, T_rad, u, p, z, Rs_1, Rs24, vza, zs,
            aleafv, aleafn, aleafl, adeadv, adeadn, adeadl,
            albedo, ndvi, lai, clump, hc, time, t_rise, t_end,
            leaf_width, a_PT_in=1.32, iterations=35):
    """Priestley-Taylor TSEB

    Calculates the Priestley Taylor TSEB fluxes using a single observation of
    composite radiometric temperature and using resistances in series.

    Parameters
    ----------
    T_air : ee.Image
        Air temperature (Kelvin).
    T_rad : ee.Image
        Radiometric composite temperature (Kelvin).
    u : ee.Image
        Wind speed above the canopy (m s-1).
    p : ee.Image
        Atmospheric pressure (kPa)
    z : ee.Image
        Elevation (m)
    Rs_1 : ee.Image
        Overpass insolation (w m-2)
    Rs24 : ee.Image
        Daily insolation (w m-2)
    vza : float
        View Zenith Angle (radians).
    zs : ee.Image
        Solar Zenith Angle (radians).
    aleafv : ee.Image

    aleafn : ee.Image

    aleafl : ee.Image

    adeadv : ee.Image

    adeadn : ee.Image

    adeadl : ee.Image

    albedo : ee.Image

    ndvi : ee.Image
        Normalized Difference Vegetation Index
    lai : ee.Image
        Effective Leaf Area Index (m2 m-2).
    clump : ee.Image

    hc : ee.Image
        Canopy height (m).
    time

    t_rise : ee.Image

    t_end : ee.Image

    leaf_width : ee.Image
        Average/effective leaf width (m)
    a_PT_in : float, optional
        Priestley Taylor coefficient for canopy potential transpiration
        (the default is 1.32).
    iterations: int, optional
        Number of iterations of main calculation
        (the default is 35)

    Returns
    -------
    ET : ee.Image
        Evapotranspiration (mm).

    References
    ----------
    .. [Norman1995] J.M. Norman, W.P. Kustas, & K.S. Humes (1995),
        Source approach for estimating soil and vegetation energy fluxes in
        observations of directional radiometric surface temperature,
        Agricultural and Forest Meteorology,
        Volume 77, Issues 3-4, Pages 263-293,
        http://dx.doi.org/10.1016/0168-1923(95)02265-Y.
    .. [Kustas1999] W.P. Kustas, & J.M. Norman (1999), Evaluation of soil
        and vegetation heat flux predictions using a simple two-source
        model with radiometric temperatures for partial canopy cover,
        Agricultural and Forest Meteorology, Volume 94, Issue 1, Pages 13-29,
        http://dx.doi.org/10.1016/S0168-1923(99)00005-2.
    """
    # print('\nINPUTS')
    # print('T_rad:    {:20.14f}'.format(float(utils.image_value(T_rad).values()[0])))
    # print('T_air:    {:20.14f}'.format(float(utils.image_value(T_air).values()[0])))
    # print('u:        {:20.14f}'.format(float(utils.image_value(u).values()[0])))
    # print('Rs_1:     {:20.14f}'.format(float(utils.image_value(Rs_1).values()[0])))
    # print('Rs24:     {:20.14f}'.format(float(utils.image_value(Rs24).values()[0])))
    # # print('vza:      {:20.14f}'.format(float(utils.image_value(vza).values()[0])))
    # print('zs:       {:20.14f}'.format(float(utils.image_value(zs).values()[0])))
    # print('albedo:   {:20.14f}'.format(float(utils.image_value(albedo).values()[0])))
    # print('ndvi:     {:20.14f}'.format(float(utils.image_value(ndvi).values()[0])))
    # print('lai:      {:20.14f}'.format(float(utils.image_value(lai).values()[0])))
    # print('clump:    {:20.14f}'.format(float(utils.image_value(clump).values()[0])))
    # print('hc:       {:20.14f}'.format(float(utils.image_value(hc).values()[0])))
    # print('time:     {:20.14f}'.format(float(utils.image_value(time).values()[0])))
    # print('t_rise:   {:20.14f}'.format(float(utils.image_value(t_rise).values()[0])))
    # print('t_end:    {:20.14f}'.format(float(utils.image_value(t_end).values()[0])))

    # ************************************************************************
    # Correct Clumping Factor
    f_green = 1.

    # LAI for leaf spherical distribution
    F = lai.expression('lai * clump', {'lai': lai, 'clump': clump})

    # Fraction cover at nadir (view=0)
    fc = F.expression('1.0 - exp(-0.5 * F)', {'F': F}) \
        .clamp(0.01, 0.9)

    # LAI relative to canopy projection only
    lai_c = lai.expression('lai / fc', {'lai': lai, 'fc': fc})

    # Houborg modification (according to Anderson et al. 2005)
    fc_q = lai \
        .expression('1 - (exp(-0.5 * F / cos(vza)))', {'F': F, 'vza': vza}) \
        .clamp(0.05, 0.90)

    # Brutsaert (1982)
    z0m = hc.expression('hc * 0.123', {'hc': hc})
    # CGM - add(0) is to mimic numpy copy, check if needed
    z0h = z0m.add(0)
    d_0 = hc.expression('hc * (2.0 / 3.0)', {'hc': hc})

    # Correction of roughness parameters for bare soils (F < 0.1)
    d_0 = d_0.where(F.lte(0.1), 0.00001)
    z0m = z0m.where(F.lte(0.1), 0.01)
    z0h = z0h.where(F.lte(0.1), 0.0001)

    # Correction of roughness parameters for water bodies
    # (NDVI < 0 and albedo < 0.05)
    water_mask = ndvi.lte(0).And(albedo.lte(0.05))
    d_0 = d_0.where(water_mask, 0.00001)
    z0m = z0m.where(water_mask, 0.00035)
    z0h = z0h.where(water_mask, 0.00035)

    # Check to avoid division by 0 in the next computations
    z0h = z0h.where(z0h.eq(0), 0.001)
    z0m = z0m.where(z0m.eq(0), 0.01)

    # DEADBEEF
    # z_u = ee.Number(50.0)
    # z_t = ee.Number(50.0)
    z_u = ee.Image.constant(50.0)
    z_t = ee.Image.constant(50.0)
    # z_u = lai.multiply(0).add(50)
    # z_t = lai.multiply(0).add(50)

    # Parameters for In-Canopy Wind Speed Extinction
    leaf = lai.expression(
        '(0.28 * (F ** (0.66667)) * (hc ** (0.33333)) * '
        '(leaf_width ** (-0.33333)))',
        {'F': F, 'hc': hc, 'leaf_width': leaf_width})
    leaf_c = lai.expression(
        '(0.28 * (lai_c ** (0.66667)) * (hc ** (0.33333)) * '
        '(leaf_width ** (-0.33333)))',
        {'lai_c': lai_c, 'hc': hc, 'leaf_width': leaf_width})
    leaf_s = lai.expression(
        '(0.28 * (0.1 ** (0.66667)) * (hc ** (0.33333)) * '
        '(leaf_width ** (-0.33333)))',
        {'hc': hc, 'leaf_width': leaf_width})

    # ************************************************************************
    # Atmospheric Parameters
    # Saturation vapour pressure [kPa] (FAO56 3-8)
    e_s = T_air.expression(
        '0.6108 * exp((17.27 * (T_air - 273.16)) / ((T_air - 273.16) + 237.3))',
        {'T_air': T_air})
    # Slope of the saturation vapor pressure [kPa] (FAO56 3-9)
    Ss = T_air.expression(
        '4098. * e_s / (((T_air - 273.16) + 237.3) ** 2)',
        {'e_s': e_s, 'T_air': T_air})
    # Latent heat of vaporization (~2.45 at 20 C) [MJ kg-1] (FAO56 3-1)
    lambda1 = T_air.expression(
        '(2.501 - (2.361e-3 * (T_air - 273.16)))',
        {'T_air': T_air})
    # Psychrometric constant [kPa C-1] (FAO56 3-10)
    g = p.expression('1.615E-3 * p / lambda1', {'p': p, 'lambda1': lambda1})

    # ************************************************************************
    # Initialization of
    a_PT = albedo.multiply(0).add(a_PT_in)
    # a_PT = ee.Image.constant(a_PT_in)
    # a_PT = mask.multiply(a_PT)

    # CGM - This was also being computed inside albedo_separation function below
    # Commented out from here for now.
    # e_atm = T_air.expression(
    #     '1.0 - (0.2811 * (exp(-0.0003523 * ((T_air - 273.16) ** 2))))',
    #     {'T_air': T_air})

    Rs_c, Rs_s, albedo_c, albedo_s = tseb_utils.albedo_separation(
        albedo, Rs_1, F, fc, aleafv, aleafn, aleafl, adeadv, adeadn, adeadl, zs)

    # CGM - Moved emissivity calculation to separate function.
    #   I removed the Rs0 check.
    e_atm = tseb_utils.emissivity(T_air)
    # p = T_air.expression(
    #     '101.3 * (((T_air - (0.0065 * z)) / T_air) ** 5.26)',
    #     {'T_air': T_air, 'z': z})
    # Density of air? (kg m-3)
    r_air = T_air.expression(
        '101.3 * (((T_air - (0.0065 * z)) / T_air) ** 5.26) / 1.01 / T_air / 0.287',
        {'T_air': T_air, 'z': z})
    cp = ee.Number(1004.16)
    # cp = ee.Image.constant(1004.16)

    # Assume neutral conditions on first iteration (use T_air for Ts and Tc)
    # CGM - Using lai for F to match Python code
    u_attr = tseb_utils.compute_u_attr(
        u=u, d0=d_0, z0m=z0m, z_u=z_u, fm=0)
    r_ah = tseb_utils.compute_r_ah(
        u_attr=u_attr, d0=d_0, z0h=z0h, z_t=z_t, fh=0)
    # CGM - Why is this function is passing "lai" to "F"?
    r_s = tseb_utils.compute_r_s(
        u_attr=u_attr, T_s=T_air, T_c=T_air, hc=hc, F=lai, d0=d_0, z0m=z0m,
        leaf=leaf, leaf_s=leaf_s, fm_h=0)
    r_x = tseb_utils.compute_r_x(
        u_attr=u_attr, hc=hc, F=lai, d0=d_0, z0m=z0m, xl=leaf_width,
        leaf_c=leaf_c, fm_h=0)
    # r_ah, r_s, r_x, u_attr = tseb_utils.compute_resistance(
    #     u, T_air, T_air, hc, lai, d_0, z0m, z0h, z_u, z_t, leaf_width, leaf,
    #     leaf_s, leaf_c, 0, 0, 0)

    T_c = T_air
    # DEADBEEF - In IDL, this calculation is in C, not K?
    T_s = lai.expression(
        '((T_rad - 273.16) - (fc_q * (T_c - 273.16))) / (1 - fc_q) + 273.16',
        {'T_rad': T_rad, 'T_c': T_c, 'fc_q': fc_q})
    # T_s = lai.expression(
    #     '(T_rad - (fc_q * T_c)) / (1 - fc_q)',
    #     {'T_rad': T_rad, 'T_c': T_c, 'fc_q': fc_q})

    # CGM - Initialize to match T_air shape
    # This doesn't seem to do anything, commenting out for now
    # H_iter = T_air.multiply(0).add(200.16)
    EF_s = T_air.multiply(0)

    # print('\nF:        {:20.14f}'.format(float(utils.image_value(F).values()[0])))
    # print('fc:       {:20.14f}'.format(float(utils.image_value(fc).values()[0])))
    # print('lai_c:    {:20.14f}'.format(float(utils.image_value(lai_c).values()[0])))
    # print('fc_q:     {:20.14f}'.format(float(utils.image_value(fc_q).values()[0])))
    # print('z0h:      {:20.14f}'.format(float(utils.image_value(z0h).values()[0])))
    # print('z0m:      {:20.14f}'.format(float(utils.image_value(z0m).values()[0])))
    # print('leaf:     {:20.14f}'.format(float(utils.image_value(leaf).values()[0])))
    # print('leaf_c:   {:20.14f}'.format(float(utils.image_value(leaf_c).values()[0])))
    # print('leaf_s:   {:20.14f}'.format(float(utils.image_value(leaf_s).values()[0])))
    # print('e_s:      {:20.14f}'.format(float(utils.image_value(e_s).values()[0])))
    # print('Ss:       {:20.14f}'.format(float(utils.image_value(Ss).values()[0])))
    # print('lambda1:  {:20.14f}'.format(float(utils.image_value(lambda1).values()[0])))
    # print('p:        {:20.14f}'.format(float(utils.image_value(p).values()[0])))
    # print('z:        {:20.14f}'.format(float(utils.image_value(z).values()[0])))
    # print('g:        {:20.14f}'.format(float(utils.image_value(g).values()[0])))
    # print('a_PT:     {:20.14f}'.format(float(utils.image_value(a_PT).values()[0])))
    # print('Rs_c:     {:20.14f}'.format(float(utils.image_value(Rs_c).values()[0])))
    # print('Rs_s:     {:20.14f}'.format(float(utils.image_value(Rs_s).values()[0])))
    # print('albedo_c: {:20.14f}'.format(float(utils.image_value(albedo_c).values()[0])))
    # print('albedo_s: {:20.14f}'.format(float(utils.image_value(albedo_s).values()[0])))
    # print('e_atm:    {:20.14f}'.format(float(utils.image_value(e_atm).values()[0])))
    # print('r_air:    {:20.14f}'.format(float(utils.image_value(r_air).values()[0])))
    # print('cp:       {:20.14f}'.format(float(cp.getInfo())))
    # print('d_0:      {:20.14f}'.format(float(utils.image_value(d_0).values()[0])))
    # print('z0m:      {:20.14f}'.format(float(utils.image_value(z0m).values()[0])))
    # print('z0h:      {:20.14f}'.format(float(utils.image_value(z0h).values()[0])))
    # print('u_attr:   {:20.14f}'.format(float(utils.image_value(u_attr).values()[0])))
    # print('r_ah:     {:20.14f}'.format(float(utils.image_value(r_ah).values()[0])))
    # print('r_s:      {:20.14f}'.format(float(utils.image_value(r_s).values()[0])))
    # print('r_x:      {:20.14f}'.format(float(utils.image_value(r_x).values()[0])))
    # print('T_c:      {:20.14f}'.format(float(utils.image_value(T_c).values()[0])))
    # print('T_s:      {:20.14f}'.format(float(utils.image_value(T_s).values()[0])))
    # print('EF_s:     {:20.14f}'.format(float(utils.image_value(EF_s).values()[0])))
    # print('Iterations: {}'.format(iterations))

    # ************************************************************************
    # Start Loop for Stability Correction and Water Stress
    def iter_func(n, prev):
        # Extract inputs from previous iteration
        a_PT_iter = ee.Image(ee.Dictionary(prev).get('a_PT'))
        EF_s_iter = ee.Image(ee.Dictionary(prev).get('EF_s'))
        r_ah_iter = ee.Image(ee.Dictionary(prev).get('r_ah'))
        r_s_iter = ee.Image(ee.Dictionary(prev).get('r_s'))
        r_x_iter = ee.Image(ee.Dictionary(prev).get('r_x'))
        T_c_iter = ee.Image(ee.Dictionary(prev).get('T_c'))
        T_s_iter = ee.Image(ee.Dictionary(prev).get('T_s'))
        u_attr_iter = ee.Image(ee.Dictionary(prev).get('u_attr'))

        Rn_c = tseb_utils.compute_Rn_c(
            albedo_c, T_air, T_c_iter, T_s_iter, e_atm, Rs_c, F)
        Rn_s = tseb_utils.compute_Rn_s(
            albedo_s, T_air, T_c_iter, T_s_iter, e_atm, Rs_s, F)
        Rn = Rn_c.add(Rn_s)
        # Rn_s, Rn_c, Rn = tseb_utils.compute_Rn(
        #     albedo_c, albedo_s, T_air, T_c_iter, T_s_iter, e_atm, Rs_c, Rs_s, F)

        G = tseb_utils.compute_G0(
            Rn, Rn_s, albedo, ndvi, t_rise, t_end, time, EF_s_iter)

        LE_c = albedo \
            .expression(
                'f_green * (a_PT * Ss / (Ss + g)) * Rn_c',
                {'f_green': f_green, 'a_PT': a_PT_iter, 'Ss': Ss, 'g': g,
                 'Rn_c': Rn_c}) \
            .max(0)
        H_c = albedo.expression(
            'Rn_c - LE_c', {'Rn_c': Rn_c, 'LE_c': LE_c})

        T_c_iter = tseb_utils.temp_separation_tc(
            H_c, fc_q, T_air, T_rad, r_ah_iter, r_s_iter, r_x_iter, r_air, cp)
        T_s_iter = tseb_utils.temp_separation_ts(T_c_iter, fc_q, T_air, T_rad)
        T_ac = tseb_utils.temp_separation_tac(
            T_c_iter, T_s_iter, fc_q, T_air, r_ah_iter, r_s_iter, r_x_iter)
        # T_c_iter, T_s_iter, T_ac = tseb_utils.temp_separation(
        #     H_c, fc_q, T_air, T_rad, r_ah_iter, r_s_iter, r_x_iter, r_air, cp)

        H_s = albedo.expression(
            'r_air * cp * (T_s - T_ac) / r_s',
            {'r_air': r_air, 'cp': cp, 'T_s': T_s_iter, 'T_ac': T_ac, 'r_s': r_s_iter})
        H_c = albedo.expression(
            'r_air * cp * (T_c - T_ac) / r_x',
            {'r_air': r_air, 'cp': cp, 'T_c': T_c_iter, 'T_ac': T_ac, 'r_x': r_x_iter})
        H = albedo.expression('H_s + H_c', {'H_s': H_s, 'H_c': H_c})

        LE_s = albedo.expression(
            'Rn_s - G - H_s', {'Rn_s': Rn_s, 'G': G, 'H_s': H_s})
        LE_c = albedo.expression('Rn_c - H_c', {'Rn_c': Rn_c, 'H_c': H_c})

        # CGM - Is there a reason this isn't up with the H calculation?
        H = H.where(H.eq(0), 10.0)

        # CGM - This wont doing anything at this position in the code.
        #   Commenting out for now.
        # r_ah_iter = r_ah_iter.where(r_ah_iter.eq(0), 10.0)

        # CGM - This doesn't seem to do anything, commenting out for now
        # mask_iter = H_iter.divide(H).lte(1.05).And(H_iter.divide(H).gte(0.95))
        # chk_iter = np.sum(mask_iter) / np.size(mask_iter)

        fh = tseb_utils.compute_stability_fh(
            H, T_rad, u_attr_iter, r_air, z_t, d_0, cp)
        fm = tseb_utils.compute_stability_fm(
            H, T_rad, u_attr_iter, r_air, z_u, d_0, z0m, cp)
        fm_h = tseb_utils.compute_stability_fm_h(
            H, T_rad, u_attr_iter, r_air, hc, d_0, z0m, cp)
        # CGM - z0h is not used in this function, should it be?
        # fm, fh, fm_h = tseb_utils.compute_stability(
        #     H, T_rad, r_air, cp, u_attr, z_u, z_t, hc, d_0, z0m, z0h)

        u_attr_iter = tseb_utils.compute_u_attr(
            u=u, d0=d_0, z0m=z0m, z_u=z_u, fm=fm)
        r_ah_iter = tseb_utils.compute_r_ah(
            u_attr=u_attr_iter, d0=d_0, z0h=z0h, z_t=z_t, fh=fh)
        r_s_iter = tseb_utils.compute_r_s(
            u_attr=u_attr_iter, T_s=T_s_iter, T_c=T_c_iter, hc=hc, F=lai,
            d0=d_0, z0m=z0m, leaf=leaf, leaf_s=leaf_s, fm_h=fm_h)
        # CGM - Why is this function is passing "lai" to "F"?
        r_x_iter = tseb_utils.compute_r_x(
            u_attr=u_attr_iter, hc=hc, F=lai, d0=d_0, z0m=z0m, xl=leaf_width,
            leaf_c=leaf_c, fm_h=fm_h)
        # r_ah_iter, r_s_iter, r_x_iter, u_attr_iter = tseb_utils.compute_resistance(
        #     u, T_s_iter, T_c_iter, hc, lai, d_0, z0m, z0h, z_u, z_t,
        #     leaf_width, leaf, leaf_s, leaf_c, fm, fh, fm_h)

        a_PT_iter = a_PT_iter \
            .where(LE_s.lte(0), a_PT_iter.subtract(0.05)) \
            .where(a_PT_iter.lte(0), 0.01)

        den_s = albedo.expression('Rn_s - G', {'Rn_s': Rn_s, 'G': G})
        den_s = den_s.updateMask(den_s.neq(0))
        # den_s[den_s == 0.] = np.nan

        EF_s_iter = albedo.expression(
            'LE_s / den_s', {'LE_s': LE_s, 'den_s': den_s})

        return ee.Dictionary({
            'a_PT': a_PT_iter, 'EF_s': EF_s_iter, 'G': G,
            'H_c': H_c, 'H_s': H_s, 'LE_c': LE_c, 'LE_s': LE_s,
            'Rn_c': Rn_c, 'Rn_s': Rn_s,
            'r_ah': r_ah_iter, 'r_s': r_s_iter, 'r_x': r_x_iter,
            'T_ac': T_ac, 'T_c': T_c_iter, 'T_s': T_s_iter,
            'u_attr': u_attr_iter})

    # Iterate the function n times
    # CGM - Iteration count is an input to the function
    input_images = ee.Dictionary({
        'a_PT': a_PT, 'EF_s': EF_s, 'G': ee.Image(0),
        'H_c': ee.Image(0), 'H_s': ee.Image(0),
        'LE_c': ee.Image(0), 'LE_s': ee.Image(0),
        'Rn_c': ee.Image(0), 'Rn_s': ee.Image(0),
        'r_ah': r_ah, 'r_s': r_s, 'r_x': r_x,
        'T_ac': ee.Image(0), 'T_c': T_c, 'T_s': T_s, 'u_attr': u_attr
    })
    iter_output = ee.Dictionary(
        ee.List.sequence(1, iterations).iterate(iter_func, input_images))

    # Unpack the iteration output
    a_PT = ee.Image(iter_output.get('a_PT'))
    Rn_c = ee.Image(iter_output.get('Rn_c'))
    Rn_s = ee.Image(iter_output.get('Rn_s'))
    G = ee.Image(iter_output.get('G'))
    H_c = ee.Image(iter_output.get('H_c'))
    H_s = ee.Image(iter_output.get('H_s'))
    LE_c = ee.Image(iter_output.get('LE_c'))
    LE_s = ee.Image(iter_output.get('LE_s'))
    # T_ac = ee.Image(iter_output.get('T_ac'))
    # T_c = ee.Image(iter_output.get('T_c'))
    # T_s = ee.Image(iter_output.get('T_s'))
    # r_ah = ee.Image(iter_output.get('r_ah'))
    # r_s = ee.Image(iter_output.get('r_s'))
    # r_x = ee.Image(iter_output.get('r_x'))

    # print('\na_PT:     {:20.14f}'.format(utils.image_value(a_PT).values()[0]))
    # print('Rn_c:     {:20.14f}'.format(utils.image_value(Rn_c).values()[0]))
    # print('Rn_s:     {:20.14f}'.format(utils.image_value(Rn_s).values()[0]))
    # print('G:        {:20.14f}'.format(utils.image_value(G).values()[0]))
    # print('H_c:      {:20.14f}'.format(utils.image_value(H_c).values()[0]))
    # print('H_s:      {:20.14f}'.format(utils.image_value(H_s).values()[0]))
    # print('LE_c:     {:20.14f}'.format(utils.image_value(LE_c).values()[0]))
    # print('LE_s:     {:20.14f}'.format(utils.image_value(LE_s).values()[0]))
    # print('r_ah:     {:20.14f}'.format(utils.image_value(r_ah).values()[0]))
    # print('r_s:      {:20.14f}'.format(utils.image_value(r_s).values()[0]))
    # print('r_x:      {:20.14f}'.format(utils.image_value(r_x).values()[0]))
    # print('T_ac:     {:20.14f}'.format(utils.image_value(T_ac).values()[0]))
    # print('T_c:      {:20.14f}'.format(utils.image_value(T_c).values()[0]))
    # print('T_s:      {:20.14f}'.format(utils.image_value(T_s).values()[0]))

    # ************************************************************************
    # Check Energy Balance Closure
    ind = a_PT.lte(0.01)
    LE_s = LE_s.where(ind, 1.0)
    LE_c = LE_c.where(ind, 1.0)
    G = G.where(ind, Rn_s.subtract(H_s))

    ind = LE_s.gt(Rn_s)
    LE_s = LE_s.where(ind,  Rn_s)
    H_s = H_s.where(ind,  Rn_s.subtract(G).subtract(LE_s))

    # CGM - Check order of operations
    ind = LE_c.gt(Rn_c.add(100))
    # CGM - Not used below since LE_c is recomputed
    LE_c = LE_c.where(ind, Rn_c.add(100))
    H_c = H_c.where(ind, -100)

    LE_s = albedo.expression(
        'Rn_s - G - H_s', {'Rn_s': Rn_s, 'G': G, 'H_s': H_s})
    LE_c = albedo.expression('Rn_c - H_c', {'Rn_c': Rn_c, 'H_c': H_c})

    # The latent heat of vaporization is 2.45 MJ kg-1
    # Assume Rs24 is still in W m-2 day-1 and convert to MJ kg-1
    # CGM - Leaving out scaling value for now
    ET = albedo \
        .expression(
            '((LE_c + LE_s) / Rs_1) * (Rs24 / 2.45) * scaling',
            {'LE_c': LE_c, 'LE_s': LE_s, 'Rs_1': Rs_1,
             'Rs24': Rs24.multiply(0.0864 / 24.0),
             'scaling': 1}) \
        .max(0.01)

    # print('\nRn_c:     {:20.14f}'.format(utils.image_value(Rn_c).values()[0]))
    # print('Rn_s:     {:20.14f}'.format(utils.image_value(Rn_s).values()[0]))
    # print('G:        {:20.14f}'.format(utils.image_value(G).values()[0]))
    # print('H_c:      {:20.14f}'.format(utils.image_value(H_c).values()[0]))
    # print('H_s:      {:20.14f}'.format(utils.image_value(H_s).values()[0]))
    # print('LE_c:     {:20.14f}'.format(utils.image_value(LE_c).values()[0]))
    # print('LE_s:     {:20.14f}'.format(utils.image_value(LE_s).values()[0]))
    # print('\nET:       {:20.14f}'.format(utils.image_value(ET).values()[0]))
    return ET
