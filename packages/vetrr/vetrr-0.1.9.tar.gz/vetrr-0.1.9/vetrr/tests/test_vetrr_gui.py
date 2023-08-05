from __future__ import print_function, absolute_import
from __future__ import division, unicode_literals

# TEST_UNICODE_LITERALS

import pytest
import os
import sys
# from pkg_resources import resource_filename

from PyQt5.QtWidgets import QApplication
from linetools.guis import xspecgui

# QWidget: Must construct a QApplication before a QWidget
app = QApplication(sys.argv)


def data_path(filename):
    """Get the path to the data.

    Returns:
    --------
    str:
        path to data
    """
    data_dir = os.path.join(os.path.dirname(__file__), 'files')
    return os.path.join(data_dir, filename)


def test_xspecgui():
    # Init
    spec_fil = data_path('J105935.22+144406.3.fits.gz')
    print(spec_fil)
    xsgui = xspecgui.XSpecGui(spec_fil, unit_test=True)
