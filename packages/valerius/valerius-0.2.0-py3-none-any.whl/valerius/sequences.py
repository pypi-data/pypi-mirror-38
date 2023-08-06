"""Classes for the various kinds of Biological sequence."""

from collections import Counter

class Sequence:
    """A string sequence of some kind.

    :param str string: the raw string."""

    _CODES = {}
    _type = "unknown"

    def __init__(self, string):
        self._string = string.upper()


    def __repr__(self):
        return "<{} (length: {})>".format(
         self.__class__.__name__, len(self._string)
        )


    def __str__(self):
        if len(self._string) < 25:
            return self._string
        else:
            return "{}...({} omitted)...{}".format(
             self._string[:10], len(self._string) - 20, self._string[-10:]
            )


    def __len__(self):
        return len(self._string)


    def __eq__(self, other):
        try:
            return self._string == other._string
        except AttributeError:
            return self._string == other


    def __iter__(self):
        return iter(self._string)


    def __contains__(self, substring):
        return substring in self._string


    def __getitem__(self, index):
        return self.__class__(self._string[index])


    def __setitem__(self, index, char):
        if len(char) != 1:
            raise ValueError("Can only substitute one character at a time")
        self._string = "{}{}{}".format(
         self._string[:index], char, "" if index == -1 else self._string[index + 1:]
        )


    @property
    def type(self):
        """The type of sequence.

        :rtype: ``str``"""

        return self._type


    @property
    def length(self):
        """The length of the string.

        :rtype: ``int``"""

        return len(self)


    @property
    def string(self):
        """The sequence's raw string.

        :rtype: ``str``"""

        return self._string


    @property
    def frequencies(self):
        """Returns the frequency of each character in the sequence.

        :rtype: ``Counter``"""

        return Counter(self._string)


    @property
    def codes(self):
        """Returns the list of multi-letter codes corresponding to this
        sequence.

        :rtype: ``list``"""

        return [self._CODES.get(char, "XXX") for char in self._string]



class PeptideSequence(Sequence):
    """A sequence of protein residues.

    :param str string: the raw string."""

    _CODES = {
     "V": "VAL", "I": "ILE", "L": "LEU", "E": "GLU", "Q": "GLN",
     "D": "ASP", "N": "ASN", "H": "HIS", "W": "TRP", "F": "PHE",
     "Y": "TYR", "R": "ARG", "K": "LYS", "S": "SER", "T": "THR",
     "M": "MET", "A": "ALA", "G": "GLY", "P": "PRO", "C": "CYS"
    }
    _type = "peptide"



class NucleotideSequence(Sequence):
    """A sequence of nucleotide bases.

    :param str string: the raw string."""

    _type = "nucleotide"

    @property
    def gc_content(self):
        """Returns the proportion of G and C residues in the sequence.

        :rtype: ``float``"""

        if len(self._string) == 0: return 0
        gc_bases = self._string.count("G") + self._string.count("C")
        return gc_bases / len(self._string)



class DnaSequence(NucleotideSequence):
    """A sequence of DNA nucleotide bases.

    :param str string: the raw string."""


    _CODES = {
     "A": "DA", "C": "DC", "G": "DG", "T": "DT"
    }
    _type = "DNA"



class RnaSequence(NucleotideSequence):
    """A sequence of RNA nucleotide bases.

    :param str string: the raw string."""


    _CODES = {
     "A": "A", "C": "C", "G": "G", "U": "U"
    }
    _type = "RNA"
