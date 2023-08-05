#!python
#cython: boundscheck=False
#cython: wraparound=False
#cython: initializedcheck=False
import numpy
cimport numpy
from libc.math cimport exp, fabs, log
from libc.stdio cimport *
from libc.stdlib cimport *
import cython
from cpython.mem cimport PyMem_Malloc
from cpython.mem cimport PyMem_Realloc
from cpython.mem cimport PyMem_Free
from hydpy.cythons.autogen cimport pointerutils
from hydpy.cythons.autogen cimport configutils
from hydpy.cythons.autogen cimport smoothutils
from hydpy.cythons.autogen cimport annutils

@cython.final
cdef class Parameters(object):
    cdef public ControlParameters control
    cdef public DerivedParameters derived
@cython.final
cdef class ControlParameters(object):
    cdef public numpy.int32_t n
    cdef public double[:] w
    cdef public double[:] v
    cdef public double[:,:] q
    cdef public double maxdt
    cdef public double[:] maxdw
    cdef public double[:] verzw
@cython.final
cdef class DerivedParameters(object):
    cdef public numpy.int32_t[:] toy
    cdef public double seconds
    cdef public numpy.int32_t nmbsubsteps
    cdef public double[:,:] vq
@cython.final
cdef class Sequences(object):
    cdef public InletSequences inlets
    cdef public FluxSequences fluxes
    cdef public StateSequences states
    cdef public AideSequences aides
    cdef public OutletSequences outlets
    cdef public StateSequences old_states
    cdef public StateSequences new_states
@cython.final
cdef class InletSequences(object):
    cdef double **q
    cdef public int len_q
    cdef public int _q_ndim
    cdef public int _q_length
    cdef public int _q_length_0
    cpdef inline alloc(self, name, int length):
        if name == "q":
            self._q_length_0 = length
            self.q = <double**> PyMem_Malloc(length * sizeof(double*))
    cpdef inline dealloc(self):
        PyMem_Free(self.q)
    cpdef inline set_pointer1d(self, str name, pointerutils.PDouble value, int idx):
        if name == "q":
            self.q[idx] = value.p_value
@cython.final
cdef class FluxSequences(object):
    cdef public double qz
    cdef public int _qz_ndim
    cdef public int _qz_length
    cdef public bint _qz_diskflag
    cdef public str _qz_path
    cdef FILE *_qz_file
    cdef public bint _qz_ramflag
    cdef public double[:] _qz_array
    cdef public double qa
    cdef public int _qa_ndim
    cdef public int _qa_length
    cdef public bint _qa_diskflag
    cdef public str _qa_path
    cdef FILE *_qa_file
    cdef public bint _qa_ramflag
    cdef public double[:] _qa_array
    cpdef open_files(self, int idx):
        if self._qz_diskflag:
            self._qz_file = fopen(str(self._qz_path).encode(), "rb+")
            fseek(self._qz_file, idx*8, SEEK_SET)
        if self._qa_diskflag:
            self._qa_file = fopen(str(self._qa_path).encode(), "rb+")
            fseek(self._qa_file, idx*8, SEEK_SET)
    cpdef inline close_files(self):
        if self._qz_diskflag:
            fclose(self._qz_file)
        if self._qa_diskflag:
            fclose(self._qa_file)
    cpdef inline void save_data(self, int idx)  nogil:
        cdef int jdx0, jdx1, jdx2, jdx3, jdx4, jdx5
        if self._qz_diskflag:
            fwrite(&self.qz, 8, 1, self._qz_file)
        elif self._qz_ramflag:
            self._qz_array[idx] = self.qz
        if self._qa_diskflag:
            fwrite(&self.qa, 8, 1, self._qa_file)
        elif self._qa_ramflag:
            self._qa_array[idx] = self.qa
@cython.final
cdef class StateSequences(object):
    cdef public double v
    cdef public int _v_ndim
    cdef public int _v_length
    cdef public bint _v_diskflag
    cdef public str _v_path
    cdef FILE *_v_file
    cdef public bint _v_ramflag
    cdef public double[:] _v_array
    cdef public double w
    cdef public int _w_ndim
    cdef public int _w_length
    cdef public bint _w_diskflag
    cdef public str _w_path
    cdef FILE *_w_file
    cdef public bint _w_ramflag
    cdef public double[:] _w_array
    cpdef open_files(self, int idx):
        if self._v_diskflag:
            self._v_file = fopen(str(self._v_path).encode(), "rb+")
            fseek(self._v_file, idx*8, SEEK_SET)
        if self._w_diskflag:
            self._w_file = fopen(str(self._w_path).encode(), "rb+")
            fseek(self._w_file, idx*8, SEEK_SET)
    cpdef inline close_files(self):
        if self._v_diskflag:
            fclose(self._v_file)
        if self._w_diskflag:
            fclose(self._w_file)
    cpdef inline void save_data(self, int idx)  nogil:
        cdef int jdx0, jdx1, jdx2, jdx3, jdx4, jdx5
        if self._v_diskflag:
            fwrite(&self.v, 8, 1, self._v_file)
        elif self._v_ramflag:
            self._v_array[idx] = self.v
        if self._w_diskflag:
            fwrite(&self.w, 8, 1, self._w_file)
        elif self._w_ramflag:
            self._w_array[idx] = self.w
@cython.final
cdef class AideSequences(object):
    cdef public double qa
    cdef public int _qa_ndim
    cdef public int _qa_length
    cdef public double vq
    cdef public int _vq_ndim
    cdef public int _vq_length
    cdef public double v
    cdef public int _v_ndim
    cdef public int _v_length
@cython.final
cdef class OutletSequences(object):
    cdef double *q
    cdef public int _q_ndim
    cdef public int _q_length
    cpdef inline set_pointer0d(self, str name, pointerutils.PDouble value):
        if name == "q":
            self.q = value.p_value

@cython.final
cdef class Model(object):
    cdef public int idx_sim
    cdef public Parameters parameters
    cdef public Sequences sequences
    cpdef inline void doit(self, int idx)  nogil:
        self.idx_sim = idx
        self.update_inlets()
        self.run()
        self.new2old()
        self.update_outlets()
    cpdef inline void open_files(self):
        self.sequences.fluxes.open_files(self.idx_sim)
        self.sequences.states.open_files(self.idx_sim)
    cpdef inline void close_files(self):
        self.sequences.fluxes.close_files()
        self.sequences.states.close_files()
    cpdef inline void save_data(self, int idx) nogil:
        self.sequences.fluxes.save_data(self.idx_sim)
        self.sequences.states.save_data(self.idx_sim)
    cpdef inline void new2old(self) nogil:
        cdef int jdx0, jdx1, jdx2, jdx3, jdx4, jdx5
        self.sequences.old_states.v = self.sequences.new_states.v
        self.sequences.old_states.w = self.sequences.new_states.w
    cpdef inline void run(self) nogil:
        self.solve_dv_dt_v1()
        self.interp_w_v1()
        self.corr_dw_v1()
        self.modify_qa_v1()
    cpdef inline void update_inlets(self) nogil:
        self.pick_q_v1()
    cpdef inline void update_outlets(self) nogil:
        self.pass_q_v1()
    cpdef inline void update_receivers(self, int idx) nogil:
        self.idx_sim = idx
        pass
    cpdef inline void update_senders(self, int idx) nogil:
        self.idx_sim = idx
        pass

    cpdef inline void solve_dv_dt_v1(self)  nogil:
        cdef int i
        self.sequences.fluxes.qa = 0.
        self.sequences.aides.v = self.sequences.old_states.v
        for i in range(self.parameters.derived.nmbsubsteps):
            self.calc_vq()
            self.interp_qa()
            self.calc_v_qa()
            self.sequences.fluxes.qa = self.sequences.fluxes.qa + (self.sequences.aides.qa)
        self.sequences.fluxes.qa = self.sequences.fluxes.qa / (self.parameters.derived.nmbsubsteps)
        self.sequences.new_states.v = self.sequences.aides.v
    cpdef inline void interp_w_v1(self)  nogil:
        cdef int jdx
        for jdx in range(1, self.parameters.control.n):
            if self.parameters.control.v[jdx] >= self.sequences.new_states.v:
                break
        self.sequences.new_states.w = ((self.sequences.new_states.v-self.parameters.control.v[jdx-1]) *             (self.parameters.control.w[jdx]-self.parameters.control.w[jdx-1]) /             (self.parameters.control.v[jdx]-self.parameters.control.v[jdx-1]) +             self.parameters.control.w[jdx-1])
    cpdef inline void corr_dw_v1(self)  nogil:
        cdef int idx
        idx = self.parameters.derived.toy[self.idx_sim]
        if (self.parameters.control.maxdw[idx] > 0.) and ((self.sequences.old_states.w-self.sequences.new_states.w) > self.parameters.control.maxdw[idx]):
            self.sequences.new_states.w = self.sequences.old_states.w-self.parameters.control.maxdw[idx]
            self.interp_v()
            self.sequences.fluxes.qa = self.sequences.fluxes.qz+(self.sequences.old_states.v-self.sequences.new_states.v)/self.parameters.derived.seconds
    cpdef inline void modify_qa_v1(self)  nogil:
        cdef int idx
        idx = self.parameters.derived.toy[self.idx_sim]
        self.sequences.fluxes.qa = max(self.sequences.fluxes.qa-self.parameters.control.verzw[idx], 0.)
    cpdef inline void solve_dv_dt(self)  nogil:
        cdef int i
        self.sequences.fluxes.qa = 0.
        self.sequences.aides.v = self.sequences.old_states.v
        for i in range(self.parameters.derived.nmbsubsteps):
            self.calc_vq()
            self.interp_qa()
            self.calc_v_qa()
            self.sequences.fluxes.qa = self.sequences.fluxes.qa + (self.sequences.aides.qa)
        self.sequences.fluxes.qa = self.sequences.fluxes.qa / (self.parameters.derived.nmbsubsteps)
        self.sequences.new_states.v = self.sequences.aides.v
    cpdef inline void interp_w(self)  nogil:
        cdef int jdx
        for jdx in range(1, self.parameters.control.n):
            if self.parameters.control.v[jdx] >= self.sequences.new_states.v:
                break
        self.sequences.new_states.w = ((self.sequences.new_states.v-self.parameters.control.v[jdx-1]) *             (self.parameters.control.w[jdx]-self.parameters.control.w[jdx-1]) /             (self.parameters.control.v[jdx]-self.parameters.control.v[jdx-1]) +             self.parameters.control.w[jdx-1])
    cpdef inline void corr_dw(self)  nogil:
        cdef int idx
        idx = self.parameters.derived.toy[self.idx_sim]
        if (self.parameters.control.maxdw[idx] > 0.) and ((self.sequences.old_states.w-self.sequences.new_states.w) > self.parameters.control.maxdw[idx]):
            self.sequences.new_states.w = self.sequences.old_states.w-self.parameters.control.maxdw[idx]
            self.interp_v()
            self.sequences.fluxes.qa = self.sequences.fluxes.qz+(self.sequences.old_states.v-self.sequences.new_states.v)/self.parameters.derived.seconds
    cpdef inline void modify_qa(self)  nogil:
        cdef int idx
        idx = self.parameters.derived.toy[self.idx_sim]
        self.sequences.fluxes.qa = max(self.sequences.fluxes.qa-self.parameters.control.verzw[idx], 0.)
    cpdef inline void interp_v_v1(self)  nogil:
        cdef int jdx
        for jdx in range(1, self.parameters.control.n):
            if self.parameters.control.w[jdx] >= self.sequences.new_states.w:
                break
        self.sequences.new_states.v = ((self.sequences.new_states.w-self.parameters.control.w[jdx-1]) *             (self.parameters.control.v[jdx]-self.parameters.control.v[jdx-1]) /             (self.parameters.control.w[jdx]-self.parameters.control.w[jdx-1]) +             self.parameters.control.v[jdx-1])
    cpdef inline void calc_vq_v1(self)  nogil:
        self.sequences.aides.vq = 2.*self.sequences.aides.v+self.parameters.derived.seconds/self.parameters.derived.nmbsubsteps*self.sequences.fluxes.qz
    cpdef inline void interp_qa_v1(self)  nogil:
        cdef int jdx
        cdef int idx
        idx = self.parameters.derived.toy[self.idx_sim]
        for jdx in range(1, self.parameters.control.n):
            if self.parameters.derived.vq[idx, jdx] >= self.sequences.aides.vq:
                break
        self.sequences.aides.qa = ((self.sequences.aides.vq-self.parameters.derived.vq[idx, jdx-1]) *              (self.parameters.control.q[idx, jdx]-self.parameters.control.q[idx, jdx-1]) /              (self.parameters.derived.vq[idx, jdx]-self.parameters.derived.vq[idx, jdx-1]) +              self.parameters.control.q[idx, jdx-1])
        self.sequences.aides.qa = max(self.sequences.aides.qa, 0.)
    cpdef inline void calc_v_qa_v1(self)  nogil:
        self.sequences.aides.qa = min(self.sequences.aides.qa, self.sequences.fluxes.qz+self.parameters.derived.nmbsubsteps/self.parameters.derived.seconds*self.sequences.aides.v)
        self.sequences.aides.v = max(self.sequences.aides.v+self.parameters.derived.seconds/self.parameters.derived.nmbsubsteps*(self.sequences.fluxes.qz-self.sequences.aides.qa), 0.)
    cpdef inline void interp_v(self)  nogil:
        cdef int jdx
        for jdx in range(1, self.parameters.control.n):
            if self.parameters.control.w[jdx] >= self.sequences.new_states.w:
                break
        self.sequences.new_states.v = ((self.sequences.new_states.w-self.parameters.control.w[jdx-1]) *             (self.parameters.control.v[jdx]-self.parameters.control.v[jdx-1]) /             (self.parameters.control.w[jdx]-self.parameters.control.w[jdx-1]) +             self.parameters.control.v[jdx-1])
    cpdef inline void calc_vq(self)  nogil:
        self.sequences.aides.vq = 2.*self.sequences.aides.v+self.parameters.derived.seconds/self.parameters.derived.nmbsubsteps*self.sequences.fluxes.qz
    cpdef inline void interp_qa(self)  nogil:
        cdef int jdx
        cdef int idx
        idx = self.parameters.derived.toy[self.idx_sim]
        for jdx in range(1, self.parameters.control.n):
            if self.parameters.derived.vq[idx, jdx] >= self.sequences.aides.vq:
                break
        self.sequences.aides.qa = ((self.sequences.aides.vq-self.parameters.derived.vq[idx, jdx-1]) *              (self.parameters.control.q[idx, jdx]-self.parameters.control.q[idx, jdx-1]) /              (self.parameters.derived.vq[idx, jdx]-self.parameters.derived.vq[idx, jdx-1]) +              self.parameters.control.q[idx, jdx-1])
        self.sequences.aides.qa = max(self.sequences.aides.qa, 0.)
    cpdef inline void calc_v_qa(self)  nogil:
        self.sequences.aides.qa = min(self.sequences.aides.qa, self.sequences.fluxes.qz+self.parameters.derived.nmbsubsteps/self.parameters.derived.seconds*self.sequences.aides.v)
        self.sequences.aides.v = max(self.sequences.aides.v+self.parameters.derived.seconds/self.parameters.derived.nmbsubsteps*(self.sequences.fluxes.qz-self.sequences.aides.qa), 0.)
    cpdef inline void pick_q_v1(self)  nogil:
        cdef int idx
        self.sequences.fluxes.qz = 0.
        for idx in range(self.sequences.inlets.len_q):
            self.sequences.fluxes.qz = self.sequences.fluxes.qz + (self.sequences.inlets.q[idx][0])
    cpdef inline void pick_q(self)  nogil:
        cdef int idx
        self.sequences.fluxes.qz = 0.
        for idx in range(self.sequences.inlets.len_q):
            self.sequences.fluxes.qz = self.sequences.fluxes.qz + (self.sequences.inlets.q[idx][0])
    cpdef inline void pass_q_v1(self)  nogil:
        self.sequences.outlets.q[0] = self.sequences.outlets.q[0] + (self.sequences.fluxes.qa)
    cpdef inline void pass_q(self)  nogil:
        self.sequences.outlets.q[0] = self.sequences.outlets.q[0] + (self.sequences.fluxes.qa)
