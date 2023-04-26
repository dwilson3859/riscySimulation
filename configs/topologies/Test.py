# Copyright (c) 2010 Advanced Micro Devices, Inc.
#               2016 Georgia Institute of Technology
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met: redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer;
# redistributions in binary form must reproduce the above copyright
# notice, this list of conditions and the following disclaimer in the
# documentation and/or other materials provided with the distribution;
# neither the name of the copyright holders nor the names of its
# contributors may be used to endorse or promote products derived from
# this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

from m5.params import *
from m5.objects import *

from common import FileSystemConfig

from topologies.BaseTopology import SimpleTopology

# Creates a generic Mesh assuming an equal number of cache
# and directory controllers.
# XY routing is enforced (using link weights)
# to guarantee deadlock freedom.


class Test(SimpleTopology):
    description = "test"

    def __init__(self, controllers):
        self.nodes = controllers

    # Makes a generic mesh
    # assuming an equal number of cache and directory cntrls

    def makeTopology(self, options, network, IntLink, ExtLink, Router):
        nodes = self.nodes


        link_latency = options.link_latency  # used by simple and garnet
        router_latency = options.router_latency  # only used by garnet
        routers = [Router (router_id=i, latency=router_latency) for i in range(5)]

        network.routers = routers
        
        # link counter to set unique link ids
        link_count = 0

        # Add all but the remainder nodes to the list of nodes to be uniformly
        # distributed across the network.
        network_nodes = []
        remainder_nodes = []  
        # Connect each node to the appropriate router
        # Create the mesh links.
        int_links = []
        ext_links = []
        
        
        for i in range(2):
            n = nodes[i]
            ext_links.append(
				ExtLink(
						link_id=link_count,
						ext_node=n,
						int_node=routers[0],
						latency=link_latency,            
				)
			)
            link_count += 1
        
        for i in range(2):
            n = nodes[i+2]
            ext_links.append(
				ExtLink(
						link_id=link_count,
						ext_node=n,
						int_node=routers[1],
						latency=link_latency,            
				)
			)
            link_count += 1
        for i in range(2):
            n = nodes[i + 4]
            ext_links.append(
				ExtLink(
						link_id=link_count,
						ext_node=n,
						int_node=routers[2],
						latency=link_latency,            
				)
			)
            link_count += 1
        
        for i in range(2):
            n = nodes[i+6]
            ext_links.append(
				ExtLink(
						link_id=link_count,
						ext_node=n,
						int_node=routers[3],
						latency=link_latency,            
				)
			)
            link_count += 1
        for i in range(3):
            n = nodes[i + 8]
            ext_links.append(
				ExtLink(
						link_id=link_count,
						ext_node=n,
						int_node=routers[4],
						latency=link_latency,            
				)
			)
            link_count += 1

        network.ext_links = ext_links









        int_links.append(
            IntLink(
                link_id=link_count,
                src_node=routers[0],
                dst_node=routers[1],
                src_outport="West",
                dst_inport="East",
                latency=link_latency,
                weight=1,
            )
        )
        link_count += 1
        int_links.append(
            IntLink(
                link_id=link_count,
                src_node=routers[1],
                dst_node=routers[0],
                src_outport="East",
                dst_inport="West",
                latency=link_latency,
                weight=1,
            )
        )
        link_count += 1
        int_links.append(
            IntLink(
                link_id=link_count,
                src_node=routers[1],
                dst_node=routers[2],
                src_outport="West",
                dst_inport="East",
                latency=link_latency,
                weight=1,
            )
        )
        link_count += 1
        int_links.append(
            IntLink(
                link_id=link_count,
                src_node=routers[2],
                dst_node=routers[1],
                src_outport="East",
                dst_inport="West",
                latency=link_latency,
                weight=1,
            )
        )
        link_count += 1
        int_links.append(
            IntLink(
                link_id=link_count,
                src_node=routers[2],
                dst_node=routers[3],
                src_outport="West",
                dst_inport="East",
                latency=link_latency,
                weight=1,
            )
        )
        link_count += 1
        int_links.append(
            IntLink(
                link_id=link_count,
                src_node=routers[3],
                dst_node=routers[2],
                src_outport="East",
                dst_inport="West",
                latency=link_latency,
                weight=1,
            )
        )
        link_count += 1
        int_links.append(
            IntLink(
                link_id=link_count,
                src_node=routers[3],
                dst_node=routers[0],
                src_outport="West",
                dst_inport="East",
                latency=link_latency,
                weight=1,
            )
        )
        link_count += 1
        int_links.append(
            IntLink(
                link_id=link_count,
                src_node=routers[0],
                dst_node=routers[3],
                src_outport="East",
                dst_inport="West",
                latency=link_latency,
                weight=1,
            )
        )
        link_count += 1
        int_links.append(
            IntLink(
                link_id=link_count,
                src_node=routers[4],
                dst_node=routers[0],
                src_outport="West",
                dst_inport="East",
                latency=link_latency,
                weight=1,
            )
        )
        link_count += 1
        int_links.append(
            IntLink(
                link_id=link_count,
                src_node=routers[0],
                dst_node=routers[4],
                src_outport="East",
                dst_inport="West",
                latency=link_latency,
                weight=1,
            )
        )
        link_count += 1

        network.int_links = int_links



    # Register nodes with filesystem
    def registerTopology(self, options):
        for i in range(options.num_cpus):
            FileSystemConfig.register_node(
                [i], MemorySize(options.mem_size) // options.num_cpus, i
            )
