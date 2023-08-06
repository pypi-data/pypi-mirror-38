#!/usr/bin/env python3
"""CarvPath library for Python3.

This module provides a Python3 implementation of CarvPath data designations as used
in the computer-forensics file-systems CarvFS and MattockFS.

"""

class SparseFragment(object):
    """The SparseFragment class represents a sparse section in a CarvPath designation"""
    def __init__(self, size):
        if isinstance(size, str):
            if size[0] != "S":
                raise ValueError("Invalid sparse fragment string.")
            self._size = int(size[1:])
        else:
            if isinstance(size, int):
                self._size = size
            else:
                raise TypeError("Constructor takes int or string")
        if self._size < 1:
            raise ValueError("Size of sparse section should be at least one byte")
    def offset(self):
        """Retreive offset; This duck-typeing method throws an exception in this class
        as sparse fragments don't have an offset"""
        # pylint: disable=no-self-use
        raise ReferenceError("No offset on sparse fragment")
    def size(self):
        """Retreive size of sparse fragment."""
        return self._size
    def is_sparse(self):
        """Check fragment subtype"""
        # pylint: disable=no-self-use
        return True
    def __str__(self):
        return "S" + str(self._size)
    def __iadd__(self, other):
        if other.is_sparse():
            self._size += other.size()
        else:
            raise TypeError("Can only add sparse to sparse")
        return self
    def __add__(self, other):
        if other.is_sparse():
            return SparseFragment(self._size + other.size())
        else:
            raise TypeError("Can only add sparse to sparse")
    def adjacent(self, other):
        """Check if an other fragment is adjacent to this one."""
        # pylint: disable=no-self-use
        return  other.is_sparse()
    def __call__(self, poffset, child):
        roffset = child.offset() - poffset
        rlast = roffset + child.size()
        if rlast > self.size():
            rlast = self.size()
        if roffset < 0:
            roffset = 0
        rsize = rlast - roffset
        if rsize > 0:
            yield SparseFragment(rsize)

class BaseFragment(object):
    """The BaseFragment class represents a single archive fragment within a CarvPath designation."""
    def __init__(self, offset, size=None):
        if size is None:
            if isinstance(offset, str):
                offset2, size2 = offset.split("+")
                self._offset = int(offset2)
                self._size = int(size2)
            else:
                raise TypeError("Constructor takes two integers or a string")
        else:
            if isinstance(offset, int):
                self._offset = offset
            else:
                raise TypeError("Constructor takes two integers or a string")
            if isinstance(size, int):
                self._size = size
            else:
                raise TypeError("Constructor takes two integers or a string")
        if self._offset < 0:
            raise ValueError("Offset can not be negative")
        if self._size < 1:
            raise ValueError("Size can not be less than one byte")
    def offset(self):
        """Fetch fragment offset."""
        return self._offset
    def size(self):
        """Fetch fragment size."""
        return self._size
    def is_sparse(self):
        """Check fragment subtype"""
        # pylint: disable=no-self-use
        return False
    def __str__(self):
        return str(self._offset) + "+" + str(self._size)
    def __iadd__(self, other):
        if hasattr(other, 'is_sparse'):
            if other.is_sparse():
                raise TypeError("Can only add regular fragment to regular fragment")
            else:
                if other.offset() == self._offset + self._size:
                    self._size += other.size()
                else:
                    raise ValueError("Fragments not directly adjacent")
        else:
            raise TypeError("Can only add regular fragment to regular fragment")
        return self
    def __add__(self, other):
        if hasattr(other, 'is_sparse'):
            if other.is_sparse():
                raise TypeError("Can only add regular fragment to regular fragment")
            else:
                if other.offset() == self._offset + self._size:
                    return BaseFragment(self._offset, self._size + other.offset())
                else:
                    raise ValueError("Fragments not directly adjacent")
        else:
            raise TypeError("Can only add regular fragment to regular fragment")
    def adjacent(self, other):
        """Check if an other fragment is adjacent to this one."""
        if other.is_sparse():
            return False
        if other.offset() == self._offset + self._size:
            return True
        return False
    def __call__(self, poffset, child):
        roffset = child.offset() - poffset
        rlast = roffset + child.size()
        if rlast > self.size():
            rlast = self.size()
        if roffset < 0:
            roffset = 0
        rsize = rlast - roffset
        if rsize > 0:
            yield BaseFragment(self.offset() + roffset, rsize)

class CarvPath(object):
    """The CarvPath class represents a CarvPath designation
    that is made up of one or more fragments"""
    def __init__(self, arg):
        self.fragments = []
        if isinstance(arg, str):
            frgs = arg.split("/")
            frags = frgs[0].split("_")
            for frag in frags:
                if frag[0] == "S":
                    self += SparseFragment(frag)
                else:
                    self += BaseFragment(frag)
            if len(frgs) > 1:
                layers = "/".join(frgs[1:])
                self.fragments = self[layers].fragments
        else:
            for frag in arg:
                self += frag
    def __str__(self):
        rparts = []
        for frag in self.fragments:
            rparts.append(str(frag))
        return "_".join(rparts)
    def __iadd__(self, other):
        if isinstance(other, CarvPath):
            for fragment in other.fragments:
                self += fragment
        else:
            if hasattr(other, 'is_sparse'):
                if not self.fragments:
                    self.fragments.append(other)
                else:
                    if self.fragments[-1].adjacent(other):
                        self.fragments[-1] += other
                    else:
                        self.fragments.append(other)
            else:
                raise TypeError("Can only add CarvPath or Fragment to CarvPath")
        return self
    def __add__(self, other):
        rval = CarvPath([])
        rval.fragments = self.fragments
        if isinstance(other, CarvPath):
            for fragment in other.fragments:
                rval += fragment
        else:
            if hasattr(other, 'is_sparse'):
                rval += other
            else:
                raise TypeError("Can only add CarvPath or Fragment to CarvPath")
        return rval
    def size(self):
        """Fetch the size of the entire CarvPath"""
        rval = 0
        for fragment in self.fragments:
            rval += fragment.size()
        return rval
    def __iter__(self):
        return CpIter(self)
    def __getitem__(self, key):
        if isinstance(key, int):
            if key < 0 or key >= len(self.fragments):
                raise IndexError
            return self.fragments[key]
        else:
            if isinstance(key, str):
                rval = CarvPath([])
                subcp = CarvPath(key)
                for fragment in subcp:
                    rval += self[fragment]
                return rval
            else:
                if hasattr(key, 'is_sparse'):
                    if key.is_sparse():
                        return CarvPath([key])
                    frags = []
                    for fragment in self.flatten(key):
                        frags.append(fragment)
                    return CarvPath(frags)
                else:
                    raise TypeError("Index should be int, string or fragment.")
    def flatten(self, childfragment):
        """Flatten a multi-layer CarvPath into a single level 0 CarvPath."""
        parentoffset = 0
        flatsize = 0
        for parent_fragment in self.fragments:
            for flattened_fragment in  parent_fragment(parentoffset, childfragment):
                flatsize += flattened_fragment.size()
                yield flattened_fragment
            parentoffset += parent_fragment.size()
        if childfragment.size() != flatsize:
            raise RuntimeError("flatten results in bogus flattened size")


class CpIter(object):
    """Helper class for itterating CarvPath fragments."""
    # pylint: disable=too-few-public-methods
    def __init__(self, cp):
        self.carvpath = cp
        self.next = 0
    def __next__(self):
        if self.next > len(self.carvpath.fragments) -1:
            raise StopIteration
        else:
            self.next += 1
            return self.carvpath.fragments[self.next - 1]
