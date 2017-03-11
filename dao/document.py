import os

from config import SETTINGS
from service import utils


class DocumentDAO:
    DOCUMENTS_COLLECTION = 'documents'
    DOCUMENTS_DIRECTORY_PATH = SETTINGS['bot_path'] + '/res/documents'
    DOCUMENTS_EXTENSIONS = ['doc']

    def __init__(self):
        self._storage = utils.get_storage()

    def _collection(self):
        return self._storage.collection(self.DOCUMENTS_COLLECTION)

    def _get_path(self, name):
        files = os.listdir(self.DOCUMENTS_DIRECTORY_PATH)
        filtred_files = filter(lambda x: x.split('.')[-1] in self.DOCUMENTS_EXTENSIONS and x.split('.')[0] == name, files)
        try:
            result = self.DOCUMENTS_DIRECTORY_PATH + '/' + next(filtred_files)
        except StopIteration:
            return None
        return result

    def _hash(self, name):
        with open(self._get_path(name), 'rb') as document:
            return utils.get_file_hash(document)

    def _validate(self, name):
        document_path = self._get_path(name)
        if document_path is None:
            return False
        return True

    def reload_files(self):
        files = os.listdir(self.DOCUMENTS_DIRECTORY_PATH)
        document_files = filter(lambda x: x.split('.')[-1] in self.DOCUMENTS_EXTENSIONS, files)
        document_names = list(map(lambda x: x.split('.')[0], document_files))
        for document_name in document_names:
            try:
                document_info = self.get_document_info(document_name)
                if document_info['hash'] != self._hash(document_name):
                    self.add_document(document_name)
            except KeyError:
                self.add_document(document_name)
        outdated_documents = self._collection().get_object(filter_options={'name': {'$nin': document_names}}, multi=True)
        for outdated_document in outdated_documents:
            self.delete_document(outdated_document['name'])

    def add_document(self, name):
        if self._validate(name):
            document_info = dict()
            document_info['name'] = name
            document_info['hash'] = self._hash(document_info['name'])
            document_info['file_id'] = ''
            return self._collection().set_object(document_info,
                                                 filter_options={'name': document_info['name']})

    def add_file_id_for_document(self, name, file_id):
        self.get_document_info(name)  # check that document exist
        return self._collection().set_field(key='file_id',
                                            new_value=file_id,
                                            name=name)

    def get_document(self, name):
        document_info = self.get_document_info(name)
        if document_info['file_id'] == '':
            return open(self._get_path(name), 'rb')
        else:
            return document_info['file_id']

    def get_document_message(self, name):
        document_info = self.get_document_info(name)
        return document_info['message']

    def get_document_info(self, name):
        document_info = self._collection().get_object(filter_options={'name': name})
        if document_info is None:
            raise KeyError('document ' + name + ' not found')
        return document_info

    def get_documents_names(self):
        return self._collection().get_field(key='name')

    def delete_document(self, name):
        return self._collection().remove_object(filter_options={'name': name})
