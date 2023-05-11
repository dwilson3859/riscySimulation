#include "learning_gem5/part2/scratchpad.hh"

#include "base/trace.hh"
#include "debug/HelloExample.hh"

namespace gem5
{

Scratchpad::Scratchpad(ScratchpadParams *params) :
    SimObject(params),
	event([this]{processEvent();}, name()),
	myName(params.name),
	latency(params.time_to_wait),
	size(params.size)
{
    DPRINTF(Scratchpad, "Created the scratchpad\n");
}

void
Scratchpad::startup()
{
	schedule(event, latency)
}

void
Scratchpad::processEvent()
{
	timesLeft--;
	DPRINTF(Scratchpad, "Processing Scratch event :)  %d left\n", timesLeft);

	if (timesLeft <= 0) {
		DPRINTF(Scratchpad, "Done with scratch \n");
	} else {
		schedule(event, curTick() + latency);
	}
}


} // namespace gem5
