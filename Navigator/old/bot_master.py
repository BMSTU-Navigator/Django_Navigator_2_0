#https://groosha.gitbooks.io/telegram-bot-lessons/content/chapter1.h

import config
from telebot import TeleBot
from bot import *
import logging

id_counter=0
id_list=[]
bots={}



logging.basicConfig(filename='example.log',level=logging.DEBUG)

#logging.debug('This message should go to the log file')
#logging.info('So should this')
#logging.warning('And this, too')


print('start')
logging.debug('start')
bot = TeleBot(config.token)
logging.debug('sucsess start')
print('sucsess start')


@bot.message_handler(content_types=["text"])
def repeat_all_messages(message): # Название функции не играет никакой роли, в принципе
    if message.chat.id not in id_list:
        id_list.append(message.chat.id)
        tmp_bot=Bot(bot,message.chat.id,len(id_list))

        bots[message.chat.id]=tmp_bot
        tmp_bot=None

    bots[message.chat.id].get_answer(message.text)





if __name__ == '__main__':
     bot.polling(none_stop=True)







     # if(message.text!='Привет'):
     #    bot.send_message(message.chat.id,'и тебе привет')
     # else:
     #    bot.send_message(message.chat.id, 'start')
     #    bot.send_photo(message.chat.id,open('fl2.jpeg', 'rb'))
     #    bot.send_message(message.chat.id, 'stop')