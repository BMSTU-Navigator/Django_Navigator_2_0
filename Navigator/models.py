from django.db import models

"""получить код поинта по его нзвнию
    нужно обвесить эксепшеном
"""


class Instance(models.Model):
    path = models.CharField(max_length=255, default=None)  #
    inst_name = models.CharField(verbose_name="instance_name", max_length=255, default=None)

    @staticmethod
    def get_instance_path_by_id(id):
        tmp = (Instance.objects.get(id=id)).path
        return tmp

    @staticmethod
    def get_instance_by_id(id):
        return Instance.objects.get(id=id)

    def __str__(self):
        return self.id


"""поинт - место на карте (кабинет, лвход на лестницу итд)"""


class Point(models.Model):
    name = models.CharField(max_length=255, default='')  # имя
    floor = models.ForeignKey(Instance, null=False)  # индекс инстанса в котором находится точка
    path = models.CharField(max_length=255, default=None)  # путь к картинке
    x = models.IntegerField(default=0)  # координата х на карте инстанса
    y = models.IntegerField(default=0)  # координата у на карте инстанса
    hidden = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    @staticmethod
    def get_id(string):
        try:
            return (Point.objects.get(name=string)).id
        except Exception as ex:
            print(ex)
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

    def __str__(self):
        return 'pint1=' + str(self.point1.id) + ' point2=' + str(self.point2.id)

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

    def __str__(self):
        return 'style1=' + str(self.style1)


class TelegramUser(models.Model):
    username = models.TextField(verbose_name='username', default="")
    first_name = models.TextField(verbose_name='first_name', default="")
    last_name = models.TextField(verbose_name='last_name', default="")
    user_telegram_id = models.BigIntegerField(verbose_name='id', primary_key=True)
    dialog_state = models.IntegerField(verbose_name='dialog_state', default=0)
    dialog_style = models.IntegerField(default=1)
    from_id = models.IntegerField(default=-1)
    to_id = models.IntegerField(default=-1)

    @staticmethod
    def add_telegram_user(chat):
        user = TelegramUser()
        user.username = chat['username']
        user.first_name = chat['first_name']
        user.last_name = chat['last_name']
        user.user_telegram_id = chat['id']
        user.dialog_state = 1
        user.save()
        return TelegramUser.objects.get(user_telegram_id=chat['id'])

    @staticmethod
    def get_user(chat):
        return TelegramUser.objects.get(user_telegram_id=chat['id'])

    def __str__(self):
        return str(self.username)


class HistoryPath(models.Model):
    point1 = models.ForeignKey(Point, related_name='hpoint1', null=False)  # указатель на поинт 1
    point2 = models.ForeignKey(Point, related_name='hpoint2', null=False)  # указатель на поит 2
    telegram_user_id = models.IntegerField(default=-1)
