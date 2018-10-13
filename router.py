import json
from collections import OrderedDict
from aiohttp.web_urldispatcher import UrlDispatcher

from view.collections import CollectionView
from view.instance import InstanceView


class Router:
    def __init__(self, factory, properties):
        self.factory = factory
        self.properties = properties
        self.collection_view = CollectionView(self)
        self.instance_view = InstanceView(self)

    def register(self, router: UrlDispatcher):
        router.add_route('*', '/posts',
                         self.collection_view.dispatch)
        router.add_route('*', '/posts/{instance_id}',
                         self.instance_view.dispatch)

    def render(self, instance):
        return OrderedDict((posts, getattr(instance, posts))
                           for posts in self.properties)

    def encode(self, data):
        return json.dumps(data, indent=4).encode('utf-8')

    def render_and_encode(self, instance):
        return self.encode(self.render(instance))
