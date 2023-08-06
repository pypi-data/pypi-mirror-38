# coding: utf-8
# Copyright (c) Max-Planck-Institut für Eisenforschung GmbH - Computational Materials Design (CM) Department
# Distributed under the terms of "New BSD License", see the LICENSE file.

from __future__ import print_function
from collections import OrderedDict
import numpy as np
from pyiron.base.objects.generic.parameters import GenericParameters

__author__ = "Joerg Neugebauer, Sudarsan Surendralal, Jan Janssen"
__copyright__ = "Copyright 2017, Max-Planck-Institut für Eisenforschung GmbH - Computational Materials Design (CM) Department"
__version__ = "1.0"
__maintainer__ = "Sudarsan Surendralal"
__email__ = "surendralal@mpie.de"
__status__ = "production"
__date__ = "Sep 1, 2017"


class LammpsControl(GenericParameters):
    def __init__(self, input_file_name=None, **qwargs):
        super(LammpsControl, self).__init__(input_file_name=input_file_name,
                                            table_name="control_inp",
                                            comment_char="#")
        self._init_block_dict()

    @property
    def dataset(self):
        return self._dataset

    def _init_block_dict(self):
        block_dict = OrderedDict()
        block_dict['read_restart'] = 'read_restart'
        block_dict['structure'] = ('units', 'dimension', 'boundary', 'atom_style', 'read_data', 'include')
        block_dict['potential'] = ('group', 'set', 'pair_style', 'pair_coeff', 'bond_style', 'bond_coeff',
                                   'angle_style', 'angle_coeff', 'kspace_style', 'neighbor')
        block_dict['compute'] = 'compute'
        block_dict['control'] = ('fix', 'min_style', 'min_modify', 'neigh_modify',
                                 'velocity', 'dump', 'dump_modify', 'thermo_style', 'thermo_modify', 'thermo',
                                 'timestep', 'dielectric', 'fix_modify')
        block_dict['run'] = ('run', 'minimize')
        block_dict['write_restart'] = 'write_restart'
        self._block_dict = block_dict

    def load_default(self, file_content=None):
        if file_content is None:
            file_content = '''\
units      metal
dimension  3
boundary   p p p
atom_style atomic
read_data structure.inp
include potential.inp
fix 1 all nve
variable dumptime equal 100
dump 1 all custom ${dumptime} dump.out id type xsu ysu zsu fx fy fz
dump_modify 1 sort id format line "%d %d %20.15g %20.15g %20.15g %20.15g %20.15g %20.15g"
thermo_style custom step temp pe etotal pxx pxy pxz pyy pyz pzz vol
thermo_modify format  float %20.15g
thermo 100
run 0
'''
        self.load_string(file_content)

    def calc_minimize(self, e_tol=0.0, f_tol=1e-8, max_iter=100000, pressure=None, n_print=100):
        max_evaluations = 10 * max_iter
        if pressure is not None:
            if type(pressure) == float or type(pressure) == int:
                pressure = pressure*np.ones(3)
            str_press = ''
            for press, str_axis in zip(pressure, [' x ', ' y ', ' z ']):
                if press is not None:
                    str_press += str_axis+str(press*1.0e4)
            if len(str_press) == 0:
                raise ValueError('Pressure values cannot be three times None')
            elif len(str_press)>1:
                str_press += ' couple none'
            self.set(fix___1=r'all box/relax' + str_press)
        else:
            self.remove_keys(["fix"])
        self.set(minimize=str(e_tol) + ' ' + str(f_tol) + ' ' + str(max_iter) + " " + str(max_evaluations))
        self.remove_keys(['run', 'velocity'])
        self.modify(variable___dumptime___equal=n_print, thermo=n_print)

    def calc_static(self):
        self.set(run='0')
        self.remove_keys(['minimize', 'velocity'])

    def calc_md(self, temperature=None, pressure=None, n_ionic_steps=1000, dt=None, time_step=None, n_print=100,
                delta_temp=100.0, delta_press=None, seed=None, tloop=None, rescale_velocity=True, langevin=False):

        if time_step is not None:
            # time_step in fs
            if self['units'] == 'metal':
                self['timestep'] = time_step * 1e-3  # lammps in ps
            elif self['units'] in ['si', 'cgs']:
                self['timestep'] = time_step * 1e-12
            elif self['units'] in ['real', 'electron']:
                self['timestep'] = time_step
            else:
                raise NotImplementedError()

        if seed is None:
            seed = np.random.randint(99999)
        if pressure is not None:
            pressure = float(pressure)*1.0e4  # TODO; why needed?
            if delta_press is None:
                delta_press = delta_temp*10
            if temperature is None or temperature == 0.0:
                raise ValueError('Target temperature for fix nvt/npt/nph cannot be 0.0')
            if langevin:
                ensamble = 'nph'

                fix_str = 'all {0} aniso {1} {2} {3}'.format(ensamble, str(temperature), str(temperature), str(delta_temp),
                                                                              str(pressure), str(pressure), str(delta_press))
                self.modify(fix___langevin='all langevin {0} {1} {2} {3}'.format(str(temperature), str(temperature), str(delta_temp), str(seed)),
                            append_if_not_present=True)
            else:
                ensamble = 'npt'
                fix_str = 'all {0} temp {1} {2} {3} aniso {4} {5} {6}'.format(ensamble, str(temperature), str(temperature),
                                                                              str(delta_temp), str(pressure), str(pressure),
                                                                              str(delta_press))
        elif temperature is not None:
            temperature = float(temperature)  # TODO; why needed?
            if temperature == 0.0:
                raise ValueError('Target temperature for fix nvt/npt/nph cannot be 0.0')
            if langevin:
                ensamble = 'nve'
                fix_str = 'all {0}'.format(ensamble)
                self.modify(fix___langevin='all langevin {0} {1} {2} {3}'.format(str(temperature), str(temperature), str(delta_temp), str(seed)),
                            velocity='all create ' + str(2 * temperature) + ' ' + str(seed) + ' dist gaussian ', append_if_not_present=True)
            else:
                ensamble = 'nvt'
                fix_str = 'all {0} temp {1} {2} {3}'.format(ensamble, str(temperature), str(temperature), str(delta_temp))
        else:
            ensamble = 'nve'
            fix_str = 'all {0}'.format(ensamble)
        if tloop is not None:
            fix_str += " tloop " + str(tloop)
        self.remove_keys(["minimize"])
        if rescale_velocity and ensamble in ['npt', 'nvt', 'nph']:
            self.modify(fix___1=fix_str,
                        variable=' dumptime equal {} '.format(n_print),
                        thermo=int(n_print),
                        run=int(n_ionic_steps),
                        velocity='all create ' + str(2 * temperature) + ' ' + str(seed) + ' dist gaussian ',
                        append_if_not_present=True)
        else:
            self.modify(fix___1=fix_str,
                        variable=' dumptime equal {} '.format(n_print),
                        thermo=int(n_print),
                        run=int(n_ionic_steps),
                        append_if_not_present=True)
