
from way_builder_class import *
from sql import *
from bot_master import logging
class Bot:
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
        logging.debug('init bot '+str(id))
        logging.debug('request building')
        self.building = get_building()
        logging.debug('init WB class')
        self.wb = WayBuilderClass(self.building)
        logging.debug('config wb')
        self.wb.init_pre_count()


    def get_answer(self,input_string):

        logging.debug('request amswer from bot '+str(self.bot_id))
        logging.debug('request by string '+input_string)
        logging.debug('bot in  state ' + str(self.dialog_state))

        if self.dialog_state==0:
            self.send_message(sql.get_dialog_item(0,1))
            self.dialog_state=1
            return

        if self.dialog_state==1:
            if int(input_string) in (1,3):
                self.dialog_style=int(input_string)
                self.send_message(sql.get_dialog_item(1,self.dialog_style))
                self.send_message(sql.get_dialog_item(2,self.dialog_style))
                self.send_message(sql.get_dialog_item(3,self.dialog_style))
                self.send_photo('all.jpeg')
                self.send_message(sql.get_dialog_item(4, self.dialog_style))
                self.dialog_state=2
            else:
                self.send_message(sql.get_dialog_item(5, self.dialog_style))
            return


        if self.dialog_state==2:
            self.from_id = get_id(input_string)
            self.send_message(sql.get_dialog_item(6,self.dialog_style))
            self.send_message(sql.get_dialog_item(7, self.dialog_style))
            self.dialog_state=3
            return

        if self.dialog_state==3:
            self.to_id = get_id(input_string)
            self.send_message(sql.get_dialog_item(8,self.dialog_style))
            self.send_message(sql.get_dialog_item(9, self.dialog_style))
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
        logging.debug('bot ' + str(self.bot_id)+' sending text:'+text)
        self.telebot.send_message(self.dialog_id,
                                  text)  # + '  answer of bot '+str(self.bot_id) +'  chat_id='+ str(self.dialog_id))
    def send_photo(self, path):
        logging.debug('bot ' + str(self.bot_id) + ' sending photo:' + path)
        #self.telebot.send_message(self.dialog_id, '+')
        self.telebot.send_photo(self.dialog_id, open(path, 'rb'))
        #self.telebot.send_message(self.dialog_id, '+')






#        if self.dialog_state==0:
#            self.send_message('Привет!!!')
#            self.send_message('Скажи мне "да"')
#            self.dialog_state=1
#            return
#
#
#
##if self.dialog_state==1:
#    if(input_string=='да'):
#        self.send_message('Молодец')
#        self.send_message('Все, я готов тебе помочь.')
#        self.send_message('Вот карта здания')
#        self.send_photo('all.jpeg')
#        self.send_message('Напиши где ты? (ключ)')
#        self.dialog_state=2
#    else:
#        self.send_message('Еще раз. Я тебя не понял')
#    return




#if self.dialog_state==2:
#    if True:#if int(input_string) in range(0,17):
#        self.from_id=get_id(input_string)#
#        #self.from_id=int(input_string)
#        self.send_message('Ага. ТЫ у кабинета '+input_string+' key='+str(self.from_id))
#        self.send_message('А куда тебе надо? (ключ)')
#        self.dialog_state=3
#    else:
#        self.send_message('Еще раз. Я тебя не понял')
#    return




#if self.dialog_state==3:
#    if True:#if int(input_string) in range(0,17):
#        self.to_id=get_id(input_string)#
#    #if int(input_string) in range(0,17):
#        #self.to_id=int(input_string)
#        self.send_message('Ага. ТЫ хочешь пройти в кабинет '+input_string +" key="+str(self.to_id))
#        self.send_message('Скажи тебе "подробный" или "простой" маршрут?')
#        #self.send_message('Все, ща посчитаю маршрут и напишу тебе')
#        self.dialog_state=4
#    else:
#        self.send_message('Еще раз. Я тебя не понял')
#    return





#if self.dialog_state==4:
#        path = self.wb.request_path(self.from_id, self.to_id)#
#
#        for i in range(len(path.points)):
#            self.send_message(path.points[i].name)
#            if input_string=='подробный':
#                if (i < len(path.connections)): self.send_message(str(path.connections[i].connection_comment))

#        self.dialog_state=1









