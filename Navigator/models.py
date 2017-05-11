from django.db import models

"""получить код поинта по его нзвнию
    нужно обвесить эксепшеном
"""


class Instance(models.Model):
    path = models.CharField(max_length=255, default=None)  #

    @staticmethod
    def get_instance_path_by_id(id):
        tmp = (Instance.objects.get(id=id)).path
        return tmp

    @staticmethod
    def get_instance_by_id(id):
        return Instance.objects.get(id=id)


"""поинт - место на карте (кабинет, лвход на лестницу итд)"""


class Point(models.Model):
    name = models.CharField(max_length=255, default='')  # имя
    floor = models.ForeignKey(Instance, null=False)  # индекс инстанса в котором находится точка
    path = models.CharField(max_length=255, default=None)  # путь к картинке
    x = models.IntegerField(default=0)  # координата х на карте инстанса
    y = models.IntegerField(default=0)  # координата у на карте инстанса
    hidden = models.BooleanField(default=False)

    @staticmethod
    def get_id(string):
        try:
            return (Point.objects.get(name=string)).id
        except Exception as ex:
            return -1


""" этаж
    в близжайшем буду щем станет
    инстансом
    ИНСТАНС - фрагмент местности внутри здания (кусок циркуля, часть этажа)
    """


class GraphConnection(models.Model):
    point1 = models.ForeignKey(Point, related_name='point1', null=False)  # указатель на поинт 1
    point2 = models.ForeignKey(Point, related_name='point2', null=False)  # указатель на поит 2
    connection_weight = models.IntegerField(default=0)  # вес соедиения
    connection_comment = models.CharField(max_length=255, default=None)  # коментарий соединения
    path = models.CharField(max_length=255, default=None)  # путь к картинке соединения
    instance = models.ForeignKey(Instance, null=True)  # указатель на инстанс если соединение внутри одного инстанса
    trans_instance_marker = models.BooleanField(
        default=False)  # маркер того что поинты входящие в соединение находятся в разных инстансах


""" таблица диалогов с тремя стилями
1й стиль - официальный
2й стиль - средний
3й стиль - не официал

например реплика с ключом 0
1й стиль - здравствуйте
2й стиль - привет
3й стиль - здарова братуха
"""


class Dialogs(models.Model):  #
    style1 = models.CharField(max_length=255, default=None)  #
    style2 = models.CharField(max_length=255, default=None)  #
    style3 = models.CharField(max_length=255, default=None)  #

    @staticmethod
    def get_dialog_item(id, style):
        if style == 1: return Dialogs.objects.get(id=id).style1
        if style == 2: return Dialogs.objects.get(id=id).style2
        if style == 3: return Dialogs.objects.get(id=id).style3

        # Instance.create_table(True)
        # Point.create_table(True)
        # GraphConnection.create_table(True)
        # Dialogs.create_table(True)

        # grandma = Person.select().where(Person.name == 'Grandma L.').get()
