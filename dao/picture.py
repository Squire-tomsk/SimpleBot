import os

from config import SETTINGS
from service import utils


class PictureDAO:
    PICTURES_COLLECTION = 'pictures'
    PICTURES_DIRECTORY_PATH = SETTINGS['bot_path'] + '/res/pictures'
    PICTURE_EXTENSIONS = ['jpg', 'png']

    def __init__(self):
        self._storage = utils.get_storage()

    def _collection(self):
        return self._storage.collection(self.PICTURES_COLLECTION)

    def _get_path(self, name):
        files = os.listdir(self.PICTURES_DIRECTORY_PATH)
        filtred_files = filter(lambda x: x.split('.')[-1] in self.PICTURE_EXTENSIONS and x.split('.')[0] == name, files)
        try:
            # TODO what function should do if folder contains several same name pictures?
            result = self.PICTURES_DIRECTORY_PATH + '/' + next(filtred_files)
        except StopIteration:
            return None
        return result

    def _hash(self, name):
        with open(self._get_path(name), 'rb') as picture:
            return utils.get_file_hash(picture)

    def _validate(self, name):
        picture_path = self._get_path(name)
        if picture_path is None:
            return False
        return True

    def reload_files(self):
        files = os.listdir(self.PICTURES_DIRECTORY_PATH)
        picture_files = filter(lambda x: x.split('.')[-1] in self.PICTURE_EXTENSIONS, files)
        picture_names = list(map(lambda x: x.split('.')[0], picture_files))
        for picture_name in picture_names:
            try:
                picture_info = self.get_picture_info(picture_name)
                if picture_info['hash'] != self._hash(picture_name):
                    self.add_picture(picture_name)
            except KeyError:
                self.add_picture(picture_name)
        outdated_pictures = self._collection().get_object(filter_options={'name': {'$nin': picture_names}}, multi=True)
        for outdated_picture in outdated_pictures:
            self.delete_picture(outdated_picture['name'])

    def add_picture(self, name):
        if self._validate(name):
            picture_info = dict()
            picture_info['name'] = name
            picture_info['hash'] = self._hash(picture_info['name'])
            picture_info['file_id'] = ''
            return self._collection().set_object(picture_info,
                                                 filter_options={'name': picture_info['name']})

    def add_file_id_for_picture(self, name, file_id):
        self.get_picture_info(name)  # check that picture exist
        return self._collection().set_field(key='file_id',
                                            new_value=file_id,
                                            name=name)

    def get_picture(self, name):
        picture_info = self.get_picture_info(name)
        if picture_info['file_id'] == '':
            return open(self._get_path(name), 'rb')
        else:
            return picture_info['file_id']

    def get_picture_info(self, name):
        picture_info = self._collection().get_object(filter_options={'name': name})
        if picture_info is None:
            raise KeyError('Picture ' + name + ' not found')
        return picture_info

    def get_pictures_names(self):
        return self._collection().get_field(key='name')

    def delete_picture(self, name):
        return self._collection().remove_object(filter_options={'name': name})
