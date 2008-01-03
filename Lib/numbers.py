# Copyright 2007 Google, Inc. All Rights Reserved.
# Licensed to PSF under a Contributor Agreement.

"""Abstract Base Classes (ABCs) for numbers, according to PEP 3141.

TODO: Fill out more detailed documentation on the operators."""

from abc import ABCMeta, abstractmethod, abstractproperty

__all__ = ["Number", "Exact", "Inexact",
           "Complex", "Real", "Rational", "Integral",
           ]


class Number(object):
    """All numbers inherit from this class.

    If you just want to check if an argument x is a number, without
    caring what kind, use isinstance(x, Number).
    """
    __metaclass__ = ABCMeta


class Exact(Number):
    """Operations on instances of this type are exact.

    As long as the result of a homogenous operation is of the same
    type, you can assume that it was computed exactly, and there are
    no round-off errors. Laws like commutativity and associativity
    hold.
    """

Exact.register(int)
Exact.register(long)


class Inexact(Number):
    """Operations on instances of this type are inexact.

    Given X, an instance of Inexact, it is possible that (X + -X) + 3
    == 3, but X + (-X + 3) == 0. The exact form this error takes will
    vary by type, but it's generally unsafe to compare this type for
    equality.
    """

Inexact.register(complex)
Inexact.register(float)
# Inexact.register(decimal.Decimal)


class Complex(Number):
    """Complex defines the operations that work on the builtin complex type.

    In short, those are: a conversion to complex, .real, .imag, +, -,
    *, /, abs(), .conjugate, ==, and !=.

    If it is given heterogenous arguments, and doesn't have special
    knowledge about them, it should fall back to the builtin complex
    type as described below.
    """

    @abstractmethod
    def __complex__(self):
        """Return a builtin complex instance. Called for complex(self)."""

    def __bool__(self):
        """True if self != 0. Called for bool(self)."""
        return self != 0

    @abstractproperty
    def real(self):
        """Retrieve the real component of this number.

        This should subclass Real.
        """
        raise NotImplementedError

    @abstractproperty
    def imag(self):
        """Retrieve the real component of this number.

        This should subclass Real.
        """
        raise NotImplementedError

    @abstractmethod
    def __add__(self, other):
        """self + other"""
        raise NotImplementedError

    @abstractmethod
    def __radd__(self, other):
        """other + self"""
        raise NotImplementedError

    @abstractmethod
    def __neg__(self):
        """-self"""
        raise NotImplementedError

    def __pos__(self):
        """+self"""
        raise NotImplementedError

    def __sub__(self, other):
        """self - other"""
        return self + -other

    def __rsub__(self, other):
        """other - self"""
        return -self + other

    @abstractmethod
    def __mul__(self, other):
        """self * other"""
        raise NotImplementedError

    @abstractmethod
    def __rmul__(self, other):
        """other * self"""
        raise NotImplementedError

    @abstractmethod
    def __div__(self, other):
        """self / other; should promote to float or complex when necessary."""
        raise NotImplementedError

    @abstractmethod
    def __rdiv__(self, other):
        """other / self"""
        raise NotImplementedError

    @abstractmethod
    def __pow__(self, exponent):
        """self**exponent; should promote to float or complex when necessary."""
        raise NotImplementedError

    @abstractmethod
    def __rpow__(self, base):
        """base ** self"""
        raise NotImplementedError

    @abstractmethod
    def __abs__(self):
        """Returns the Real distance from 0. Called for abs(self)."""
        raise NotImplementedError

    @abstractmethod
    def conjugate(self):
        """(x+y*i).conjugate() returns (x-y*i)."""
        raise NotImplementedError

    @abstractmethod
    def __eq__(self, other):
        """self == other"""
        raise NotImplementedError

    # __ne__ is inherited from object and negates whatever __eq__ does.

Complex.register(complex)


class Real(Complex):
    """To Complex, Real adds the operations that work on real numbers.

    In short, those are: a conversion to float, trunc(), divmod,
    %, <, <=, >, and >=.

    Real also provides defaults for the derived operations.
    """

    @abstractmethod
    def __float__(self):
        """Any Real can be converted to a native float object.

        Called for float(self)."""
        raise NotImplementedError

    @abstractmethod
    def __trunc__(self):
        """trunc(self): Truncates self to an Integral.

        Returns an Integral i such that:
          * i>0 iff self>0;
          * abs(i) <= abs(self);
          * for any Integral j satisfying the first two conditions,
            abs(i) >= abs(j) [i.e. i has "maximal" abs among those].
        i.e. "truncate towards 0".
        """
        raise NotImplementedError

    @abstractmethod
    def __floor__(self):
        """Finds the greatest Integral <= self."""
        raise NotImplementedError

    @abstractmethod
    def __ceil__(self):
        """Finds the least Integral >= self."""
        raise NotImplementedError

    @abstractmethod
    def __round__(self, ndigits=None):
        """Rounds self to ndigits decimal places, defaulting to 0.

        If ndigits is omitted or None, returns an Integral, otherwise
        returns a Real. Rounds half toward even.
        """
        raise NotImplementedError

    def __divmod__(self, other):
        """divmod(self, other): The pair (self // other, self % other).

        Sometimes this can be computed faster than the pair of
        operations.
        """
        return (self // other, self % other)

    def __rdivmod__(self, other):
        """divmod(other, self): The pair (self // other, self % other).

        Sometimes this can be computed faster than the pair of
        operations.
        """
        return (other // self, other % self)

    @abstractmethod
    def __floordiv__(self, other):
        """self // other: The floor() of self/other."""
        raise NotImplementedError

    @abstractmethod
    def __rfloordiv__(self, other):
        """other // self: The floor() of other/self."""
        raise NotImplementedError

    @abstractmethod
    def __mod__(self, other):
        """self % other"""
        raise NotImplementedError

    @abstractmethod
    def __rmod__(self, other):
        """other % self"""
        raise NotImplementedError

    @abstractmethod
    def __lt__(self, other):
        """self < other

        < on Reals defines a total ordering, except perhaps for NaN."""
        raise NotImplementedError

    @abstractmethod
    def __le__(self, other):
        """self <= other"""
        raise NotImplementedError

    # Concrete implementations of Complex abstract methods.
    def __complex__(self):
        """complex(self) == complex(float(self), 0)"""
        return complex(float(self))

    @property
    def real(self):
        """Real numbers are their real component."""
        return +self

    @property
    def imag(self):
        """Real numbers have no imaginary component."""
        return 0

    def conjugate(self):
        """Conjugate is a no-op for Reals."""
        return +self

Real.register(float)
# Real.register(decimal.Decimal)


class Rational(Real, Exact):
    """.numerator and .denominator should be in lowest terms."""

    @abstractproperty
    def numerator(self):
        raise NotImplementedError

    @abstractproperty
    def denominator(self):
        raise NotImplementedError

    # Concrete implementation of Real's conversion to float.
    def __float__(self):
        """float(self) = self.numerator / self.denominator"""
        return self.numerator / self.denominator


class Integral(Rational):
    """Integral adds a conversion to long and the bit-string operations."""

    @abstractmethod
    def __long__(self):
        """long(self)"""
        raise NotImplementedError

    def __index__(self):
        """index(self)"""
        return long(self)

    @abstractmethod
    def __pow__(self, exponent, modulus=None):
        """self ** exponent % modulus, but maybe faster.

        Accept the modulus argument if you want to support the
        3-argument version of pow(). Raise a TypeError if exponent < 0
        or any argument isn't Integral. Otherwise, just implement the
        2-argument version described in Complex.
        """
        raise NotImplementedError

    @abstractmethod
    def __lshift__(self, other):
        """self << other"""
        raise NotImplementedError

    @abstractmethod
    def __rlshift__(self, other):
        """other << self"""
        raise NotImplementedError

    @abstractmethod
    def __rshift__(self, other):
        """self >> other"""
        raise NotImplementedError

    @abstractmethod
    def __rrshift__(self, other):
        """other >> self"""
        raise NotImplementedError

    @abstractmethod
    def __and__(self, other):
        """self & other"""
        raise NotImplementedError

    @abstractmethod
    def __rand__(self, other):
        """other & self"""
        raise NotImplementedError

    @abstractmethod
    def __xor__(self, other):
        """self ^ other"""
        raise NotImplementedError

    @abstractmethod
    def __rxor__(self, other):
        """other ^ self"""
        raise NotImplementedError

    @abstractmethod
    def __or__(self, other):
        """self | other"""
        raise NotImplementedError

    @abstractmethod
    def __ror__(self, other):
        """other | self"""
        raise NotImplementedError

    @abstractmethod
    def __invert__(self):
        """~self"""
        raise NotImplementedError

    # Concrete implementations of Rational and Real abstract methods.
    def __float__(self):
        """float(self) == float(long(self))"""
        return float(long(self))

    @property
    def numerator(self):
        """Integers are their own numerators."""
        return +self

    @property
    def denominator(self):
        """Integers have a denominator of 1."""
        return 1

Integral.register(int)
Integral.register(long)
