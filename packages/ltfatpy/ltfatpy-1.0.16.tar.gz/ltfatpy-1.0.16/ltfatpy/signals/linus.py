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


"""Module of linus signal loading

Ported from ltfat_2.1.0/signals/linus.m

.. moduleauthor:: Florent Jaillet
"""

from __future__ import print_function, division

from scipy.io.wavfile import read as wavread
import pkg_resources
import numpy as np


def linus():
    """Load the 'linus' test signal

    - Usage:

        | ``(s, fs) = linus()``

    - Output parameters:

    :returns: ``(s, fs)``
    :rtype: tuple

    :var numpy.ndarray s: 'linus' signal
    :var int fs: sampling frequency in Hz

    ``linus`` loads the 'linus' signal. It is a recording of Linus Thorvalds
    pronouncing the words "Hello. My name is Linus Thorvalds, and I pronounce
    Linux as Linux".

    The signal is 41461 samples long and is sampled at 8 kHz.

    See `<http://www.paul.sladen.org/pronunciation/>`_.
    """

    f = pkg_resources.resource_stream(__name__, "linus.wav")

    fs, s = wavread(f)
    s = s.astype(np.float64) / 2.**15.
    return (s, fs)
