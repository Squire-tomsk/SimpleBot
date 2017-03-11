import hashlib
import logging
import sys

from botlab import storage
from botlab.configuration_manager import ConfigurationManager
from botlab.exceptions import UnknownStorageException

from config import SETTINGS

BUF_SIZE = 65536

logging.basicConfig(filename=SETTINGS['bot_path'] + '/res/logs/errors.log',
                    level=logging.ERROR,
                    format='%(asctime)s - %(message)s')


def get_storage():
    config_manager = ConfigurationManager(SETTINGS)
    storage_type = config_manager.get('db_storage').get('type')
    storage_params = config_manager.get('db_storage').get('params')
    if storage_type == 'mongo':
        return storage.MongoStorage(storage_params)
    elif storage_type == 'inmemory':
        return storage.InMemoryStorage(storage_params)
    elif storage_type == 'disk':
        return storage.DiskStorage(storage_params)
    else:
        raise UnknownStorageException()


def error_log_decorator(handler):
    def log_wrapper(session, message):
        try:
            handler(session, message)
        except:
            logging.exception(msg='Controller error: ', exc_info=sys.exc_info())
    return log_wrapper


def get_file_hash(input_stream):
    sha1 = hashlib.sha1()
    while True:
        data = input_stream.read(BUF_SIZE)
        if not data:
            break
        sha1.update(data)
    return sha1.hexdigest()
