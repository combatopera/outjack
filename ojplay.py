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

'Usage example.'
__import__('pyrbo.jit')
from outjack.jackclient import JackClient
from outjack.portaudioclient import PortAudioClient
import numpy as np

amplitude = .5
frequency = 440
ringsize = 2

def main():
    if True:
        client = PortAudioClient(1, 44100, 1024, ringsize, True)
    else:
        client = JackClient('ojplay', 1, ringsize, True)
    client.start()
    try:
        buffersize = client.buffersize
        outputrate = client.outputrate
        client.activate()
        try:
            k = 0
            buffer = client.current_output_buffer()
            while True:
                buffer[:] = np.sin(np.arange(k, k + buffersize) * (2 * np.pi * frequency / outputrate)) * amplitude
                k += buffersize
                buffer = client.send_and_get_output_buffer()
        finally:
            client.deactivate()
    finally:
        client.stop()

if '__main__' == __name__:
    main()
