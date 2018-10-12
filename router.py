import json
from collections import OrderedDict
from aiohttp.web_urldispatcher import UrlDispatcher

from api import CollectionView, InstanceView


class Router:
    def __init__(self, factory, properties, id_field):
        self.factory = factory
        self.properties = properties
        self.id_field = id_field

        self.collection_view = CollectionView(self)
        self.instance_view = InstanceView(self)

    def register(self, router: UrlDispatcher):
        router.add_route('*', '/posts',
                         self.collection_view.dispatch)
        router.add_route('*', '/posts/{{instance_id}}',
                         self.instance_view.dispatch)

    def render(self, instance):
        return OrderedDict((posts, getattr(instance, posts))
                           for posts in self.properties)

    @staticmethod
    def encode(data):
        return json.dumps(data, indent=4).encode('utf-8')

    def render_and_encode(self, instance):
        return self.encode(self.render(instance))
