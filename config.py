import os

TOKEN = os.environ.get('BOT_TOKEN','')
BOT_PATH = os.environ.get('BOT_PATH', '')


SETTINGS = {
    'config': {
        'sync_strategy': 'cold'
    },
    'bot': {
        'token': TOKEN,
        'initial_state': 'main_menu',
        'initial_inline_state': None,
        'suppress_exceptions': False
    },
    'db_storage': {
        'type': 'mongo',
        'params': {
            'host': os.environ.get('MONGO_HOST', 'localhost'),
            'port': os.environ.get('MONGO_PORT', 27017),
            'database': os.environ.get('MONGO_DBNAME', 'car_wash_bot')
        }
    },
    'l10n': {
        'default_lang': 'ru',
        'locales': ['ru'],
        'file_path': 'res/l10n.json'
    },
    'reception_method': {
        'type': 'polling',
        'params': {
            'timeout': 1
        }
    },
    'bot_path': BOT_PATH,
    'pictures': {'picture_request_1': 'pic1',
                 'picture_request_2': 'pic2',
                 'picture_request_3': 'pic11',
                 'picture_request_4': 'pic4',
                 'picture_request_5': 'pic5',
                 'picture_request_6': 'pic6',
                 'picture_request_7': 'pic7',
                 'picture_request_8': 'pic8',
                 'picture_request_9': 'pic9',
                 'picture_request_a': 'pic10',
                 'picture_request_b': 'pic3',
                 'info_button': 'pic12'
                 },
    'show_picture': {'picture_request_1': True,
                 'picture_request_2': True,
                 'picture_request_3': True,
                 'picture_request_4': False,
                 'picture_request_5': True,
                 'picture_request_6': True,
                 'picture_request_7': True,
                 'picture_request_8': True,
                 'picture_request_9': True,
                 'picture_request_a': True,
                 'picture_request_b': True,
                 'info_button': True
                 },
    'documents': {'wheels':BOT_PATH+'/res/documents/wheels.doc',
                  'price':BOT_PATH+'/res/documents/price.doc'
    }
}
