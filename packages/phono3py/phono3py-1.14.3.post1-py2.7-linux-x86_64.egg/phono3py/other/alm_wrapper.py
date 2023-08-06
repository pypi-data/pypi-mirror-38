# Copyright (C) 2016 Atsushi Togo
# All rights reserved.
#
# This file is part of phonopy.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# * Redistributions of source code must retain the above copyright
#   notice, this list of conditions and the following disclaimer.
#
# * Redistributions in binary form must reproduce the above copyright
#   notice, this list of conditions and the following disclaimer in
#   the documentation and/or other materials provided with the
#   distribution.
#
# * Neither the name of the phonopy project nor the names of its
#   contributors may be used to endorse or promote products derived
#   from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

import sys
import numpy as np
from phono3py.phonon3.fc3 import distribute_fc3
from phonopy.harmonic.force_constants import distribute_force_constants
from phonopy.structure.cells import compute_all_sg_permutations


def get_fc2(supercell,
            forces_fc2,
            disp_dataset,
            symmetry,
            log_level=0):
    natom = supercell.get_number_of_atoms()
    assert natom == disp_dataset['natom']
    force = np.array(forces_fc2, dtype='double', order='C')
    lattice = supercell.get_cell().T
    positions = supercell.get_scaled_positions()
    numbers = supercell.get_atomic_numbers()
    disp = _get_alm_disp_fc2(disp_dataset)
    pure_trans = _collect_pure_translations(symmetry)
    rotations = np.array([np.eye(3, dtype='intc')] * len(pure_trans),
                         dtype='intc', order='C')

    if log_level:
        print("------------------------------"
              " ALM FC2 start "
              "------------------------------")

    from alm import ALM
    sys.stdout.flush()
    with ALM(lattice, positions, numbers) as alm:
        alm.set_verbosity(log_level)
        nkd = len(np.unique(numbers))
        rcs = -np.ones((1, nkd, nkd), dtype='double')
        alm.define(1, rcs)
        alm.set_displacement_and_force(disp, force)
        info = alm.optimize()
        fc2_alm = alm.get_fc(1)

    if log_level:
        print("-------------------------------"
              " ALM FC2 end "
              "-------------------------------")

    fc2 = _expand_fc2(fc2_alm, supercell, pure_trans, rotations)

    return fc2


def get_fc3(supercell,
            forces_fc3,
            disp_dataset,
            symmetry,
            log_level=0):
    natom = supercell.get_number_of_atoms()
    assert natom == disp_dataset['natom']

    force = np.array(forces_fc3, dtype='double', order='C')
    lattice = supercell.get_cell().T
    positions = supercell.get_scaled_positions()
    numbers = supercell.get_atomic_numbers()
    disp, indices = _get_alm_disp_fc3(disp_dataset)
    pure_trans = _collect_pure_translations(symmetry)
    rotations = np.array([np.eye(3, dtype='intc')] * len(pure_trans),
                         dtype='intc', order='C')

    if log_level:
        print("------------------------------"
              " ALM FC3 start "
              "------------------------------")

    from alm import ALM
    sys.stdout.flush()
    with ALM(lattice, positions, numbers) as alm:
        alm.set_verbosity(log_level)
        nkd = len(np.unique(numbers))
        if 'cutoff_distance' in disp_dataset:
            cut_d = disp_dataset['cutoff_distance']
            rcs = np.ones((2, nkd, nkd), dtype='double')
            rcs[0] *= -1
            rcs[1] *= cut_d
        else:
            rcs = -np.ones((2, nkd, nkd), dtype='double')
        alm.define(2, rcs)
        alm.set_displacement_and_force(disp[indices], force[indices])
        info = alm.optimize()
        fc2_alm = alm.get_fc(1)
        fc3_alm = alm.get_fc(2)

    if log_level:
        print("-------------------------------"
              " ALM FC3 end "
              "-------------------------------")

    fc2 = _expand_fc2(fc2_alm,
                      supercell,
                      pure_trans,
                      rotations,
                      verbose=(log_level > 0))
    fc3 = _expand_fc3(fc3_alm,
                      supercell,
                      pure_trans,
                      rotations,
                      verbose=(log_level > 0))

    return fc2, fc3


def write_DFILE_and_FFILE(disp_dataset, forces_fc3,
                          dfilename="DFILE", ffilename="FFILE"):
    """Write displacements and forces to DFILE and FFILE in ALM formats.

    Parameters
    ----------
    disp_dataset : dict
        Phono3py displacement data set
    forces_fc3 : array_like
        Sets of supercell forces
        shape=(n_disp, n_atoms, 3)
    dfilename : str, optional, default="DFILE"
        Output filename of sets of supercell displacements.
    ffilename : str, optional, default="FFILE"
        Output filename of sets of supercell forces.

    """

    disp, indices = _get_alm_disp_fc3(disp_dataset)
    force = np.array(forces_fc3, dtype='double', order='C')
    for filename, data in zip((dfilename, ffilename),
                              (disp[indices], force[indices])):
        with open(filename, 'w') as w:
            for d_supercell in data:
                for d_atom in d_supercell:
                    w.write("  %21.16f %21.16f %21.16f\n" % tuple(d_atom))


def _get_alm_disp_fc2(disp_dataset):
    count = 0
    natom = disp_dataset['natom']
    disp = np.zeros((len(disp_dataset['first_atoms']), natom, 3),
                    dtype='double', order='C')
    for disp1 in disp_dataset['first_atoms']:
        disp[count, disp1['number']] = disp1['displacement']
        count += 1
    return disp


def _get_alm_disp_fc3(disp_dataset):
    """Create displacements of atoms for ALM input

    Note
    ----
    Dipslacements of all atoms in supercells for all displacement
    configurations in phono3py are returned, i.e., most of
    displacements are zero. Only the configurations with 'included' ==
    True are included in the list of indices that is returned, too.

    Parameters
    ----------
    disp_dataset : dict
        Displacement dataset that may be obtained by
        file_IO.parse_disp_fc3_yaml.

    Returns
    -------
    disp : ndarray
        Displacements of atoms in supercells of all displacement
        configurations.
        shape=(ndisp, natom, 3)
        dtype='double'
    indices : list of int
        The indices of the displacement configurations with 'included' == True.

    """

    natom = disp_dataset['natom']
    ndisp = len(disp_dataset['first_atoms'])
    for disp1 in disp_dataset['first_atoms']:
        ndisp += len(disp1['second_atoms'])
    disp = np.zeros((ndisp, natom, 3), dtype='double', order='C')
    indices = []
    count = 0
    for disp1 in disp_dataset['first_atoms']:
        indices.append(count)
        disp[count, disp1['number']] = disp1['displacement']
        count += 1

    for disp1 in disp_dataset['first_atoms']:
        for disp2 in disp1['second_atoms']:
            if 'included' in disp2:
                if disp2['included']:
                    indices.append(count)
            else:
                indices.append(count)
            disp[count, disp1['number']] = disp1['displacement']
            disp[count, disp2['number']] = disp2['displacement']
            count += 1

    return disp, indices


def _expand_fc2(fc2_alm,
                supercell,
                pure_trans,
                rotations,
                symprec=1e-5,
                verbose=True):
    natom = supercell.get_number_of_atoms()
    fc2 = np.zeros((natom, natom, 3, 3), dtype='double', order='C')
    (fc_values, elem_indices) = fc2_alm
    first_atoms = np.unique(elem_indices[:, 0] // 3)

    for (fc, indices) in zip(fc_values, elem_indices):
        v1 = indices[0] // 3
        c1 = indices[0] % 3
        v2 = indices[1] // 3
        c2 = indices[1] % 3
        fc2[v1, v2, c1, c2] = fc

    lattice = np.array(supercell.get_cell().T, dtype='double', order='C')
    positions = supercell.get_scaled_positions()
    permutations = compute_all_sg_permutations(positions,
                                               rotations,
                                               pure_trans,
                                               lattice,
                                               symprec)
    distribute_force_constants(fc2,
                               first_atoms,
                               lattice,
                               rotations,
                               permutations)

    return fc2


def _expand_fc3(fc3_alm,
                supercell,
                pure_trans,
                rotations,
                symprec=1e-5,
                verbose=True):
    (fc_values, elem_indices) = fc3_alm

    natom = supercell.get_number_of_atoms()
    fc3 = np.zeros((natom, natom, natom, 3, 3, 3), dtype='double', order='C')
    first_atoms = np.unique(elem_indices[:, 0] // 3)

    for (fc, indices) in zip(fc_values, elem_indices):
        v1, v2, v3 = indices // 3
        c1, c2, c3 = indices % 3
        fc3[v1, v2, v3, c1, c2, c3] = fc
        fc3[v1, v3, v2, c1, c3, c2] = fc

    lattice = np.array(supercell.get_cell().T, dtype='double', order='C')
    positions = supercell.get_scaled_positions()
    s2compact = np.arange(supercell.get_number_of_atoms(), dtype='intc')
    target_atoms = [i for i in s2compact if i not in first_atoms]
    permutations = compute_all_sg_permutations(positions,
                                               rotations,
                                               pure_trans,
                                               lattice,
                                               symprec)
    if verbose:
        print("Expanding fc3")

    distribute_fc3(fc3,
                   first_atoms,
                   target_atoms,
                   lattice,
                   rotations,
                   permutations,
                   s2compact,
                   verbose=verbose)
    return fc3


def _collect_pure_translations(symmetry):
    pure_trans = []
    rotations = symmetry.get_symmetry_operations()['rotations']
    translations = symmetry.get_symmetry_operations()['translations']
    for r, t in zip(rotations, translations):
        if (r == np.eye(3, dtype='intc')).all():
            pure_trans.append(t)
    return np.array(pure_trans, dtype='double', order='C')
