import numpy as np
from pyiron.base.objects.job.generic import GenericJob
from pyiron.atomistics.structure.atoms import Atoms
from pyiron.atomistics.job.atomistic import AtomisticGenericJob, GenericOutput


class InteractiveBase(GenericJob):
    def __init__(self, project, job_name):
        super(InteractiveBase, self).__init__(project, job_name)
        self._interactive_library = None
        self._interactive_write_input_files = False
        self._interactive_flush_frequency = 1
        self._interactive_write_frequency = 1
        self.interactive_cache = {}

    @property
    def interactive_flush_frequency(self):
        return self._interactive_flush_frequency

    @interactive_flush_frequency.setter
    def interactive_flush_frequency(self, frequency):
        if not isinstance(frequency, int):
            raise AssertionError()
        self._interactive_flush_frequency = frequency

    @property
    def interactive_write_frequency(self):
        return self._interactive_write_frequency

    @interactive_write_frequency.setter
    def interactive_write_frequency(self, frequency):
        if not isinstance(frequency, int):
            raise AssertionError()
        self._interactive_write_frequency = frequency

    def _run_if_running(self):
        if self.server.run_mode.interactive:
            self.run_if_interactive()
        else:
            super(InteractiveBase, self)._run_if_running()

    def _run_if_created(self, que_wait_for=None):
        if self._interactive_write_input_files:
            self.project_hdf5.create_working_directory()
            self.write_input()
            self._copy_restart_files()
            self._write_run_wrapper()
        super(InteractiveBase, self)._run_if_created(que_wait_for=que_wait_for)

    def interactive_is_activated(self):
        if self._interactive_library is None:
            return False
        else:
            return True

    @staticmethod
    def _extend_hdf(h5, path, key, data):
        if path in h5.list_groups() and key in h5[path].list_nodes(): 
            current_hdf = h5[path + "/" + key]
            if isinstance(data, list):
                entry = current_hdf.tolist() + data
            else: 
                entry = current_hdf.tolist() + data.tolist()
            data = np.array(entry)
        h5[path + "/" + key] = data

    @staticmethod
    def _include_last_step(array, step=1, include_last=False):
        if step == 1:
            return array
        if len(array) > 0:
            if len(array) > step:
                new_array = array[::step]
                index_lst = list(range(len(array)))
                if include_last and index_lst[-1] != index_lst[::step][-1]:
                    new_array.append(array[-1])
                return new_array
            else:
                if include_last:
                    return [array[-1]]
                else:
                    return []
        return []

    def interactive_flush(self, path="interactive", include_last_step=False):
        with self.project_hdf5.open("output") as h5:
            for key in self.interactive_cache.keys():
                if len(self.interactive_cache[key])==0:
                    continue
                data = self._include_last_step(array=self.interactive_cache[key],
                                               step=self.interactive_write_frequency,
                                               include_last=include_last_step)
                if len(data) > 0 and \
                        isinstance(data[0], list) and \
                        len(np.shape(data)) == 1:
                    self._extend_hdf(h5=h5, path=path, key=key, data=data)
                elif np.array(data).dtype == np.dtype('O'):
                    self._extend_hdf(h5=h5, path=path, key=key, data=data)
                else:
                    self._extend_hdf(h5=h5, path=path, key=key, data=np.array(data))
                self.interactive_cache[key] = []

    def interactive_close(self):
        if len(list(self.interactive_cache.keys())) > 0 and \
                len(self.interactive_cache[list(self.interactive_cache.keys())[0]]) != 0:
            self.interactive_flush(path="interactive", include_last_step=True)
        self.project.db.item_update(self._runtime(), self._job_id)
        self.status.finished = True
        self.interactive_cache = {}

    def interactive_store_in_cache(self, key, value):
        self.interactive_cache[key] = value

    # def __del__(self):
    #     self.interactive_close()

    def run_if_interactive(self):
        raise NotImplementedError('run_if_interactive() is not implemented!')

    def run_if_interactive_non_modal(self):
        raise NotImplementedError('run_if_interactive_non_modal() is not implemented!')

    def to_hdf(self, hdf=None, group_name=None):
        """
        Store the InteractiveBase object in the HDF5 File

        Args:
            hdf (ProjectHDFio): HDF5 group object - optional
            group_name (str): HDF5 subgroup name - optional
        """
        super(InteractiveBase, self).to_hdf(hdf=hdf, group_name=group_name)
        with self.project_hdf5.open("input") as hdf5_input:
            hdf5_input["interactive"] = {"interactive_flush_frequency": self._interactive_flush_frequency,
                                         "interactive_write_frequency": self._interactive_write_frequency}

    def from_hdf(self, hdf=None, group_name=None):
        """
        Restore the InteractiveBase object in the HDF5 File

        Args:
            hdf (ProjectHDFio): HDF5 group object - optional
            group_name (str): HDF5 subgroup name - optional
        """
        super(InteractiveBase, self).from_hdf(hdf=hdf, group_name=group_name)
        with self.project_hdf5.open("input") as hdf5_input:
            if "interactive" in hdf5_input.list_nodes():
                interactive_dict = hdf5_input["interactive"]
                self._interactive_flush_frequency = interactive_dict["interactive_flush_frequency"]
                if "interactive_write_frequency" in interactive_dict.keys():
                    self._interactive_write_frequency = interactive_dict["interactive_write_frequency"]
                else:
                    self._interactive_write_frequency = 1


class GenericInteractive(AtomisticGenericJob, InteractiveBase):
    def __init__(self, project, job_name):
        super(GenericInteractive, self).__init__(project, job_name)
        self.output = GenericInteractiveOutput(job=self)
        self._structure_previous = None
        self._structure_current = None
        self._interactive_enforce_structure_reset = False
        self._interactive_grand_canonical = False
        self.interactive_cache = {'cells': [],
                                  'energy_pot': [],
                                  'energy_tot': [],
                                  'forces': [],
                                  'positions': [],
                                  'pressures': [],
                                  'stress': [],
                                  'steps': [],
                                  'temperature': [],
                                  'indices': [],
                                  'computation_time': [],
                                  'unwrapped_positions': [],
                                  'atom_spin_constraints': [],
                                  'atom_spins': [],
                                  'magnetic_forces': [],
                                  'volume': []}

    @property
    def interactive_enforce_structure_reset(self):
        return self._interactive_enforce_structure_reset

    @interactive_enforce_structure_reset.setter
    def interactive_enforce_structure_reset(self, reset):
        if not isinstance(reset, bool):
            raise AssertionError()
        self._interactive_enforce_structure_reset = reset

    @property
    def initial_structure(self):
        return AtomisticGenericJob.structure.fget(self)

    @property
    def current_structure(self):
        return self.structure

    @current_structure.setter
    def current_structure(self, structure):
        self.structure = structure

    @property
    def structure(self):
        if self._structure_current is not None:
            return self._structure_current
        elif self.server.run_mode.interactive:
            self._structure_current = AtomisticGenericJob.structure.fget(self)
            return self._structure_current
        else:
            return AtomisticGenericJob.structure.fget(self)

    @structure.setter
    def structure(self, structure):
        if self.server.run_mode.interactive:
            # only overwrite the initial structure if it is not set already.
            if AtomisticGenericJob.structure.fget(self) is None:
                AtomisticGenericJob.structure.fset(self, structure.copy())
            self._structure_current = structure
        else:
            AtomisticGenericJob.structure.fset(self, structure)

    def run_if_interactive(self):
        self.status.running = True
        if self.structure is None:
            raise ValueError("Input structure not set. Use method set_structure()")
        if not self.interactive_is_activated():
            self.interactive_open()
        if self._structure_previous is None:
            if self.get("output/generic/cells") is not None and len(self.get("output/generic/cells")) != 0:
                self._structure_previous = self.get_structure(-1)
            else:
                self._structure_previous = self.structure.copy()
        if self._structure_current is not None:
            if len(self._structure_current) != len(self._structure_previous) and not self._interactive_grand_canonical:
                raise ValueError('The number of atoms changed, this is currently not supported!')
            el_lst = list(set(list(self._structure_current.get_species_symbols()) +
                              list(self._structure_previous.get_species_symbols())))
            current_structure_index = [el_lst.index(el) for el in self._structure_current.get_chemical_symbols()]
            previous_structure_index = [el_lst.index(el) for el in self._structure_previous.get_chemical_symbols()]
            if np.array_equal(np.array(current_structure_index), np.array(previous_structure_index)) and \
                    not self._interactive_enforce_structure_reset:
                if not np.allclose(self._structure_current.cell, self._structure_previous.cell, rtol=1e-15, atol=1e-15):
                    self._logger.debug('Generic library: cell changed!')
                    self.interactive_cells_setter(self._structure_current.cell)
                if not np.allclose(self._structure_current.scaled_positions,
                                   self._structure_previous.scaled_positions, rtol=1e-15, atol=1e-15):
                    self._logger.debug('Generic library: positions changed!')
                    self.interactive_positions_setter(self._structure_current.positions)
                if np.any(self._structure_current.get_initial_magnetic_moments()) and \
                        not np.allclose(self._structure_current.get_initial_magnetic_moments(),
                                        self._structure_previous.get_initial_magnetic_moments()):
                    self._logger.debug('Generic library: magnetic moments changed!')
                    self.interactive_spin_constraints_setter(self._structure_current.get_initial_magnetic_moments())
            elif not self._interactive_enforce_structure_reset and \
                    len(self._structure_current) == len(self._structure_previous) and \
                    np.allclose(self._structure_current.cell, self._structure_previous.cell, rtol=1e-15, atol=1e-15) and \
                    np.allclose(self._structure_current.scaled_positions,
                                self._structure_previous.scaled_positions, rtol=1e-15, atol=1e-15) and \
                    (not np.any(self._structure_current.get_initial_magnetic_moments()) or
                     np.allclose(self._structure_current.get_initial_magnetic_moments(),
                                 self._structure_previous.get_initial_magnetic_moments())):
                self._logger.debug('Generic library: indices changed!')
                self.interactive_indices_setter(self._structure_current.indices)
            else:
                self._logger.debug('Generic library: structure changed!')
                self.interactive_structure_setter(self._structure_current)
            self._structure_previous = self._structure_current.copy()

    def interactive_cells_getter(self):
        return self.initial_structure.cell

    def interactive_collect(self):
        if 'cells' in self.interactive_cache.keys():
            self.interactive_cache['cells'].append(self.interactive_cells_getter())
        if 'energy_pot' in self.interactive_cache.keys():
            self.interactive_cache['energy_pot'].append(self.interactive_energy_pot_getter())
        if 'energy_tot' in self.interactive_cache.keys():
            self.interactive_cache['energy_tot'].append(self.interactive_energy_tot_getter())
        if 'forces' in self.interactive_cache.keys():
            self.interactive_cache['forces'].append(self.interactive_forces_getter())
        if 'positions' in self.interactive_cache.keys():
            self.interactive_cache['positions'].append(self.interactive_positions_getter())
        if 'pressures' in self.interactive_cache.keys():
            self.interactive_cache['pressures'].append(self.interactive_pressures_getter())
        if 'stress' in self.interactive_cache.keys():
            self.interactive_cache['stress'].append(self.interactive_stress_getter())
        if 'steps' in self.interactive_cache.keys():
            self.interactive_cache['steps'].append(self.interactive_steps_getter())
        if 'temperature' in self.interactive_cache.keys():
            self.interactive_cache['temperature'].append(self.interactive_temperatures_getter())
        if 'computation_time' in self.interactive_cache.keys():
            self.interactive_cache['computation_time'].append(self.interactive_time_getter())
        if 'indices' in self.interactive_cache.keys():
            self.interactive_cache['indices'].append(self.interactive_indices_getter())
        if 'atom_spins' in self.interactive_cache.keys():
            self.interactive_cache['atom_spins'].append(self.interactive_spins_getter())
        if 'atom_spin_constraints' in self.interactive_cache.keys():
            if self._generic_input['fix_spin_constraint']:
                self.interactive_cache['atom_spin_constraints'].append(self.interactive_spin_constraints_getter())
        if 'magnetic_forces' in self.interactive_cache.keys():
            if self._generic_input['fix_spin_constraint']:
                self.interactive_cache['magnetic_forces'].append(self.interactive_magnetic_forces_getter())
        if 'unwrapped_positions' in self.interactive_cache.keys():
            self.interactive_cache['unwrapped_positions'].append(self.interactive_unwrapped_positions_getter())
        if 'volume' in self.interactive_cache.keys():
            self.interactive_cache['volume'].append(self.interactive_volume_getter())
        if len(list(self.interactive_cache.keys()))>0 and len(self.interactive_cache[list(self.interactive_cache.keys())[0]]) % self._interactive_flush_frequency == 0:
            self.interactive_flush(path="interactive")

    def interactive_indices_getter(self):
        return self.current_structure.get_chemical_indices()

    def interactive_positions_getter(self):
        return self.current_structure.positions

    def interactive_steps_getter(self):
        return len(self.interactive_cache[list(self.interactive_cache.keys())[0]])

    def interactive_time_getter(self):
        return self.interactive_steps_getter()

    def interactive_volume_getter(self):
        return self.initial_structure.get_volume()

    def get_structure(self, iteration_step=-1):
        if self.server.run_mode.interactive and self.interactive_is_activated():
            # Warning: We only copy symbols, positions and cell information - no tags.
            el_lst = [el.Abbreviation for el in self.structure.species]
            return Atoms(symbols=np.array([el_lst[el] for el in self.output.indices[iteration_step]]),
                         positions=self.output.positions[iteration_step],
                         cell=self.output.cells[iteration_step])
        else:
            return super(GenericInteractive, self).get_structure(iteration_step=iteration_step)

    # Functions which have to be implemented by the fin
    def interactive_cells_setter(self, cell):
        raise NotImplementedError('interactive_cells_getter() is not implemented!')

    def interactive_energy_pot_getter(self):
        raise NotImplementedError('interactive_energy_pot_getter() is not implemented!')

    def interactive_energy_tot_getter(self):
        raise NotImplementedError('interactive_energy_tot_getter() is not implemented!')

    def interactive_forces_getter(self):
        raise NotImplementedError('interactive_forces_getter() is not implemented!')

    def interactive_indices_setter(self, indices):
        raise NotImplementedError('interactive_indices_setter() is not implemented!')

    def interactive_spins_getter(self):
        raise NotImplementedError('interactive_spins_getter() is not implemented!')

    def interactive_spin_constraints_getter(self):
        raise NotImplementedError('interactive_spin_constraints_getter() is not implemented!')

    def interactive_magnetic_forces_getter(self):
        raise NotImplementedError('interactive_magnetic_forces_getter() is not implemented!')

    def interactive_spin_constraints_setter(self, spins):
        raise NotImplementedError('iinteractive_spin_constraints_setter() is not implemented!')

    def interactive_open(self):
        raise NotImplementedError('interactive_open() is not implemented!')

    def interactive_positions_setter(self, positions):
        raise NotImplementedError('interactive_positions_setter() is not implemented!')

    def interactive_pressures_getter(self):
        raise NotImplementedError('interactive_pressures_getter() is not implemented!')

    def interactive_stress_getter(self):
        raise NotImplementedError('interactive_stress_getter() is not implemented!')

    def interactive_structure_setter(self, structure):
        raise NotImplementedError('interactive_structure_setter() is not implemented!')

    def interactive_temperatures_getter(self):
        raise NotImplementedError('interactive_temperatures_getter() is not implemented!')

    def interactive_unwrapped_positions_getter(self):
        raise NotImplementedError('interactive_unwrapped_positions_getter() is not implemented!')


class GenericInteractiveOutput(GenericOutput):
    def __init__(self, job):
        self._job = job

    def _key_from_cache(self, key):
        if key in self._job.interactive_cache.keys() and self._job.interactive_is_activated() and len(self._job.interactive_cache[key]) != 0:
            return self._job.interactive_cache[key]
        else: 
            return []

    def _lst_from_cache(self, key):
        lst = self._key_from_cache(key)
        if len(lst) != 0 and isinstance(lst[-1], list):
            return [np.array(out) for out in lst]
        else: 
            return lst

    def _key_from_hdf(self, key):
        return self._job['output/interactive/' + key]

    def _key_from_property(self, key, prop):
        return_lst = self._key_from_cache(key)
        hdf5_output = self._key_from_hdf(key)
        if hdf5_output is not None:
            return_lst = hdf5_output.tolist() + return_lst
        else:
            prop_result = prop(self)
            if prop_result is not None:
                return_lst = prop(self).tolist() + return_lst
        return np.array(return_lst)

    def _lst_from_property(self, key, prop=None):
        return_lst = self._lst_from_cache(key)
        hdf5_output = self._key_from_hdf(key)
        if hdf5_output is not None and len(hdf5_output) != 0:
            if isinstance(hdf5_output[-1], list):
                return_lst = [np.array(out) for out in hdf5_output] + return_lst
            else:
                return_lst = hdf5_output.tolist() + return_lst
        elif prop is not None:
            prop_result = prop(self)
            if prop_result is not None:
                return_lst = prop_result.tolist() + return_lst
        return np.array(return_lst)

    @property
    def indices(self):
        return self._lst_from_property(key='indices')

    @property
    def cells(self):
        return self._key_from_property(key='cells', prop=GenericOutput.cells.fget)

    @property
    def energy_pot(self):
        return self._key_from_property(key='energy_pot', prop=GenericOutput.energy_pot.fget)

    @property
    def energy_tot(self):
        return self._key_from_property(key='energy_tot', prop=GenericOutput.energy_tot.fget)

    @property
    def forces(self):
        return self._lst_from_property(key='forces', prop=GenericOutput.forces.fget)

    @property
    def positions(self):
        return self._lst_from_property(key='positions', prop=GenericOutput.positions.fget)

    @property
    def pressures(self):
        return self._key_from_property(key='pressures', prop=GenericOutput.pressures.fget)

    @property
    def steps(self):
        return self._key_from_property(key='steps', prop=GenericOutput.steps.fget)

    @property
    def temperature(self):
        return self._key_from_property(key='temperature', prop=GenericOutput.temperature.fget)

    @property
    def time(self):
        return self._key_from_property(key='computation_time', prop=GenericOutput.computation_time.fget)

    @property
    def unwrapped_positions(self):
        return self._lst_from_property(key='unwrapped_positions', prop=GenericOutput.unwrapped_positions.fget)

    @property
    def volume(self):
        return self._key_from_property(key='volume', prop=GenericOutput.volume.fget)

    def __dir__(self):
        return list(set(list(self._job.interactive_cache.keys()) + super(GenericOutput).__dir__()))


class InteractiveInterface(object): 
        
    def get_cell(self):
        raise NotImplementedError
        
    def set_cell(self, cell): 
        raise NotImplementedError
    
    def get_temperature(self):
        raise NotImplementedError
        
    def set_temperature(self, temperature): 
        raise NotImplementedError
    
    def get_positions(self):
        raise NotImplementedError
        
    def set_positions(self, positions): 
        raise NotImplementedError
        
    def get_forces(self):
        raise NotImplementedError
        
    def set_forces(self, forces): 
        raise NotImplementedError
        
    def get_energy_tot(self):
        raise NotImplementedError
        
    def set_energy_tot(self, energy_tot): 
        raise NotImplementedError
        
    def get_energy_pot(self):
        raise NotImplementedError
        
    def set_energy_pot(self, energy_pot): 
        raise NotImplementedError
        
    def get_pressure(self):
        raise NotImplementedError
        
    def set_pressure(self, pressure): 
        raise NotImplementedError
        
    def run_interactive(self): 
        raise NotImplementedError

