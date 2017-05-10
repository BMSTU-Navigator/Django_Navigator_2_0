

building = Building.get_building()
wb = WayBuilderClass(building)
wb.init_pre_count()
path = wb.request_path(Point.get_id('101'), Point.get_id('112'))


