# -*- coding: utf-8 -*-
# ######### COPYRIGHT #########
# Credits
# #######
#
# Copyright(c) 2015-2018
# ----------------------
#
# * `LabEx Archimède <http://labex-archimede.univ-amu.fr/>`_
# * `Laboratoire d'Informatique Fondamentale <http://www.lif.univ-mrs.fr/>`_
#   (now `Laboratoire d'Informatique et Systèmes <http://www.lis-lab.fr/>`_)
# * `Institut de Mathématiques de Marseille <http://www.i2m.univ-amu.fr/>`_
# * `Université d'Aix-Marseille <http://www.univ-amu.fr/>`_
#
# This software is a port from LTFAT 2.1.0 :
# Copyright (C) 2005-2018 Peter L. Soendergaard <peter@sonderport.dk>.
#
# Contributors
# ------------
#
# * Denis Arrivault <contact.dev_AT_lis-lab.fr>
# * Florent Jaillet <contact.dev_AT_lis-lab.fr>
#
# Description
# -----------
#
# ltfatpy is a partial Python port of the
# `Large Time/Frequency Analysis Toolbox <http://ltfat.sourceforge.net/>`_,
# a MATLAB®/Octave toolbox for working with time-frequency analysis and
# synthesis.
#
# Version
# -------
#
# * ltfatpy version = 1.0.16
# * LTFAT version = 2.1.0
#
# Licence
# -------
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# ######### COPYRIGHT #########


"""Test of the read_dgt_signal_ex_mat function

.. moduleauthor:: Denis Arrivault
"""

from __future__ import print_function, division

import unittest
import numpy
try:
    from math import gcd
except ImportError:
    # fractions.gcd() is deprecated since Python 3.5 and math.gcd() should be
    # used instead, but for backward compatibilty we use fractions.gcd() if
    # math.gcd() is not available
    from fractions import gcd

from ltfatpy.tests.datasets.read_dgt_signal_ex_mat import DgtSignals
from ltfatpy.tests.datasets.get_dataset_path import get_dataset_path


class TestReadDgtSignalExt(unittest.TestCase):
    """ Test read_dgt_signal_ex.py """

    # Called before the tests.
    def setUp(self):
        self.filename = get_dataset_path('sepdgt_signal_ex.mat')

    # Called after the tests.
    def tearDown(self):
        print('Test done')

    def test_default(self):
        dgs = DgtSignals(self.filename)
        (TYPE, PHASETYPE, L, W, a, M, gl, SIGNAL, WINDOW, DGT, DUAL_WINDOW,
         IDGT) = dgs.read_next_signal()
        while TYPE != '':
            '''
            print ("\n\nTYPE = ", TYPE, "\nPHASETYPE = ", PHASETYPE, "\nL = ",
                   L, "\nW = ", W, "\na = ", a, "\nM = ", M, "\ngl = ",
                   gl, "\nSIGNAL =\n", SIGNAL, "\nWINDOW =\n", WINDOW,
                   "\nDGT\n", DGT, "\nDUAL_WINDOW\n", DUAL_WINDOW,
                   "\nIDGT\n", IDGT)
            '''

            assert (TYPE == "REAL" or TYPE == "CMPLX")
            assert (PHASETYPE == "freqinv" or PHASETYPE == "timeinv")
            assert isinstance(L, int)
            assert isinstance(W, int)
            assert isinstance(a, int)
            assert isinstance(M, int)
            assert isinstance(gl, int)
            assert type(SIGNAL).__module__ == numpy.__name__
            assert type(WINDOW).__module__ == numpy.__name__
            assert type(DGT).__module__ == numpy.__name__
            assert type(IDGT).__module__ == numpy.__name__
            assert WINDOW.size == gl
            if (gl == M):
                assert DUAL_WINDOW.size == gl
            elif (a != M):
                assert DUAL_WINDOW.size == a * M // gcd(a, M)
            else:
                assert DUAL_WINDOW.size == a * 2

            if W == 1:
                assert SIGNAL.size == L
                assert IDGT.size == L
            else:
                assert SIGNAL.shape == (L, W)
                assert IDGT.shape == (L, W)

            if TYPE == "REAL":
                if W == 1:
                    assert DGT.shape == ((M//2+1), L//a)
                else:
                    assert DGT.shape == ((M//2+1), L//a, W)
            else:
                if W == 1:
                    assert DGT.shape == (M, L//a)
                else:
                    assert DGT.shape == (M, L//a, W)
            (TYPE, PHASETYPE, L, W, a, M, gl, SIGNAL, WINDOW, DGT, DUAL_WINDOW,
             IDGT) = dgs.read_next_signal()

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestReadDgtSignalExt)
    unittest.TextTestRunner(verbosity=2).run(suite)
