from os import path as op
import json
import codecs
from spectral.io.envi import read_envi_header


def parse_from_config_file(filename):
    if not op.exists(filename):
        raise ValueError("%s not exist" % filename)

    with codecs.open(filename, 'rb', encoding='utf-8') as fd:
        json_string = fd.readline()
    return json.loads(json_string)


def parse_from_hdr_file(filename):
    if not op.exists(filename):
        raise ValueError("%s not exist" % filename)
    return read_envi_header(filename)
