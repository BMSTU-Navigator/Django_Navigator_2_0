
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from Navigator.sub_models import Building, Graph, WayBuilderClass
from Navigator.models import Dialogs, Point
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton, ParseMode


import time


key_val = 1
pre_key = 'tmp_pic'
pre_path = './pic_dir/tmp_pic_dir/'


id_counter = 0
id_list = []
bots = {}


import logging
logging.basicConfig(filename='ex.log',level=logging.DEBUG)
logger = logging.getLogger('lg')
logger.debug('test')


class BotChild_oldold:
    bot_id = -1
    dialog_id = -1
    dialog_state = -1
    dialog_style = 0
    telebot = None

    building = None
    wb = None

    from_id = -1
    to_id = -1
    detalization_level = 2

    def __init__(self, telebot, dialog_id, id_ind, way_builder_instance):
        self.telebot = telebot
        self.dialog_id = dialog_id
        self.dialog_state = 0
        self.dialog_style = 1
        self.bot_id = id_ind
        # logging.debug('init bot '+str(id))
        # logging.debug('request building')
        # self.building = Building.get_building()
        # logging.debug('init WB class')
        self.wb = way_builder_instance
        # logging.debug('config wb')
        self.wb.init_pre_count()

    def get_answer(self, input_string):

        # logging.debug('request amswer from bot '+str(self.bot_id))
        # logging.debug('request by string '+input_string)
        # logging.debug('bot in  state ' + str(self.dialog_state))

        if self.dialog_state == 0:
            self.send_message(Dialogs.get_dialog_item(0, 1))
            #self.send_message(Dialogs.get_dialog_item(8, 1))
            self.dialog_state = 1
            return

        if self.dialog_state == 1:
            if int(input_string) in (1, 3):
                self.dialog_style = int(input_string)
                self.send_message(Dialogs.get_dialog_item(1, self.dialog_style))
                self.send_message(Dialogs.get_dialog_item(2, self.dialog_style))
                self.send_message(Dialogs.get_dialog_item(3, self.dialog_style))
                #self.send_photo('all.jpeg')
                self.send_message(Dialogs.get_dialog_item(4, self.dialog_style))
                self.dialog_state = 2
            else:
                self.send_message(Dialogs.get_dialog_item(5, self.dialog_style))
            return

        if self.dialog_state == 2:
            self.from_id = Point.get_id(input_string)
            self.send_message(Dialogs.get_dialog_item(6, self.dialog_style))
            #self.send_message(Dialogs.get_dialog_item(7, self.dialog_style))
            self.dialog_state = 3
            return

        if self.dialog_state == 3:
            self.to_id = Point.get_id(input_string)
            self.send_message(Dialogs.get_dialog_item(7, self.dialog_style))
            self.send_message(Dialogs.get_dialog_item(8, self.dialog_style))
            self.dialog_state = 4
            return

        if self.dialog_state == 4:
            out_style = int(input_string)
            path = self.wb.request_path(self.from_id, self.to_id)  #
            for i in range(len(path.points)):
                self.send_message(path.points[i].name)
                if 1 < out_style:
                    if i < len(path.connections):
                        self.send_message(str(path.connections[i].connection_comment))
            if out_style == 3:
                for i in path.floors_obj:
                    pic_path = path.floors_obj[i].picture_path
                    self.send_photo(pic_path)
            return

    def send_message(self, text):
        # logging.debug('bot ' + str(self.bot_id)+' sending text:'+text)
        self.telebot.send_message(self.dialog_id,
                                  text)

    def send_photo(self, path):
        # logging.debug('bot ' + str(self.bot_id) + ' sending photo:' + path)
        self.telebot.send_photo(self.dialog_id, open(path, 'rb'))


class BotChild_old:
    bot_id = -1
    dialog_id = -1
    dialog_state = -1
    dialog_style = 0
    telebot = None

    building = None
    wb = None

    from_id = -1
    to_id = -1
    detalization_level = 2

    def __init__(self, telebot, dialog_id, id_ind, way_builder_instance):
        self.telebot = telebot
        self.dialog_id = dialog_id
        self.dialog_state = 0
        self.dialog_style = 1
        self.bot_id = id_ind
        # logging.debug('init bot '+str(id))
        # logging.debug('request building')
        # self.building = Building.get_building()
        # logging.debug('init WB class')
        self.wb = way_builder_instance
        # logging.debug('config wb')
        self.wb.init_pre_count()

    def get_answer(self, input_string):

        # logging.debug('request amswer from bot '+str(self.bot_id))
        # logging.debug('request by string '+input_string)
        # logging.debug('bot in  state ' + str(self.dialog_state))

        if self.dialog_state == 0:
            self.send_message('get style')
            self.send_message('send keyboard')
            self.dialog_state = 1
            return

        if self.dialog_state == 1:
            if int(input_string) in (1, 3):
                self.dialog_style = int(input_string)
                self.send_message('greet')
                self.send_message('ask for route point 1')
                self.send_message('change keyboard to new way change style')
                self.dialog_state = 2
            else:
                self.send_message('eror choosing style message')
            return

        if self.dialog_state == 2:
            id=Point.get_id(input_string)
            if id==-1:
                self.send_message('eror no such a point')
            else:
                self.from_id = id
                self.send_message('point1 - ok')
                self.send_message('ask for 2nd point')
                self.dialog_state = 3
            return

        if self.dialog_state == 3:
            id=Point.get_id(input_string)
            if id==-1:
                self.send_message('eror no such a point')
            else:
                self.to_id = id
                self.send_message('point2 - ok')
                self.send_message('wait for route')
                self.dialog_state = 4

                path = self.wb.request_path(self.from_id, self.to_id)

                prev_inst_id=path.connections[0].instance.id
                cur_instance=0
                for i in range(len(path.points)):
                    self.send_message(path.points[i].name)
                    if i < len(path.connections):
                        self.send_message(str(path.connections[i].connection_comment))

                        if path.connections[i].trans_instance_marker:
                            pic_path = path.floors_obj[prev_inst_id].picture_path
                            self.send_photo(pic_path)
                        else:
                            prev_inst_id=path.connections[i].instance.id
                    #for i in path.floors_obj:
                    #    pic_path = path.floors_obj[i].picture_path
                    #    self.send_photo(pic_path)
                pic_path = path.floors_obj[prev_inst_id].picture_path
                self.send_photo(pic_path)
                self.send_message('write something to new path')
                self.dialog_state=4
            return

        if self.dialog_state == 4:
            self.send_message('get point 1')
            self.dialog_state=1
            return
        if self.dialog_state ==5:
            #wait for new route or change style
            return

    def send_message(self, text):
        # logging.debug('bot ' + str(self.bot_id)+' sending text:'+text)
        self.telebot.send_message(self.dialog_id,
                                  text)

    def send_photo(self, path):
        # logging.debug('bot ' + str(self.bot_id) + ' sending photo:' + path)
        self.telebot.send_photo(self.dialog_id, open(path, 'rb'))

class BotChild:
    bot_id = -1
    dialog_id = -1
    dialog_state = -1
    dialog_style = 0
    telebot = None

    building = None
    wb = None

    from_id = -1
    to_id = -1
    detalization_level = 2
    logger=None



    @staticmethod
    def get_keyboard_for_change_style():
        keyboard = [
                ['F'],
                ['NF'],
                ['SNF',]
            ]
        return ReplyKeyboardMarkup(keyboard, one_time_keyboard=False)

    @staticmethod
    def get_keyboard():
        keyboard = [
            ['NW','CS']
        ]
        return ReplyKeyboardMarkup(keyboard, one_time_keyboard=False)

    def __init__(self, telebot, dialog_id, id_ind, way_builder_instance):
        self.telebot = telebot
        self.dialog_id = dialog_id
        self.dialog_state = 0
        self.dialog_style = 1
        self.bot_id = id_ind
        # logging.debug('init bot '+str(id))
        # logging.debug('request building')
        # self.building = Building.get_building()
        # logging.debug('init WB class')
        self.wb = way_builder_instance
        # logging.debug('config wb')
        self.wb.init_pre_count()





    def get_answer(self, input_string):

        # logging.debug('request amswer from bot '+str(self.bot_id))
        # logging.debug('request by string '+input_string)
        # logging.debug('bot in  state ' + str(self.dialog_state))
        if input_string == 'NW' or input_string == 'CS':
            if input_string == 'CS':
                self.send_message_with_keyboard('get style', self.get_keyboard_for_change_style())
                self.dialog_state = 1
                return
            if input_string == 'NW':
                self.send_message('ask for route point 1')
                self.dialog_state = 2
                return



        if self.dialog_state == 0:
            self.send_message_with_keyboard('get style',self.get_keyboard_for_change_style())
            #self.send_message('send keyboard')
            self.dialog_state = 1
            return

        if self.dialog_state == 1:
            if input_string=='F'or input_string=='NF' or input_string=='SNF':

                if input_string=='F': self.dialog_style=1;
                if input_string == 'NF': self.dialog_style = 2;
                if input_string == 'SNF': self.dialog_style = 3;
                self.send_message_with_keyboard('change is registered',self.get_keyboard())
                self.send_message('greet')
                self.dialog_state = 5
            else:
                self.send_message('eror choosing style message')
            return

        if self.dialog_state == 2:
            id=Point.get_id(input_string)
            if id==-1:
                self.send_message('eror no such a point')
            else:
                self.from_id = id
                self.send_message('point1 - ok')
                self.send_message('ask for 2nd point')
                self.dialog_state = 3
            return

        if self.dialog_state == 3:
            id=Point.get_id(input_string)
            if id==-1:
                self.send_message('eror no such a point')
            else:
                self.to_id = id
                self.send_message('point2 - ok')
                self.send_message('wait for route')


                path = self.wb.request_path(self.from_id, self.to_id)

                prev_inst_id=path.connections[0].instance.id


                message=''
                for i in range(len(path.points)):
                    if not path.points[i].hidden:
                        message+='\n'+path.points[i].name

                    if i < len(path.connections):
                        message += '\n' + str(path.connections[i].connection_comment)

                        if path.connections[i].trans_instance_marker:
                            self.send_message(message)
                            pic_path = path.floors_obj[prev_inst_id].picture_path
                            self.send_photo(pic_path)
                            message=''
                        else:
                            prev_inst_id=path.connections[i].instance.id

                self.send_message(message)
                pic_path = path.floors_obj[prev_inst_id].picture_path
                self.send_photo(pic_path)

                self.send_message('going to wait state')
                self.dialog_state=5
            return

        if self.dialog_state == 4:
            self.send_message('get point 1')
            self.dialog_state=2
            return
        if self.dialog_state ==5:
            #wait for new route or change style
            if input_string=='NW' or input_string=='CS':
                if input_string=='CS':
                    self.send_message_with_keyboard('get style', self.get_keyboard_for_change_style())
                    self.dialog_state = 1
                    return
                if input_string=='NW':
                    self.send_message('ask for route point 1')
                    #self.send_message('change keyboard to new way change style')
                    self.dialog_state = 2
                    return

            else:
                self.send_message('dont understand')
            return

    def send_message(self, text):
        # logging.debug('bot ' + str(self.bot_id)+' sending text:'+text)
        self.telebot.send_message(self.dialog_id,
                                  text)

    def send_message_clear_keyboard(self,text):
        keyboard = [
        ]
        keyboard= ReplyKeyboardMarkup(keyboard, one_time_keyboard=False)

        self.telebot.sendMessage(chat_id=self.dialog_id, text=text,reply_markup=keyboard, disable_notification=False,disable_web_page_prewview=True)

    def send_message_with_keyboard(self, text,keyboard):
        # logging.debug('bot ' + str(self.bot_id)+' sending text:'+text)
        self.telebot.sendMessage(chat_id=self.dialog_id, text=text,
                              reply_markup=keyboard, disable_notification=False,disable_web_page_prewview=True)
        #self.telebot.send_message(self.dialog_id,
        #                          text,keyboard)

    def send_photo(self, path):
        # logging.debug('bot ' + str(self.bot_id) + ' sending photo:' + path)
        self.telebot.send_photo(self.dialog_id, open(path, 'rb'))

print('start')
# logging.debug('start')


building = Building.get_building()
# logging.debug('init WB class')
main_way_builder_instance = WayBuilderClass(building)


def echo(bot, update):
    if update.message.chat.id not in id_list:
        id_list.append(update.message.chat.id)
        tmp_bot = BotChild(bot, update.message.chat.id, len(id_list), main_way_builder_instance)
        tmp_bot.logger=logger
        bots[update.message.chat.id] = tmp_bot

    bots[update.message.chat.id].get_answer(update.message.text)


def command(bot, update):

    for i in building.graph.connections:
        if i.trans_instance_marker:
            print('true')

    # echo a command
    path=main_way_builder_instance.request_path(Point.get_id('101'), Point.get_id('105'))
    bot.send_message(text='received command:' + update.message.text, chat_id=update.message.chat_id,disable_web_page_preview=True)


def error(bot, updater):
    pass  # handle error


def work_cycle():
    try:
        updater.start_polling()
        time.sleep(10)
        work_cycle()
    except Exception as exc:
        print('bot crashed:')
        print(exc)
        work_cycle()


command_handler = MessageHandler(Filters.command, command)
echo_handler = MessageHandler(Filters.text, echo)
updater = Updater(token='333359292:AAGf_E6lYBiojMkuyfxW1wefq65D9f2QAss')

dispatcher = updater.dispatcher
dispatcher.add_handler(command_handler)
#dispatcher.add_error_handler(error)
dispatcher.add_handler(echo_handler)

# updater.dispatcher.add_handler(CallbackQueryHandler(button)) #for message inline



work_cycle()
#
#while True:
#    print('new poling')
#    try:
#        updater.start_polling()
#        time.sleep(10)
#    except Exception as excp:
#        print('bot crashed:')
#        print(excp)
