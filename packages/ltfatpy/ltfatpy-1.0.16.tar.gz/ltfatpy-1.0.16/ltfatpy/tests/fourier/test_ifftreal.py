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


"""Test of the ifftreal function

.. moduleauthor:: Florent Jaillet
"""

from __future__ import print_function, division

import unittest
import numpy as np
from numpy.testing import assert_allclose

from ltfatpy.fourier.ifftreal import ifftreal
from ltfatpy.fourier.fftreal import fftreal
from ltfatpy.tests.datasets.read_ref_mat import read_ref_mat
from ltfatpy.tests.datasets.get_dataset_path import get_dataset_path


class TestIfftreal(unittest.TestCase):

    # Called before the tests.
    def setUp(self):
        print('\nStart TestIfftreal')

    # Called after the tests.
    def tearDown(self):
        print('Test done')

    def test_shape(self):
        """Check that the output has the expected shape
        """
        shapes = ((4,), (4, 3), (4, 3, 2))
        N_val = (range(2, 10))
        inputs = {}
        for shape in shapes:
            inputs['c'] = (np.random.random(shape) +
                           1.0j * np.random.random(shape))
            for dim in range(len(shape)):
                inputs['dim'] = dim
                for N in N_val:
                    inputs['N'] = N
                    f = ifftreal(**inputs)
                    expected_shape = list(shape)
                    expected_shape[dim] = N
                    expected_shape = tuple(expected_shape)
                    msg = ('Wrong shape in the ouput of ifftreal with ' +
                           'inputs ' + str(inputs))
                    self.assertEqual(f.shape, expected_shape, msg)

    def test_inversion(self):
        """Check that ifftreal is the inverse of fftreal
        """
        K = 16
        shapes = ((K,), (K, K-1), (K, K-1, K-2))
        inputs = {}
        for shape in shapes:
            f_ref = np.random.random(shape)
            for dim in range(len(shape)):
                inputs['dim'] = dim
                N_val = (range(shape[dim], 2*shape[dim]))
                for N in N_val:
                    inputs['N'] = N
                    c = fftreal(f_ref, **inputs)
                    f = ifftreal(c, **inputs)
                    f = np.take(f, np.arange(f_ref.shape[dim]), dim)
                    msg = ('Result of inversion is not close enough to the ' +
                           'original when composing fftreal and ifftreal ' +
                           'with inputs ' + str(inputs))
                    assert_allclose(f, f_ref, rtol=1e-10, atol=1e-14,
                                    err_msg=msg)

    def test_known(self):
        """Checking ifftreal on some known results taken from Octave
        """
        filename = get_dataset_path('ifftreal_ref.mat')
        data = read_ref_mat(filename)

        for inputs, outputs in data:
            h = ifftreal(**inputs)
            msg = ('Wrong value in output of ifftreal with inputs ' +
                   str(inputs))
            assert_allclose(h, outputs[0], rtol=5e-13, atol=1e-15, err_msg=msg)


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestIfftreal)
    unittest.TextTestRunner(verbosity=2).run(suite)
