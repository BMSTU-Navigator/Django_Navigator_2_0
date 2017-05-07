class Building:
    graph=None
    floors=None

class Graph:
    connections = []
    points=[]

    points_dict={} #id-to point
    #connections_point_1_dict={}
    #connections_point_2_dict = {}
    def __init__(self):
        super().__init__()
        # load data from db

    def reque_path(self, start_point, stop_point, detalization_level):
        return None

class Path:
    points = []
    connections = []
    floors = []
    floors_obj={}
    weight=-1
    def clearr(self):
        self.points = []
        self.connections = []
        self.floors = []
        self.weight = -1



        # class GraphConnection:
        #    point1 = None
        #    point2 = None
        #
        #    connection_weight = -1
        #
        #    connection_comment = None
        #
        #    picture_path = None
        #
        #    floor_index = -1
        #    trans_floor_marker=False;
        #    #def __init__(self, point1, point2, connection_weight, connection_comment, picture_path, floor_index):
        #    #    super().__init__()
        #    #    self.point1 = point1
        #    #    self.point2 = point2
        #    #    self.connection_weight = connection_weight
        #    #    self.connection_comment = connection_comment
        #    #    self.picture_path = picture_path
        #    #    self.floor_index = floor_index


        # class Floor:
        #    picture_path = None
        #    floor_index = -1
        #
#class Point:
#    id=-1
#    name=None
#    floor_index=-1
#    path_for_point_pic=None
#    x=-1
#    y=-1

