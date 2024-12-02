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
from argparse import ArgumentParser
from outjack.jackclient import JackClient
from outjack.portaudioclient import PortAudioClient
import logging, numpy as np

log = logging.getLogger(__name__)
amplitude = .5
ringsize = 2

def main(): # FIXME: Do not play garbage at first.
    logging.basicConfig(format = "%(levelname)s %(message)s", level = logging.DEBUG)
    parser = ArgumentParser()
    parser.add_argument('--client', choices = ['jack', 'portaudio'], default = 'portaudio')
    parser.add_argument('--frequency', type = float, default = 440)
    args = parser.parse_args()
    frequency = args.frequency
    if 'portaudio' == args.client:
        client = PortAudioClient(1, 44100, 1024, ringsize, True)
        def onstart():
            pass
        def onactivate():
            pass
    else:
        client = JackClient('ojplay', 1, ringsize, True)
        def onstart():
            client.port_register_output('tone')
        def onactivate():
            for sink in 'playback_1', 'playback_2':
                client.connect(0, f"system:{sink}")
    client.start()
    try:
        buffersize = client.buffersize
        outputrate = client.outputrate
        log.debug(dict(buffersize = buffersize, outputrate = outputrate))
        onstart()
        client.activate()
        try:
            onactivate()
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
