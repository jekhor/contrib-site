from jinja2 import BaseLoader, TemplateNotFound
from os.path import join, exists, getmtime

class AbsPathLoader(BaseLoader):

    def __init__(self):
        super(AbsPathLoader, self).__init__()

    def get_source(self, environment, path):
        if not exists(path):
            raise TemplateNotFound(template)
        mtime = getmtime(path)
        with file(path) as f:
            source = f.read().decode('utf-8')
        return source, path, lambda: mtime == getmtime(path)
