from m5.params import *
from m5.SimObject import SimObject


class Scratchpad(SimObject):
    type = "Scratchpad"
    cxx_header = "mem/ruby/structures/scratchpad.hh"
    cxx_class = "gem5::ruby::Scratchpad"

    time_to_wait = Param.Latency("Time before firing the event")
    size = Param.MemorySize("64MiB", "Size of memory inside of scratchpad")
    ruby_system = Param.RubySystem(Parent.any, "the parent ruby system")
