from spectral.io.envi import write_envi_header


def add_band_to_hdr(config_header, envi_header):
    st_wave = float(config_header['startband'])
    ed_wave = float(config_header['endband'])
    nu_wave = int(config_header['bandnum'])
    step_wave = float(ed_wave - st_wave) / (nu_wave - 1)
    waves = []

    for i in range(0, nu_wave, 1):
        waves.append("%.6f" % (st_wave + i * step_wave))
    envi_header['wavelength'] = waves

    return envi_header


def write_meta_to_hdr(envi_header, filename):
    write_envi_header(filename, envi_header)
