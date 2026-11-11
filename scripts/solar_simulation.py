import math


def calculate_solar_irradiance(
        latitude=52.8,
        longitude=-1.2,
        day_of_year=172,
        local_time=12,
        panel_tilt=0,
        panel_azimuth=0,
        ground_reflectance=0.2,
        daylight_saving=None
):
    """
    Calculate clear-sky solar irradiance incident on a PV panel.

    Returns irradiance components in W/m².

    Azimuth convention:
        0° = South
        Negative = East
        Positive = West
    """

    rad = math.radians
    deg = math.degrees

    # 1. Time correction
    B = rad(360 * (day_of_year - 81) / 364)

    equation_of_time = (
            9.87 * math.sin(2 * B)
            - 7.53 * math.cos(B)
            - 1.5 * math.sin(B)
    )

    # Original workbook uses UTC meridian (0°)
    time_correction = 4 * longitude + equation_of_time

    # Account for daylight saving time
    if daylight_saving is None:
        daylight_saving = 87 <= day_of_year < 304

    #local_time = hour + minute / 60
    standard_time = local_time - int(daylight_saving)

    solar_time = standard_time + time_correction / 60
    hour_angle = rad(15 * (12 - solar_time))

    # 2. Solar declination
    delta = rad(
        23.45 * math.sin(
            rad(360 * (284 + day_of_year) / 365.25)
        )
    )

    phi = rad(latitude)

    # 3. Solar altitude angle
    sin_altitude = (
            math.sin(phi) * math.sin(delta)
            + math.cos(phi) * math.cos(delta) * math.cos(hour_angle)
    )

    altitude = math.asin(max(-1, min(1, sin_altitude)))

    # No solar radiation when the sun is below the horizon
    if altitude <= 0:
        """
        return {
            "beam_horizontal": 0.0,
            "direct_panel": 0.0,
            "diffuse_panel": 0.0,
            "reflected_panel": 0.0,
            "total": 0.0
        }
        """
        return 0.0

    # 4. Solar azimuth
    sin_azimuth = (
            math.cos(delta) * math.sin(hour_angle)
            / math.cos(altitude)
    )

    azimuth = math.asin(max(-1, min(1, sin_azimuth)))

    # Correct the azimuth quadrant (same logic as Excel)
    if math.cos(hour_angle) < math.tan(delta) / math.tan(phi):
        if azimuth > 0:
            azimuth = math.pi - azimuth
        elif azimuth < 0:
            azimuth = -math.pi - azimuth

    # 5. Extraterrestrial radiation
    extraterrestrial = 1367 * (
            1 + 0.034 * math.cos(2 * math.pi * day_of_year / 365.25)
    )

    # 6. Atmospheric optical depth
    optical_depth = (
            0.174
            + 0.035 * math.sin(rad(360 * (day_of_year - 100) / 365))
    )

    # 7. Beam radiation on horizontal surface
    beam_horizontal = (
            extraterrestrial
            * math.exp(-optical_depth / math.sin(altitude))
    )

    # 8. Solar incidence angle on the panel
    tilt = rad(panel_tilt)
    panel_az = rad(panel_azimuth)

    cos_incidence = (
            math.cos(altitude)
            * math.cos(azimuth - panel_az)
            * math.sin(tilt)
            + math.sin(altitude) * math.cos(tilt)
    )

    incidence = math.acos(max(-1, min(1, cos_incidence)))

    # 9. Direct beam radiation on panel
    direct_panel = (
        beam_horizontal * math.cos(incidence)
        if incidence <= math.pi / 2
        else 0.0
    )

    # 10. Diffuse radiation
    diffuse_factor = (
            0.095
            + 0.04 * math.sin(rad(360 * (day_of_year - 100) / 365))
    )

    diffuse_panel = (
            diffuse_factor
            * beam_horizontal
            * (1 + math.cos(tilt)) / 2
    )

    # 11. Ground-reflected radiation
    reflected_panel = (
            ground_reflectance
            * beam_horizontal
            * (math.sin(altitude) + diffuse_factor)
            * (1 - math.cos(tilt)) / 2
    )

    # 12. Total irradiance incident on panel
    total = direct_panel + diffuse_panel + reflected_panel

    """
    return {
        "beam_horizontal": beam_horizontal,
        "direct_panel": direct_panel,
        "diffuse_panel": diffuse_panel,
        "reflected_panel": reflected_panel,
        "total": total
    }
    """
    return total
