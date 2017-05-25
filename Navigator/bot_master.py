import time
import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from telegram.ext import Updater, MessageHandler, Filters, CallbackQueryHandler

from Navigator.models import Dialogs, Point, HistoryPath
from Navigator.models import TelegramUser
from Navigator.sub_models import Building, WayBuilderClass

key_val = 1
pre_key = 'tmp_pic'
pre_path = './pic_dir/tmp_pic_dir/'

id_counter = 0
id_list = []
bots = {}

logging.basicConfig(filename='ex.log', level=logging.DEBUG)
master_logger = logging.getLogger('BotMaster')


def get_dialog(id, user):
    if user.dialog_style == 1:
        return Dialogs.objects.get(id=id).style1
    if user.dialog_style == 2:
        return Dialogs.objects.get(id=id).style2
    if user.dialog_style == 3:
        return Dialogs.objects.get(id=id).style3


class BotChild:
    @staticmethod
    def get_keyboard_for_change_style():
        keyboard = [
            ['Формальный'],
            ['Для друзей'],
            ['Для братишек', ]
        ]
        return ReplyKeyboardMarkup(keyboard, one_time_keyboard=False)

    @staticmethod
    def get_keyboard():
        keyboard = [
            ['Построить маршрут', 'Посмотреть избранные маршруты'], ['Показать карту здания'], ['Сменить стиль диалога']
        ]
        return ReplyKeyboardMarkup(keyboard, one_time_keyboard=False)

    @staticmethod
    def get_keyboard_for_fav_mode():
        keyboard = [
            ['Создать новый избранный путь', 'Вернуться в режим ожидания']
        ]
        return ReplyKeyboardMarkup(keyboard, one_time_keyboard=False)

    @staticmethod
    def get_keyboard_for_cancel():
        keyboard = [
            ['Отмена']
        ]
        return ReplyKeyboardMarkup(keyboard, one_time_keyboard=False)

    @staticmethod
    def make_message_from_path(path, user):
        text = get_dialog(0, user) + path.point1.name + '\n' + get_dialog(1, user) + path.point2.name
        return text

    @staticmethod
    def send_fav_paths(bot, user):
        keyboard = BotChild.get_keyboard_for_fav_mode()
        BotChild.send_message_with_keyboard(bot, user, get_dialog(2, user), keyboard)
        paths = HistoryPath.objects.filter(telegram_user_id=user.user_telegram_id)

        for path in paths:
            keyboard = [[InlineKeyboardButton("Построить", callback_data=str(str(path.id) + '#^*_1')),
                         InlineKeyboardButton("Удалить", callback_data=str(str(path.id) + '#^*_0'))]]
            keyboard = InlineKeyboardMarkup(keyboard)
            text = BotChild.make_message_from_path(path, user)
            BotChild.send_message_with_keyboard(bot, user, text, keyboard)

        user.dialog_state = 6
        user.save()

    @staticmethod
    def build_and_send_path(bot, user, wb):
        keyboard = BotChild.get_keyboard()
        BotChild.send_message_with_keyboard(bot, user, get_dialog(3, user), keyboard)
        user.save()

        path = wb.request_path(user.from_id, user.to_id)

        prev_inst_id = path.connections[0].instance.id

        message = ''
        for i in range(len(path.points)):

            if i < len(path.connections):
                message += '\n' + str(path.connections[i].connection_comment)
                if not path.points[i].hidden:
                    message += ' ' + path.points[i].name
                if path.connections[i].trans_instance_marker:
                    BotChild.send_message(bot, user, message)
                    pic_path = path.floors_obj[prev_inst_id].picture_path
                    BotChild.send_photo(bot, user, pic_path)
                    message = ''
                else:
                    prev_inst_id = path.connections[i].instance.id
        message += '\n ' + path.points[len(path.points) - 1].name
        BotChild.send_message(bot, user, message)
        pic_path = path.floors_obj[prev_inst_id].picture_path
        BotChild.send_photo(bot, user, pic_path)

        BotChild.send_message(bot, user, get_dialog(4, user))
        user.dialog_state = 5
        user.save()

    @staticmethod
    def get_answer(input_string, user, wb, bot):

        logger = logging.getLogger('tmp BotChild')
        logger.debug('request amswer from bot ')
        logger.debug('request by string ' + input_string)
        logger.debug('bot in  state ' + str(user.dialog_state))

        if input_string == 'Построить маршрут' or input_string == 'Сменить стиль диалога' or input_string == 'Посмотреть избранные маршруты' or input_string == 'Показать карту здания':
            if input_string == 'Показать карту здания':
                BotChild.send_message(bot, user, get_dialog(23, user))
                for instance in main_way_builder_instance.building.floors:
                    try:
                        BotChild.send_message(bot, user, instance.inst_name)
                    except Exception as ex:
                        print(ex)
                    BotChild.send_photo(bot, user, instance.path)
                return

            if input_string == 'Сменить стиль диалога':
                BotChild.send_message_with_keyboard(bot, user, get_dialog(5, user),
                                                    BotChild.get_keyboard_for_change_style())
                user.dialog_state = 1
                user.save()
                return

            if input_string == 'Построить маршрут':
                BotChild.send_message_with_keyboard(bot, user, get_dialog(6, user),
                                                    BotChild.get_keyboard_for_cancel())
                user.dialog_state = 2
                user.save()
                return
            if input_string == 'Посмотреть избранные маршруты':
                BotChild.send_fav_paths(bot, user)
                return

        if user.dialog_state == 0:
            BotChild.send_message_with_keyboard(bot, user, get_dialog(5, user),
                                                BotChild.get_keyboard_for_change_style())

            user.dialog_state = 1
            user.save()

            return

        if user.dialog_state == 1:
            if input_string == 'Формальный' or input_string == 'Для друзей' or input_string == 'Для братишек':

                if input_string == 'Формальный':
                    user.dialog_style = 1
                if input_string == 'Для друзей':
                    user.dialog_style = 2
                if input_string == 'Для братишек':
                    user.dialog_style = 3
                user.save()
                BotChild.send_message_with_keyboard(bot, user, get_dialog(7, user), BotChild.get_keyboard())
                BotChild.send_message(bot, user, get_dialog(8, user))
                user.dialog_state = 5
                user.save()
            else:
                BotChild.send_message(bot, user, get_dialog(9, user))
            return

        if user.dialog_state == 2:
            if input_string == "Отмена":
                user.dialog_state = 5
                user.save()
                BotChild.send_message_with_keyboard(bot, user, get_dialog(22, user), BotChild.get_keyboard())
                return
            point_id = Point.get_id(input_string)
            if point_id == -1:
                BotChild.send_message(bot, user, get_dialog(10, user))
            else:
                user.from_id = point_id
                BotChild.send_message(bot, user, get_dialog(11, user))
                BotChild.send_message(bot, user, get_dialog(12, user))
                user.dialog_state = 3
                user.save()
            return

        if user.dialog_state == 3:
            if input_string == "Отмена":
                user.dialog_state = 5
                user.save()
                BotChild.send_message_with_keyboard(bot, user, get_dialog(22, user), BotChild.get_keyboard())
                return

            point_id = Point.get_id(input_string)
            if point_id == -1:
                BotChild.send_message(bot, user, get_dialog(10, user))
            else:
                user.to_id = point_id
                if user.to_id == user.from_id:
                    user.dialog_state = 5
                    user.save()
                    BotChild.send_message_with_keyboard(bot, user, get_dialog(21, user), BotChild.get_keyboard())
                    return

                BotChild.send_message(bot, user, get_dialog(13, user))
                user.save()
                BotChild.build_and_send_path(bot, user, wb)
            return

        if user.dialog_state == 5:
            BotChild.send_message(bot, user, get_dialog(14, user))
            return

        if user.dialog_state == 6:
            if input_string == 'Вернуться в режим ожидания' or input_string == 'Создать новый избранный путь':
                if input_string == 'Вернуться в режим ожидания':
                    keyboard = BotChild.get_keyboard()
                    BotChild.send_message_with_keyboard(bot, user, get_dialog(4, user), keyboard)
                    return
                if input_string == 'Создать новый избранный путь':
                    keyboard = BotChild.get_keyboard_for_cancel()
                    BotChild.send_message_with_keyboard(bot, user, get_dialog(6, user), keyboard)
                    user.dialog_state = 7
                    user.save()
                    return
            else:
                BotChild.send_message(bot, user, text=get_dialog(19, user))

        if user.dialog_state == 7:

            if input_string == 'Отмена':
                keyboard = BotChild.get_keyboard_for_fav_mode()
                BotChild.send_message_with_keyboard(bot, user, get_dialog(17, user), keyboard)
                BotChild.send_fav_paths(bot, user)
                return

            point_id = Point.get_id(input_string)
            if point_id == -1:
                BotChild.send_message(bot, user, get_dialog(10, user))
            else:
                user.from_id = point_id
                BotChild.send_message(bot, user, get_dialog(11, user))
                BotChild.send_message(bot, user, get_dialog(12, user))
                user.dialog_state = 8
                user.save()
            return

        if user.dialog_state == 8:

            if input_string == 'Отмена':
                keyboard = BotChild.get_keyboard_for_fav_mode()
                BotChild.send_message_with_keyboard(bot, user, get_dialog(17, user), keyboard)
                BotChild.send_fav_paths(bot, user)
                return

            point_id = Point.get_id(input_string)
            if point_id == -1:
                BotChild.send_message(bot, user, get_dialog(10, user))
            else:
                user.to_id = point_id
                BotChild.send_message(bot, user, get_dialog(13, user))
                user.save()

                HistoryPath.objects.get_or_create(telegram_user_id=user.user_telegram_id,
                                                  point1=Point.objects.get(id=user.from_id),
                                                  point2=Point.objects.get(id=user.to_id))
                keyboard = BotChild.get_keyboard_for_fav_mode()
                BotChild.send_message_with_keyboard(bot, user, get_dialog(16, user), keyboard)
                BotChild.send_fav_paths(bot, user)

    @staticmethod
    def send_message(bot, user, text):
        bot.sendMessage(chat_id=user.user_telegram_id, text=text, disable_notification=False,
                        disable_web_page_prewview=True)

    @staticmethod
    def send_message_clear_keyboard(bot, user, text):
        keyboard = [
        ]
        keyboard = ReplyKeyboardMarkup(keyboard, one_time_keyboard=False)

        bot.sendMessage(chat_id=user.user_telegram_id, text=text, reply_markup=keyboard, disable_notification=False,
                        disable_web_page_prewview=True)

    @staticmethod
    def send_message_with_keyboard(bot, user, text, keyboard):
        bot.sendMessage(chat_id=user.user_telegram_id, text=text,
                        reply_markup=keyboard, disable_notification=False, disable_web_page_prewview=True)

    @staticmethod
    def send_photo(bot, user, path):
        bot.send_photo(user.user_telegram_id, open(path, 'rb'))


def echo(bot, update):
    text = update.message.text
    BotChild.get_answer(text, TelegramUser.get_user(update.message.chat), main_way_builder_instance, bot)


def command(bot, update):
    if update.message.text == '/start':
        user = TelegramUser.add_telegram_user(update.message.chat)
        bot.send_message(text=get_dialog(18, user)+' '+user.username, chat_id=update.message.chat_id, disable_web_page_preview=True)
        BotChild.send_message_with_keyboard(bot, TelegramUser.get_user(update.message.chat), get_dialog(5, user),
                                            BotChild.get_keyboard_for_change_style())

    else:
        user = TelegramUser()
        user.dialog_style = 1
        bot.send_message(text=get_dialog(19, user) + update.message.text, chat_id=update.message.chat_id,
                         disable_web_page_preview=True)


def error(bot, updater):
    pass  # handle error


def get_data_tuple(query_data):
    ind = query_data.index('#^*_')
    data1 = query_data[:ind]
    data2 = int(query_data[ind + 4:])
    return data1, data2


def button(bot, update):
    try:
        query = update.callback_query
        query_data_tuple = get_data_tuple(query.data)

        user = TelegramUser.get_user(update.callback_query.message.chat)
        print(query_data_tuple[1])
        if query_data_tuple[1] == 0:
            f_path = HistoryPath.objects.filter(id=query_data_tuple[0])
            if len(f_path) != 0:
                text = "Маршрут \n" + BotChild.make_message_from_path(f_path[0], user) + '\n ' + get_dialog(20, user)

                for del_path in f_path:
                    del_path.delete()

                BotChild.send_message(bot, user, text)
                BotChild.send_fav_paths(bot, user)
            return
        if query_data_tuple[1] == 1:
            f_path = HistoryPath.objects.filter(id=query_data_tuple[0])
            if len(f_path) != 0:
                path = f_path[0]

                user.from_id = path.point1.id
                user.to_id = path.point2.id
                user.save()
                BotChild.build_and_send_path(bot, user, main_way_builder_instance)
            else:
                BotChild.send_message(bot, user, 'Fatal eror')

    except Exception as ex:
        print(ex)


def work_cycle():
    try:
        updater.start_polling()
        master_logger.debug('new pol')
        time.sleep(10)
        work_cycle()
    except Exception as exc:
        print('bot crashed:')
        master_logger.debug('bot crashed')
        print(exc)
        master_logger.debug(exc)
        work_cycle()


print('start')
master_logger.debug('start')
building = Building.get_building()
master_logger.debug('init WB class')
main_way_builder_instance = WayBuilderClass(building)

command_handler = MessageHandler(Filters.command, command)
echo_handler = MessageHandler(Filters.text, echo)

import getpass

user = getpass.getuser()

token1 = '315208477:AAFj0IrsEQFl7s-X_DVqmBwN4_GO9Hh5Q6E'
token2 = '362627334:AAHil__LDmOE0WQ0FY-Czyh7yd6KS9JlDbc'

token = ''
if user == 'aleksa':
    token = token2
else:
    token = token1

updater = Updater(token=token)

dispatcher = updater.dispatcher
dispatcher.add_handler(command_handler)
# dispatcher.add_error_handler(error)
dispatcher.add_handler(echo_handler)

updater.dispatcher.add_handler(CallbackQueryHandler(button))  # for message inline

import threading

th = threading.Thread(target=work_cycle)
th.start()
