# -*- coding: utf-8 -*-

# import...
# ...from site-packages
import numpy
# ...from HydPy
from hydpy.core import parametertools
from hydpy.core import objecttools


class Responses(parametertools.Parameter):
    """Assigns different ARMA models to different discharge thresholds.

    Parameter |Responses| is not involved in the actual calculations
    during the simulation run.  Instead, it is thought for the intuitive
    handling of different ARMA models.  It can be applied as follows.

    Initially, each new `responses` object is emtpy:

    >>> from hydpy.models.arma import *
    >>> parameterstep()
    >>> responses
    responses()

    One can assign ARMA models as attributes to it:

    >>> responses.th_0_0 = ((1, 2), (3, 4, 6))

    `th_0_0` stands for a threshold discharge value of 0.0 m³/s, which the
    given ARMA model corresponds to.  For integer discharge values, one can
    omit the decimal digit:

    >>> responses.th_1 = ((), (7,))

    One can also omit the leading letters, but not the underscore:

    >>> responses.th_2_5 = ([8], range(9, 20))

    Internally, all threshold keys are brought into the standard format:

    >>> responses
    responses(th_0_0=((1.0, 2.0),
                      (3.0, 4.0, 6.0)),
              th_1_0=((),
                      (7.0,)),
              th_2_5=((8.0,),
                      (9.0, 10.0, 11.0, 12.0, 13.0, 14.0, 15.0, 16.0, 17.0,
                       18.0, 19.0)))

    All ARMA models are available via attribute access and their attribute
    names are made available to function |dir|:

    >>> 'th_1_0' in dir(responses)
    True

    Note that all iterables containing the AR and MA coefficients are
    converted to tuples, to prevent them from being changed by accident:

    >>> responses.th_1[1][0]
    7.0
    >>> responses.th_1_0[1][0] = 77
    Traceback (most recent call last):
    ...
    TypeError: 'tuple' object does not support item assignment

    Instead, one can delete and or overwrite existing ARMA models:

    >>> del responses.th_2_5
    >>> responses.th_1 = ((), (77,))
    >>> responses
    responses(th_0_0=((1.0, 2.0),
                      (3.0, 4.0, 6.0)),
              th_1_0=((),
                      (77.0,)))

    Names that cannot be identified as threshold values result in an exception:

    >>> responses.test = ((), ())
    Traceback (most recent call last):
    ...
    AttributeError: To define different response functions for parameter `responses` of element `?`, one has to pass them as keyword arguments or set them as additional attributes.  The used name must meet a specific format (see the documentation for further information).  The given name `test` does not meet this format.

    Suitable get-related attribute exceptions are also implemented:

    >>> responses.test
    Traceback (most recent call last):
    ...
    AttributeError: Parameter `responses` of element `?` does not have an attribute named `test` and the name `test` is also not a valid threshold value identifier.

    >>> responses._0_1
    Traceback (most recent call last):
    ...
    AttributeError: Parameter `responses` of element `?` does not have an attribute attribute named `_0_1` nor an arma model corresponding to a threshold value named `th_0_1`.

    The above examples show that all AR and MA coefficients are converted to
    floating point values.  It this is not possible or something else goes
    totally wrong during the definition of a new ARMA model, errors like the
    following are raised:

    >>> responses.th_10 = ()
    Traceback (most recent call last):
    ...
    IndexError: While trying to set a new threshold (th_10) coefficient pair for parameter `responses` of element `?`, the following error occurred: tuple index out of range

    Except for the mentioned conversion to floating point values, there are
    no plausibility checks performed.  You have to use other tools to gain
    plausible coefficients.  The HydPy framework offers the module
    |iuhtools| for such purposes.

    Prepare one instantaneous unit hydrograph (iuh) based on the
    Translation Diffusion Equation and another one based on the Linear
    Storage Cascade:

    >>> from hydpy.auxs.iuhtools import TranslationDiffusionEquation
    >>> tde = TranslationDiffusionEquation(d=5., u=2., x=4.)
    >>> from hydpy.auxs.iuhtools import LinearStorageCascade
    >>> lsc = LinearStorageCascade(n=2.5, k=1.)

    The following line deletes the coefficients defined above and assigns the
    ARMA approximations of both iuh models:

    >>> responses(lsc, _2=tde)

    One can change the parameter values of the translation diffusion iuh and
    assign it to the `responses` parameter, without affecting the ARMA
    coefficients of the first tde parametrization:

    >>> tde.u = 1.
    >>> responses._5 = tde
    >>> responses
    responses(th_0_0=((1.001744, -0.32693, 0.034286),
                      (0.050456, 0.199156, 0.04631, -0.004812, -0.00021)),
              th_2_0=((2.028483, -1.447371, 0.420257, -0.039595, -0.000275),
                      (0.165732, 0.061819, -0.377523, 0.215754, -0.024597,
                       -0.002684)),
              th_5_0=((3.032315, -3.506645, 1.908546, -0.479333, 0.042839,
                       0.00009),
                      (0.119252, -0.054959, -0.342744, 0.433585, -0.169102,
                       0.014189, 0.001967)))

    One may have noted the Linear Storage Cascade model was passed as
    a positional argument and was assigned to a treshold value of 0.0 m³/s
    automatically, which is the default value.  As each treshold value has to
    be unique, one can pass only one positional argument:

    >>> responses(tde, lsc)
    Traceback (most recent call last):
    ...
    ValueError: For parameter `responses` of element `?` at most one positional argument is allowed, but `2` are given.

    Checks for the repeated definition of the same threshold values are also
    performed:

    >>> responses(tde, _0=lsc, _1=tde, _1_0=lsc)
    Traceback (most recent call last):
    ...
    ValueError: For parameter `responses` of element `?` `4` arguments have been given but only `2` response functions could be prepared.  Most probably, you defined the same threshold value(s) twice.

    The number of response functions and the number of the respective AR and
    MA coefficients of a given `responses` parameter can be easily queried:

    >>> responses(_0=((1.0, 2.0),
    ...               (3.0, 4.0, 6.0)),
    ...           _1=((),
    ...               (7.0,)))
    >>> len(responses)
    2
    >>> responses.ar_orders
    (2, 0)
    >>> responses.ma_orders
    (3, 1)

    The threshold values and AR coefficients and the MA coefficients can all
    be queried as numpy arrays:

    >>> responses.thresholds
    array([ 0.,  1.])
    >>> responses.ar_coefs
    array([[  1.,   2.],
           [ nan,  nan]])
    >>> responses.ma_coefs
    array([[  3.,   4.,   6.],
           [  7.,  nan,  nan]])

    Technical notes:

    The implementation of this class is much to tricky for subpackage `models`.
    It should be generalized and moved to the framework core later.

    Furthermore, it would be nice to avoid the `nan` values in the coefficent
    representations.  But this would possibly require to define a specialized
    `arrays in list` type in Cython.
    """
    NDIM, TYPE, TIME, SPAN = 0, float, None, (None, None)

    def __init__(self):
        with objecttools.ResetAttrFuncs(self):
            self.subpars = None
            self.fastaccess = None
            self._coefs = {}
        parametertools.Parameter.__init__(self)

    def connect(self, subpars):
        self.__dict__['subpars'] = subpars

    def __call__(self, *args, **kwargs):
        self._coefs.clear()
        if len(args) > 1:
            raise ValueError(
                'For parameter `%s` of element `%s` at most one positional '
                'argument is allowed, but `%d` are given.'
                % (self.name, objecttools.devicename(self.subpars), len(args)))
        for (key, value) in kwargs.items():
            setattr(self, key, value)
        if len(args) == 1:
            setattr(self, 'th_0_0', args[0])
        if len(args)+len(kwargs) != len(self):
            raise ValueError(
                'For parameter `%s` of element `%s` `%d` arguments have been '
                'given but only `%s` response functions could be prepared.  '
                'Most probably, you defined the same threshold value(s) twice.'
                % (self.name, objecttools.devicename(self.subpars),
                   len(args)+len(kwargs), len(self)))

    def _has_predefined_attr(self, name):
        return ((name in self.__dict__ or
                 name in Responses.__dict__ or
                 name in parametertools.Parameter.__dict__) and
                not name.startswith('th_'))

    def __getattribute__(self, key):
        try:
            return object.__getattribute__(self, key)
        except AttributeError:
            pass
        try:
            std_key = self._standardize_key(key)
        except AttributeError:
            raise AttributeError(
                'Parameter `%s` of element `%s` does not have an attribute '
                'named `%s` and the name `%s` is also not a valid threshold '
                'value identifier.'
                % (self.name, objecttools.devicename(self.subpars), key, key))
        if std_key in self._coefs:
            return self._coefs[std_key]
        else:
            raise AttributeError(
                'Parameter `%s` of element `%s` does not have an attribute '
                'attribute named `%s` nor an arma model corresponding to a '
                'threshold value named `%s`.'
                % (self.name, objecttools.devicename(self.subpars),
                   key, std_key))

    def __setattr__(self, key, value):
        if self._has_predefined_attr(key):
            object.__setattr__(self, key, value)
        else:
            std_key = self._standardize_key(key)
            try:
                try:
                    self._coefs[std_key] = value.arma.coefs
                except AttributeError:
                    self._coefs[std_key] = (tuple(float(v) for v in value[0]),
                                            tuple(float(v) for v in value[1]))
            except BaseException:
                objecttools.augment_excmessage(
                    'While trying to set a new threshold (%s) coefficient '
                    'pair for parameter `%s` of element `%s`'
                    % (key, self.name, objecttools.devicename(self.subpars)))

    def __delattr__(self, key):
        std_key = self._standardize_key(key)
        if std_key in self._coefs:
            del self._coefs[std_key]

    def _standardize_key(self, key):
        try:
            tuple_ = str(key).split('_')
            if (len(tuple_) > 1) and tuple_[-2].isdigit():
                integer = int(tuple_[-2])
                decimal = int(tuple_[-1])
            else:
                integer = int(tuple_[-1])
                decimal = 0
            return '_'.join(('th', str(integer), str(decimal)))
        except BaseException:
            raise AttributeError(
                'To define different response functions for parameter `%s` of '
                'element `%s`, one has to pass them as keyword arguments or '
                'set them as additional attributes.  The used name must meet '
                'a specific format (see the documentation for further '
                'information).  The given name `%s` does not meet this format.'
                % (self.name, objecttools.devicename(self.subpars), key))

    @property
    def thresholds(self):
        """Threshold values of the response functions."""
        return numpy.array(sorted(self._key2float(key)
                                  for key in self._coefs.keys()), dtype=float)

    @staticmethod
    def _key2float(key):
        return float(key[3:].replace('_', '.'))

    def _get_orders(self, index):
        orders = []
        for _, coefs in self:
            orders.append(len(coefs[index]))
        return tuple(orders)

    @property
    def ar_orders(self):
        """Number of AR coefficients of the different response functions."""
        return self._get_orders(0)

    @property
    def ma_orders(self):
        """Number of MA coefficients of the different response functions."""
        return self._get_orders(1)

    def _get_coefs(self, index):
        orders = self._get_orders(index)
        max_orders = max(orders) if len(orders) else 0
        coefs = numpy.full((len(self), max_orders), numpy.nan)
        for idx, (order, (_, coef)) in enumerate(zip(orders, self)):
            coefs[idx, :order] = coef[index]
        return coefs

    @property
    def ar_coefs(self):
        """AR coefficients of the different response functions.

        The first row contains the AR coefficients related to the the smallest
        threshold value, the last row contains the AR coefficients related to
        the highest threshold value.  The number of columns depend on the
        highest number of AR coefficients among all response functions."""
        return self._get_coefs(0)

    @property
    def ma_coefs(self):
        """AR coefficients of the different response functions.

        The first row contains the MA coefficients related to the the smallest
        threshold value, the last row contains the AR coefficients related to
        the highest threshold value.  The number of columns depend on the
        highest number of MA coefficients among all response functions."""
        return self._get_coefs(1)

    def __len__(self):
        return len(self._coefs)

    def __iter__(self):
        for key in sorted(self._coefs.keys(),  key=self._key2float):
            yield key, self._coefs[key]

    def __repr__(self):
        strings = self.commentrepr()
        prefix = '%s(' % self.name
        blanks = ' '*len(prefix)
        if len(self):
            for idx, (th, coefs) in enumerate(self):
                subprefix = ('%s%s=' % (prefix, th) if idx == 0 else
                             '%s%s=' % (blanks, th))
                strings.append(objecttools.assignrepr_tuple2(coefs, subprefix,
                                                             75) + ',')
            strings[-1] = strings[-1][:-1] + ')'
        else:
            strings.append(prefix + ')')
        return '\n'.join(strings)

    def __dir__(self):
        attrs = objecttools.dir_(self)
        attrs.extend(self._coefs.keys())
        return attrs


class ControlParameters(parametertools.SubParameters):
    """Control parameters of arma, directly defined by the user."""
    CLASSES = (Responses,)
