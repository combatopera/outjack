# Copyright 2017, 2020 Andrzej Cichocki

# This file is part of outjack.
#
# outjack is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# outjack is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with outjack.  If not, see <http://www.gnu.org/licenses/>.

# cython: language_level=3

from .jack cimport jack_default_audio_sample_t, jack_nframes_t

cdef extern from "pthread.h":

    ctypedef struct pthread_mutex_t:
        pass

    ctypedef struct pthread_cond_t:
        pass

    int pthread_mutex_init(pthread_mutex_t*, void*)
    int pthread_mutex_lock(pthread_mutex_t*)
    int pthread_mutex_unlock(pthread_mutex_t*)
    int pthread_cond_init(pthread_cond_t*, void*)
    int pthread_cond_signal(pthread_cond_t*)
    int pthread_cond_wait(pthread_cond_t*, pthread_mutex_t*) nogil

cdef class Payload:

    cdef object ports
    cdef pthread_mutex_t mutex
    cdef pthread_cond_t cond
    cdef unsigned ringsize
    cdef jack_default_audio_sample_t** chunks
    cdef unsigned writecursor # Always points to a free chunk.
    cdef unsigned readcursor
    cdef size_t bufferbytes
    cdef size_t buffersize
    cdef bint coupling

    cdef unsigned send(self, jack_default_audio_sample_t* samples)

    cdef callback(self, jack_nframes_t nframes)
