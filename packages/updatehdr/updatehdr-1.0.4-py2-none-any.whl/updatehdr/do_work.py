from jobs.parser import parse_from_config_file, parse_from_hdr_file
from jobs.processor import add_band_to_hdr, write_meta_to_hdr
import sys
from os import path as op


def update_hdr(filename):
    name, ext = op.splitext(filename)
    dirname = op.dirname(op.realpath(filename))
    configname = op.join(dirname, name + '.mono.config.txt')
    hdrname = op.join(dirname, name + '.hdr')
    if op.exists(configname) and op.exists(hdrname):
        config = parse_from_config_file(configname)
        hdr = parse_from_hdr_file(hdrname)
        improved_hdr = add_band_to_hdr(config, hdr)
        write_meta_to_hdr(improved_hdr, hdrname)
    else:
        print("%s need config.txt file or hdr file.")


def main():
    if len(sys.argv) != 2:
        print("python do_work.py filename")
        exit(1)
    else:
        update_hdr(sys.argv[1])


if __name__ == "__main__":
    main()
