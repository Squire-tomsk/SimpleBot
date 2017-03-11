import json

import botlab
import telebot

from config import SETTINGS
from dao.picture import PictureDAO
from dao.message import MessageDAO
from dao.document import DocumentDAO
from service import utils

bot = botlab.BotLab(SETTINGS)
picture_dao = PictureDAO()
message_dao = MessageDAO()
document_dao = DocumentDAO()
l10n_requests_map = {}
l10n_inverse_requests_map = {}


def init():
    picture_dao.reload_files()
    message_dao.reload_files()
    document_dao.reload_files()
    with open(SETTINGS['bot_path'] + '/res/l10n.json') as l10n_file:
        l10n_json = json.load(l10n_file)
    #pictures existence check
    for picture_name in SETTINGS['pictures'].values():
        if picture_name not in picture_dao.get_pictures_names():
            raise KeyError('Initialisation error: picture ' + "'picture_name'" + ' not in database')
    #reqests map sceleton build
    for locale in SETTINGS['l10n']['locales']:
        l10n_requests_map[locale] = {}
    #picture reqests map build
    for picture_request in SETTINGS['pictures'].keys():
        for (locale, l10n_picture_request) in l10n_json[picture_request].items():
            if 'picture_requests' not in l10n_requests_map[locale]:
                l10n_requests_map[locale]['picture_requests'] = []
            l10n_requests_map[locale]['picture_requests'].append(l10n_picture_request)
            l10n_inverse_requests_map[l10n_picture_request] = picture_request
    #message reqests map build
    for (locale, message) in l10n_json['tire_button'].items():
        l10n_requests_map[locale]['tire_button'] = [message]
    for (locale, message) in l10n_json['info_button'].items():
        l10n_requests_map[locale]['info_button'] = [message]
        l10n_inverse_requests_map[message] = 'info_button'
    for (locale, message) in l10n_json['price_button'].items():
        l10n_requests_map[locale]['price_button'] = [message]
    for (locale, message) in l10n_json['back_button'].items():
        l10n_requests_map[locale]['back_button'] = [message]


@bot.message_handler(commands=['start'])
@utils.error_log_decorator
def start_handler(session, message):
    kb = build_main_menu_keyboard(session)
    check_locale(session)
    session.reply_message(message_dao.get_message(session._("welcome_message")), reply_markup=kb)
    default_handler(session, message)

@bot.message_handler(commands=['anybots'])
@utils.error_log_decorator
def start_handler(session, message):
    kb = build_main_menu_keyboard(session)
    check_locale(session)
    session.reply_message(message_dao.get_message(session._("anybots_message")), reply_markup=kb)
    default_handler(session, message)

@bot.message_handler(commands=['info'])
@utils.error_log_decorator
def info_handler(session, message):
    picture_handler(session, 'info_button')
    default_handler(session, message)

def check_locale(session):
    if session.get_lang() not in SETTINGS['l10n']['locales']:
        session.set_lang(SETTINGS['l10n']['default_lang'])


@bot.message_handler(func=lambda msg: True)
@utils.error_log_decorator
def main_handler(session, message):
    if message.text in l10n_requests_map[session.get_lang()]['picture_requests']:
        picture_handler(session, l10n_inverse_requests_map[message.text])
    elif message.text in l10n_requests_map[session.get_lang()]['tire_button']:
        document_handler(session, 'wheels')
    elif message.text in l10n_requests_map[session.get_lang()]['info_button']:
        picture_handler(session, l10n_inverse_requests_map[message.text])
    elif message.text in l10n_requests_map[session.get_lang()]['price_button']:
        document_handler(session, 'price')
    elif message.text in l10n_requests_map[session.get_lang()]['back_button']:
        default_handler(session, message)
    else:
        wrong_command_handler(session, message)


def default_handler(session, message):
    kb = build_main_menu_keyboard(session)
    ikb = build_main_inline_keyboard(session)
    session.reply_message(message_dao.get_message(session._("default_message")), reply_markup=kb)
    session.reply_message(message_dao.get_message(session._("selection_message")), reply_markup=ikb)

def document_handler(session, name):
    document = document_dao.get_document(name)
    if isinstance(document, str):
        bot.send_document(session.chat_id, document)
    else:
        bot_message = bot.send_document(session.chat_id, document)
        file_id = bot_message.document.file_id
        document_dao.add_file_id_for_document(name, file_id)

@bot.callback_query_handler()
def callback_handler(session, cbq):
    picture_handler(session,cbq.data)

def picture_handler(session,picture_name):
    name = SETTINGS['pictures'][picture_name]
    picture = picture_dao.get_picture(name)
    if SETTINGS['show_picture'][picture_name]:
        if isinstance(picture, str):
            bot.send_photo(session.chat_id, picture)
        else:
            bot_message = bot.send_photo(session.chat_id, picture)
            file_id = bot_message.photo[1].file_id
            picture_dao.add_file_id_for_picture(name, file_id)
    message = picture_dao.get_picture_message(name)
    kb = build_service_menu_keyboard(session)
    bot.send_message(session.chat_id, message, reply_markup=kb)

def wrong_command_handler(session, message):
    pass

def build_service_menu_keyboard(session):
    kb = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    kb.add(telebot.types.KeyboardButton(text=session._("back_button")),
           telebot.types.KeyboardButton(text=session._("price_button")))
    return kb

def build_main_menu_keyboard(session):
    kb = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    kb.add(telebot.types.KeyboardButton(text=session._("tire_button")),
           telebot.types.KeyboardButton(text=session._("info_button")))
    return kb

def build_main_inline_keyboard(session):
    kb = telebot.types.InlineKeyboardMarkup(row_width=2)
    button_data = list(SETTINGS['pictures'].keys())
    button_data.sort()
    button_data = button_data[1:]
    picture_requests = list(map(lambda x: session._(x), button_data))
    for i in range(int(len(picture_requests) / 2 + 0.5)):
        if len(picture_requests) - 2 * i > 1:
            kb.add(telebot.types.InlineKeyboardButton(text=picture_requests[2 * i],
                                                      callback_data=button_data[2 * i]),
                   telebot.types.InlineKeyboardButton(text=picture_requests[2 * i + 1],
                                                      callback_data=button_data[2 * i + 1]))
        else:
            kb.add(telebot.types.InlineKeyboardButton(text=picture_requests[2 * i],
                                                      callback_data=button_data[2 * i]))
    return kb
