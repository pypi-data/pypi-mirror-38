# -*- coding: utf-8 -*-
from copy import deepcopy as copy
from functools import lru_cache
from glob import glob
from itertools import islice
from os import mkdir
from pathlib import Path
from urllib.request import urlretrieve

import numpy as np
from spglib import find_primitive
from spglib import get_error_message
from spglib import get_spacegroup_type
from spglib import get_symmetry_dataset

from .affine import affine_map
from .atom import Atom
from .base import AtomicStructure
from .lattice import Lattice
from .parsers import CIFParser
from .parsers import CODParser
from .parsers import PDBParser

CIF_ENTRIES = frozenset((Path(__file__).parent / "cifs").glob("*.cif"))


def symmetry_expansion(atoms, symmetry_operators):
    """
    Generate a set of unique atoms from an asymmetric cell and symmetry operators.

    Parameters
    ----------
    atoms : iterable of Atom
        Assymetric unit cell atoms. It is assumed that the atomic 
        coordinates are in fractional form.
    symmetry_operators : iterable of array_like
        Symmetry operators that generate the full unit cell.
    
    Yields
    ------
    Atom
    """
    # TODO: provide ability to reduce to primitive, niggli_reduce, etc.
    #       using spglib?
    uniques = set([])
    symmetry_operators = tuple(map(affine_map, symmetry_operators))

    for atm in atoms:
        for sym_op in symmetry_operators:
            new = copy(atm)
            new.transform(sym_op)
            new.coords_fractional[:] = np.mod(new.coords_fractional, 1)
            uniques.add(new)
    yield from uniques


class Crystal(AtomicStructure, Lattice):
    """
    The :class:`Crystal` class is a set-like container that represent crystalline structures. 

    In addition to constructing the ``Crystal`` object yourself, other constructors
    are also available (and preferred):
    
    * ``Crystal.from_cif``: create an instance from a CIF file;
    
    * ``Crystal.from_pdb``: create an instance from a Protein Data Bank entry;
    
    * ``Crystal.from_database``: create an instance from the internal database of CIF files;
    
    * ``Crystal.from_cod``: create an instance from a Crystallography Open Database entry.

    * ``Crystal.from_ase``: create an instance from an ``ase.Atoms`` instance.

    Parameters
    ----------
    unitcell : iterable of ``Atom``
        Unit cell atoms. It is assumed that the atoms are in fractional coordinates.
    lattice_vectors : iterable of array_like
        Lattice vectors. If ``lattice_vectors`` is provided as a 3x3 array, it 
        is assumed that each lattice vector is a row.
    source : str or None, optional
        Provenance, e.g. filename. Only used for bookkeeping.
    """

    builtins = frozenset(map(lambda fn: fn.stem, CIF_ENTRIES))

    def __init__(self, unitcell, lattice_vectors, source=None, **kwargs):
        super().__init__(atoms=unitcell, lattice_vectors=lattice_vectors, **kwargs)

        for atom in iter(self):
            atom.lattice = self

        self.source = source

    @classmethod
    @lru_cache(maxsize=len(builtins), typed=True)  # saves a lot of time in tests
    def from_cif(cls, path, **kwargs):
        """
        Returns a Crystal object created from a CIF 1.0, 1.1 or 2.0 file.

        Parameters
        ----------
        path : path-like
            File path
        """
        with CIFParser(filename=path, **kwargs) as parser:
            return cls(
                unitcell=symmetry_expansion(
                    parser.atoms(), parser.symmetry_operators()
                ),
                lattice_vectors=parser.lattice_vectors(),
                source=str(path),
            )

    @classmethod
    def from_database(cls, name, **kwargs):
        """ 
        Returns a Crystal object create from the internal CIF database.

        Parameters
        ----------
        name : path-like
            Name of the database entry. Available items can be retrieved from `Crystal.builtins`
        """
        if name not in cls.builtins:
            raise ValueError(
                "Entry {} is not available in the database. See `Crystal.builtins` for valid entries.".format(
                    name
                )
            )

        path = Path(__file__).parent / "cifs" / (name + ".cif")
        return cls.from_cif(path, **kwargs)

    @classmethod
    def from_cod(cls, num, revision=None, download_dir=None, overwrite=False, **kwargs):
        """ 
        Returns a Crystal object built from the Crystallography Open Database. 

        Parameters
        ----------
        num : int
            COD identification number.
        revision : int or None, optional
            Revision number. If None (default), the latest revision is used.
        download_dir : path-like object, optional
            Directory where to save the CIF file. Default is a local folder in the current directory
        overwrite : bool, optional
            Whether or not to overwrite files in cache if they exist. If no revision 
            number is provided, files will always be overwritten. 
        """
        with CODParser(num, revision, download_dir, overwrite, **kwargs) as parser:
            return cls(
                unitcell=symmetry_expansion(
                    parser.atoms(), parser.symmetry_operators()
                ),
                lattice_vectors=parser.lattice_vectors(),
                source="COD num:{n} rev:{r}".format(n=num, r=revision),
            )

    @classmethod
    def from_pdb(cls, ID, download_dir=None, overwrite=False, **kwargs):
        """
        Returns a Crystal object created from a Protein DataBank entry.

        Parameters
        ----------
        ID : str
            Protein DataBank identification. The correct .pdb file will be downloaded,
            cached and parsed.
        download_dir : path-like object, optional
            Directory where to save the PDB file.
        overwrite : bool, optional
            Whether or not to overwrite files in cache if they exist. If no revision 
            number is provided, files will always be overwritten. 
        """
        with PDBParser(ID=ID, download_dir=download_dir, **kwargs) as parser:
            return cls(
                unitcell=symmetry_expansion(
                    parser.atoms(), parser.symmetry_operators()
                ),
                lattice_vectors=parser.lattice_vectors(),
                source=parser.filename,
            )

    @classmethod
    def from_ase(cls, atoms):
        """
        Returns a Crystal object created from an ASE Atoms object.
        
        Parameters
        ----------
        atoms : ase.Atoms
            Atoms group.
        """
        lattice_vectors = atoms.get_cell()

        return cls(
            unitcell=[Atom.from_ase(atm) for atm in atoms],
            lattice_vectors=lattice_vectors,
        )

    # TODO: test against known XYZ file
    def write_xyz(self, fname, comment=None):
        """
        Generate an atomic coordinates .xyz file from a crystal structure.

        Parameters
        ----------
        fname : path-like
            The XYZ file will be written to this file. If the file already exists,
            it will be overwritten.
        comment : str or None, optional
            Comment to include at the second line of ``fname``.
        """
        # Format is specified here:
        #   http://openbabel.org/wiki/XYZ_%28format%29
        comment = comment or ""
        atom_format_str = "  {:<2}       {:10.5f}       {:10.5f}       {:10.5f}"

        with open(fname, "wt", encoding="ascii") as file:
            # First two lines are:
            #   1. Number of atoms described in the file
            #   2. Optional comment
            file.write(str(len(self)) + "\n")
            file.write(comment + "\n")

            # Write atomic data row-by-row
            # For easier human readability, atoms are sorted
            # by element
            for atom in self.itersorted():
                row = atom_format_str.format(atom.element, *atom.xyz(self))
                file.write(row + "\n")

    def _spglib_cell(self):
        """ Returns an array in spglib's cell format. """
        arr = np.asarray(self)
        return np.array(self.lattice_vectors), arr[:, 1:], arr[:, 0]

    def primitive(self, symprec=1e-2):
        """ 
        Returns a Crystal object in the primitive unit cell.
        
        Parameters
        ----------
        symprec : float, optional
            Symmetry-search distance tolerance in Cartesian coordinates [Angstroms].

        Returns
        -------
        primitive : Crystal
            Crystal with primitive cell. If primitive cell is the same size as
            the source Crystal, a reference to the source Crystal is returned.

        Raises
        ------
        RuntimeError : If primitive cell could not be found.
        
        Notes
        -----
        Optional atomic properties (e.g magnetic moment) might be lost in the reduction.
        """
        search = find_primitive(self._spglib_cell(), symprec=symprec)
        if search is None:
            raise RuntimeError("Primitive cell could not be found.")

        lattice_vectors, scaled_positions, numbers = search
        if numbers.size == len(self):  # Then there's no point in creating a new crystal
            return self

        atoms = [
            Atom(int(Z), coords=coords) for Z, coords in zip(numbers, scaled_positions)
        ]

        return Crystal(
            unitcell=atoms, lattice_vectors=lattice_vectors, source=self.source
        )

    def symmetry(self, symprec=1e-2, angle_tolerance=-1.0):
        """ 
        Returns a dictionary containing space-group information. This information 
        is computed from the crystal unit cell.
        
        Parameters
        ----------
        symprec : float, optional
            Symmetry-search distance tolerance in Cartesian coordinates [Angstroms].
        angle_tolerance: float, optional
            Symmetry-search tolerance in degrees. If the value is negative (default), 
            an internally optimized routine is used to judge symmetry.
        
        Returns
        -------
        info : dict or None
            Dictionary of space-group information. The following keys are available:

            * ``'international_symbol'``: International Tables of Crystallography 
              space-group symbol (short);

            * ``'international_full'``: International Tables of 
              Crystallography space-group full symbol;

            * ``'hall_symbol'`` : Hall symbol;

            * ``'pointgroup'`` : International Tables of 
              Crystallography point-group;

            * ``'international_number'`` : International Tables of 
              Crystallography space-group number (between 1 and 230);

            * ``'hall_number'`` : Hall number (between 1 and 531).

            If symmetry-determination has failed, None is returned.
        
        Raises
        ------
        RuntimeError : If symmetry-determination has yielded an error.
        
        Notes
        -----
        Note that crystals generated from the Protein Data Bank are often incomplete; 
        in such cases the space-group information will be incorrect.
        """
        dataset = get_symmetry_dataset(
            cell=self._spglib_cell(), symprec=symprec, angle_tolerance=angle_tolerance
        )

        if dataset:
            spg_type = get_spacegroup_type(dataset["hall_number"])

            info = {
                "international_symbol": dataset["international"],
                "hall_symbol": dataset["hall"],
                "international_number": dataset["number"],
                "hall_number": dataset["hall_number"],
                "international_full": spg_type["international_full"],
                "pointgroup": spg_type["pointgroup_international"],
            }

            err_msg = get_error_message()
            if err_msg != "no error":
                raise RuntimeError(
                    "Symmetry-determination has returned the following error: {}".format(
                        err_msg
                    )
                )

            return info

        return None

    @property
    def international_symbol(self):
        """ International Tables of Crystallography space-group short symbol. """
        return self.symmetry()["international_symbol"]

    @property
    def international_full(self):
        """ International Tables of Crystallography space-group full symbo.l """
        return self.symmetry()["international_full"]

    @property
    def hall_symbol(self):
        """ Hall symbol. """
        return self.symmetry()["hall_symbol"]

    @property
    def pointgroup(self):
        """ International Tables of Crystallography point-group. """
        return self.symmetry()["pointgroup"]

    @property
    def international_number(self):
        """ International Tables of Crystallography space-group number (between 1 and 230). """
        return self.symmetry()["international_number"]

    @property
    def hall_number(self):
        """ Hall number (between 1 and 531). """
        return self.symmetry()["hall_number"]

    def __str__(self):
        """ String representation of this instance. Atoms may be omitted. """
        return self._to_string(natoms=10)

    def __repr__(self):
        """ Verbose string representation of this instance. """
        return self._to_string(natoms=len(self))

    def _to_string(self, natoms):
        """ Generate a string representation of this Crystal. Only include
         a maximum of `natoms` if provided. """

        # Note : Crystal subclasses need not override this method
        # since the class name is dynamically determined
        rep = "< {clsname} object with following unit cell:".format(
            clsname=self.__class__.__name__
        )
        atoms = islice(self.itersorted(), natoms)

        # Note that repr(Atom(...)) includes these '< ... >'
        # We remove those for cleaner string representation
        rep += "".join(
            "\n    " + repr(atm).replace("<", "").replace(">", "").strip()
            for atm in atoms
        )

        num_omitted_atms = len(self) - natoms
        if num_omitted_atms > 0:
            rep += "\n      ... omitting {:d} atoms ...".format(num_omitted_atms)

        # Lattice parameters are split between lengths and angles
        rep += "\nLattice parameters:"
        rep += "\n    a={:.3f}Å, b={:.3f}Å, c={:.3f}Å".format(
            *self.lattice_parameters[0:3]
        )
        rep += "\n    α={:.3f}°, β={:.3f}°, γ={:.3f}°".format(
            *self.lattice_parameters[3::]
        )

        # Show stochiometric information
        rep += "\nChemical composition:"
        for chem_symbol, composition in self.chemical_composition.items():
            rep += "\n    {s}: {p:.3f}%".format(s=chem_symbol, p=100 * composition)

        rep += "\nSource: \n    {} >".format(self.source or "N/A")
        return rep
