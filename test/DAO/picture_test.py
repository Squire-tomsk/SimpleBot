import unittest
from shutil import move

from config import SETTINGS
from dao.picture import PictureDAO
from service import utils


class TestStringMethods(unittest.TestCase):
    def setUp(self):
        self._dao = PictureDAO()
        self._dao.PICTURES_DIRECTORY_PATH = SETTINGS['bot_path'] + '/test/res/pictures'
        self._dao.PICTURES_COLLECTION = 'pictures_test'

    def test_insert_read_delete(self):
        original_picture_name = 'test1'
        self._dao.add_picture(original_picture_name)
        self._check_hashes([original_picture_name])
        self._dao.delete_picture(original_picture_name)
        with self.assertRaises(KeyError):
            self._dao.get_picture(original_picture_name)

    def test_reload(self):
        picture_names = ['test1', 'test2', 'test3', 'test4']
        self._dao.reload_files()
        self._check_hashes(picture_names)

        src = self._dao.PICTURES_DIRECTORY_PATH + '/' + picture_names[-1] + '.png'
        dst = SETTINGS['bot_path'] + '/test/res'
        move(src, dst)
        self._dao.reload_files()
        self._check_hashes(picture_names[:-1])
        with self.assertRaises(KeyError):
            self._dao.get_picture(picture_names[-1])

        src = SETTINGS['bot_path'] + '/test/res' + '/' + picture_names[-1] + '.png'
        dst = self._dao.PICTURES_DIRECTORY_PATH
        move(src, dst)
        self._dao.reload_files()
        self._check_hashes(picture_names)

        for picture_name in picture_names:
            self._dao.delete_picture(picture_name)

    def test_names_load(self):
        original_picture_names = ['test1', 'test2', 'test3', 'test4']
        self._dao.reload_files()
        loaded_picture_names = self._dao.get_pictures_names()
        self.assertEqual(set(original_picture_names), set(loaded_picture_names))
        for picture_name in original_picture_names:
            self._dao.delete_picture(picture_name)

    def _check_hashes(self, picture_names):
        for picture_name in picture_names:
            with open(self._dao.PICTURES_DIRECTORY_PATH + '/' + picture_name + '.png', 'rb') as picture:
                original_picture_hash = utils.get_file_hash(picture)
            loaded_picture = self._dao.get_picture(picture_name)
            loaded_picture_hash = utils.get_file_hash(loaded_picture)
            self.assertEqual(original_picture_hash, loaded_picture_hash)


if __name__ == '__main__':
    unittest.main()
