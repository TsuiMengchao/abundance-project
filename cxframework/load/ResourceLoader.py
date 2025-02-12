import os

from cxframework.load.Resource import Resource


class ResourceLoader:
    def __init__(self):
        self.sources = None

    def get_resource(self, location):
        if os.path.exists(location):
            with open(location, 'rb') as f:
                self.sources = Resource(f.read())
        else:
            self.sources = Resource(None)
        return self.sources
