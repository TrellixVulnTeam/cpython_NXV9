"""Classes to represent arbitrary sets (including sets of sets).

This module implements sets using dictionaries whose values are
ignored.  The usual operations (union, intersection, deletion, etc.)
are provided as both methods and operators.

Important: sets are not sequences!  While they support 'x in s',
'len(s)', and 'for x in s', none of those operations are unique for
sequences; for example, mappings support all three as well.  The
characteristic operation for sequences is subscripting with small
integers: s[i], for i in range(len(s)).  Sets don't support
subscripting at all.  Also, sequences allow multiple occurrences and
their elements have a definite order; sets on the other hand don't
record multiple occurrences and don't remember the order of element
insertion (which is why they don't support s[i]).

The following classes are provided:

BaseSet -- All the operations common to both mutable and immutable
    sets. This is an abstract class, not meant to be directly
    instantiated.

Set -- Mutable sets, subclass of BaseSet; not hashable.

ImmutableSet -- Immutable sets, subclass of BaseSet; hashable.
    An iterable argument is mandatory to create an ImmutableSet.

_TemporarilyImmutableSet -- Not a subclass of BaseSet: just a wrapper
    around a Set, hashable, giving the same hash value as the
    immutable set equivalent would have.  Do not use this class
    directly.

Only hashable objects can be added to a Set. In particular, you cannot
really add a Set as an element to another Set; if you try, what is
actually added is an ImmutableSet built from it (it compares equal to
the one you tried adding).

When you ask if `x in y' where x is a Set and y is a Set or
ImmutableSet, x is wrapped into a _TemporarilyImmutableSet z, and
what's tested is actually `z in y'.

"""

# Code history:
#
# - Greg V. Wilson wrote the first version, using a different approach
#   to the mutable/immutable problem, and inheriting from dict.
#
# - Alex Martelli modified Greg's version to implement the current
#   Set/ImmutableSet approach, and make the data an attribute.
#
# - Guido van Rossum rewrote much of the code, made some API changes,
#   and cleaned up the docstrings.
#
# - Raymond Hettinger added a number of speedups and other
#   improvements.


__all__ = ['BaseSet', 'Set', 'ImmutableSet']


class BaseSet(object):
    """Common base class for mutable and immutable sets."""

    __slots__ = ['_data']

    # Constructor

    def __init__(self):
        """This is an abstract class."""
        # Don't call this from a concrete subclass!
        if self.__class__ is BaseSet:
            raise TypeError, ("BaseSet is an abstract class.  "
                              "Use Set or ImmutableSet.")

    # Standard protocols: __len__, __repr__, __str__, __iter__

    def __len__(self):
        """Return the number of elements of a set."""
        return len(self._data)

    def __repr__(self):
        """Return string representation of a set.

        This looks like 'Set([<list of elements>])'.
        """
        return self._repr()

    # __str__ is the same as __repr__
    __str__ = __repr__

    def _repr(self, sorted=False):
        elements = self._data.keys()
        if sorted:
            elements.sort()
        return '%s(%r)' % (self.__class__.__name__, elements)

    def __iter__(self):
        """Return an iterator over the elements or a set.

        This is the keys iterator for the underlying dict.
        """
        return self._data.iterkeys()

    # Equality comparisons using the underlying dicts

    def __eq__(self, other):
        self._binary_sanity_check(other)
        return self._data == other._data

    def __ne__(self, other):
        self._binary_sanity_check(other)
        return self._data != other._data

    # Copying operations

    def copy(self):
        """Return a shallow copy of a set."""
        result = self.__class__()
        result._data.update(self._data)
        return result

    __copy__ = copy # For the copy module

    def __deepcopy__(self, memo):
        """Return a deep copy of a set; used by copy module."""
        # This pre-creates the result and inserts it in the memo
        # early, in case the deep copy recurses into another reference
        # to this same set.  A set can't be an element of itself, but
        # it can certainly contain an object that has a reference to
        # itself.
        from copy import deepcopy
        result = self.__class__()
        memo[id(self)] = result
        data = result._data
        value = True
        for elt in self:
            data[deepcopy(elt, memo)] = value
        return result

    # Standard set operations: union, intersection, both differences.
    # Each has an operator version (e.g. __or__, invoked with |) and a
    # method version (e.g. union).
    # Subtle:  Each pair requires distinct code so that the outcome is
    # correct when the type of other isn't suitable.  For example, if
    # we did "union = __or__" instead, then Set().union(3) would return
    # NotImplemented instead of raising TypeError (albeit that *why* it
    # raises TypeError as-is is also a bit subtle).

    def __or__(self, other):
        """Return the union of two sets as a new set.

        (I.e. all elements that are in either set.)
        """
        if not isinstance(other, BaseSet):
            return NotImplemented
        result = self.__class__()
        result._data = self._data.copy()
        result._data.update(other._data)
        return result

    def union(self, other):
        """Return the union of two sets as a new set.

        (I.e. all elements that are in either set.)
        """
        return self | other

    def __and__(self, other):
        """Return the intersection of two sets as a new set.

        (I.e. all elements that are in both sets.)
        """
        if not isinstance(other, BaseSet):
            return NotImplemented
        if len(self) <= len(other):
            little, big = self, other
        else:
            little, big = other, self
        common = filter(big._data.has_key, little._data)
        return self.__class__(common)

    def intersection(self, other):
        """Return the intersection of two sets as a new set.

        (I.e. all elements that are in both sets.)
        """
        return self & other

    def __xor__(self, other):
        """Return the symmetric difference of two sets as a new set.

        (I.e. all elements that are in exactly one of the sets.)
        """
        if not isinstance(other, BaseSet):
            return NotImplemented
        result = self.__class__()
        data = result._data
        value = True
        selfdata = self._data
        otherdata = other._data
        for elt in selfdata:
            if elt not in otherdata:
                data[elt] = value
        for elt in otherdata:
            if elt not in selfdata:
                data[elt] = value
        return result

    def symmetric_difference(self, other):
        """Return the symmetric difference of two sets as a new set.

        (I.e. all elements that are in exactly one of the sets.)
        """
        return self ^ other

    def  __sub__(self, other):
        """Return the difference of two sets as a new Set.

        (I.e. all elements that are in this set and not in the other.)
        """
        if not isinstance(other, BaseSet):
            return NotImplemented
        result = self.__class__()
        data = result._data
        otherdata = other._data
        value = True
        for elt in self:
            if elt not in otherdata:
                data[elt] = value
        return result

    def difference(self, other):
        """Return the difference of two sets as a new Set.

        (I.e. all elements that are in this set and not in the other.)
        """
        return self - other

    # Membership test

    def __contains__(self, element):
        """Report whether an element is a member of a set.

        (Called in response to the expression `element in self'.)
        """
        try:
            return element in self._data
        except TypeError:
            transform = getattr(element, "_as_temporarily_immutable", None)
            if transform is None:
                raise # re-raise the TypeError exception we caught
            return transform() in self._data

    # Subset and superset test

    def issubset(self, other):
        """Report whether another set contains this set."""
        self._binary_sanity_check(other)
        if len(self) > len(other):  # Fast check for obvious cases
            return False
        otherdata = other._data
        for elt in self:
            if elt not in otherdata:
                return False
        return True

    def issuperset(self, other):
        """Report whether this set contains another set."""
        self._binary_sanity_check(other)
        if len(self) < len(other):  # Fast check for obvious cases
            return False
        selfdata = self._data
        for elt in other:
            if elt not in selfdata:
                return False
        return True

    # Inequality comparisons using the is-subset relation.
    __le__ = issubset
    __ge__ = issuperset

    def __lt__(self, other):
        self._binary_sanity_check(other)
        return len(self) < len(other) and self.issubset(other)

    def __gt__(self, other):
        self._binary_sanity_check(other)
        return len(self) > len(other) and self.issuperset(other)

    # Assorted helpers

    def _binary_sanity_check(self, other):
        # Check that the other argument to a binary operation is also
        # a set, raising a TypeError otherwise.
        if not isinstance(other, BaseSet):
            raise TypeError, "Binary operation only permitted between sets"

    def _compute_hash(self):
        # Calculate hash code for a set by xor'ing the hash codes of
        # the elements.  This ensures that the hash code does not depend
        # on the order in which elements are added to the set.  This is
        # not called __hash__ because a BaseSet should not be hashable;
        # only an ImmutableSet is hashable.
        result = 0
        for elt in self:
            result ^= hash(elt)
        return result

    def _update(self, iterable):
        # The main loop for update() and the subclass __init__() methods.
        data = self._data

        # Use the fast update() method when a dictionary is available.
        if isinstance(iterable, BaseSet):
            data.update(iterable._data)
            return
        if isinstance(iterable, dict):
            data.update(iterable)
            return

        value = True
        it = iter(iterable)
        while True:
            try:
                for element in it:
                    data[element] = value
                return
            except TypeError:
                transform = getattr(element, "_as_immutable", None)
                if transform is None:
                    raise # re-raise the TypeError exception we caught
                data[transform()] = value


class ImmutableSet(BaseSet):
    """Immutable set class."""

    __slots__ = ['_hashcode']

    # BaseSet + hashing

    def __init__(self, iterable=None):
        """Construct an immutable set from an optional iterable."""
        self._hashcode = None
        self._data = {}
        if iterable is not None:
            self._update(iterable)

    def __hash__(self):
        if self._hashcode is None:
            self._hashcode = self._compute_hash()
        return self._hashcode


class Set(BaseSet):
    """ Mutable set class."""

    __slots__ = []

    # BaseSet + operations requiring mutability; no hashing

    def __init__(self, iterable=None):
        """Construct a set from an optional iterable."""
        self._data = {}
        if iterable is not None:
            self._update(iterable)

    def __hash__(self):
        """A Set cannot be hashed."""
        # We inherit object.__hash__, so we must deny this explicitly
        raise TypeError, "Can't hash a Set, only an ImmutableSet."

    # In-place union, intersection, differences.
    # Subtle:  The xyz_update() functions deliberately return None,
    # as do all mutating operations on built-in container types.
    # The __xyz__ spellings have to return self, though.

    def __ior__(self, other):
        """Update a set with the union of itself and another."""
        self._binary_sanity_check(other)
        self._data.update(other._data)
        return self

    def union_update(self, other):
        """Update a set with the union of itself and another."""
        self |= other

    def __iand__(self, other):
        """Update a set with the intersection of itself and another."""
        self._binary_sanity_check(other)
        self._data = (self & other)._data
        return self

    def intersection_update(self, other):
        """Update a set with the intersection of itself and another."""
        self &= other

    def __ixor__(self, other):
        """Update a set with the symmetric difference of itself and another."""
        self._binary_sanity_check(other)
        data = self._data
        value = True
        for elt in other:
            if elt in data:
                del data[elt]
            else:
                data[elt] = value
        return self

    def symmetric_difference_update(self, other):
        """Update a set with the symmetric difference of itself and another."""
        self ^= other

    def __isub__(self, other):
        """Remove all elements of another set from this set."""
        self._binary_sanity_check(other)
        data = self._data
        for elt in other:
            if elt in data:
                del data[elt]
        return self

    def difference_update(self, other):
        """Remove all elements of another set from this set."""
        self -= other

    # Python dict-like mass mutations: update, clear

    def update(self, iterable):
        """Add all values from an iterable (such as a list or file)."""
        self._update(iterable)

    def clear(self):
        """Remove all elements from this set."""
        self._data.clear()

    # Single-element mutations: add, remove, discard

    def add(self, element):
        """Add an element to a set.

        This has no effect if the element is already present.
        """
        try:
            self._data[element] = True
        except TypeError:
            transform = getattr(element, "_as_immutable", None)
            if transform is None:
                raise # re-raise the TypeError exception we caught
            self._data[transform()] = True

    def remove(self, element):
        """Remove an element from a set; it must be a member.

        If the element is not a member, raise a KeyError.
        """
        try:
            del self._data[element]
        except TypeError:
            transform = getattr(element, "_as_temporarily_immutable", None)
            if transform is None:
                raise # re-raise the TypeError exception we caught
            del self._data[transform()]

    def discard(self, element):
        """Remove an element from a set if it is a member.

        If the element is not a member, do nothing.
        """
        try:
            self.remove(element)
        except KeyError:
            pass

    def pop(self):
        """Remove and return an arbitrary set element."""
        return self._data.popitem()[0]

    def _as_immutable(self):
        # Return a copy of self as an immutable set
        return ImmutableSet(self)

    def _as_temporarily_immutable(self):
        # Return self wrapped in a temporarily immutable set
        return _TemporarilyImmutableSet(self)


class _TemporarilyImmutableSet(BaseSet):
    # Wrap a mutable set as if it was temporarily immutable.
    # This only supplies hashing and equality comparisons.

    def __init__(self, set):
        self._set = set
        self._data = set._data  # Needed by ImmutableSet.__eq__()

    def __hash__(self):
        return self._set._compute_hash()
