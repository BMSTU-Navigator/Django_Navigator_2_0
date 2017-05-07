from Navigator.models import *

def get_building()->Building:
    building = Building()
    building.graph=get_graph()
    building.floors=Instance.select()
    return building



def get_graph()->Graph:
    graph=Graph()
    graph.connections=GraphConnection.select()
    graph.points=Point.select()
    graph.points_dict={}
    for point in graph.points:
        graph.points_dict[point.id]=point
    return graph
