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
from math import isqrt

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
        num_routers = options.num_cpus // 4 + 1
        print("num of routers: " + str(num_routers))


        link_latency = options.link_latency  # used by simple and garnet
        router_latency = options.router_latency  # only used by garnet
        routers = [Router (router_id=i, latency=router_latency) for i in range(num_routers)]

        network.routers = routers

        # Count for every single link to make each link unique
        link_count = 0

        # list of all links that connect routers to other routers
        int_links = []

        # list of all links that connect external components to routers
        ext_links = []

        # lists of specific controllers
        cpu_nodes = [n for n in nodes if n.type == "L1Cache_Controller" ]
        print("initial size: " + str(len(cpu_nodes)))
        l2_nodes  = [n for n in nodes if n.type == "L2Cache_Controller"] 
        print("l2 nodes: " + str(len(l2_nodes)))
        dir_nodes = [n for n in nodes if n.type == "Directory_Controller"]
        print("dir nodes: " + str(len(dir_nodes)))
        
        cpu_per_router = 4

        for rtrId in range(num_routers):
            #only mpe links
            if rtrId == num_routers - 1:
                ext_links.append(
                    ExtLink(
                            link_id=link_count,
                            ext_node=cpu_nodes.pop(),
                            int_node=routers[num_routers - 1],
                            latency=link_latency*2,            
                    )
			    )
                link_count += 1
                ext_links.append(
                    ExtLink(
                            link_id=link_count,
                            ext_node=dir_nodes.pop(),
                            int_node=routers[num_routers - 1],
                            latency=link_latency,            
                        )
                    )
                link_count += 1
                for n in l2_nodes:
                    ext_links.append(
                    ExtLink(
                            link_id=link_count,
                            ext_node=l2_nodes.pop(),
                            int_node=routers[num_routers - 1],
                            latency=link_latency,            
                        )
                    )
                    link_count += 1
                
                print("not initial size: " + str(len(cpu_nodes)))
                
            # other cpe links
            else:
                for cpuId in range(cpu_per_router):
                    print("id: " + str((rtrId * cpu_per_router) + cpuId))
                    ext_links.append(
                    ExtLink(
                            link_id=link_count,
                            ext_node=cpu_nodes.pop(),
                            int_node=routers[rtrId],
                            latency=link_latency,            
                        )
                    )      
                link_count += 1          

            


        # for i, n in  enumerate(nodes):
        #     ext_links.append(
        #         ExtLink(
        #             link_id=link_count,
        #             ext_node=n,
        #             int_node=routers[i % num_routers],
        #             latency=link_latency,
        #         )
        #     )
        #     link_count += 1
        
        
        # for i in range(2):
        #     n = nodes[i]
        #     ext_links.append(
		# 		ExtLink(
		# 				link_id=link_count,
		# 				ext_node=n,
		# 				int_node=routers[0],
		# 				latency=link_latency,            
		# 		)
		# 	)
        #     link_count += 1
        
        # for i in range(2):
        #     n = nodes[i+2]
        #     ext_links.append(
		# 		ExtLink(
		# 				link_id=link_count,
		# 				ext_node=n,
		# 				int_node=routers[1],
		# 				latency=link_latency,            
		# 		)
		# 	)
        #     link_count += 1
        # for i in range(2):
        #     n = nodes[i + 4]
        #     ext_links.append(
		# 		ExtLink(
		# 				link_id=link_count,
		# 				ext_node=n,
		# 				int_node=routers[2],
		# 				latency=link_latency,            
		# 		)
		# 	)
        #     link_count += 1
        
        # for i in range(2):
        #     n = nodes[i+6]
        #     ext_links.append(
		# 		ExtLink(
		# 				link_id=link_count,
		# 				ext_node=n,
		# 				int_node=routers[3],
		# 				latency=link_latency,            
		# 		)
		# 	)
        #     link_count += 1
        # for i in range(3):
        #     n = nodes[i + 8]
        #     ext_links.append(
		# 		ExtLink(
		# 				link_id=link_count,
		# 				ext_node=n,
		# 				int_node=routers[4],
		# 				latency=link_latency,            
		# 		)
		# 	)
        #     link_count += 1

        network.ext_links = ext_links









        # int_links.append(
        #     IntLink(
        #         link_id=link_count,
        #         src_node=routers[4],
        #         dst_node=routers[1],
        #         src_outport="West",
        #         dst_inport="East",
        #         latency=link_latency,
        #         weight=1,
        #     )
        # )
        # link_count += 1
        # int_links.append(
        #     IntLink(
        #         link_id=link_count,
        #         src_node=routers[1],
        #         dst_node=routers[4],
        #         src_outport="East",
        #         dst_inport="West",
        #         latency=link_latency,
        #         weight=1,
        #     )
        # )
        # link_count += 1
        # int_links.append(
        #     IntLink(
        #         link_id=link_count,
        #         src_node=routers[1],
        #         dst_node=routers[2],
        #         src_outport="West",
        #         dst_inport="East",
        #         latency=link_latency,
        #         weight=1,
        #     )
        # )
        # link_count += 1
        # int_links.append(
        #     IntLink(
        #         link_id=link_count,
        #         src_node=routers[2],
        #         dst_node=routers[1],
        #         src_outport="East",
        #         dst_inport="West",
        #         latency=link_latency,
        #         weight=1,
        #     )
        # )
        # link_count += 1
        # int_links.append(
        #     IntLink(
        #         link_id=link_count,
        #         src_node=routers[2],
        #         dst_node=routers[3],
        #         src_outport="West",
        #         dst_inport="East",
        #         latency=link_latency,
        #         weight=1,
        #     )
        # )
        # link_count += 1
        # int_links.append(
        #     IntLink(
        #         link_id=link_count,
        #         src_node=routers[3],
        #         dst_node=routers[2],
        #         src_outport="East",
        #         dst_inport="West",
        #         latency=link_latency,
        #         weight=1,
        #     )
        # )
        # link_count += 1
        # int_links.append(
        #     IntLink(
        #         link_id=link_count,
        #         src_node=routers[3],
        #         dst_node=routers[4],
        #         src_outport="West",
        #         dst_inport="East",
        #         latency=link_latency,
        #         weight=1,
        #     )
        # )
        # link_count += 1
        # int_links.append(
        #     IntLink(
        #         link_id=link_count,
        #         src_node=routers[4],
        #         dst_node=routers[3],
        #         src_outport="East",
        #         dst_inport="West",
        #         latency=link_latency,
        #         weight=1,
        #     )
        # )
        # link_count += 1
        # int_links.append(
        #     IntLink(
        #         link_id=link_count,
        #         src_node=routers[0],
        #         dst_node=routers[4],
        #         src_outport="West",
        #         dst_inport="East",
        #         latency=link_latency,
        #         weight=1,
        #     )
        # )
        # link_count += 1
        # int_links.append(
        #     IntLink(
        #         link_id=link_count,
        #         src_node=routers[4],
        #         dst_node=routers[0],
        #         src_outport="East",
        #         dst_inport="West",
        #         latency=link_latency,
        #         weight=1,
        #     )
        # )
        # link_count += 1

        # East output to West input links (weight = 1)
        num_rows = isqrt(num_routers-1)
        print("rows that are supposed to be there : " + str(num_rows))
        num_columns = num_rows
        for row in range(num_rows):
            for col in range(num_columns):
                if col + 1 < num_columns:
                    east_out = col + (row * num_columns)
                    west_in = (col + 1) + (row * num_columns)
                    int_links.append(
                        IntLink(
                            link_id=link_count,
                            src_node=routers[east_out],
                            dst_node=routers[west_in],
                            src_outport="East",
                            dst_inport="West",
                            latency=link_latency,
                            weight=1,
                        )
                    )
                    link_count += 1

        # West output to East input links (weight = 1)
        for row in range(num_rows):
            for col in range(num_columns):
                if col + 1 < num_columns:
                    east_in = col + (row * num_columns)
                    west_out = (col + 1) + (row * num_columns)
                    int_links.append(
                        IntLink(
                            link_id=link_count,
                            src_node=routers[west_out],
                            dst_node=routers[east_in],
                            src_outport="West",
                            dst_inport="East",
                            latency=link_latency,
                            weight=1,
                        )
                    )
                    link_count += 1

        # North output to South input links (weight = 2)
        for col in range(num_columns):
            for row in range(num_rows):
                if row + 1 < num_rows:
                    north_out = col + (row * num_columns)
                    south_in = col + ((row + 1) * num_columns)
                    int_links.append(
                        IntLink(
                            link_id=link_count,
                            src_node=routers[north_out],
                            dst_node=routers[south_in],
                            src_outport="North",
                            dst_inport="South",
                            latency=link_latency,
                            weight=1,
                        )
                    )
                    link_count += 1

        # South output to North input links (weight = 2)
        for col in range(num_columns):
            for row in range(num_rows):
                if row + 1 < num_rows:
                    north_in = col + (row * num_columns)
                    south_out = col + ((row + 1) * num_columns)
                    int_links.append(
                        IntLink(
                            link_id=link_count,
                            src_node=routers[south_out],
                            dst_node=routers[north_in],
                            src_outport="South",
                            dst_inport="North",
                            latency=link_latency,
                            weight=1,
                        )
                    )
                    link_count += 1

        int_links.append(
            IntLink(
                    link_id=link_count,
                    src_node=routers[-1],
                    dst_node=routers[0],
                    src_outport="South",
                    dst_inport="North",
                    latency=link_latency,
                    weight=1,
            )   
        )

        int_links.append(
            IntLink(
                    link_id=link_count,
                    src_node=routers[0],
                    dst_node=routers[-1],
                    src_outport="South",
                    dst_inport="North",
                    latency=link_latency,
                    weight=1,
            )   
        )


        # #connect the mesh to big bus router
        # for i in range(num_columns + 1):
        #     if i == 0:
        #         continue
        #     id = len(routers) - i - 2
        #     busRouter = len(routers) - 1
        #     int_links.append(
        #         IntLink(
        #             link_id=link_count,
        #             src_node=routers[id],
        #             dst_node=routers[busRouter],
        #             src_outport="toBus",
        #             dst_inport="forBus" + str(link_count),
        #             latency=link_latency,
        #             weight=1,
        #         )
        #     )
        #     int_links.append(
        #         IntLink(
        #             link_id=link_count,
        #             src_node=routers[busRouter],
        #             dst_node=routers[id],
        #             src_outport="fromBus" + str(link_count),
        #             dst_inport="byBus",
        #             latency=link_latency,
        #             weight=1,
        #         )
        #     )

        network.int_links = int_links



    # Register nodes with filesystem
    def registerTopology(self, options):
        for i in range(options.num_cpus):
            FileSystemConfig.register_node(
                [i], MemorySize(options.mem_size) // options.num_cpus, i
            )
