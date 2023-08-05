#!/usr/bin/env python

"""
Script to run VetRedRockGui
"""
from __future__ import print_function, absolute_import
from __future__ import division, unicode_literals

# import pdb

try:
    ustr = unicode
except NameError:
    ustr = str


def parser(options=None):
    """ Parser for VetRedRockGui
    Parameters
    ----------
    options

    Returns
    -------

    """

    import argparse

    parser = argparse.ArgumentParser(description='Run the VetRedRockGUI on\
                                     RedRock output')
    parser.add_argument("in_file", type=str, help="RedRock output FITS file")
    parser.add_argument("outfile", type=str, help="Output vetted .json file")
    parser.add_argument("--coadd_file", type=str, help="YAML file for\
                        coadding; will print xval to screen")

    if options is None:
        args = parser.parse_args()
    else:
        args = parser.parse_args(namespace=options)
    return args


def main(args=None):
    pargs = parser(options=args)
    import sys
    import os
    from linetools import utils as ltu
    from vetrr.vet_redrock import VetRedRockGui
    from PyQt5.QtWidgets import QApplication
    from collections import OrderedDict
    import yaml

    # Load outfile if it exists
    if os.path.isfile(pargs.outfile):
        print("******************************************************")
        print("WARNING:  Loading previous file and will over-write it!")
        print("******************************************************")
        zdict = ltu.loadjson(pargs.outfile)
        zdict = OrderedDict(zdict)
    else:
        zdict = None

    # YAML coadd file?
    if pargs.coadd_file is not None:
        # Load the input file
        with open(pargs.coadd_file, 'r') as infile:
            coadd_dict = yaml.load(infile)

    app = QApplication(sys.argv)
    gui = VetRedRockGui(pargs.in_file, outfile=pargs.outfile,
                        zdict=zdict, coadd_dict=coadd_dict)
    gui.show()
    app.exec_()


if __name__ == '__main__':
    main()
