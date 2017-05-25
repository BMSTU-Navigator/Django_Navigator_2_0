from Navigator.models import *
import logging
from shutil import copyfile
from Navigator.views import *


class Building:
    graph = None
    floors = None

    @staticmethod
    def get_building():
        building = Building()
        building.graph = Graph.get_graph()
        building.floors = Instance.objects.filter()
        return building


class Graph:
    connections = []
    points = []
    points_dict = {}

    def __init__(self):
        super().__init__()
        # load data from db

    @staticmethod
    def get_graph():
        graph = Graph()
        graph.connections = GraphConnection.objects.filter()
        graph.points = Point.objects.filter()
        graph.points_dict = {}
        for point in graph.points:
            graph.points_dict[point.id] = point
        return graph


class Path:
    points = []
    connections = []
    floors = []
    floors_obj = {}
    weight = -1

    def clearr(self):
        self.points = []
        self.connections = []
        self.floors = []
        self.weight = -1


class WayBuilderClass:
    building = None
    paths = None
    dijkstra_weight = None
    dijkstra_connectons = None
    max_id = -1
    key_val = 1
    pre_key = 'tmp_pic'
    pre_path = './pic_dir/tmp_pic_dir/'
    logger = None

    def __init__(self, building):
        self.logger = logging.getLogger('WayBuilder')
        self.logger.debug('init WB class')
        self.logger.debug('request building')
        self.building = building
        self.logger.debug('pre count')
        self.init_pre_count()
        return

    def init_pre_count(self):
        for tmp_point in self.building.graph.points:
            if tmp_point.id >= self.max_id:
                self.max_id = tmp_point.id
        self.max_id += 1
        self.paths = [self.max_id]
        self.dijkstra_weight = []
        for i in range(self.max_id):
            self.dijkstra_weight.append([10000] * self.max_id)
        for conection in self.building.graph.connections:
            self.dijkstra_weight[conection.point1.id][conection.point2.id] = conection.connection_weight

    def dijkstra(self, start, stop):
        self.logger.debug('dekstra start:' + str(start) + ' stop:' + str(stop))
        self.dijkstra_connectons = []
        for i in range(0, len(self.dijkstra_weight)):
            self.dijkstra_connectons.append([])
            for j in range(0, len(self.dijkstra_weight[i])):
                if self.dijkstra_weight[i][j] < 10000:
                    self.dijkstra_connectons[i].append(j)

        print(self.dijkstra_connectons)
        self.logger.debug(self.dijkstra_connectons)
        size = self.max_id
        infinity = 10 ** 10

        dist = [infinity] * size
        dist[start] = 0
        prev = [None] * size
        used = [False] * size
        min_dist = 0
        min_vertex = start
        while min_dist < infinity:
            i = min_vertex
            used[i] = True
            for j in self.dijkstra_connectons[i]:
                if dist[i] + self.dijkstra_weight[i][j] < dist[j]:
                    dist[j] = dist[i] + self.dijkstra_weight[i][j]
                    prev[j] = i
            min_dist = infinity
            for i in range(size):
                if not used[i] and dist[i] < min_dist:
                    min_dist = dist[i]
                    min_vertex = i

        self.paths = []
        while stop is not None:
            self.paths.append(stop)
            stop = prev[stop]
        self.paths = self.paths[::-1]

        sum_weight = 0
        for i in range(0, len(self.paths) - 1):
            sum_weight += self.dijkstra_weight[self.paths[i]][self.paths[i + 1]]

        return sum_weight

    def request_path(self, start, stop):
        self.logger.debug('start request path start:' + str(start) + ' stop:' + str(stop))
        weight = self.dijkstra(start, stop)
        print(self.paths)

        path = Path()
        path.clearr()
        print(Path.floors)
        self.logger.debug(Path.floors)

        path.weight = weight

        for point_id in self.paths:
            for point in self.building.graph.points:
                if point.id == point_id:
                    path.points.append(point)
                    break

        for i in range(0, len(path.points) - 1):
            for connection in self.building.graph.connections:
                if connection.point1.id == path.points[i].id and connection.point2.id == path.points[i + 1].id:
                    path.connections.append(connection)

        floors_set = set()
        for point in path.points:
            floors_set.add(point.floor.id)

        for floor in floors_set:
            path.floors.append(floor)

        print(path.floors)
        self.logger.debug(path.floors)
        print(path.weight)
        self.logger.debug(path.weight)

        # нужен рерайтер картинок
        old_picture_path = {}
        new_picture_path = {}
        draw_points_dict_of_sequences = {}

        for id in path.floors:
            draw_points_dict_of_sequences[id] = []

        for point in path.points:
            mas = draw_points_dict_of_sequences[point.floor.id]
            mas.append(point)
            draw_points_dict_of_sequences[point.floor.id] = mas

        for floor_id in path.floors:
            old_picture_path[floor_id] = Instance.get_instance_path_by_id(floor_id)
            new_picture_path[floor_id] = self.pre_path + self.pre_key + str(self.key_val) + '.jpg'
            self.key_val += 1
            copyfile(old_picture_path[floor_id], new_picture_path[floor_id])
            redraw_picture(new_picture_path[floor_id], draw_points_dict_of_sequences[floor_id])

        path.floors_obj = {}
        for id in floors_set:
            path.floors_obj[id] = Instance.get_instance_by_id(id)
            path.floors_obj[id].picture_path = new_picture_path[id]
        self.logger.debug('return path')
        return path
