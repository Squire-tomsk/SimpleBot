import os

TOKEN = os.environ.get('BOT_TOKEN','')

SETTINGS = {
    'config': {
        'sync_strategy': 'cold'
    },
    'bot': {
        'token': TOKEN,
        'initial_state': 'main_menu',
        'initial_inline_state': None,
        'suppress_exceptions': True
    },
    'db_storage': {
        'type': 'mongo',
        'params': {
            'host': os.environ.get('MONGO_HOST', 'localhost'),
            'port': os.environ.get('MONGO_PORT', 27017),
            'database': os.environ.get('MONGO_DBNAME', 'simplebot')
        }
    },
    'l10n': {
        'default_lang': 'en',
        'locales': ['en'],
        'file_path': 'res/l10n.json'
    },
    'reception_method': {
        'type': 'polling',
        'params': {
            'timeout': 1
        }
    },
    'bot_path': os.environ.get('BOT_PATH', '/Users/abuca/TelegramBots/SimpleBot'),
    'pictures': {'picture_request_1': '1',
                 'picture_request_2': '2',
                 'picture_request_3': '3',
                 'picture_request_4': '4'
                 }
}
