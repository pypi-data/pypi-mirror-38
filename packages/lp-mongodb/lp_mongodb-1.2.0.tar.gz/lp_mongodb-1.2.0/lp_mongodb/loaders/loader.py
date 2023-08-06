#!/usr/bin/python
# -*- coding: utf-8 -*-

# thumbor imaging service
# https://github.com/TechLaProvence/lp_mongodb

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 figarocms dhardy@figarocms.fr

from tornado.concurrent import return_future

from lp_mongodb.storages.mongo_storage import Storage
from thumbor.context import Context
from thumbor.config import Config

@return_future
def load(context, path, callback):
  storage = Storage(context)
  callback(storage.get(path))