#https://groosha.gitbooks.io/telegram-bot-lessons/content/chapter1.h


from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from Navigator.sub_models import Building,Graph,WayBuilderClass
from Navigator.models import Dialogs,Point
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton, ParseMode


import time

key_val=1
pre_key='tmp_pic'
pre_path='/home/alexdark/'





id_counter=0
id_list=[]
bots={}


#comment logging
##logging.basicConfig(filename='example.log',level=#logging.DEBUG)
##logging example
##logging.debug('This message should go to the log file')
##logging.info('So should this')
##logging.warning('And this, too')





class BotChild:
    bot_id=-1
    dialog_id=-1;
    dialog_state=-1
    dialog_style=0
    telebot =None

    building = None
    wb = None

    from_id=-1
    to_id=-1
    detalization_level=2


    def __init__(self,telebot,dialog_id,id):
        self.telebot=telebot
        self.dialog_id=dialog_id
        self.dialog_state=0
        self.dialog_style=1
        self.bot_id=id
        #logging.debug('init bot '+str(id))
        #logging.debug('request building')
        self.building = Building.get_building()
        #logging.debug('init WB class')
        self.wb = WayBuilderClass(self.building)
        #logging.debug('config wb')
        self.wb.init_pre_count()


    def get_answer(self,input_string):

        #logging.debug('request amswer from bot '+str(self.bot_id))
        #logging.debug('request by string '+input_string)
        #logging.debug('bot in  state ' + str(self.dialog_state))

        if self.dialog_state==0:
            self.send_message(Dialogs.get_dialog_item(0, 1))
            self.send_message(Dialogs.get_dialog_item(0,1))
            self.dialog_state=1
            return

        if self.dialog_state==1:
            if int(input_string) in (1,3):
                self.dialog_style=int(input_string)
                self.send_message(Dialogs.get_dialog_item(1,self.dialog_style))
                self.send_message(Dialogs.get_dialog_item(2,self.dialog_style))
                self.send_message(Dialogs.get_dialog_item(3,self.dialog_style))
                self.send_photo('all.jpeg')
                self.send_message(Dialogs.get_dialog_item(4, self.dialog_style))
                self.dialog_state=2
            else:
                self.send_message(Dialogs.get_dialog_item(5, self.dialog_style))
            return


        if self.dialog_state==2:
            self.from_id = Point.get_id(input_string)
            self.send_message(Dialogs.get_dialog_item(6,self.dialog_style))
            self.send_message(Dialogs.get_dialog_item(7, self.dialog_style))
            self.dialog_state=3
            return

        if self.dialog_state==3:
            self.to_id = Point.get_id(input_string)
            self.send_message(Dialogs.get_dialog_item(8,self.dialog_style))
            self.send_message(Dialogs.get_dialog_item(9, self.dialog_style))
            self.dialog_state=4
            return

        if self.dialog_state==4:
            out_style = int(input_string)
            path = self.wb.request_path(self.from_id, self.to_id)  #
            for i in range(len(path.points)):
                self.send_message(path.points[i].name)
                if 1<out_style:
                    if (i < len(path.connections)): self.send_message(str(path.connections[i].connection_comment))
            if out_style==3:
                for id in path.floors_obj:

                    pic_path=path.floors_obj[id].picture_path
                    self.send_photo(pic_path)
            return

    def send_message(self, text):
        #logging.debug('bot ' + str(self.bot_id)+' sending text:'+text)
        self.telebot.send_message(self.dialog_id,
                                  text)
    def send_photo(self, path):
        #logging.debug('bot ' + str(self.bot_id) + ' sending photo:' + path)
        self.telebot.send_photo(self.dialog_id, open(path, 'rb'))












print('start')
#logging.debug('start')

def echo(bot, update):
    if update.message.chat.id not in id_list:
        id_list.append(update.message.chat.id)
        tmp_bot=BotChild(bot, update.message.chat.id, len(id_list))

        bots[update.message.chat.id]=tmp_bot
        tmp_bot=None

    bots[update.message.chat.id].get_answer(update.message.text)

def command(bot, update):
    #echo a command
    bot.send_message(text='received command:'+update.message.text,chat_id=update.message.chat_id)

def error(bot,updater):
    pass #handle error

def work_cycle():
    try:
        updater.start_polling()
        time.sleep(10)
    except Exception as ex:
        print('bot crashed:')
        work_cycle()


command_handler = MessageHandler(Filters.command, command)
echo_handler = MessageHandler(Filters.text, echo)
updater = Updater(token='333359292:AAGf_E6lYBiojMkuyfxW1wefq65D9f2QAss')

dispatcher = updater.dispatcher
dispatcher.add_handler(command_handler)
dispatcher.add_error_handler(error)
dispatcher.add_handler(echo_handler)

#updater.dispatcher.add_handler(CallbackQueryHandler(button)) #for message inline

while True:
    print('new poling')
    try:
        updater.start_polling()
        time.sleep(10)
    except Exception as ex:
        print('bot crashed:')






