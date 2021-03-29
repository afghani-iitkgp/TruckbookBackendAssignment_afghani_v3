import json
import sys

from Scripts.Services.DatabaseConnection.read_and_write_json_files import *
from Constants import const
from Scripts.Utility import utils

class CalculateShortestPath:
    def __init__(self):
        self.nodes = []
        self.adjacency_list = defaultdict(list)

    def create_graph(self):
        try:
            json_stations = "./Data/NammaMetro/jsonAllStations.json"
            # json_stations = "./Data/NammaMetro/jsonAllStationsDuplicate.json"
            with open(json_stations) as fl:
                data = json.load(fl)
            fl.close()

            for stations_line_dict in data:
                for line, stations_lst in stations_line_dict.items():
                    length_of_line = len(stations_lst)
                    for pos in range(length_of_line):
                        # print(stations_lst[pos], end='<-->')
                        self.add_node(stations_lst[pos].lower())

                    for pos in range(length_of_line-1):
                        if stations_lst[pos] in const.intersections_list:
                            # Handle intersection stations
                            print(stations_lst[pos], '--', line)
                        else:
                            pass
                        self.add_edge(stations_lst[pos].lower(), stations_lst[pos + 1].lower(), const.weight, line.lower())

            # return self.adjacency_list, self.nodes
        except Exception as e:
            utils.logger.error("-Error--" + str(e))



    def add_node(self, station_node):
        try:
            if station_node not in self.nodes:
                self.nodes.append(station_node)
            if station_node not in self.adjacency_list.keys():
                self.adjacency_list[station_node] = []
            # print(self.nodes)
        except Exception as e:
            utils.logger.error("-Error--" + str(e))


    def add_edge(self, station_node1, station_node2, weight, line):
        try:
            self.adjacency_list[station_node1].append( {"station_node": station_node2, "weight": weight, "line": line} )
            self.adjacency_list[station_node2].append( {"station_node": station_node1, "weight": weight, "line": line} )
        except Exception as e:
            utils.logger.error("-Error--" + str(e))




    def print_shortest_distance(self, src, dest):
        # predecessor[i] array stores predecessor of
        # i and distance array stores distance of i
        # from s
        # predecessor = [0 for i in range(v)]
        # dist = [0 for i in range(v)]

        try:
            result = {}

            # Check corner cases:
            if src != dest:

                self.create_graph()

                if ( (src in self.nodes) and (dest in self.nodes)) :
                    distance, predecessor = self.bfs_traversal_for_distance_calculation(src, dest)

                    path_src_to_dest = []
                    crawl = dest
                    path_src_to_dest.append(crawl)

                    while (predecessor[crawl] != -1):
                        path_src_to_dest.append(predecessor[crawl])
                        crawl = predecessor[crawl]

                    path_src_to_dest.reverse()
                    numberOfStationsTraverse = len(path_src_to_dest)

                    ticket_cost = const.ticket_fare["metro_fixed_cost"]
                    for i in range(numberOfStationsTraverse):

                        if "(intersection)" in path_src_to_dest[i]:
                            ticket_cost += const.ticket_fare["cost_at_intersection"]
                        else:
                            ticket_cost += const.ticket_fare["cost_at_every_station_passes"]

                        path_src_to_dest[i] = path_src_to_dest[i].title()

                    result["time_to_travel_distance"] = distance
                    result["path"] = path_src_to_dest
                    result["number_of_stations_traversed"] = numberOfStationsTraverse
                    result["ticket_cost"] = round(ticket_cost, 2)

                    result["status"] = 200
                    result["message"] = "Success"
                else:
                    result["time_to_travel_distance"] = 0
                    result["path"] = []
                    result["number_of_stations_traversed"] = 0
                    result["ticket_cost"] = 0

                    if src not in self.nodes and dest in self.nodes:
                        result["status"] = 4061
                        result["message"] = "Source not found in the route"
                    elif src in self.nodes and dest not in self.nodes:
                        result["status"] = 4062
                        result["message"] = "Destination not found in the route"
                    elif src not in self.nodes and dest not in self.nodes:
                        result["status"] = 4062
                        result["message"] = "Neither source nor destination found in the route"

            else:
                result["time_to_travel_distance"] = 0
                result["path"] = []
                result["number_of_stations_traversed"] = 0
                result["ticket_cost"] = 0

                result["status"] = 404
                result["message"] = "source and destination are same, please enter different stations"

            return result


        except Exception as e:
            utils.logger.error("-Error--" + str(e))


    def bfs_traversal_for_distance_calculation(self, src, dest):
        try:
            # V = len(self.nodes)

            queue = []
            dist = {}
            pred = {}
            visited = {}

            for station in self.nodes:
                dist[station] = sys.maxsize
                pred[station] = -1
                visited[station] = False

            visited[src] = True
            dist[src] = 0
            queue.append(src)

            while (len(queue) > 0):
                u = queue[0]
                queue.pop(0)

                for node in self.adjacency_list[u]:
                    if ( visited[ node['station_node'] ] == False ):
                        visited[node["station_node"]] = True
                        dist[node["station_node"]] = dist[u] + const.distance_between_two_stations
                        pred[node["station_node"]] = u

                        queue.append(node["station_node"])

                        if node["station_node"] == dest:
                            return dist[node["station_node"]], pred

        except Exception as e:
            utils.logger.error("-Error--" + str(e))



