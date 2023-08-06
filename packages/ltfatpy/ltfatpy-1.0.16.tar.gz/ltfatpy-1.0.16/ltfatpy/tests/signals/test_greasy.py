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


"""Test of the greasy function

.. moduleauthor:: Florent Jaillet
"""

from __future__ import print_function, division

import unittest
from numpy.testing import assert_array_equal

from ltfatpy.signals.greasy import greasy
from ltfatpy.tests.datasets.read_ref_mat import read_ref_mat
from ltfatpy.tests.datasets.get_dataset_path import get_dataset_path


class TestGreasy(unittest.TestCase):

    # Called before the tests.
    def setUp(self):
        print('\nStart TestGreasy')

    # Called after the tests.
    def tearDown(self):
        print('Test done')

    def test_data(self):
        """ Checking that the read data match the expectations
        """
        filename = get_dataset_path('greasy_ref.mat')
        # Known values of samples as read by Octave with ltfat 2.1.0
        data = read_ref_mat(filename)
        inputs, outputs = data[0]
        (s, fs) = greasy()
        self.assertEqual(s.shape, outputs[0].shape,
                         'Wrong signal shape in greasy')
        assert_array_equal(s, outputs[0], 'Wrong sample values in greasy')
        self.assertEqual(fs, outputs[1], 'Wrong sampling frequency in greasy')


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestGreasy)
    unittest.TextTestRunner(verbosity=2).run(suite)
