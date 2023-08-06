# encoding: utf-8
"""
base_file_cache.py

Provides class for caching data in files.

Read and write methods must be provided by the subclass
"""

import os
import sys
import pprint
import logging
from abc import ABCMeta, abstractmethod
from .base_cache import Cache, CacheError
from fdutil.path_tools import ensure_path_exists


class BaseFileCache(Cache):

    __metaclass__ = ABCMeta  # Marks this as an abstract class

    # Also re-implement key and fetch_from_source and optionally filename

    @abstractmethod
    def read(self,
             filepath):
        """
        Reads the contents of the cached file

        :param filepath: Full path to the file.
        :return: contents of the file
        """
        raise NotImplementedError(u'BaseFileCache.read must be implemented')

    @abstractmethod
    def write(self,
              item,
              filepath):
        """
        Writes the item to the filepath

        :param item:
        :param filepath:
        :return: N/A
        """
        raise NotImplementedError(u'BaseFileCache.write must be implemented')

    def filename(self,
                 key):
        """
        uses the cached item key to make a suitable filename.
        e.g. add a file extension. If the key and filename are the same,
             there's no need to override filename

        :param key: cached item key
        :return: cached item filename
        """
        return key

    u"""
        ┌────────────────────────────┐
        │ Don't re-implement methods │
        │ below when subclassing...  │
        └────────────────────────────┘
     """

    def __init__(self,
                 max_age=0,
                 folder=u'',
                 sub_folder=u'',
                 **params):
        """
        Cached data to files. When the are older than max_age, the date
        will be refetched. When younger than max_age, the cached file
        is used.

        Note that old cached files are not automatically deleted, but
        will be replaces when a new fetch is made.

        :param max_age: time in seconds to maintain the cached files
                        the default is 0, which is to never expire.
        :param folder: path to a folder containing the cache or the parent
                       folder of the cache. If it's a parent folder, you
                       should also supply a sub_folder path
        :param sub_folder: path from the folder to the sub_folder intended
                           to contain the files for this cache.
        """
        super(BaseFileCache, self).__init__(**params)
        self.__max_age = max_age
        self.__folder = os.path.join(folder, sub_folder)
        if os.path.exists(self.__folder):
            if not os.path.isdir(self.__folder):
                raise CacheError(u'Invalid folder:"{folder}"'
                                 .format(folder=self.__folder))
        else:
            try:
                os.makedirs(self.__folder)
            except Exception as e:
                raise CacheError(u'Could not create folder: '
                                 u'"{folder}" because:"{e}"'
                                 .format(folder=self.__folder,
                                         e=e))

    def filepath(self,
                 key):
        """
        Assembles folder path and filename

        NOT INDENTED FOR RE-IMPLEMENTION IN SUBCLASS

        :param key: cache key
        :return: full path to the file
        """
        return os.path.normpath(os.path.join(self.__folder,
                                             self.filename(key)))

    def cache(self,
              item,
              **params):
        """
        Writes the data in 'value' to the cached file

        NOT INTENDED FOR RE-IMPLEMENTION IN SUBCLASS

        :param item: data to write to the cache
        :param params: parameters required to build the filename
        :return: n/a
        """
        # TODO write to a temporary file and move
        try:
            # Get fully qualified filepath
            filepath = self.filepath(self.key(**params))

            # Ensure directories exist
            ensure_path_exists(filepath,
                               includes_filename=True)

            # Write the file
            self.write(item=item,
                       filepath=filepath)

        except TypeError as te:
            logging.exception(te)
            logging.error(u'params:')
            for p in params:
                logging.error(u'{param}'
                              .format(param=pprint.pformat(p)))
            raise te

        except IOError as ioe:
            logging.exception(ioe)
            logging.error(u'params:')
            for p in params:
                logging.error(u'{param}'
                              .format(param=pprint.pformat(p)))

            # Not re-raising as we can still use the in-memory object

    def fetch_from_cache_by_key(self,
                                key):
        """
        Returns the contents of the cached file

        NOT INDENTED FOR RE-IMPLEMENTION IN SUBCLASS

        :param key: key required to build the filename
        :return: contents of the cached file
        """
        return self.read(self.filepath(key))

    def cached_time(self,
                    key):
        return os.path.getmtime(self.filepath(key))

    def expiry(self,
               key):
        """
        OVERRIDE in subclass if per-item file expiry
        can be calculated from the file contents.
        (e.g. file contains HTTP Cache-Control)

        Ca
        :param key: cache key
        :return: None: (Default) there's no per item expiry calculation
                 True: Item has not expired
                 False: Item has expired
                 Delta - number of seconds to keep the cached item
        """
        return None

    def expiry_time(self,
                    key):
        """
        Get the expiry time of the item.

        :return: expiry time as epoch seconds
        """
        if os.path.exists(self.filepath(key)):
            try:
                expiry = self.expiry(key)
                if expiry is True or self.__max_age == 0:
                    return sys.maxsize
                elif expiry is False:
                    return 0
                elif expiry is not None:
                    return self.cached_time(key) + expiry
                return self.cached_time(key) + self.__max_age
            except Exception as e:
                raise CacheError(u'{e}: {key}'
                                 .format(e=e,
                                         key=key))
        else:
            raise CacheError(u'No such file: {filepath}'
                             .format(filepath=self.filepath(key)))

    def delete_by_key(self,
                      key):
        """
        Delete a file from the cache.

        NOT INDENTED FOR RE-IMPLEMENTION IN SUBCLASS

        :param key: cache key
        """
        filepath = self.filepath(key)
        if os.path.exists(filepath):
            try:
                os.remove(filepath)
            except Exception as e:
                raise CacheError(u'{e}: {filepath}'.format(e=e, filepath=filepath))
        else:
            raise CacheError(u'No such file: {filepath}'.format(filepath=filepath))

    def delete(self,
               **params):
        """
        Delete a file from the cache.

        NOT INDENTED FOR RE-IMPLEMENTION IN SUBCLASS

        :param params: list of parameters required to
                       fetch the item and create a key
        """
        try:
            self.delete_by_key(self.key(**params))
        except TypeError as te:
            logging.exception(te)
            logging.error(u'params:')
            for p in params:
                logging.error(u'{param}'
                              .format(param=pprint.pformat(p)))
            raise te

    def reset_cache(self):
        # get list of files
        for filename in [f for f in os.listdir(self.__folder) if os.path.isfile(f)]:
            os.remove(filename)
