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

from .ring cimport Payload
from cpython.ref cimport PyObject

cdef extern from "portaudio.h":

    DEF paFloat32 = 0x00000001

    cdef enum PaStreamCallbackResult:
        paContinue = 0

    ctypedef double PaTime

    ctypedef struct PaStreamCallbackTimeInfo:
        PaTime inputBufferAdcTime
        PaTime currentTime
        PaTime outputBufferDacTime

    ctypedef int PaError

    ctypedef void PaStream

    ctypedef unsigned long PaSampleFormat

    ctypedef unsigned long PaStreamCallbackFlags

    ctypedef int PaStreamCallback(const void*, void*, unsigned long, const PaStreamCallbackTimeInfo*, PaStreamCallbackFlags, void*)

    PaError Pa_Initialize()
    PaError Pa_Terminate()
    PaError Pa_OpenDefaultStream(PaStream**, int, int, PaSampleFormat, double, unsigned long, PaStreamCallback*, void*)
    PaError Pa_CloseStream(PaStream*)

cdef int callback(const void* input, void* output, unsigned long frameCount, const PaStreamCallbackTimeInfo* timeInfo, PaStreamCallbackFlags statusFlags, void* userData):
    cdef Payload payload = <Payload> userData
    payload.callback(frameCount)
    return paContinue

cdef class Client:

    cdef PaStream* stream
    cdef Payload payload
    cdef int chancount
    cdef double samplerate
    cdef unsigned long buffersize

    def __init__(self, chancount, samplerate, buffersize):
        Pa_Initialize()
        self.payload = Payload()
        self.chancount = chancount
        self.samplerate = samplerate
        self.buffersize = buffersize

    def activate(self):
        Pa_OpenDefaultStream(&self.stream, 0, self.chancount, paFloat32, self.samplerate, self.buffersize, &callback, <PyObject*> self.payload)

    def current_output_buffer(self):
        raise Exception('Implement me!')

    def send_and_get_output_buffer(self):
        raise Exception('Implement me!')

    def deactivate(self):
        Pa_CloseStream(self.stream)

    def dispose(self):
        Pa_Terminate()
