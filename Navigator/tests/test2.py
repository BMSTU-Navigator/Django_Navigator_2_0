import unittest
from clases import *
from sql import *
from way_builder_class import *



class FloorCheck(unittest.TestCase):
    def test_dialog(self):
        building = get_building()
        wb = WayBuilderClass(building)
        wb.init_pre_count()
        path = wb.request_path(get_id('11'), get_id('25'))
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