import unittest
from Navigator.views import *
from Navigator.models import *
from Navigator.sub_models import *



class FloorCheck(unittest.TestCase):
    def test_dialog(self):
        building = Building.get_building()
        wb = WayBuilderClass(building)
        wb.init_pre_count()
        path = wb.request_path(Point.get_id('101'), Point.get_id('112'))
        print('pre first assert')


        self.assertEquals(path.floors, [1, 2])

        ids_mas=[]

        for point in path.points:
            ids_mas.append(point.id)

        self.assertEquals(ids_mas,[1,2,7,10,14,16])


##
# Успешно найдена ошибка
# Не сбрасывается класс Path
#

unittest.TextTestRunner().run(unittest.defaultTestLoader.loadTestsFromTestCase(FloorCheck))