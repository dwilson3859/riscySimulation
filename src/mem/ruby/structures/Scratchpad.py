from m5.params import *
from m5.SimObject import SimObject

class Scratchpad(SimObject):
    type = 'Scratchpad'
    cxx_header = "mem/ruby/structures/scratchpad.hh"
    cxx_class = "gem5::ruby::Scratchpad"

    time_to_wait = Param.Latency("Time before firing the event")
    number_of_fires = Param.Int(1, "Number of times to fire the event before "
                                   "goodbye")