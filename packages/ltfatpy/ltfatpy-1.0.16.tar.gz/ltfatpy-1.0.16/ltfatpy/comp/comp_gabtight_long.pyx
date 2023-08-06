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


"""This module contains interface functions for the LTFAT computed
versions of tight gabor windows calculation.

.. moduleauthor:: Denis Arrivault
"""

from __future__ import print_function, division

import cython
import numpy as np

from ltfat cimport ltfatInt, gabtight_long_d, gabtight_long_cd

# cython: profile=True

# don’t check for out-of-bounds indexing.
@cython.boundscheck(False)
# assume no negative indexing.
@cython.wraparound(False)
cdef comp_gabtight_long_real(const double[:] g, const ltfatInt L,
                             const ltfatInt R, const ltfatInt a,
                             const ltfatInt M, double[:] out):
    """ Internal function, do not use it """
    gabtight_long_d(&g[0], L, R, a, M, &out[0])

# don’t check for out-of-bounds indexing.
@cython.boundscheck(False)
# assume no negative indexing.
@cython.wraparound(False)
cdef comp_gabtight_long_cmplx(const double complex[:] g, const ltfatInt L,
                              const ltfatInt R, const ltfatInt a,
                              const ltfatInt M, double complex[:] out):
    """ Internal function, do not use it """
    gabtight_long_cd(&g[0], L, R, a, M, &out[0])

cpdef comp_gabtight_long(g, a, M):
    """Compute tight window

    This is a computational subroutine, do not call it directly, use
    :func:`~ltfatpy.gabor.gabtight.gabtight` instead.

    .. seealso:: :func:`~ltfatpy.gabor.gabtight.gabtight`
    """
    cdef ltfatInt L = g.shape[0]
    cdef ltfatInt R = 1
    if g.ndim > 1:
        if g.ndim > 2:
            raise TypeError("g dimensions should be 1 or 2.")
        R = g.shape[1]
        g_combined = g.reshape(L*R, order='F')
    else:
        g_combined = g

    if np.issubdtype(g.dtype, np.float64):
        gd = np.ndarray((L * R), dtype=np.float64)
        comp_gabtight_long_real(g_combined, L, R, a, M, gd)
    elif np.issubdtype(g.dtype, np.complex128):
        gd = np.ndarray((L * R), dtype=np.complex128)
        comp_gabtight_long_cmplx(g_combined, L, R, a, M, gd)
    else:
        raise TypeError("g data should be numpy.float64 or numpy.complex128")

    if R == 1:
        return gd
    else:
        return gd.reshape(R, L).transpose()
