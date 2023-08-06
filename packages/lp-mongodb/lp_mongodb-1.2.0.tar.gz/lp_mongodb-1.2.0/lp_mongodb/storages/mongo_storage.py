# -*- coding: utf-8 -*-
# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2015 Thumbor-Community
# Copyright (c) 2011 globo.com timehome@corp.globo.com

from datetime import datetime, timedelta
from cStringIO import StringIO


from pymongo import MongoClient
import gridfs

from thumbor.storages import BaseStorage
from tornado.concurrent import return_future


class Storage(BaseStorage):

    connection = None
    db = None
    storage = None

    def __init__(self, context, shared_client=True):
      ''' Init the MongoStorage
      :param thumbor.context.Context shared_client : Current Context
      :param boolean shared_client: When set to True a singleton client will be used.

      '''
      BaseStorage.__init__(self, context)
      self.shared_client = shared_client
      self.connection, self.db, self.storage = self.reconnect_mongo()


    def get_storage(self):
      ''' Get the storage instance.

      :return MongoClient: MongoClient Storage instance
      '''

      if self.connection and self.db and self.storage:
        return self.connection, self.db, self.storage

      return self.reconnect_mongo()
    

    def reconnect_mongo(self):
      if self.shared_client and Storage.connection and Storage.db and Storage.storage:
        return Storage.connection, Storage.db, Storage.storage

      connection = MongoClient(self.context.config.MONGO_LP_SERVER_HOST, self.context.config.MONGO_LP_SERVER_PORT)
      db = connection[self.context.config.MONGO_LP_SERVER_DB]
      storage = db[self.context.config.MONGO_LP_SERVER_COLLECTION]

      if self.shared_client:
        Storage.connection = connection
        Storage.db = db
        Storage.storage = storage

      return connection, db, storage


    def put(self, path, bytes):
        connection, db, storage = self.get_storage()
        print(self)
        doc = {
            'path': path,
            'created_at': datetime.now()
        }

        doc_with_crypto = dict(doc)
        if self.context.config.STORES_CRYPTO_KEY_FOR_EACH_IMAGE:
            if not self.context.server.security_key:
                raise RuntimeError("STORES_CRYPTO_KEY_FOR_EACH_IMAGE can't be True if no SECURITY_KEY specified")
            doc_with_crypto['crypto'] = self.context.server.security_key

        fs = gridfs.GridFS(db)
        file_data = fs.put(StringIO(bytes), **doc)

        doc_with_crypto['file_id'] = file_data
        storage.insert(doc_with_crypto)
        return path

    def put_crypto(self, path):
        if not self.context.config.STORES_CRYPTO_KEY_FOR_EACH_IMAGE:
            return

        connection, db, storage = self.get_storage()

        if not self.context.server.security_key:
            raise RuntimeError("STORES_CRYPTO_KEY_FOR_EACH_IMAGE can't be True if no SECURITY_KEY specified")

        crypto = storage.find_one({'path': path})

        crypto['crypto'] = self.context.server.security_key
        storage.update({'path': path}, crypto)
        return path

    def put_detector_data(self, path, data):
        connection, db, storage = self.get_storage()

        storage.update({'path': path}, {"$set": {"detector_data": data}})
        return path

    @return_future
    def get_crypto(self, path, callback):
        connection, db, storage = self.get_storage()

        crypto = storage.find_one({'path': path})
        callback(crypto.get('crypto') if crypto else None)

    @return_future
    def get_detector_data(self, path, callback):
        connection, db, storage = self.get_storage()

        doc = storage.find_one({'path': path})
        callback(doc.get('detector_data') if doc else None)

    @return_future
    def get(self, path, callback):
        connection, db, storage = self.get_storage()

        stored = storage.find_one({'path': path})

        if not stored :
            callback(None)
            return

        fs = gridfs.GridFS(db)
        contents = fs.get(stored['file_id']).read()

        callback(str(contents))

    @return_future
    def exists(self, path, callback):
        connection, db, storage = self.get_storage()

        stored = storage.find_one({'path': path})

        if not stored :
            callback(False)
        else:
            callback(True)

    def remove(self, path):
        if not self.exists(path):
            return

        connection, db, storage = self.get_storage()
        fs = gridfs.GridFS(db)

        stored = storage.find_one({'path':path})

        fs.delete(stored['file_id'])
        storage.remove({'path': path})

    def __is_expired(self, stored):
        timediff = datetime.now() - stored.get('created_at')
        return timediff > timedelta(seconds=self.context.config.STORAGE_EXPIRATION_SECONDS)
