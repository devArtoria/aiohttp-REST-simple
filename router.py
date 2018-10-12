from api import *


class Router:
    def __init__(self, posts, factory, collection, properties, id_field):
        self.posts = posts
        self.factory = factory
        self.collection = collection
        self.properties = properties
        self.id_field = id_field

        self.collection_view = CollectionView(self)
        self.instance_view = InstanceView(self)

    def register(self, router: UrlDispatcher):
        router.add_route('*', '/{posts}'.format(posts=self.posts), self.collection_view.dispatch)
        router.add_route('*', '/{posts}/{{instance_id}}'.format(posts=self.posts), self.instance_view.dispatch)

    def render(self, instance):
        return OrderedDict((posts, getattr(instance, posts)) for posts in self.properties)

    @staticmethod
    def encode(data):
        return json.dumps(data, indent=4).encode('utf-8')

    def render_and_encode(self, instance):
        return self.encode(self.render(instance))
