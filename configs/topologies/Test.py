# hehehe donaldo rocks

from m5.params import *
from m5.objects import *
from math import isqrt

from common import FileSystemConfig

from topologies.BaseTopology import SimpleTopology


class Test(SimpleTopology):
    description = "test"

    def __init__(self, controllers):
        self.nodes = controllers

    # Makes a generic mesh
    # assuming an equal number of cache and directory cntrls

    def makeTopology(self, options, network, IntLink, ExtLink, Router):
        nodes = self.nodes
        num_coregroups = options.num_dirs
        rtrs_per_mesh = 16
        rtrs_per_mpe = 1
        num_routers = (rtrs_per_mesh + rtrs_per_mpe) * num_coregroups
        cpu_per_router = 4
        sockets = 1
        print("num of routers: " + str(num_routers))

        link_latency = options.link_latency  # used by simple and garnet
        router_latency = options.router_latency  # only used by garnet
        cpe_routers = [
            Router(router_id=i, latency=router_latency)
            for i in range(rtrs_per_mesh * num_coregroups)
        ]
        mpe_routers = [
            Router(router_id=i + len(cpe_routers), latency=router_latency)
            for i in range(num_coregroups)
        ]

        network.routers = cpe_routers + mpe_routers

        # Count for every single link to make each link unique
        link_count = 0

        # list of all links that connect routers to other routers
        int_links = []

        # list of all links that connect external components to routers
        ext_links = []

        # lists of specific controllers
        cpu_nodes = [n for n in nodes if n.type == "L1Cache_Controller"]
        print("initial size: " + str(len(cpu_nodes)))
        l2_nodes = [n for n in nodes if n.type == "L2Cache_Controller"]
        print("l2 nodes: " + str(len(l2_nodes)))
        dir_nodes = [n for n in nodes if n.type == "Directory_Controller"]
        print("dir nodes: " + str(len(dir_nodes)))

        for rtr in cpe_routers:
            for cpuId in range(cpu_per_router):
                ext_links.append(
                    ExtLink(
                        link_id=link_count,
                        ext_node=cpu_nodes.pop(),
                        int_node=rtr,
                        latency=link_latency,
                    )
                )
            link_count += 1

        for rtr in mpe_routers:
            ext_links.append(
                ExtLink(
                    link_id=link_count,
                    ext_node=cpu_nodes.pop(),
                    int_node=rtr,
                    latency=link_latency * 2,
                )
            )
            link_count += 1
            ext_links.append(
                ExtLink(
                    link_id=link_count,
                    ext_node=dir_nodes.pop(),
                    int_node=rtr,
                    latency=link_latency,
                )
            )
            link_count += 1
            for n in l2_nodes:
                ext_links.append(
                    ExtLink(
                        link_id=link_count,
                        ext_node=l2_nodes.pop(),
                        int_node=rtr,
                        latency=link_latency,
                    )
                )
                link_count += 1

        network.ext_links = ext_links

        # _________________________link inbetween routers :)  _______________________________________________________

        # make mesh topology for routers connected to cpe's

        # East output to West input links (weight = 1)
        num_rows = isqrt(num_routers // num_coregroups)
        print("rows that are supposed to be there : " + str(num_rows))
        num_columns = num_rows
        for cgid in range(num_coregroups):
            for row in range(num_rows):
                for col in range(num_columns):
                    if col + 1 < num_columns:
                        east_out = col + (row * num_columns)
                        west_in = (col + 1) + (row * num_columns)
                        int_links.append(
                            IntLink(
                                link_id=link_count,
                                src_node=cpe_routers[
                                    east_out + (cgid * num_rows * num_columns)
                                ],
                                dst_node=cpe_routers[
                                    west_in + (cgid * num_rows * num_columns)
                                ],
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
                                src_node=cpe_routers[
                                    west_out + (cgid * num_rows * num_columns)
                                ],
                                dst_node=cpe_routers[
                                    east_in + (cgid * num_rows * num_columns)
                                ],
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
                                src_node=cpe_routers[
                                    north_out + (cgid * num_rows * num_columns)
                                ],
                                dst_node=cpe_routers[
                                    south_in + (cgid * num_rows * num_columns)
                                ],
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
                                src_node=cpe_routers[
                                    south_out + (cgid * num_rows * num_columns)
                                ],
                                dst_node=cpe_routers[
                                    north_in + (cgid * num_rows * num_columns)
                                ],
                                src_outport="South",
                                dst_inport="North",
                                latency=link_latency,
                                weight=1,
                            )
                        )
                        link_count += 1

        # inter connect mpe routers to their corresponding mesh
        for cgid, rtr in enumerate(mpe_routers):
            int_links.append(
                IntLink(
                    link_id=link_count,
                    src_node=rtr,
                    dst_node=cpe_routers[cgid * num_rows * num_columns],
                    src_outport="North",
                    dst_inport="South",
                    latency=link_latency,
                    weight=1,
                )
            )
            link_count += 1

            int_links.append(
                IntLink(
                    link_id=link_count,
                    src_node=cpe_routers[cgid * num_rows * num_columns],
                    dst_node=rtr,
                    src_outport="South",
                    dst_inport="North",
                    latency=link_latency,
                    weight=1,
                )
            )
            link_count += 1

        for mpeCount, rtr in enumerate(mpe_routers):

            # make ring under here :)
            if num_coregroups == 1:
                continue
            elif num_coregroups == 2:
                int_links.append(
                    IntLink(
                        link_id=link_count,
                        src_node=mpe_routers[0],
                        dst_node=rtr,
                        src_outport="leftRing",
                        dst_inport="rightRing",
                        latency=link_latency,
                        weight=1,
                    )
                )
                link_count += 1
                int_links.append(
                    IntLink(
                        link_id=link_count,
                        src_node=rtr,
                        dst_node=mpe_routers[0],
                        src_outport="rightRing",
                        dst_inport="leftRing",
                        latency=link_latency,
                        weight=1,
                    )
                )
                link_count += 1

            elif mpeCount == len(mpe_routers) - 1:
                int_links.append(
                    IntLink(
                        link_id=link_count,
                        src_node=mpe_routers[0],
                        dst_node=rtr,
                        src_outport="leftRing",
                        dst_inport="rightRing",
                        latency=link_latency,
                        weight=1,
                    )
                )
                link_count += 1
                int_links.append(
                    IntLink(
                        link_id=link_count,
                        src_node=rtr,
                        dst_node=mpe_routers[0],
                        src_outport="rightRing",
                        dst_inport="leftRing",
                        latency=link_latency,
                        weight=1,
                    )
                )
                link_count += 1
            else:
                int_links.append(
                    IntLink(
                        link_id=link_count,
                        src_node=rtr,
                        dst_node=mpe_routers[mpeCount + 1],
                        src_outport="leftRing",
                        dst_inport="rightRing",
                        latency=link_latency,
                        weight=1,
                    )
                )
                link_count += 1
                int_links.append(
                    IntLink(
                        link_id=link_count,
                        src_node=mpe_routers[mpeCount + 1],
                        dst_node=rtr,
                        src_outport="rightRing",
                        dst_inport="leftRing",
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
