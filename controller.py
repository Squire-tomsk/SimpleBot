import json

import botlab
import telebot

from config import SETTINGS
from dao.picture import PictureDAO
from service import utils

bot = botlab.BotLab(SETTINGS)
picture_dao = PictureDAO()
locales = []
l10n_commands = {}


def init():
    picture_dao.reload_files()
    with open(SETTINGS['bot_path'] + '/res/l10n.json') as l10n_file:
        l10n_json = json.load(l10n_file)
    for (locale, message) in l10n_json['bot_picture_request'].items():
        commands = list(map(lambda x: message.replace('{name}', x), picture_dao.get_pictures_names()))
        l10n_commands[locale] = {}
        l10n_commands[locale]['picture_requests'] = commands
    for (locale, message) in l10n_json['bot_message_request'].items():
        l10n_commands[locale]['message_requests'] = message
    locales.extend(list(l10n_commands.keys()))


@bot.message_handler(commands=['start'])
@utils.error_log_decorator
def start_handler(session, message):
    kb = build_main_menu_keyboard(session)
    check_locale(session)
    session.reply_message(session._("welcome_message"), reply_markup=kb)


def check_locale(session):
    if session.get_lang() not in locales:
        session.set_lang(SETTINGS['l10n']['default_lang'])


@bot.message_handler(func=lambda msg: True)
@utils.error_log_decorator
def main_handler(session, message):
    if message.text in l10n_commands[session.get_lang()]['picture_requests']:
        picture_request_handler(session, message)
    elif message.text in l10n_commands[session.get_lang()]['message_requests']:
        text_request_handler(session, message)
    else:
        wrong_command_handler(session, message)


def picture_request_handler(session, message):
    name = message.text.split("'")[1]
    picture = picture_dao.get_picture(name)
    if isinstance(picture, str):
        bot.send_photo(session.chat_id, picture)
    else:
        bot_message = bot.send_photo(session.chat_id, picture)
        file_id = bot_message.photo[1].file_id
        picture_dao.add_file_id_for_picture(name, file_id)


def text_request_handler(session, message):
    session.reply_message(session._("bot_message"))


def wrong_command_handler(session, message):
    kb = build_main_menu_keyboard(session)
    session.reply_message(session._("wrong_command_message"), reply_markup=kb)


def build_main_menu_keyboard(session):
    kb = telebot.types.ReplyKeyboardMarkup(row_width=1)
    for name in picture_dao.get_pictures_names():
        btn_text = session._('bot_picture_request', name=name)
        kb.add(telebot.types.KeyboardButton(text=btn_text))
    btn_text = session._("bot_message_request")
    kb.add(telebot.types.KeyboardButton(text=btn_text))
    return kb
