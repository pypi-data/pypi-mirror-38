from __future__ import division
"""Pencil decomposition

This module contains classes for performing FFTs with pencil decomposition
of three-dimensional data structures data[Nx,Ny,Nz],  where (Nx, Ny, Nz) is
the shape of the input data. With slab decomposition only one of these three
indices is shared, leading to local datastructures on each processor
with shape data[Nx/P, Ny, Nz], where P is the total number of processors.
With pencil, two of the input arrays indices are shared, leading to local
data of shape (Nx/P1, Ny/P2, Nz), i.e., pencils aligned in the z-direction.

The final transformed data can be aligned in either the y-direction or
the x-direction.

classes:
    R2CX - For real to complex transforms. Final alignment in x-direction
        Args:
        N - NumPy array([Nx, Ny, Nz]) setting the dimensions of the real mesh
        L - NumPy array([Lx, Ly, Lz]) size of the computational domain
        comm - The MPI communicator object
        precision - "single" or "double"
        communication - Communication scheme ('AlltoallN', 'Alltoall' or 'Alltoallw')
        padsize - The size of padding, if padding is used in transforms
        threads - Number of threads used by FFTs
        planner_effort - Planner effort used by FFTs (e.g., "FFTW_MEASURE",
                         "FFTW_PATIENT", "FFTW_EXHAUSTIVE")

    R2CY - For real to complex transforms. Final alignment in y-direction
        Args:
        N - NumPy array([Nx, Ny, Nz]) number of nodes for the real mesh
        L - NumPy array([Lx, Ly, Lz]) size of the computational domain
        comm - The MPI communicator object
        precision - "single" or "double"
        P1 - Decomposition along first dimension
        communication - Communication scheme ('AlltoallN', 'Alltoall' or 'Alltoallw')
        padsize - The size of padding, if padding is used in transforms
        threads - Number of threads used by FFTs
        planner_effort - Planner effort used by FFTs ("FFTW_MEASURE",
                         "FFTW_PATIENT", "FFTW_EXHAUSTIVE")

function:
    R2C

    Args:
        N - NumPy array([Nx, Ny, Nz]) number of nodes for the real mesh
        L - NumPy array([Lx, Ly, Lz]) size of the computational domain
        comm - The MPI communicator object
        precision - "single" or "double"
        P1 - Decomposition along first dimension
        communication - Communication scheme ('AlltoallN', 'Alltoall' or 'Alltoallw')
        padsize - The size of padding, if padding is used in transforms
        threads - Number of threads used by FFTs
        alignment - Final alignment, ('X' or 'Y')
        planner_effort - Planner effort used by FFTs ("FFTW_MEASURE",
                         "FFTW_PATIENT", "FFTW_EXHAUSTIVE")

"""
__author__ = "Mikael Mortensen <mikaem@math.uio.no>"
__date__ = "2016-02-16"
__copyright__ = "Copyright (C) 2016 " + __author__
__license__ = "GNU Lesser GPL version 3 or any later version"

from .serialFFT import *
import numpy as np
from .mpibase import work_arrays, datatypes
from .cython.maths import dealias_filter
from numpy.fft import fftfreq, rfftfreq
from collections import defaultdict
from mpi4py import MPI

#__all__ = ['R2C']

# Using Lisandro Dalcin's code for Alltoallw.
# Note that _subsize and _distribution are modified for a mesh of power two.

def _subsize(N, size, rank):
    return N // size + ((N % size) * (rank == size -1))
    #return N // size + (N % size > rank) # Generic

def _distribution(N, size):
    q = N // size
    r = N % size
    n = s = i = 0
    while i < size:
        n = q
        s = q * i
        if r == 1 and i+1 == size:
            n += 1
        yield n, s
        i += 1

# Generic
#def _distribution2(N, size):
    #q = N // size
    #r = N % size
    #n = s = i = 0
    #while i < size:
        #n = q
        #s = q * i
        #if i < r:
            #n += 1
            #s += i
        #else:
            #s += r
        #yield n, s
        #i += 1


def transform_Uc_xz(Uc_hat_x, Uc_hat_z, P1):
    sz = Uc_hat_z.shape
    sx = Uc_hat_x.shape
    Uc_hat_x[:] = np.rollaxis(Uc_hat_z[:,:,:-1].reshape((sz[0], sz[1], P1, sx[2])), 2).reshape(sx)
    return Uc_hat_x

def transform_Uc_zx(Uc_hat_z, Uc_hat_xr, P1):
    sz = Uc_hat_z.shape
    sx = Uc_hat_xr.shape
    Uc_hat_z[:, :, :-1] = np.rollaxis(Uc_hat_xr.reshape((P1, sz[0], sz[1], sx[2])), 0, 3).reshape((sz[0], sz[1], sz[2]-1))
    return Uc_hat_z

def transform_Uc_xy(Uc_hat_x, Uc_hat_y, P):
    sy = Uc_hat_y.shape
    sx = Uc_hat_x.shape
    Uc_hat_x[:] = np.rollaxis(Uc_hat_y.reshape((sy[0], P, sx[1], sx[2])), 1).reshape(sx)
    return Uc_hat_x

def transform_Uc_yx(Uc_hat_y, Uc_hat_x, P):
    sy = Uc_hat_y.shape
    sx = Uc_hat_x.shape
    Uc_hat_y[:] = np.rollaxis(Uc_hat_x.reshape((P, sx[0]//P, sx[1], sx[2])), 1).reshape(sy)
    return Uc_hat_y

def transform_Uc_yz(Uc_hat_y, Uc_hat_z, P):
    sz = Uc_hat_z.shape
    sy = Uc_hat_y.shape
    Uc_hat_y[:] = np.rollaxis(Uc_hat_z[:,:,:-1].reshape((sz[0], sz[1], P, sy[2])), 1, 3).reshape(sy)
    return Uc_hat_y

def transform_Uc_zy(Uc_hat_z, Uc_hat_y, P):
    sz = Uc_hat_z.shape
    sy = Uc_hat_y.shape
    Uc_hat_z[:, :, :-1] = np.rollaxis(Uc_hat_y.reshape((sy[0], P, sz[1], sy[2])), 1, 3).reshape((sz[0], sz[1], sz[2]-1))
    return Uc_hat_z

class R2CY(object):
    """Class for performing FFT in 3D using MPI

    Pencil decomposition

    Args:
        N - NumPy array([Nx, Ny, Nz]) Number of nodes for the real mesh
        L - NumPy array([Lx, Ly, Lz]) The actual size of the computational domain
        comm - The MPI communicator object
        precision - "single" or "double"
        P1 - Decomposition along first dimension
        communication - Communication scheme ('AlltoallN', 'Alltoall' or 'Alltoallw')
        padsize - The size of padding, if padding is used in transforms
        threads - Number of threads used by FFTs
        planner_effort - Planner effort used by FFTs ("FFTW_MEASURE", "FFTW_PATIENT", "FFTW_EXHAUSTIVE")
                         Give as defaultdict, with keys representing transform (e.g., fft, ifft)

    This version has the final complex data aligned in the y-direction, in agreement
    with the paper in CPC (http://arxiv.org/pdf/1602.03638v1.pdf)

    """

    def __init__(self, N, L, comm, precision, P1=None, communication='Alltoallw', padsize=1.5, threads=1,
                 planner_effort=defaultdict(lambda: "FFTW_MEASURE")):
        self.N = N
        assert len(L) == 3
        assert len(N) == 3
        self.Nf = N[2]//2+1 # Number of independent complex wavenumbers in z-direction
        self.comm = comm
        self.float, self.complex, self.mpitype = float, complex, mpitype = datatypes(precision)
        self.num_processes = comm.Get_size()
        assert self.num_processes > 1
        self.L = L.astype(float)
        self.dealias = np.zeros(0)
        self.communication = communication
        self.padsize = padsize
        self.threads = threads
        self.planner_effort = planner_effort
        self.rank = comm.Get_rank()
        if P1 is None:
            P1, P2 = MPI.Compute_dims(self.num_processes, 2)
            self.P1, self.P2 = P1, P2
        else:
            self.P1 = P1
            self.P2 = P2 = self.num_processes // P1
        self.N1 = N // P1
        self.N2 = N // P2
        self.comm0 = comm.Split(self.rank/P1)
        self.comm1 = comm.Split(self.rank%P1)
        self.comm0_rank = self.comm0.Get_rank()
        self.comm1_rank = self.comm1.Get_rank()
        self.work_arrays = work_arrays()
        self.N1f = self.N1[2]//2 if self.comm0_rank < self.P1-1 else self.N1[2]//2+1
        if self.communication == 'AlltoallN':
            self.N1f = self.N1[2]//2

        if not (self.num_processes % 2 == 0 or self.num_processes == 1):
            raise IOError("Number of cpus must be even")

        if (P1 % 2 != 0) or (P2 % 2 != 0):
            raise IOError("Number of cpus in each direction must be even power of 2")

        self._subarrays1A = []
        self._subarrays1B = []
        self._subarrays2A = []
        self._subarrays2B = []
        self._subarrays1A_pad = []
        self._subarrays1B_pad = []
        self._subarrays2A_pad = []
        self._subarrays2B_pad = []
        self._counts_displs1 = None
        self._counts_displs2 = None

    def get_subarrays(self, padsize=1):
        datatype = MPI._typedict[np.dtype(self.complex).char]
        M, N, Q = self.N[0], self.N[1], self.Nf
        m = _subsize(M, self.P2, self.comm1_rank)
        n = _subsize(int(padsize*N), self.P2, self.comm1_rank)
        q = _subsize(Q, self.P1, self.comm0_rank)
        _subarrays1A = [
            datatype.Create_subarray([m,int(padsize*N),q], [m,l,q], [0,s,0]).Commit()
            for l, s in _distribution(int(padsize*N), self.P2)
        ]
        _subarrays1B = [
            datatype.Create_subarray([M,n,q], [l,n,q], [s,0,0]).Commit()
            for l, s in _distribution(M, self.P2)
        ]
        _counts_displs1 = ([1] * self.P2, [0] * self.P2)

        m = _subsize(int(padsize*M), self.P1, self.comm0_rank)
        n = _subsize(int(padsize*N), self.P2, self.comm1_rank)
        q = _subsize(Q, self.P1, self.comm0_rank)
        _subarrays2A = [
            datatype.Create_subarray([int(padsize*M),n,q], [l,n,q], [s,0,0]).Commit()
            for l, s in _distribution(int(padsize*M), self.P1)
        ]
        _subarrays2B = [
            datatype.Create_subarray([m,n,Q], [m,n,l], [0,0,s]).Commit()
            for l, s in _distribution(Q, self.P1)
        ]
        _counts_displs2 = ([1] * self.P1, [0] * self.P1)
        return _subarrays1A, _subarrays1B, _subarrays2A, _subarrays2B, _counts_displs1, _counts_displs2

    def real_shape(self):
        """The local shape of the real data"""
        return (self.N1[0], self.N2[1], self.N[2])

    def complex_shape(self):
        """The local shape of the complex data"""
        return (self.N2[0], self.N[1], self.N1f)

    def complex_shape_T(self):
        """The local transposed shape of the complex data"""
        return (self.Np[0], self.N[1], self.Nf)

    def complex_shape_I(self):
        """A local intermediate shape of the complex data"""
        return (self.Np[0], self.num_processes, self.Np[1], self.Nf)

    def real_shape_padded(self):
        return (int(self.padsize*self.N1[0]), int(self.padsize*self.N2[1]), int(self.padsize*self.N[2]))

    def work_shape(self, dealias):
        """Shape of work arrays used in convection with dealiasing. Different shape whether or not padding is involved"""
        if dealias == '3/2-rule':
            return self.real_shape_padded()

        else:
            return self.real_shape()

    def real_local_slice(self, padsize=1):
        xzrank = self.comm0.Get_rank() # Local rank in xz-plane
        xyrank = self.comm1.Get_rank() # Local rank in xy-plane
        return (slice(int(padsize * xzrank * self.N1[0]), int(padsize * (xzrank+1) * self.N1[0]), 1),
                slice(int(padsize * xyrank * self.N2[1]), int(padsize * (xyrank+1) * self.N2[1]), 1),
                slice(0, int(padsize*self.N[2])))

    def complex_local_slice(self):
        xzrank = self.comm0.Get_rank() # Local rank in xz-plane
        xyrank = self.comm1.Get_rank() # Local rank in xy-plane
        return (slice(xyrank*self.N2[0], (xyrank+1)*self.N2[0], 1),
                slice(0, self.N[1]),
                slice(xzrank*self.N1[2]//2, xzrank*self.N1[2]//2 + self.N1f, 1))

    def complex_local_wavenumbers(self):
        s = self.complex_local_slice()
        return (fftfreq(self.N[0], 1./self.N[0]).astype(int)[s[0]],
                fftfreq(self.N[1], 1./self.N[1]).astype(int),
                rfftfreq(self.N[2], 1./self.N[2]).astype(int)[s[2]])

    def get_P(self):
        return self.P1, self.P2

    def get_local_mesh(self):
        xzrank = self.comm0.Get_rank() # Local rank in xz-plane
        xyrank = self.comm1.Get_rank() # Local rank in xy-plane

        # Create the physical mesh
        x1 = slice(xzrank * self.N1[0], (xzrank+1) * self.N1[0], 1)
        x2 = slice(xyrank * self.N2[1], (xyrank+1) * self.N2[1], 1)
        X = np.ogrid[x1, x2, :self.N[2]]

        X[0] = (X[0]*self.L[0]/self.N[0]).astype(self.float)
        X[1] = (X[1]*self.L[1]/self.N[1]).astype(self.float)
        X[2] = (X[2]*self.L[2]/self.N[2]).astype(self.float)
        X = [np.broadcast_to(x, self.real_shape()) for x in X]
        return X

    def get_local_wavenumbermesh(self, scaled=False, broadcast=False,
                                 eliminate_highest_freq=False):
        """Returns (scaled) local decomposed wavenumbermesh

        If scaled is True, then the wavenumbermesh is scaled with physical mesh
        size. This takes care of mapping the physical domain to a computational
        cube of size (2pi)**3


        """
        s = self.complex_local_slice()
        kx = fftfreq(self.N[0], 1./self.N[0]).astype(int)
        ky = fftfreq(self.N[1], 1./self.N[1]).astype(int)
        kz = rfftfreq(self.N[2], 1./self.N[2]).astype(int)
        if eliminate_highest_freq:
            for i, k in enumerate((kx, ky, kz)):
                if self.N[i] % 2 == 0:
                    k[self.N[i]//2] = 0
        kx = kx[s[0]]
        kz = kz[s[2]]
        Ks = np.meshgrid(kx, ky, kz, indexing='ij', sparse=True)
        if scaled is True:
            Lp = 2*np.pi/self.L
            for i in range(3):
                Ks[i] = (Ks[i]*Lp[i]).astype(self.float)
        K = Ks
        if broadcast is True:
            K = [np.broadcast_to(k, self.complex_shape()) for k in Ks]
        return K

    def get_dealias_filter(self):
        """Filter for dealiasing nonlinear convection"""
        K = self.get_local_wavenumbermesh()
        kmax = 2./3.*(self.N//2+1)
        dealias = np.array((abs(K[0]) < kmax[0])*(abs(K[1]) < kmax[1])*
                           (abs(K[2]) < kmax[2]), dtype=np.uint8)
        return dealias

    def copy_to_padded_x(self, fu, fp):
        fp[:self.N[0]//2] = fu[:self.N[0]//2]
        fp[-(self.N[0]//2):] = fu[self.N[0]//2:]
        return fp

    def copy_to_padded_y(self, fu, fp):
        fp[:, :self.N[1]//2] = fu[:, :self.N[1]//2]
        fp[:, -(self.N[1]//2):] = fu[:, self.N[1]//2:]
        return fp

    def copy_to_padded_z(self, fu, fp):
        fp[:, :, :self.Nf] = fu[:]
        return fp

    def copy_from_padded_z(self, fp, fu):
        fu[:] = fp[:, :, :self.Nf]
        return fu

    def copy_from_padded_x(self, fp, fu):
        fu.fill(0)
        fu[:self.N[0]//2+1] = fp[:self.N[0]//2+1]
        fu[self.N[0]//2:] += fp[-self.N[0]//2:]
        return fu

    def copy_from_padded_y(self, fp, fu):
        fu.fill(0)
        fu[:, :self.N[1]//2+1] = fp[:, :self.N[1]//2+1]
        fu[:, self.N[1]//2:] += fp[:, -self.N[1]//2:]
        return fu

    def global_complex_shape(self, padsize=1.0):
        """Global size of problem in complex wavenumber space"""
        return (int(padsize*self.N[0]), int(padsize*self.N[1]),
                int(padsize*self.N[2]//2+1))

    def ifftn(self, fu, u, dealias=None):
        """ifft in three directions using mpi.
        Need to do ifft in reversed order of fft
        """
        assert dealias in ('3/2-rule', '2/3-rule', 'None', None)

        if dealias == '2/3-rule' and self.dealias.shape == (0,):
            self.dealias = self.get_dealias_filter()

        # Strip off self
        N, N1, N2, Nf, N1f = self.N, self.N1, self.N2, self.Nf, self.N1f

        if not dealias == '3/2-rule':

            fu_ = fu
            if dealias == '2/3-rule':
                fu_ = self.work_arrays[(fu, 0, False)]
                fu_[:] = fu
                fu_ = dealias_filter(fu_, self.dealias)
                #fu_ *= self.dealias

            Uc_hat_y = self.work_arrays[((N2[0], N[1], N1f), self.complex, 0, False)]
            Uc_hat_z = self.work_arrays[((N1[0], N2[1], Nf), self.complex, 0, False)]

            if self.communication == 'AlltoallN':
                Uc_hat_x = self.work_arrays[((N[0], N2[1], N1[2]//2), self.complex, 0, False)]

                # Do first owned direction
                Uc_hat_y = ifft(fu_, Uc_hat_y, axis=1, threads=self.threads,
                                planner_effort=self.planner_effort['ifft'])

                # Transform to x all but k=N//2 (the neglected Nyquist mode)
                Uc_hat_x[:] = transform_Uc_xy(Uc_hat_x, Uc_hat_y, self.P2)

                # Communicate in xz-plane and do fft in x-direction
                self.comm1.Alltoall(MPI.IN_PLACE, [Uc_hat_x, self.mpitype])
                Uc_hat_x[:] = ifft(Uc_hat_x, axis=0, threads=self.threads,
                                   planner_effort=self.planner_effort['ifft'])

                # Communicate and transform in xy-plane
                self.comm0.Alltoall(MPI.IN_PLACE, [Uc_hat_x, self.mpitype])
                Uc_hat_z[:] = transform_Uc_zx(Uc_hat_z, Uc_hat_x, self.P1)

                # Do fft for z-direction
                Uc_hat_z[:, :, -1] = 0
                u[:] = irfft(Uc_hat_z, overwrite_input=True, axis=2, threads=self.threads,
                             planner_effort=self.planner_effort['irfft'])

            elif self.communication == 'Alltoall':
                # Additional work arrays
                Uc_hat_x  = self.work_arrays[((N[0], N2[1], N1[2]//2), self.complex, 0, False)]
                Uc_hat_xp = self.work_arrays[((N[0], N2[1], N1f), self.complex, 0, False)]
                xy_plane  = self.work_arrays[((N[0], N2[1]), self.complex, 0, False)]
                xy_recv   = self.work_arrays[((N1[0], N2[1]), self.complex, 0, False)]

                # Do first owned direction
                Uc_hat_y = ifft(fu_, Uc_hat_y, axis=1, threads=self.threads,
                                planner_effort=self.planner_effort['ifft'])

                # Transform to x
                Uc_hat_xp = transform_Uc_xy(Uc_hat_xp, Uc_hat_y, self.P2)

                ###### In-place
                ## Communicate in xz-plane and do fft in x-direction
                #self.comm1.Alltoall(MPI.IN_PLACE, [Uc_hat_xp, self.mpitype])
                #Uc_hat_xp[:] = ifft(Uc_hat_xp, axis=0, threads=self.threads,
                                    #planner_effort=self.planner_effort['ifft'])

                #Uc_hat_x[:] = Uc_hat_xp[:, :, :self.N1[2]//2]

                ## Communicate and transform in xy-plane all but k=N//2
                #self.comm0.Alltoall(MPI.IN_PLACE, [Uc_hat_x, self.mpitype])

                ####### Not in-place
                # Communicate in xz-plane and do fft in x-direction
                Uc_hat_xp2 = self.work_arrays[((N[0], N2[1], N1f), self.complex, 1, False)]
                self.comm1.Alltoall([Uc_hat_xp, self.mpitype], [Uc_hat_xp2, self.mpitype])
                Uc_hat_xp = ifft(Uc_hat_xp2, Uc_hat_xp, axis=0, threads=self.threads,
                                 planner_effort=self.planner_effort['ifft'])

                Uc_hat_x2 = self.work_arrays[((N[0], N2[1], N1[2]//2), self.complex, 1, False)]
                Uc_hat_x2[:] = Uc_hat_xp[:, :, :N1[2]//2]

                # Communicate and transform in xy-plane all but k=N//2
                self.comm0.Alltoall([Uc_hat_x2, self.mpitype], [Uc_hat_x, self.mpitype])
                #########################

                Uc_hat_z[:] = transform_Uc_zx(Uc_hat_z, Uc_hat_x, self.P1)

                xy_plane[:] = Uc_hat_xp[:, :, -1]
                self.comm0.Scatter(xy_plane, xy_recv, root=self.P1-1)
                Uc_hat_z[:, :, -1] = xy_recv

                # Do ifft for z-direction
                u = irfft(Uc_hat_z, u, axis=2, threads=self.threads,
                          planner_effort=self.planner_effort['irfft'])

            elif self.communication == 'Alltoallw':
                if len(self._subarrays1A) == 0:
                    (self._subarrays1A, self._subarrays1B, self._subarrays2A,
                     self._subarrays2B, self._counts_displs1, self._counts_displs2) = self.get_subarrays()

                Uc_hat_x  = self.work_arrays[((N[0], N2[1], N1f), self.complex, 0, False)]

                # Do first owned direction
                Uc_hat_y = ifft(fu_, Uc_hat_y, axis=1, threads=self.threads,
                                planner_effort=self.planner_effort['ifft'])

                self.comm1.Alltoallw(
                    [Uc_hat_y, self._counts_displs1, self._subarrays1A],
                    [Uc_hat_x, self._counts_displs1, self._subarrays1B])

                Uc_hat_x[:] = ifft(Uc_hat_x, axis=0, threads=self.threads,
                                   planner_effort=self.planner_effort['ifft'])

                self.comm0.Alltoallw(
                    [Uc_hat_x, self._counts_displs2, self._subarrays2A],
                    [Uc_hat_z, self._counts_displs2, self._subarrays2B])

                # Do fft for z-direction
                u[:] = irfft(Uc_hat_z, overwrite_input=True, axis=2, threads=self.threads,
                             planner_effort=self.planner_effort['irfft'])

            return u

        else:  # padded

            padsize = self.padsize
            Uc_pad_hat_y  = self.work_arrays[((N2[0], int(padsize*N[1]), N1f), self.complex, 0)]
            Uc_pad_hat_z  = self.work_arrays[((int(padsize*N1[0]), int(padsize*N2[1]), Nf), self.complex, 0)]
            Uc_pad_hat_z2 = self.work_arrays[((int(padsize*N1[0]), int(padsize*N2[1]), int(padsize*N[2]//2)+1), self.complex, 0)]

            if self.communication == 'AlltoallN':
                Uc_pad_hat_x  = self.work_arrays[((N[0], int(padsize*N2[1]), N1[2]//2), self.complex, 0)]
                Uc_pad_hat_xy = self.work_arrays[((int(padsize*N[0]), int(padsize*N2[1]), N1[2]//2), self.complex, 0)]

                Uc_pad_hat_y = self.copy_to_padded_y(fu*padsize**3, Uc_pad_hat_y)

                # Do first owned direction
                Uc_pad_hat_y[:] = ifft(Uc_pad_hat_y, axis=1, threads=self.threads,
                                       planner_effort=self.planner_effort['ifft'])

                # Transform to x all but k=N//2 (the neglected Nyquist mode)
                Uc_pad_hat_x = transform_Uc_xy(Uc_pad_hat_x, Uc_pad_hat_y, self.P2)

                # Communicate in xz-plane
                self.comm1.Alltoall(MPI.IN_PLACE, [Uc_pad_hat_x, self.mpitype])

                # Pad and do fft in x-direction
                Uc_pad_hat_xy = self.copy_to_padded_x(Uc_pad_hat_x, Uc_pad_hat_xy)
                Uc_pad_hat_xy[:] = ifft(Uc_pad_hat_xy, axis=0, threads=self.threads,
                                        planner_effort=self.planner_effort['ifft'])

                # Communicate in xy-plane
                self.comm0.Alltoall(MPI.IN_PLACE, [Uc_pad_hat_xy, self.mpitype])

                # Transform
                Uc_pad_hat_z[:] = transform_Uc_zx(Uc_pad_hat_z, Uc_pad_hat_xy, self.P1)
                Uc_pad_hat_z[:, :, -1] = 0

                # Pad in z-dir
                Uc_pad_hat_z2 = self.copy_to_padded_z(Uc_pad_hat_z, Uc_pad_hat_z2)

                # Do ifft for z-direction
                u = irfft(Uc_pad_hat_z2, u, axis=2, threads=self.threads,
                          planner_effort=self.planner_effort['irfft'])

            elif self.communication == 'Alltoall':
                Uc_pad_hat_x  = self.work_arrays[((N[0], int(padsize*N2[1]), N1[2]//2), self.complex, 0)]
                Uc_pad_hat_xy = self.work_arrays[((int(padsize*N[0]), int(padsize*N2[1]), N1[2]//2), self.complex, 0)]
                Uc_pad_hat_xr2  = self.work_arrays[((N[0], int(padsize*N2[1]), N1f), self.complex, 0)]
                Uc_pad_hat_xy3  = self.work_arrays[((int(padsize*N[0]), int(padsize*N2[1]), N1f), self.complex, 0)]
                xy2_pad_plane   = self.work_arrays[((int(padsize*N[0]), int(padsize*N2[1])), self.complex, 0)]
                xy2_pad_recv    = self.work_arrays[((int(padsize*N1[0]), int(padsize*N2[1])), self.complex, 1)]

                # Pad in y-direction
                Uc_pad_hat_y = self.copy_to_padded_y(fu*padsize**3, Uc_pad_hat_y)

                # Transform first owned direction
                Uc_pad_hat_y[:] = ifft(Uc_pad_hat_y, axis=1, threads=self.threads,
                                       planner_effort=self.planner_effort['ifft'])

                # Transpose datastructure to x
                Uc_pad_hat_xr2[:] = transform_Uc_xy(Uc_pad_hat_xr2, Uc_pad_hat_y, self.P2)

                # Communicate in xz-plane and do fft in x-direction
                self.comm1.Alltoall(MPI.IN_PLACE, [Uc_pad_hat_xr2, self.mpitype])

                # Pad and do fft in x-direction
                Uc_pad_hat_xy3 = self.copy_to_padded_x(Uc_pad_hat_xr2, Uc_pad_hat_xy3)
                Uc_pad_hat_xy3[:] = ifft(Uc_pad_hat_xy3, axis=0, threads=self.threads,
                                         planner_effort=self.planner_effort['ifft'])

                Uc_pad_hat_xy[:] = Uc_pad_hat_xy3[:, :, :N1[2]//2]

                # Communicate and transform in xy-plane all but k=N//2
                self.comm0.Alltoall(MPI.IN_PLACE, [Uc_pad_hat_xy, self.mpitype])

                Uc_pad_hat_z[:] = transform_Uc_zx(Uc_pad_hat_z, Uc_pad_hat_xy, self.P1)

                xy2_pad_plane[:] = Uc_pad_hat_xy3[:, :, -1]
                self.comm0.Scatter(xy2_pad_plane, xy2_pad_recv, root=self.P1-1)
                Uc_pad_hat_z[:, :, -1] = xy2_pad_recv

                # Pad in z-dir
                Uc_pad_hat_z2 = self.copy_to_padded_z(Uc_pad_hat_z, Uc_pad_hat_z2)

                # Do ifft for z-direction
                u = irfft(Uc_pad_hat_z2, u, axis=2, overwrite_input=True, threads=self.threads,
                          planner_effort=self.planner_effort['irfft'])

            elif self.communication == 'Alltoallw':
                if len(self._subarrays1A_pad) == 0:
                    (self._subarrays1A_pad, self._subarrays1B_pad, self._subarrays2A_pad,
                     self._subarrays2B_pad, self._counts_displs1, self._counts_displs2) = self.get_subarrays(padsize=self.padsize)

                Uc_pad_hat_x  = self.work_arrays[((N[0], int(padsize*N2[1]), N1f), self.complex, 0)]
                Uc_pad_hat_xy = self.work_arrays[((int(padsize*N[0]), int(padsize*N2[1]), N1f), self.complex, 0)]

                # Pad in y-direction
                Uc_pad_hat_y = self.copy_to_padded_y(fu*padsize**3, Uc_pad_hat_y)

                # Transform first owned direction
                Uc_pad_hat_y[:] = ifft(Uc_pad_hat_y, axis=1, threads=self.threads,
                                       planner_effort=self.planner_effort['ifft'])

                self.comm1.Alltoallw(
                    [Uc_pad_hat_y, self._counts_displs1, self._subarrays1A_pad],
                    [Uc_pad_hat_x, self._counts_displs1, self._subarrays1B_pad])

                # Pad and do fft in x-direction
                Uc_pad_hat_xy = self.copy_to_padded_x(Uc_pad_hat_x, Uc_pad_hat_xy)
                Uc_pad_hat_xy[:] = ifft(Uc_pad_hat_xy, axis=0, threads=self.threads,
                                        planner_effort=self.planner_effort['ifft'])

                self.comm0.Alltoallw(
                    [Uc_pad_hat_xy, self._counts_displs2, self._subarrays2A_pad],
                    [Uc_pad_hat_z,  self._counts_displs2, self._subarrays2B_pad])

                # Pad in z-dir
                Uc_pad_hat_z2 = self.copy_to_padded_z(Uc_pad_hat_z, Uc_pad_hat_z2)

                # Do fft for z-direction
                u = irfft(Uc_pad_hat_z2, u, overwrite_input=True, axis=2, threads=self.threads,
                          planner_effort=self.planner_effort['irfft'])

            return u

    def fftn(self, u, fu, dealias=None):
        """fft in three directions using mpi."""

        assert dealias in ('3/2-rule', '2/3-rule', 'None', None)

        # Strip off self
        N, N1, N2, Nf, N1f = self.N, self.N1, self.N2, self.Nf, self.N1f

        if not dealias == '3/2-rule':

            Uc_hat_y  = self.work_arrays[((N2[0], N[1], N1f), self.complex, 0)]
            Uc_hat_z  = self.work_arrays[((N1[0], N2[1], Nf), self.complex, 0)]

            if self.communication == 'AlltoallN':
                Uc_hat_x  = self.work_arrays[((N[0], N2[1], N1[2]//2), self.complex, 0)]

                # Do fft in z direction on owned data
                Uc_hat_z = rfft(u, Uc_hat_z, axis=2, threads=self.threads,
                                planner_effort=self.planner_effort['rfft'])

                # Transform to x direction neglecting k=N//2 (Nyquist)
                Uc_hat_x = transform_Uc_xz(Uc_hat_x, Uc_hat_z, self.P1)

                # Communicate and do fft in x-direction
                self.comm0.Alltoall(MPI.IN_PLACE, [Uc_hat_x, self.mpitype])
                Uc_hat_x[:] = fft(Uc_hat_x, axis=0, threads=self.threads,
                                  planner_effort=self.planner_effort['fft'])

                # Communicate and transform to final y-direction
                self.comm1.Alltoall(MPI.IN_PLACE, [Uc_hat_x, self.mpitype])
                Uc_hat_y[:] = transform_Uc_yx(Uc_hat_y, Uc_hat_x, self.P2)

                # Do fft for last direction
                fu = fft(Uc_hat_y, fu, axis=1, threads=self.threads,
                         planner_effort=self.planner_effort['fft'])

            elif self.communication == 'Alltoall':

                # Additional work arrays
                Uc_hat_x  = self.work_arrays[((N[0], N2[1], N1[2]//2), self.complex, 0)]
                Uc_hat_xr2= self.work_arrays[((N[0], N2[1], N1f), self.complex, 1)]
                xy_plane  = self.work_arrays[((N[0], N2[1]), self.complex, 0)]
                xy_plane2 = self.work_arrays[((N[0]//2+1, N2[1]), self.complex, 0)]
                xy_recv   = self.work_arrays[((N1[0], N2[1]), self.complex, 0)]

                # Do fft in z direction on owned data
                Uc_hat_z = rfft(u, Uc_hat_z, axis=2, threads=self.threads,
                                planner_effort=self.planner_effort['rfft'])

                # Move real part of Nyquist to k=0
                Uc_hat_z[:, :, 0] += 1j*Uc_hat_z[:, :, -1]

                # Transform to x direction neglecting k=N//2 (Nyquist)
                Uc_hat_x = transform_Uc_xz(Uc_hat_x, Uc_hat_z, self.P1)

                # In-place
                # Communicate and do fft in x-direction
                #self.comm0.Alltoall(MPI.IN_PLACE, [Uc_hat_x, self.mpitype])
                #Uc_hat_x[:] = fft(Uc_hat_x, axis=0, threads=self.threads,
                                  #planner_effort=self.planner_effort['fft'])

                # Not in-place
                Uc_hat_x2 = self.work_arrays[((N[0], N2[1], N1[2]//2), self.complex, 2, False)]
                self.comm0.Alltoall([Uc_hat_x, self.mpitype], [Uc_hat_x2, self.mpitype])
                Uc_hat_x = fft(Uc_hat_x2, Uc_hat_x, axis=0, threads=self.threads,
                               planner_effort=self.planner_effort['fft'])
                ################

                Uc_hat_xr2[:, :, :N1[2]//2] = Uc_hat_x[:]

                # Now both k=0 and k=N//2 are contained in 0 of comm0_rank = 0
                if self.comm0_rank == 0:
                    M = N[0]
                    xy_plane[:] = Uc_hat_x[:, :, 0]
                    xy_plane2[:] = np.vstack((xy_plane[0].real, 0.5*(xy_plane[1:M//2]+np.conj(xy_plane[:M//2:-1])), xy_plane[M//2].real))
                    Uc_hat_xr2[:, :, 0] = np.vstack((xy_plane2, np.conj(xy_plane2[(M//2-1):0:-1])))
                    xy_plane2[:] = np.vstack((xy_plane[0].imag, -0.5*1j*(xy_plane[1:M//2]-np.conj(xy_plane[:M//2:-1])), xy_plane[M//2].imag))
                    xy_plane[:] = np.vstack((xy_plane2, np.conj(xy_plane2[(M//2-1):0:-1])))
                    self.comm0.Send([xy_plane, self.mpitype], dest=self.P1-1, tag=77)

                if self.comm0_rank == self.P1-1:
                    self.comm0.Recv([xy_plane, self.mpitype], source=0, tag=77)
                    Uc_hat_xr2[:, :, -1] = xy_plane

                # Communicate and transform to final y-direction
                #self.comm1.Alltoall(MPI.IN_PLACE, [Uc_hat_xr2, self.mpitype])
                #Uc_hat_y = transform_Uc_yx(Uc_hat_y, Uc_hat_xr2, self.P2)
                # Not in-place
                Uc_hat_xr3 = self.work_arrays[((N[0], N2[1], N1f), self.complex, 3)]
                self.comm1.Alltoall([Uc_hat_xr2, self.mpitype], [Uc_hat_xr3, self.mpitype])
                Uc_hat_y = transform_Uc_yx(Uc_hat_y, Uc_hat_xr3, self.P2)

                # Do fft for last direction
                fu = fft(Uc_hat_y, fu, axis=1, threads=self.threads,
                         planner_effort=self.planner_effort['fft'])

            elif self.communication == 'Alltoallw':
                if len(self._subarrays1A) == 0:
                    (self._subarrays1A, self._subarrays1B, self._subarrays2A,
                     self._subarrays2B, self._counts_displs1, self._counts_displs2) = self.get_subarrays()

                Uc_hat_x  = self.work_arrays[((N[0], N2[1], N1f), self.complex, 0)]

                # Do fft in z direction on owned data
                Uc_hat_z = rfft(u, Uc_hat_z, axis=2, threads=self.threads,
                                planner_effort=self.planner_effort['rfft'])

                self.comm0.Alltoallw(
                    [Uc_hat_z, self._counts_displs2, self._subarrays2B],
                    [Uc_hat_x, self._counts_displs2, self._subarrays2A])

                Uc_hat_x[:] = fft(Uc_hat_x, axis=0, threads=self.threads,
                                  planner_effort=self.planner_effort['fft'])

                self.comm1.Alltoallw(
                    [Uc_hat_x, self._counts_displs1, self._subarrays1B],
                    [Uc_hat_y, self._counts_displs1, self._subarrays1A])

                # Do fft for last direction
                fu = fft(Uc_hat_y, fu, axis=1, threads=self.threads,
                         planner_effort=self.planner_effort['fft'])

            return fu

        else: # padded

            assert u.shape == self.real_shape_padded()

            padsize = self.padsize
            Uc_pad_hat_y  = self.work_arrays[((N2[0], int(padsize*N[1]), N1f), self.complex, 0)]
            Uc_pad_hat_z  = self.work_arrays[((int(padsize*N1[0]), int(padsize*N2[1]), Nf), self.complex, 0)]
            Uc_pad_hat_z2 = self.work_arrays[((int(padsize*N1[0]), int(padsize*N2[1]), int(padsize*N[2]//2)+1), self.complex, 0)]

            if self.communication == 'AlltoallN':
                Uc_pad_hat_x  = self.work_arrays[((N[0], int(padsize*N2[1]), N1[2]//2), self.complex, 0)]
                Uc_pad_hat_xy = self.work_arrays[((int(padsize*N[0]), int(padsize*N2[1]), N1[2]//2), self.complex, 0)]

                # Do fft in z direction on owned data
                Uc_pad_hat_z2 = rfft(u, Uc_pad_hat_z2, axis=2, threads=self.threads,
                                     planner_effort=self.planner_effort['rfft'])

                Uc_pad_hat_z = self.copy_from_padded_z(Uc_pad_hat_z2, Uc_pad_hat_z)

                # Transform to x direction neglecting k=N//2 (Nyquist)
                Uc_pad_hat_xy = transform_Uc_xz(Uc_pad_hat_xy, Uc_pad_hat_z, self.P1)

                # Communicate and do fft in x-direction
                self.comm0.Alltoall(MPI.IN_PLACE, [Uc_pad_hat_xy, self.mpitype])
                Uc_pad_hat_xy[:] = fft(Uc_pad_hat_xy, axis=0, threads=self.threads,
                                       planner_effort=self.planner_effort['fft'])

                Uc_pad_hat_x = self.copy_from_padded_x(Uc_pad_hat_xy, Uc_pad_hat_x)

                # Communicate and transform to final y-direction
                self.comm1.Alltoall(MPI.IN_PLACE, [Uc_pad_hat_x, self.mpitype])
                Uc_pad_hat_y = transform_Uc_yx(Uc_pad_hat_y, Uc_pad_hat_x, self.P2)

                # Do fft for last direction
                Uc_pad_hat_y[:] = fft(Uc_pad_hat_y, axis=1, threads=self.threads,
                                      planner_effort=self.planner_effort['fft'])
                fu = self.copy_from_padded_y(Uc_pad_hat_y, fu)
                fu /= padsize**3

            elif self.communication == 'Alltoall':

                Uc_pad_hat_x  = self.work_arrays[((N[0], int(padsize*N2[1]), N1[2]//2), self.complex, 0)]
                Uc_pad_hat_xy = self.work_arrays[((int(padsize*N[0]), int(padsize*N2[1]), N1[2]//2), self.complex, 0)]
                xy_pad_plane = self.work_arrays[((N[0], int(padsize*N2[1])), self.complex, 0)]
                xy_pad_plane2= self.work_arrays[((N[0]//2+1, int(padsize*N2[1])), self.complex, 0)]
                Uc_pad_hat_xr2  = self.work_arrays[((N[0], int(padsize*N2[1]), N1f), self.complex, 0)]

                # Do fft in z direction on owned data
                Uc_pad_hat_z2 = rfft(u, Uc_pad_hat_z2, axis=2, threads=self.threads,
                                     planner_effort=self.planner_effort['rfft'])

                Uc_pad_hat_z = self.copy_from_padded_z(Uc_pad_hat_z2, Uc_pad_hat_z)

                # Move real part of Nyquist to k=0
                Uc_pad_hat_z[:, :, 0] += 1j*Uc_pad_hat_z[:, :, -1]

                # Transform to x direction neglecting k=N//2 (Nyquist)
                Uc_pad_hat_xy[:] = transform_Uc_xz(Uc_pad_hat_xy, Uc_pad_hat_z, self.P1)

                # Communicate and do fft in x-direction
                self.comm0.Alltoall(MPI.IN_PLACE, [Uc_pad_hat_xy, self.mpitype])
                Uc_pad_hat_xy[:] = fft(Uc_pad_hat_xy, axis=0, threads=self.threads,
                                       planner_effort=self.planner_effort['fft'])

                Uc_pad_hat_x = self.copy_from_padded_x(Uc_pad_hat_xy, Uc_pad_hat_x)

                Uc_pad_hat_xr2[:, :, :N1[2]//2] = Uc_pad_hat_x[:]

                # Now both k=0 and k=N//2 are contained in 0 of comm0_rank = 0
                if self.comm0_rank == 0:
                    N = self.N[0]
                    xy_pad_plane[:] = Uc_pad_hat_x[:, :, 0]
                    xy_pad_plane2[:] = np.vstack((xy_pad_plane[0].real, 0.5*(xy_pad_plane[1:N//2]+np.conj(xy_pad_plane[:N//2:-1])), xy_pad_plane[N//2].real))
                    Uc_pad_hat_xr2[:, :, 0] = np.vstack((xy_pad_plane2, np.conj(xy_pad_plane2[(N//2-1):0:-1])))
                    xy_pad_plane2[:] = np.vstack((xy_pad_plane[0].imag, -0.5*1j*(xy_pad_plane[1:N//2]-np.conj(xy_pad_plane[:N//2:-1])), xy_pad_plane[N//2].imag))
                    xy_pad_plane[:] = np.vstack((xy_pad_plane2, np.conj(xy_pad_plane2[(N//2-1):0:-1])))
                    self.comm0.Send([xy_pad_plane, self.mpitype], dest=self.P1-1, tag=77)

                if self.comm0_rank == self.P1-1:
                    self.comm0.Recv([xy_pad_plane, self.mpitype], source=0, tag=77)
                    Uc_pad_hat_xr2[:, :, -1] = xy_pad_plane

                # Communicate and transform to final y-direction
                self.comm1.Alltoall(MPI.IN_PLACE, [Uc_pad_hat_xr2, self.mpitype])
                Uc_pad_hat_y = transform_Uc_yx(Uc_pad_hat_y, Uc_pad_hat_xr2, self.P2)

                # Do fft for last direction
                Uc_pad_hat_y[:] = fft(Uc_pad_hat_y, axis=1, threads=self.threads,
                                      planner_effort=self.planner_effort['fft'])
                fu = self.copy_from_padded_y(Uc_pad_hat_y, fu)
                fu /= padsize**3

            elif self.communication == 'Alltoallw':
                if len(self._subarrays1A_pad) == 0:
                    (self._subarrays1A_pad, self._subarrays1B_pad, self._subarrays2A_pad,
                     self._subarrays2B_pad, self._counts_displs1, self._counts_displs2) = self.get_subarrays(padsize=self.padsize)

                Uc_pad_hat_xy = self.work_arrays[((int(padsize*N[0]), int(padsize*N2[1]), N1f), self.complex, 0)]
                Uc_pad_hat_x  = self.work_arrays[((N[0], int(padsize*N2[1]), N1f), self.complex, 0)]

                # Do fft in z direction on owned data
                Uc_pad_hat_z2 = rfft(u, Uc_pad_hat_z2, axis=2, threads=self.threads,
                                     planner_effort=self.planner_effort['rfft'])

                Uc_pad_hat_z = self.copy_from_padded_z(Uc_pad_hat_z2, Uc_pad_hat_z)

                self.comm0.Alltoallw(
                    [Uc_pad_hat_z, self._counts_displs2, self._subarrays2B_pad],
                    [Uc_pad_hat_xy, self._counts_displs2, self._subarrays2A_pad])

                Uc_pad_hat_xy[:] = fft(Uc_pad_hat_xy, axis=0, threads=self.threads,
                                       planner_effort=self.planner_effort['fft'])

                Uc_pad_hat_x = self.copy_from_padded_x(Uc_pad_hat_xy, Uc_pad_hat_x)

                self.comm1.Alltoallw(
                    [Uc_pad_hat_x, self._counts_displs1, self._subarrays1B_pad],
                    [Uc_pad_hat_y, self._counts_displs1, self._subarrays1A_pad])

                # Do fft for last direction
                Uc_pad_hat_y[:] = fft(Uc_pad_hat_y, axis=1, threads=self.threads,
                                      planner_effort=self.planner_effort['fft'])
                fu = self.copy_from_padded_y(Uc_pad_hat_y, fu)
                fu /= padsize**3

            return fu

class R2CX(R2CY):
    """Class for performing FFT in 3D using MPI

    Pencil decomposition

    Args:
        N - NumPy array([Nx, Ny, Nz]) setting the dimensions of the real mesh
        L - NumPy array([Lx, Ly, Lz]) setting the actual size of the computational domain
        MPI - The MPI object (from mpi4py import MPI)
        precision - "single" or "double"
        communication - Communication scheme. ('AlltoallN', 'Alltoall' or 'Alltoallw')
        padsize - The size of padding, if padding is used in transforms
        threads - Number of threads used by FFTs
        planner_effort - Planner effort used by FFTs (e.g., "FFTW_MEASURE", "FFTW_PATIENT", "FFTW_EXHAUSTIVE")
                         Give as defaultdict, with keys representing transform (e.g., fft, ifft)

    This version has the final complex data aligned in the x-direction
    """
    def __init__(self, N, L, comm, precision, P1=None, communication='Alltoall',
                 padsize=1.5, threads=1,
                 planner_effort=defaultdict(lambda: "FFTW_MEASURE")):
        R2CY.__init__(self, N, L, comm, precision, P1=P1, communication=communication,
                      padsize=padsize, threads=threads, planner_effort=planner_effort)
        self.N2f = self.N2[2]//2 if self.comm1_rank < self.P2-1 else self.N2[2]//2+1
        if self.communication == 'AlltoallN':
            self.N2f = self.N2[2]//2
        if self.communication == 'Alltoallw':
            q = _subsize(self.Nf, self.P2, self.comm1_rank)
            self.N2f = q

    def real_shape(self):
        """The local shape of the real data"""
        return (self.N1[0], self.N2[1], self.N[2])

    def complex_shape(self):
        """The local shape of the complex data"""
        return (self.N[0], self.N1[1], self.N2f)

    def complex_shape_T(self):
        """The local transposed shape of the complex data"""
        return (self.Np[0], self.N[1], self.Nf)

    def complex_shape_I(self):
        """A local intermediate shape of the complex data"""
        return (self.Np[0], self.num_processes, self.Np[1], self.Nf)

    def real_local_slice(self, padsize=1):
        xyrank = self.comm0.Get_rank() # Local rank in xz-plane
        yzrank = self.comm1.Get_rank() # Local rank in xy-plane
        return (slice(int(padsize * xyrank * self.N1[0]), int(padsize * (xyrank+1) * self.N1[0]), 1),
                slice(int(padsize * yzrank * self.N2[1]), int(padsize * (yzrank+1) * self.N2[1]), 1),
                slice(0, int(padsize * self.N[2])))

    def complex_local_slice(self):
        xyrank = self.comm0.Get_rank() # Local rank in xz-plane
        yzrank = self.comm1.Get_rank() # Local rank in yz-plane
        return (slice(0, self.N[0]),
                slice(xyrank*self.N1[1], (xyrank+1)*self.N1[1], 1),
                slice(yzrank*self.N2[2]//2, yzrank*self.N2[2]//2 + self.N2f, 1))

    def get_local_mesh(self):
        xyrank = self.comm0.Get_rank() # Local rank in xz-plane
        yzrank = self.comm1.Get_rank() # Local rank in xy-plane

        # Create the physical mesh
        x1 = slice(xyrank * self.N1[0], (xyrank+1) * self.N1[0], 1)
        x2 = slice(yzrank * self.N2[1], (yzrank+1) * self.N2[1], 1)
        X = np.mgrid[x1, x2, :self.N[2]].astype(self.float)
        X[0] *= self.L[0]/self.N[0]
        X[1] *= self.L[1]/self.N[1]
        X[2] *= self.L[2]/self.N[2]
        return X

    def get_local_wavenumbermesh(self):
        xyrank = self.comm0.Get_rank() # Local rank in xz-plane
        yzrank = self.comm1.Get_rank() # Local rank in yz-plane

        # Set wavenumbers in grid
        kx = fftfreq(self.N[0], 1./self.N[0]).astype(int)
        ky = fftfreq(self.N[1], 1./self.N[1]).astype(int)
        kz = fftfreq(self.N[2], 1./self.N[2]).astype(int)
        k2 = slice(xyrank*self.N1[1], (xyrank+1)*self.N1[1], 1)
        k1 = slice(yzrank*self.N2[2]//2, (yzrank+1)*self.N2[2]//2, 1)
        K  = np.array(np.meshgrid(kx, ky[k2], kz[k1], indexing='ij'), dtype=self.float)
        return K

    def get_subarrays(self, padsize=1):
        datatype = MPI._typedict[np.dtype(self.complex).char]
        M, N, Q = self.N[0], self.N[1], self.Nf
        m = _subsize(int(padsize*M), self.P1, self.comm0_rank)
        n = _subsize(N, self.P1, self.comm0_rank)
        q = _subsize(Q, self.P2, self.comm1_rank)
        _subarrays1A = [
            datatype.Create_subarray([int(padsize*M),n,q], [l,n,q], [s,0,0]).Commit()
            for l, s in _distribution(int(padsize*M), self.P1)
        ]
        _subarrays1B = [
            datatype.Create_subarray([m,N,q], [m,l,q], [0,s,0]).Commit()
            for l, s in _distribution(N, self.P1)
        ]
        _counts_displs1 = ([1] * self.P1, [0] * self.P1)

        m = _subsize(int(padsize*M), self.P1, self.comm0_rank)
        n = _subsize(int(padsize*N), self.P2, self.comm1_rank)
        q = _subsize(Q, self.P2, self.comm1_rank)
        _subarrays2A = [
            datatype.Create_subarray([m,int(padsize*N),q], [m,l,q], [0,s,0]).Commit()
            for l, s in _distribution(int(padsize*N), self.P2)
        ]
        _subarrays2B = [
            datatype.Create_subarray([m,n,Q], [m,n,l], [0,0,s]).Commit()
            for l, s in _distribution(Q, self.P2)
        ]
        _counts_displs2 = ([1] * self.P2, [0] * self.P2)
        return _subarrays1A, _subarrays1B, _subarrays2A, _subarrays2B, _counts_displs1, _counts_displs2

    def ifftn(self, fu, u, dealias=None):
        """ifft in three directions using mpi

        Need to do ifft in reversed order of fft
        """
        assert dealias in ('3/2-rule', '2/3-rule', 'None', None)

        if dealias == '2/3-rule' and self.dealias.shape == (0,):
            self.dealias = self.get_dealias_filter()

        if not dealias == '3/2-rule':

            fu_ = fu
            if dealias == '2/3-rule':
                fu_ = self.work_arrays[(fu, 0, False)]
                fu_[:] = fu
                fu_ = dealias_filter(fu_, self.dealias)
                #fu_ *= self.dealias

            # Intermediate work arrays required for transform
            Uc_hat_z  = self.work_arrays[((self.N1[0], self.N2[1], self.Nf), self.complex, 0)]
            Uc_hat_x  = self.work_arrays[((self.N[0], self.N1[1], self.N2f), self.complex, 0)]

            if self.communication == 'AlltoallN':
                Uc_hat_y_T= self.work_arrays[((self.N[1], self.N1[0], self.N2[2]//2), self.complex, 0)]
                Uc_hat_y = Uc_hat_y_T.transpose((1, 0, 2))

                # Do first owned direction
                Uc_hat_x = ifft(fu_, Uc_hat_x, axis=0, threads=self.threads,
                                planner_effort=self.planner_effort['ifft'])

                # Communicate in xz-plane and do fft in y-direction
                self.comm0.Alltoall(MPI.IN_PLACE, [Uc_hat_x, self.mpitype])

                # Transform to y all but k=N//2 (the neglected Nyquist mode)
                Uc_hat_y = transform_Uc_yx(Uc_hat_y, Uc_hat_x, self.P1)
                Uc_hat_y[:] = ifft(Uc_hat_y, axis=1, threads=self.threads,
                                   planner_effort=self.planner_effort['ifft'])

                # Communicate and transform in yz-plane. Transpose required to put distributed axis first.
                self.comm1.Alltoall(MPI.IN_PLACE, [Uc_hat_y_T, self.mpitype])
                Uc_hat_z[:] = transform_Uc_zy(Uc_hat_z, Uc_hat_y, self.P2)

                # Do ifft for z-direction
                Uc_hat_z[:, :, -1] = 0
                u = irfft(Uc_hat_z, u, axis=2, threads=self.threads,
                          planner_effort=self.planner_effort['irfft'])

            elif self.communication == 'Alltoall':
                Uc_hat_y_T= self.work_arrays[((self.N[1], self.N1[0], self.N2[2]//2), self.complex, 0)]
                Uc_hat_y = Uc_hat_y_T.transpose((1, 0, 2))
                Uc_hat_y2  = self.work_arrays[((self.N1[0], self.N[1], self.N2f), self.complex, 0)]
                xy_plane_T  = self.work_arrays[((self.N[1], self.N1[0]), self.complex, 0)]
                xy_plane  = xy_plane_T.transpose((1, 0))
                xy_recv   = self.work_arrays[((self.N2[1], self.N1[0]), self.complex, 0)]

                # Do first owned direction
                Uc_hat_x = ifft(fu_, Uc_hat_x, axis=0, threads=self.threads,
                                planner_effort=self.planner_effort['ifft'])

                # Communicate in xz-plane and do fft in y-direction
                self.comm0.Alltoall(MPI.IN_PLACE, [Uc_hat_x, self.mpitype])

                # Transform to y all but k=N//2 (the neglected Nyquist mode)
                Uc_hat_y2 = transform_Uc_yx(Uc_hat_y2, Uc_hat_x, self.P1)
                Uc_hat_y2[:] = ifft(Uc_hat_y2, axis=1, threads=self.threads,
                                    planner_effort=self.planner_effort['ifft'])
                xy_plane[:] = Uc_hat_y2[:, :, -1]

                # Communicate and transform in yz-plane. Transpose required to put distributed axis first.
                Uc_hat_y[:] = Uc_hat_y2[:, :, :self.N2[2]//2]
                self.comm1.Alltoall(MPI.IN_PLACE, [Uc_hat_y_T, self.mpitype])
                Uc_hat_z = transform_Uc_zy(Uc_hat_z, Uc_hat_y, self.P2)

                self.comm1.Scatter(xy_plane_T, xy_recv, root=self.P2-1)
                Uc_hat_z[:, :, -1] = xy_recv.transpose((1, 0))

                # Do ifft for z-direction
                u = irfft(Uc_hat_z, u, axis=2, threads=self.threads,
                          planner_effort=self.planner_effort['irfft'])

            elif self.communication == 'Alltoallw':
                if len(self._subarrays1A) == 0:
                    (self._subarrays1A, self._subarrays1B, self._subarrays2A,
                     self._subarrays2B, self._counts_displs1, self._counts_displs2) = self.get_subarrays()

                Uc_hat_y = self.work_arrays[((self.N1[0], self.N[1], self.N2f), self.complex, 0)]

                # Do first owned direction
                Uc_hat_x = ifft(fu_, Uc_hat_x, axis=0, threads=self.threads,
                                planner_effort=self.planner_effort['ifft'])

                self.comm0.Alltoallw(
                    [Uc_hat_x, self._counts_displs1, self._subarrays1A],
                    [Uc_hat_y,  self._counts_displs1, self._subarrays1B])

                Uc_hat_y[:] = ifft(Uc_hat_y, axis=1, threads=self.threads,
                                   planner_effort=self.planner_effort['ifft'])

                self.comm1.Alltoallw(
                    [Uc_hat_y, self._counts_displs2, self._subarrays2A],
                    [Uc_hat_z,  self._counts_displs2, self._subarrays2B])
                # Do ifft for z-direction
                u = irfft(Uc_hat_z, u, axis=2, threads=self.threads,
                          planner_effort=self.planner_effort['irfft'])

        else:
            # Intermediate work arrays required for transform
            Uc_pad_hat_z  = self.work_arrays[((int(self.padsize*self.N1[0]), int(self.padsize*self.N2[1]), self.Nf), self.complex, 0)]
            Uc_pad_hat_z2 = self.work_arrays[((int(self.padsize*self.N1[0]), int(self.padsize*self.N2[1]), int(self.padsize*self.N[2]//2)+1), self.complex, 0)]
            Uc_pad_hat_x  = self.work_arrays[((int(self.padsize*self.N[0]), self.N1[1], self.N2f), self.complex, 0)]

            if self.communication == 'AlltoallN':
                Uc_pad_hat_y_T= self.work_arrays[((self.N[1], int(self.padsize*self.N1[0]), self.N2[2]//2), self.complex, 0)]
                Uc_pad_hat_y = Uc_pad_hat_y_T.transpose((1, 0, 2))
                Uc_pad_hat_xy_T= self.work_arrays[((int(self.padsize*self.N[1]), int(self.padsize*self.N1[0]), self.N2[2]//2), self.complex, 0)]
                Uc_pad_hat_xy = Uc_pad_hat_xy_T.transpose((1, 0, 2))
                Uc_pad_hat_xy2= self.work_arrays[((int(self.padsize*self.N1[0]), int(self.padsize*self.N[1]), self.N2[2]//2), self.complex, 0)]

                Uc_pad_hat_x = self.copy_to_padded_x(fu*self.padsize**3, Uc_pad_hat_x)

                # Do first owned direction
                Uc_pad_hat_x[:] = ifft(Uc_pad_hat_x, axis=0, threads=self.threads,
                                       planner_effort=self.planner_effort['ifft'])

                # Communicate in xz-plane and do fft in y-direction
                self.comm0.Alltoall(MPI.IN_PLACE, [Uc_pad_hat_x, self.mpitype])

                # Transform to y
                Uc_pad_hat_y = transform_Uc_yx(Uc_pad_hat_y, Uc_pad_hat_x, self.P1)
                Uc_pad_hat_xy2 = self.copy_to_padded_y(Uc_pad_hat_y, Uc_pad_hat_xy2)

                Uc_pad_hat_xy = ifft(Uc_pad_hat_xy2, Uc_pad_hat_xy, overwrite_input=True, axis=1, threads=self.threads,
                                     planner_effort=self.planner_effort['ifft'])

                # Communicate and transform in yz-plane. Transpose required to put distributed axis first.
                self.comm1.Alltoall(MPI.IN_PLACE, [Uc_pad_hat_xy_T, self.mpitype])
                Uc_pad_hat_z[:] = transform_Uc_zy(Uc_pad_hat_z, Uc_pad_hat_xy, self.P2)
                Uc_pad_hat_z[:, :, -1] = 0

                Uc_pad_hat_z2 = self.copy_to_padded_z(Uc_pad_hat_z, Uc_pad_hat_z2)

                # Do ifft for z-direction
                u = irfft(Uc_pad_hat_z2, u, overwrite_input=True, axis=2, threads=self.threads,
                          planner_effort=self.planner_effort['irfft'])

            elif self.communication == 'Alltoall':
                Uc_pad_hat_y_T= self.work_arrays[((self.N[1], int(self.padsize*self.N1[0]), self.N2[2]//2), self.complex, 0)]
                Uc_pad_hat_y = Uc_pad_hat_y_T.transpose((1, 0, 2))
                Uc_pad_hat_xy_T= self.work_arrays[((int(self.padsize*self.N[1]), int(self.padsize*self.N1[0]), self.N2[2]//2), self.complex, 0)]
                Uc_pad_hat_xy = Uc_pad_hat_xy_T.transpose((1, 0, 2))
                Uc_pad_hat_xy2= self.work_arrays[((int(self.padsize*self.N1[0]), int(self.padsize*self.N[1]), self.N2[2]//2), self.complex, 0)]
                Uc_pad_hat_y2_T= self.work_arrays[((self.N[1], int(self.padsize*self.N1[0]), self.N2f), self.complex, 0)]
                Uc_pad_hat_y2 = Uc_pad_hat_y2_T.transpose((1, 0, 2))
                Uc_pad_hat_xy2= self.work_arrays[((int(self.padsize*self.N1[0]), int(self.padsize*self.N[1]), self.N2f), self.complex, 0)]

                xy_plane_T  = self.work_arrays[((int(self.padsize*self.N[1]), int(self.padsize*self.N1[0])), self.complex, 0)]
                xy_plane  = xy_plane_T.transpose((1, 0))
                xy_recv   = self.work_arrays[((int(self.padsize*self.N2[1]), int(self.padsize*self.N1[0])), self.complex, 0)]

                Uc_pad_hat_x = self.copy_to_padded_x(fu*self.padsize**3, Uc_pad_hat_x)

                # Do first owned direction
                Uc_pad_hat_x[:] = ifft(Uc_pad_hat_x, axis=0, threads=self.threads,
                                       planner_effort=self.planner_effort['ifft'])

                # Communicate in xz-plane and do fft in y-direction
                self.comm0.Alltoall(MPI.IN_PLACE, [Uc_pad_hat_x, self.mpitype])

                # Transform to y
                Uc_pad_hat_y2 = transform_Uc_yx(Uc_pad_hat_y2, Uc_pad_hat_x, self.P1)

                Uc_pad_hat_xy2 = self.copy_to_padded_y(Uc_pad_hat_y2, Uc_pad_hat_xy2)

                Uc_pad_hat_xy2[:] = ifft(Uc_pad_hat_xy2, axis=1, threads=self.threads,
                                         planner_effort=self.planner_effort['ifft'])
                xy_plane[:] = Uc_pad_hat_xy2[:, :, -1]

                # Communicate and transform in yz-plane. Transpose required to put distributed axis first.
                Uc_pad_hat_xy[:] = Uc_pad_hat_xy2[:, :, :self.N2[2]//2]
                self.comm1.Alltoall(MPI.IN_PLACE, [Uc_pad_hat_xy_T, self.mpitype])
                Uc_pad_hat_z = transform_Uc_zy(Uc_pad_hat_z, Uc_pad_hat_xy, self.P2)

                self.comm1.Scatter(xy_plane_T, xy_recv, root=self.P2-1)
                Uc_pad_hat_z[:, :, -1] = xy_recv.transpose((1, 0))

                Uc_pad_hat_z2 = self.copy_to_padded_z(Uc_pad_hat_z, Uc_pad_hat_z2)

                # Do ifft for z-direction
                u = irfft(Uc_pad_hat_z2, u, axis=2, threads=self.threads,
                          planner_effort=self.planner_effort['irfft'])

            elif self.communication == 'Alltoallw':
                if len(self._subarrays1A_pad) == 0:
                    (self._subarrays1A_pad, self._subarrays1B_pad, self._subarrays2A_pad,
                     self._subarrays2B_pad, self._counts_displs1, self._counts_displs2) = self.get_subarrays(padsize=self.padsize)

                Uc_pad_hat_y  = self.work_arrays[((int(self.padsize*self.N1[0]), self.N[1], self.N2f), self.complex, 0)]
                Uc_pad_hat_xy = self.work_arrays[((int(self.padsize*self.N1[0]), int(self.padsize*self.N[1]), self.N2f), self.complex, 0)]

                Uc_pad_hat_x = self.copy_to_padded_x(fu*self.padsize**3, Uc_pad_hat_x)

                # Do first owned direction
                Uc_pad_hat_x[:] = ifft(Uc_pad_hat_x, axis=0, threads=self.threads,
                                       planner_effort=self.planner_effort['ifft'])

                self.comm0.Alltoallw(
                    [Uc_pad_hat_x, self._counts_displs1, self._subarrays1A_pad],
                    [Uc_pad_hat_y,  self._counts_displs1, self._subarrays1B_pad])

                Uc_pad_hat_xy = self.copy_to_padded_y(Uc_pad_hat_y, Uc_pad_hat_xy)

                Uc_pad_hat_xy[:] = ifft(Uc_pad_hat_xy, axis=1, threads=self.threads,
                                        planner_effort=self.planner_effort['ifft'])

                self.comm1.Alltoallw(
                    [Uc_pad_hat_xy, self._counts_displs2, self._subarrays2A_pad],
                    [Uc_pad_hat_z,  self._counts_displs2, self._subarrays2B_pad])

                Uc_pad_hat_z2 = self.copy_to_padded_z(Uc_pad_hat_z, Uc_pad_hat_z2)

                # Do ifft for z-direction
                u = irfft(Uc_pad_hat_z2, u, axis=2, overwrite_input=True, threads=self.threads,
                          planner_effort=self.planner_effort['irfft'])

        return u

    def fftn(self, u, fu, dealias=None):
        """fft in three directions using mpi."""
        assert dealias in ('3/2-rule', '2/3-rule', 'None', None)

        if not dealias == '3/2-rule':

            # Intermediate work arrays required for transform
            Uc_hat_z  = self.work_arrays[((self.N1[0], self.N2[1], self.Nf), self.complex, 0)]

            if self.communication == 'AlltoallN':
                Uc_hat_x  = self.work_arrays[((self.N[0], self.N1[1], self.N2[2]//2), self.complex, 0)]
                Uc_hat_y_T= self.work_arrays[((self.N[1], self.N1[0], self.N2[2]//2), self.complex, 0)]
                Uc_hat_y  = Uc_hat_y_T.transpose((1, 0, 2))
                Uc_hat_y2= self.work_arrays[((self.N1[0], self.N[1], self.N2[2]//2), self.complex, 1)]

                # Do fft in z direction on owned data
                Uc_hat_z = rfft(u, Uc_hat_z, axis=2, threads=self.threads,
                                planner_effort=self.planner_effort['rfft'])

                # Transform to y direction neglecting k=N//2 (Nyquist)
                Uc_hat_y = transform_Uc_yz(Uc_hat_y, Uc_hat_z, self.P2)

                # Communicate and do fft in y-direction. Transpose required to put distributed axis first
                self.comm1.Alltoall(MPI.IN_PLACE, [Uc_hat_y_T, self.mpitype])
                Uc_hat_y2 = fft(Uc_hat_y, Uc_hat_y2, axis=1, threads=self.threads,
                                planner_effort=self.planner_effort['fft'])

                # Communicate and transform to final x-direction
                Uc_hat_x = transform_Uc_xy(Uc_hat_x, Uc_hat_y2, self.P1)
                self.comm0.Alltoall(MPI.IN_PLACE, [Uc_hat_x, self.mpitype])

                # Do fft for last direction
                fu = fft(Uc_hat_x, fu, axis=0, threads=self.threads,
                         planner_effort=self.planner_effort['fft'])

            elif self.communication == 'Alltoall':
                Uc_hat_x  = self.work_arrays[((self.N[0], self.N1[1], self.N2[2]//2), self.complex, 0)]
                Uc_hat_y_T= self.work_arrays[((self.N[1], self.N1[0], self.N2[2]//2), self.complex, 0)]
                Uc_hat_y  = Uc_hat_y_T.transpose((1, 0, 2))
                Uc_hat_y2  = self.work_arrays[((self.N1[0], self.N[1], self.N2f), self.complex, 0)]
                Uc_hat_x2  = self.work_arrays[((self.N[0], self.N1[1], self.N2f), self.complex, 0)]
                Uc_hat_y3  = self.work_arrays[((self.N1[0], self.N[1], self.N2[2]//2), self.complex, 0)]
                xy_plane_T = self.work_arrays[((self.N[1], self.N1[0]), self.complex, 0)]
                xy_plane = xy_plane_T.transpose((1, 0))
                xy_plane2 = self.work_arrays[((self.N[1]//2+1, self.N1[0]), self.complex, 0)]

                # Do fft in z direction on owned data
                Uc_hat_z = rfft(u, Uc_hat_z, axis=2, threads=self.threads,
                                planner_effort=self.planner_effort['rfft'])

                # Move real part of Nyquist to k=0
                Uc_hat_z[:, :, 0] += 1j*Uc_hat_z[:, :, -1]

                # Transform to y direction neglecting k=N//2 (Nyquist)
                Uc_hat_y = transform_Uc_yz(Uc_hat_y, Uc_hat_z, self.P2)

                # Communicate and do fft in y-direction. Transpose required to put distributed axis first
                self.comm1.Alltoall(MPI.IN_PLACE, [Uc_hat_y_T, self.mpitype])
                Uc_hat_y3 = fft(Uc_hat_y, Uc_hat_y3, axis=1, threads=self.threads,
                                planner_effort=self.planner_effort['fft'])
                Uc_hat_y2[:, :, :self.N2[2]//2] = Uc_hat_y3[:]

                # Now both k=0 and k=N//2 are contained in 0 of comm0_rank = 0
                if self.comm1_rank == 0:
                    M = self.N[1]
                    xy_plane[:] = Uc_hat_y3[:, :, 0]
                    xy_plane2[:] = np.vstack((xy_plane_T[0].real, 0.5*(xy_plane_T[1:M//2]+np.conj(xy_plane_T[:M//2:-1])), xy_plane_T[M//2].real))
                    Uc_hat_y2[:, :, 0] = (np.vstack((xy_plane2, np.conj(xy_plane2[(M//2-1):0:-1])))).transpose((1, 0))
                    xy_plane2[:] = np.vstack((xy_plane_T[0].imag, -0.5*1j*(xy_plane_T[1:M//2]-np.conj(xy_plane_T[:M//2:-1])), xy_plane_T[M//2].imag))
                    xy_plane_T[:] = np.vstack((xy_plane2, np.conj(xy_plane2[(M//2-1):0:-1])))
                    self.comm1.Send([xy_plane_T, self.mpitype], dest=self.P2-1, tag=77)

                if self.comm1_rank == self.P2-1:
                    self.comm1.Recv([xy_plane_T, self.mpitype], source=0, tag=77)
                    Uc_hat_y2[:, :, -1] = xy_plane_T.transpose((1, 0))

                # Communicate and transform to final x-direction
                Uc_hat_x2 = transform_Uc_xy(Uc_hat_x2, Uc_hat_y2, self.P1)
                self.comm0.Alltoall(MPI.IN_PLACE, [Uc_hat_x2, self.mpitype])

                # Do fft for last direction
                fu = fft(Uc_hat_x2, fu, axis=0, threads=self.threads,
                         planner_effort=self.planner_effort['fft'])

            elif self.communication == 'Alltoallw':
                Uc_hat_y = self.work_arrays[((self.N1[0], self.N[1], self.N2f), self.complex, 0)]
                Uc_hat_x = self.work_arrays[((self.N[0], self.N1[1], self.N2f), self.complex, 0)]

                if len(self._subarrays1A) == 0:
                    (self._subarrays1A, self._subarrays1B, self._subarrays2A,
                     self._subarrays2B, self._counts_displs1, self._counts_displs2) = self.get_subarrays()

                # Do fft in z direction on owned data
                Uc_hat_z = rfft(u, Uc_hat_z, axis=2, threads=self.threads,
                                planner_effort=self.planner_effort['rfft'])

                self.comm1.Alltoallw(
                    [Uc_hat_z, self._counts_displs2, self._subarrays2B],
                    [Uc_hat_y, self._counts_displs2, self._subarrays2A])
                Uc_hat_y[:] = fft(Uc_hat_y, axis=1, threads=self.threads,
                                  planner_effort=self.planner_effort['fft'])

                # Communicate and transform to final x-direction
                self.comm0.Alltoallw(
                    [Uc_hat_y, self._counts_displs1, self._subarrays1B],
                    [Uc_hat_x, self._counts_displs1, self._subarrays1A])

                # Do fft for last direction
                fu = fft(Uc_hat_x, fu, axis=0, threads=self.threads,
                         planner_effort=self.planner_effort['fft'])

        else:

            assert u.shape == self.real_shape_padded()
            padsize = self.padsize
            # Strip off self
            N, N1, N2, Nf, N2f = self.N, self.N1, self.N2, self.Nf, self.N2f

            # Intermediate work arrays required for transform
            Uc_pad_hat_z  = self.work_arrays[((int(padsize*N1[0]), int(padsize*N2[1]), Nf), self.complex, 0)]
            Uc_pad_hat_z2 = self.work_arrays[((int(padsize*N1[0]), int(padsize*N2[1]), int(padsize*N[2]//2)+1), self.complex, 0)]

            if self.communication == 'AlltoallN':
                Uc_pad_hat_x  = self.work_arrays[((int(padsize*N[0]), N1[1], N2[2]//2), self.complex, 0)]
                Uc_pad_hat_xy_T= self.work_arrays[((int(padsize*N[1]), int(padsize*N1[0]), N2[2]//2), self.complex, 0)]
                Uc_pad_hat_xy  = Uc_pad_hat_xy_T.transpose((1, 0, 2))
                Uc_pad_hat_xy2= self.work_arrays[((int(padsize*N1[0]), int(padsize*N[1]), N2[2]//2), self.complex, 0)]
                Uc_pad_hat_y_T= self.work_arrays[((N[1], int(padsize*N1[0]), N2[2]//2), self.complex, 0)]
                Uc_pad_hat_y  = Uc_pad_hat_y_T.transpose((1, 0, 2))

                # Do fft in z direction on owned data
                Uc_pad_hat_z2 = rfft(u, Uc_pad_hat_z2, axis=2, threads=self.threads,
                                     planner_effort=self.planner_effort['rfft'])

                Uc_pad_hat_z = self.copy_from_padded_z(Uc_pad_hat_z2, Uc_pad_hat_z)

                # Transform to y direction neglecting k=N//2 (Nyquist)
                Uc_pad_hat_xy = transform_Uc_yz(Uc_pad_hat_xy, Uc_pad_hat_z, self.P2)

                # Communicate and do fft in y-direction. Transpose required to put distributed axis first
                self.comm1.Alltoall(MPI.IN_PLACE, [Uc_pad_hat_xy_T, self.mpitype])
                Uc_pad_hat_xy2 = fft(Uc_pad_hat_xy, Uc_pad_hat_xy2, axis=1, threads=self.threads,
                                     planner_effort=self.planner_effort['fft'])

                Uc_pad_hat_y = self.copy_from_padded_y(Uc_pad_hat_xy2, Uc_pad_hat_y)

                # Communicate and transform to final x-direction
                Uc_pad_hat_x = transform_Uc_xy(Uc_pad_hat_x, Uc_pad_hat_y, self.P1)
                self.comm0.Alltoall(MPI.IN_PLACE, [Uc_pad_hat_x, self.mpitype])

                # Do fft for last direction
                Uc_pad_hat_x[:] = fft(Uc_pad_hat_x, axis=0, threads=self.threads,
                                      planner_effort=self.planner_effort['fft'])
                fu = self.copy_from_padded_x(Uc_pad_hat_x, fu)
                fu /= padsize**3

            elif self.communication == 'Alltoall':
                Uc_pad_hat_xy_T= self.work_arrays[((int(padsize*N[1]), int(padsize*N1[0]), N2[2]//2), self.complex, 0)]
                Uc_pad_hat_xy  = Uc_pad_hat_xy_T.transpose((1, 0, 2))
                Uc_pad_hat_xy2= self.work_arrays[((int(padsize*N1[0]), int(padsize*N[1]), N2[2]//2), self.complex, 0)]
                Uc_pad_hat_y_T= self.work_arrays[((N[1], int(padsize*N1[0]), N2[2]//2), self.complex, 0)]
                Uc_pad_hat_y  = Uc_pad_hat_y_T.transpose((1, 0, 2))
                Uc_pad_hat_y2_T= self.work_arrays[((N[1], int(padsize*N1[0]), N2f), self.complex, 0)]
                Uc_pad_hat_y2  = Uc_pad_hat_y2_T.transpose((1, 0, 2))
                Uc_pad_hat_x2  = self.work_arrays[((int(padsize*N[0]), N1[1], N2f), self.complex, 0)]
                xy_plane_T  = self.work_arrays[((self.N[1], int(self.padsize*self.N1[0])), self.complex, 0)]
                xy_plane = xy_plane_T.transpose((1, 0))
                xy_plane2 = self.work_arrays[((self.N[1]//2+1, int(self.padsize*self.N1[0])), self.complex, 0)]

                # Do fft in z direction on owned data
                Uc_pad_hat_z2 = rfft(u, Uc_pad_hat_z2, axis=2, threads=self.threads,
                                     planner_effort=self.planner_effort['rfft'])

                Uc_pad_hat_z = self.copy_from_padded_z(Uc_pad_hat_z2, Uc_pad_hat_z)

                # Move real part of Nyquist to k=0
                Uc_pad_hat_z[:, :, 0] += 1j*Uc_pad_hat_z[:, :, -1]

                # Transform to y direction neglecting k=N//2 (Nyquist)
                Uc_pad_hat_xy = transform_Uc_yz(Uc_pad_hat_xy, Uc_pad_hat_z, self.P2)

                # Communicate and do fft in y-direction. Transpose required to put distributed axis first
                self.comm1.Alltoall(MPI.IN_PLACE, [Uc_pad_hat_xy_T, self.mpitype])
                Uc_pad_hat_xy2 = fft(Uc_pad_hat_xy, Uc_pad_hat_xy2, axis=1, threads=self.threads,
                                     planner_effort=self.planner_effort['fft'])

                Uc_pad_hat_y = self.copy_from_padded_y(Uc_pad_hat_xy2, Uc_pad_hat_y)

                Uc_pad_hat_y2[:, :, :self.N2[2]//2] = Uc_pad_hat_y[:]

                # Now both k=0 and k=N//2 are contained in 0 of comm0_rank = 0
                if self.comm1_rank == 0:
                    M = self.N[1]
                    xy_plane[:] = Uc_pad_hat_y[:, :, 0]
                    xy_plane2[:] = np.vstack((xy_plane_T[0].real, 0.5*(xy_plane_T[1:M//2]+np.conj(xy_plane_T[:M//2:-1])), xy_plane_T[M//2].real))
                    Uc_pad_hat_y2[:, :, 0] = (np.vstack((xy_plane2, np.conj(xy_plane2[(M//2-1):0:-1])))).transpose((1, 0))
                    xy_plane2[:] = np.vstack((xy_plane_T[0].imag, -0.5*1j*(xy_plane_T[1:M//2]-np.conj(xy_plane_T[:M//2:-1])), xy_plane_T[M//2].imag))
                    xy_plane_T[:] = np.vstack((xy_plane2, np.conj(xy_plane2[(M//2-1):0:-1])))
                    self.comm1.Send([xy_plane_T, self.mpitype], dest=self.P2-1, tag=77)

                if self.comm1_rank == self.P2-1:
                    self.comm1.Recv([xy_plane_T, self.mpitype], source=0, tag=77)
                    Uc_pad_hat_y2[:, :, -1] = xy_plane_T.transpose((1, 0))

                # Communicate and transform to final x-direction
                Uc_pad_hat_x2 = transform_Uc_xy(Uc_pad_hat_x2, Uc_pad_hat_y2, self.P1)
                self.comm0.Alltoall(MPI.IN_PLACE, [Uc_pad_hat_x2, self.mpitype])

                # Do fft for last direction
                Uc_pad_hat_x2[:] = fft(Uc_pad_hat_x2, axis=0, threads=self.threads,
                                       planner_effort=self.planner_effort['fft'])
                fu = self.copy_from_padded_x(Uc_pad_hat_x2, fu)
                fu /= padsize**3

            elif self.communication == 'Alltoallw':
                Uc_pad_hat_y  = self.work_arrays[((int(padsize*N1[0]), N[1], N2f), self.complex, 0)]
                Uc_pad_hat_xy = self.work_arrays[((int(padsize*N1[0]), int(padsize*N[1]), N2f), self.complex, 0)]
                Uc_pad_hat_x  = self.work_arrays[((int(padsize*N[0]), N1[1], N2f), self.complex, 0)]

                if len(self._subarrays1A_pad) == 0:
                    (self._subarrays1A_pad, self._subarrays1B_pad, self._subarrays2A_pad,
                     self._subarrays2B_pad, self._counts_displs1, self._counts_displs2) = self.get_subarrays(padsize=self.padsize)

                # Do fft in z direction on owned data
                Uc_pad_hat_z2 = rfft(u, Uc_pad_hat_z2, axis=2, threads=self.threads,
                                     planner_effort=self.planner_effort['rfft'])

                Uc_pad_hat_z = self.copy_from_padded_z(Uc_pad_hat_z2, Uc_pad_hat_z)

                self.comm1.Alltoallw(
                    [Uc_pad_hat_z, self._counts_displs2, self._subarrays2B_pad],
                    [Uc_pad_hat_xy, self._counts_displs2, self._subarrays2A_pad])

                Uc_pad_hat_xy[:] = fft(Uc_pad_hat_xy, axis=1, threads=self.threads,
                                       planner_effort=self.planner_effort['fft'])

                Uc_pad_hat_y = self.copy_from_padded_y(Uc_pad_hat_xy, Uc_pad_hat_y)

                # Communicate and transform to final x-direction
                self.comm0.Alltoallw(
                    [Uc_pad_hat_y, self._counts_displs1, self._subarrays1B_pad],
                    [Uc_pad_hat_x, self._counts_displs1, self._subarrays1A_pad])

                # Do fft for last direction
                Uc_pad_hat_x[:] = fft(Uc_pad_hat_x, axis=0, threads=self.threads,
                                      planner_effort=self.planner_effort['fft'])
                fu = self.copy_from_padded_x(Uc_pad_hat_x, fu)
                fu /= padsize**3

        return fu

def R2C(N, L, comm, precision, P1=None, communication="Alltoall", padsize=1.5, threads=1,
        alignment="X", planner_effort=defaultdict(lambda : "FFTW_MEASURE")):
    if alignment == 'X':
        return R2CX(N, L, comm, precision, P1, communication, padsize, threads, planner_effort)
    else:
        return R2CY(N, L, comm, precision, P1, communication, padsize, threads, planner_effort)
