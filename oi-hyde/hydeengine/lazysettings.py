import time
import os
import hyde_defaults

class Target(object):
    pass

class LazySettings(object):
    
    def __init__(self):
        self._data = Target()

    def __getattr__(self, name):
        return getattr(self._data, name)

    def __setattr__(self, name, value):
        if name == '_data':
            self.__dict__['_data'] = value
        else:
            setattr(self._data, name, value)

    def configure(self, ob, **options):
        for k in dir(ob):
            setattr(self._data, k, getattr(ob, k))
        for k, v in options.items():
            setattr(self._data, k, v)

class _HydeDefaults:

    GENERATE_CLEAN_URLS = False
    GENERATE_ABSOLUTE_FS_URLS = False
    LISTING_PAGE_NAMES = ['index', 'default', 'listing']
    APPEND_SLASH = False
    MEDIA_PROCESSORS = {}
    CONTENT_PROCESSORS = {}
    SITE_PRE_PROCESSORS = {}
    SITE_POST_PROCESSORS = {}
    CONTEXT = {}

settings = LazySettings()
