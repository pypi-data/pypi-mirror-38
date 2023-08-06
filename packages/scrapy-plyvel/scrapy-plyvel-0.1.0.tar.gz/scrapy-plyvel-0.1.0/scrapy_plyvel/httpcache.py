import os
import pickle
from time import time

from scrapy.extensions.httpcache import logger
from scrapy.http import Headers
from scrapy.responsetypes import responsetypes
from scrapy.utils.project import data_path
from scrapy.utils.python import to_bytes, garbage_collect
from scrapy.utils.request import request_fingerprint


class PlyvelCacheStorage:
    def __init__(self, settings):
        import plyvel
        self._plyvel = plyvel
        self.cachedir = data_path(settings['HTTPCACHE_DIR'], createdir=True)
        self.expiration_secs = settings.getint('HTTPCACHE_EXPIRATION_SECS')
        self.db = None

    def open_spider(self, spider):
        dbpath = os.path.join(self.cachedir, f'{spider.name}.leveldb')
        self.db = self._plyvel.DB(dbpath, create_if_missing=True)

        logger.debug(f"Using Plyvel cache storage in {dbpath}")

    def close_spider(self, spider):
        # Do compaction each time to save space and also recreate files to
        # avoid them being removed in storage with timestamp-based autoremoval.
        if self.db is not None:
            self.db.compact_range()
            del self.db
        garbage_collect()

    def retrieve_response(self, spider, request):
        data = self._read_data(spider, request)
        if data is None:
            return  # not cached
        url = data['url']
        status = data['status']
        headers = Headers(data['headers'])
        body = data['body']
        respcls = responsetypes.from_args(headers=headers, url=url)
        response = respcls(url=url, headers=headers, status=status, body=body)
        return response

    def store_response(self, spider, request, response):
        key = self._request_key(request)
        data = {
            'status': response.status,
            'url': response.url,
            'headers': dict(response.headers),
            'body': response.body,
        }
        with self.db.write_batch() as wb:
            wb.put(key + b'_data', pickle.dumps(data, protocol=2))
            wb.put(key + b'_time', to_bytes(str(time())))

    def _read_data(self, spider, request):
        key = self._request_key(request)
        try:
            ts = self.db.get(key + b'_time')
        except KeyError:
            return  # not found or invalid entry

        if ts is None or 0 < self.expiration_secs < time() - float(ts):
            return  # expired

        try:
            data = self.db.get(key + b'_data')
        except KeyError:
            return  # invalid entry
        else:
            if data is not None:
                return pickle.loads(data)

    def _request_key(self, request):
        return to_bytes(request_fingerprint(request))
