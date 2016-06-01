**mcstasGenerator**
-------------------

Converts a McStas formatted output into an event stream and send it via 0MQ. It
is designed to be flexible, allowing to build an instrument and its ouput from a set of detectors.

DESCRIPTION
-----------

The package consists of an "instrument" (detector.py,instrument.py) and a
"generator" (zmqGenerator.py) section.  

The instrument can be built assempling different monitors (in McSats
language). These can be 1-D, 2-D or n-D detectors suche as ToF monitors, area
detectors,... Detectors are build passing a string containing the McStas
output. The instrument can be therefore built passing the relevant filenames and
returns the data stream using ``mcstas2stream`` method, that requires an array
containing the hardware status flags.

In order to build the generator a portnumber and a multiplier are required. The
former is the port 0MQ socket will connect to, while the latter allows to
increment the data size making use of ``multiplier`` replicas. The generator has
to be started with the method ``run``, that requires a vector containing the
data stream and a string containing the filename of a control file that drives
it (see CONTROL section for further information).


CONTROL
-------

'control.in' is an example of control file. The generator has three statuses:
``run``,``pause`` and ``stop``. The ``run`` obvious, the generator streams the header and the data blob; in ``pause`` status the generator only send the header, that acts as a hearthbeat; in ``stop`` status the generator stops and the program is terminated properly. ``bsy``,``cnt``,``rok`` and ``gat`` are hardware flags: if their value is 1 everything is ok, if any of them is 0 the event has to be discarded. ``evt`` describe the event type (according to RITA2 data specification). ``mutation`` introduces random modifications in the data stream to emulate errors. Allowed values are
  - 'nev': removes one or more events
  - 'ts': invalidates one timestamp
  - 'pos': invalidates one or more position
  - 'all': all the previous
Last, ``rate`` sets the frequency of communications.
