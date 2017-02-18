import json

import botlab
import telebot

from config import SETTINGS
from dao.picture import PictureDAO
from service import utils

bot = botlab.BotLab(SETTINGS)
picture_dao = PictureDAO()
l10n_requests_map = {}
l10n_inverse_requests_map = {}


def init():
    picture_dao.reload_files()
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
    for (locale, message) in l10n_json['message_request'].items():
        l10n_requests_map[locale]['message_requests'] = [message]


@bot.message_handler(commands=['start'])
@utils.error_log_decorator
def start_handler(session, message):
    kb = build_main_menu_keyboard(session)
    check_locale(session)
    session.reply_message(session._("welcome_message"), reply_markup=kb)


def check_locale(session):
    if session.get_lang() not in SETTINGS['l10n']['locales']:
        session.set_lang(SETTINGS['l10n']['default_lang'])


@bot.message_handler(func=lambda msg: True)
@utils.error_log_decorator
def main_handler(session, message):
    if message.text in l10n_requests_map[session.get_lang()]['picture_requests']:
        picture_request_handler(session, message)
    elif message.text in l10n_requests_map[session.get_lang()]['message_requests']:
        text_request_handler(session, message)
    else:
        wrong_command_handler(session, message)


def picture_request_handler(session, message):
    name = SETTINGS['pictures'][l10n_inverse_requests_map[message.text]]
    picture = picture_dao.get_picture(name)
    if isinstance(picture, str):
        bot.send_photo(session.chat_id, picture)
    else:
        bot_message = bot.send_photo(session.chat_id, picture)
        file_id = bot_message.photo[1].file_id
        picture_dao.add_file_id_for_picture(name, file_id)


def text_request_handler(session, message):
    session.reply_message(session._("message_response"))


def wrong_command_handler(session, message):
    kb = build_main_menu_keyboard(session)
    session.reply_message(session._("wrong_command_message"), reply_markup=kb)


def build_main_menu_keyboard(session):
    kb = telebot.types.ReplyKeyboardMarkup(row_width=2)
    picture_requests = list(map(lambda x: session._(x), SETTINGS['pictures'].keys()))
    for i in range(int(len(picture_requests) / 2 + 0.5)):
        if len(picture_requests) - 2 * i > 1:
            kb.add(telebot.types.KeyboardButton(text=picture_requests[2 * i]),
                   telebot.types.KeyboardButton(text=picture_requests[2 * i + 1]))
        else:
            kb.add(telebot.types.KeyboardButton(text=picture_requests[2 * i]))
    btn_text = session._("message_request")
    kb.add(telebot.types.KeyboardButton(text=btn_text))
    return kb
