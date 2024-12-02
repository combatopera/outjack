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
from .portaudioclient import PortAudioClient
import math

bufsize = 1024
freq = 44100
tone = 440
vol = .5

def main():
    client = PortAudioClient(1, freq, bufsize, 2, True)
    client.start()
    try:
        client.activate()
        try:
            k = 0
            buffer = client.current_output_buffer()
            while True:
                for i in range(bufsize):
                    buffer[i] = math.sin(2 * math.pi * tone * (k + i) / freq) * vol
                k += bufsize
                buffer = client.send_and_get_output_buffer()
        finally:
            client.deactivate()
    finally:
        client.stop()

if '__main__' == __name__:
    main()
