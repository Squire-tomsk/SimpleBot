import os

from config import SETTINGS
from service import utils


class MessageDAO:
    MESSAGE_COLLECTION = 'message'
    MESSAGES_DIRECTORY_PATH = SETTINGS['bot_path'] + '/res/messages'
    PICTURES_DIRECTORY_PATH = SETTINGS['bot_path'] + '/res/pictures'

    def __init__(self):
        self._storage = utils.get_storage()

    def _collection(self):
        return self._storage.collection(self.MESSAGE_COLLECTION)

    def _get_path(self, name):
        files = os.listdir(self.MESSAGES_DIRECTORY_PATH)
        try:
            result = self.MESSAGES_DIRECTORY_PATH + '/' + next(files)
        except StopIteration:
            return None
        return result

    def _hash(self, name):
        with open(self._get_path(name), 'rb') as message:
            return utils.get_file_hash(message)

    def _validate(self, name):
        picture_path = self._get_path(name)
        if picture_path is None:
            return False
        return True

    def reload_files(self):
        files = os.listdir(self.MESSAGES_DIRECTORY_PATH)
        picture_files = os.listdir(self.PICTURES_DIRECTORY_PATH)
        picture_names = list(map(lambda x: x.split('.')[0], picture_files))
        message_files = filter(lambda x: x.split('.')[0] not in picture_names, files)
        message_names = list(map(lambda x: x.split('.')[0], message_files))
        for message_name in message_names:
            message = {}
            message['name'] = message_name
            message['text'] = ''
            file = open(self.MESSAGES_DIRECTORY_PATH + '/' + message_name, 'r')
            for line in file.readlines():
                message['text'] += line
            self._collection().set_object(message,
                                      filter_options={'name': message['name']})


    def get_message(self, name):
        return self._collection().get_object(filter_options={'name': name})['text']