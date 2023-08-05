# -*- coding: utf-8 -*-
# pylint: disable=line-too-long, wildcard-import, unused-wildcard-import
"""ToDo

>>> from hydpy.models.hstream_v1 import *

"""
# import...
# ...from HydPy
from hydpy.exe.modelimports import *
from hydpy.core import masktools
from hydpy.core import modeltools
from hydpy.core import parametertools
from hydpy.core import sequencetools
# ...from hstream
from hydpy.models.hstream import hstream_masks
from hydpy.models.hstream import hstream_model
from hydpy.models.hstream import hstream_control
from hydpy.models.hstream import hstream_derived
from hydpy.models.hstream import hstream_states
from hydpy.models.hstream import hstream_inlets
from hydpy.models.hstream import hstream_outlets


class Model(modeltools.Model):
    """The HBV96 version of HydPy-H-Stream (|hstream_v1|)."""
    _INLET_METHODS = (hstream_model.pick_q_v1,)
    _RUN_METHODS = (hstream_model.calc_qjoints_v1,)
    _OUTLET_METHODS = (hstream_model.pass_q_v1,)


class ControlParameters(parametertools.SubParameters):
    """Control parameters of |hstream_v1|, directly defined by the user."""
    CLASSES = (hstream_control.Lag,
               hstream_control.Damp)


class DerivedParameters(parametertools.SubParameters):
    """Derived parameters of |hstream_v1|, indirectly defined by the user."""
    CLASSES = (hstream_derived.NmbSegments,
               hstream_derived.C1,
               hstream_derived.C2,
               hstream_derived.C3)


class StateSequences(sequencetools.StateSequences):
    """State sequences of |hstream_v1|."""
    CLASSES = (hstream_states.QJoints,)


class InletSequences(sequencetools.LinkSequences):
    """Upstream link sequences of |hstream_v1|."""
    CLASSES = (hstream_inlets.Q,)


class OutletSequences(sequencetools.LinkSequences):
    """Downstream link sequences of hstream_v1."""
    CLASSES = (hstream_outlets.Q,)


class Masks(masktools.Masks):
    """Masks applicable to |hstream_v1|."""
    CLASSES = hstream_masks.Masks.CLASSES


autodoc_applicationmodel()

# pylint: disable=invalid-name
tester = Tester()
cythonizer = Cythonizer()
cythonizer.complete()
