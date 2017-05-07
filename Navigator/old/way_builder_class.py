from clases import *
import sql
import ntpath
from shutil import copyfile
import config
import draw
from bot_master import logging

class WayBuilderClass:
    building=None;
    paths = None
    dijkstra_weight = None
    dijkstra_connectons=None
    max_id = -1

    def __init__(self,building):
        logging.debug('init WB class')
        logging.debug('request building')
        self.building=building
        logging.debug('pre count')
        self.init_pre_count()
        return

    def init_pre_count(self):
        for tmp_point in self.building.graph.points:
            if tmp_point.id >= self.max_id: self.max_id = tmp_point.id
        self.max_id+=1
        self.paths=[self.max_id]
        self.dijkstra_weight = []
        for i in range(self.max_id):
            self.dijkstra_weight.append([10000] * self.max_id)
        for conection in self.building.graph.connections:
            self.dijkstra_weight[conection.point1][conection.point2]=conection.connection_weight

    def dijkstra(self, start,stop):
        logging.debug('dekstra start:'+str(start)+' stop:'+str(stop))
        self.dijkstra_connectons = []
        for i in range(0, len(self.dijkstra_weight)):
            self.dijkstra_connectons.append([])
            for j in range(0, len(self.dijkstra_weight[i])):
                if (self.dijkstra_weight[i][j] < 10000):
                    self.dijkstra_connectons[i].append(j)

        print(self.dijkstra_connectons)
        logging.debug(self.dijkstra_connectons)
        size = self.max_id
        INF = 10 ** 10

        dist = [INF] * size
        dist[start] = 0
        prev = [None] * size
        used = [False] * size
        min_dist = 0
        min_vertex = start
        while min_dist < INF:
            i = min_vertex
            used[i] = True
            for j in self.dijkstra_connectons[i]:
                if dist[i] + self.dijkstra_weight[i][j] < dist[j]:
                    dist[j] = dist[i] + self.dijkstra_weight[i][j]
                    prev[j] = i
            min_dist = INF
            for i in range(size):
                if not used[i] and dist[i] < min_dist:
                    min_dist = dist[i]
                    min_vertex = i



        self.paths = []
        while stop is not None:
            self.paths.append(stop)
            stop = prev[stop]
        self.paths = self.paths[::-1]

        sum = 0
        for i in range(0, len(self.paths) - 1):
            sum += self.dijkstra_weight[self.paths[i]][self.paths[i + 1]]

        return sum


    def request_path(self,start,stop):
        logging.debug('start request path start:'+str(start)+' stop:'+str(stop))
        weight = self.dijkstra(start,stop)
        print(self.paths)

        path = Path()
        path.clearr()
        print(Path.floors)
        logging.debug(Path.floors)

        path.weight=weight

        for point_id in self.paths:
            for point in self.building.graph.points:
                if point.id==point_id:
                    path.points.append(point)
                    break


        for i in range(0,len(path.points)-1):
            for connection in self.building.graph.connections:
                if connection.point1==path.points[i].id and connection.point2==path.points[i+1].id:
                    path.connections.append(connection)


        floors_set=set()
        for point in path.points:
            floors_set.add(point.floor_index)

        for floor in floors_set:
            path.floors.append(floor)

        print(path.floors)
        logging.debug(path.floors)
        print(path.weight)
        logging.debug(path.weight)


        # нужен рерайтер картинок
        old_picture_path={}
        new_picture_path={}
        draw_points_dict_of_sequences={}

        for id in path.floors:
            draw_points_dict_of_sequences[id]=[]

        for point in path.points:
            draw_points_dict_of_sequences[point.floor_index].append(point)



        for floor_id in path.floors:
            old_picture_path[floor_id]=sql.get_instance_path_by_id(floor_id)
            #head, tail = ntpath.split(old_picture_path[floor_id])
            new_picture_path[floor_id]=config.pre_path+config.pre_key+str(config.key)+'.jpg'
            config.key+=1
            copyfile(old_picture_path[floor_id],new_picture_path[floor_id])
            draw.redraw_picture(new_picture_path[floor_id],draw_points_dict_of_sequences[floor_id])

        path.floors_obj={}
        for id in floors_set:
            path.floors_obj[id]=sql.get_floor_by_id(id)
            path.floors_obj[id].picture_path=new_picture_path[id]
        #copyfile(src, dst)




        logging.debug('return path')
        return path



    def make_picture(self):
        pass

