import json
from collections import OrderedDict
from aiohttp.web_urldispatcher import UrlDispatcher

from app.view.collections import CollectionView
from app.view.instance import InstanceView

from app.models.posts import Post


class Router:
    def __init__(self):
        self.factory = Post
        self.collection_view = CollectionView(self)
        self.instance_view = InstanceView(self)

    def register(self, router: UrlDispatcher):
        router.add_route('*', '/posts',
                         self.collection_view.dispatch)
        router.add_route('*', '/posts/{instance_id}',
                         self.instance_view.dispatch)

    def render(self, instance):
        return OrderedDict((posts, getattr(instance, posts))
                           for posts in ('title', 'body', 
                                                  'created_at', 'created_by'))

    def encode(self, data):
        return json.dumps(data, indent=4).encode('utf-8')

    def render_and_encode(self, instance):
        return self.encode(self.render(instance))
