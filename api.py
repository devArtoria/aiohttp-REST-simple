import inspect
import datetime
from aiohttp.http_exceptions import HttpBadRequest
from aiohttp.web_exceptions import HTTPMethodNotAllowed, HTTPNotFound
from aiohttp.web import Request, Response
from models import Post, session

DEFAULT_METHODS = ('GET', 'POST', 'DELETE', 'PATCH')


class EndpointBase:

    def __init__(self):
        self.methods = {}

        for method_name in DEFAULT_METHODS:
            method = getattr(self, method_name.lower(), None)
            if method:
                self.register_method(method_name, method)

    def register_method(self, method_name: str, method):
        self.methods[method_name.upper()] = method

    async def dispatch(self, request: Request):
        method = self.methods.get(request.method.upper())
        print(method)
        if not method:
            raise HTTPMethodNotAllowed('', DEFAULT_METHODS)
        wanted_args = list(inspect.signature(method).parameters.keys())
        available_args = request.match_info.copy()
        available_args.update({'request': request})
        unsatisfied_args = set(wanted_args) - set(available_args.keys())
        if unsatisfied_args:
            raise HttpBadRequest('')
        return await method(**{arg_name: available_args[arg_name] for arg_name in wanted_args})

class CollectionView(EndpointBase):
    def __init__(self, resource):
        super().__init__()
        self.resource = resource

    async def get(self) -> Response:
        data = []

        posts = session.query(Post).all()
        for instance in self.resource.collection.values():
            data.append(self.resource.render(instance))
        data = self.resource.encode(data)

        return Response(status=200, body=self.resource.encode({
            'posts': [
                {'id': post.id, 'title': post.title, 'body': post.body,
                 'created_at': post.created_at, 'created_by': post.created_by}
                for post in posts]
        }), content_type='application/json')

    async def post(self, request: Request) -> Response:
        data = await request.json()
        post = Post(title=data["title"],
                    body=data['body'],
                    created_at=datetime.datetime.now(),
                    created_by=data['created_by'])

        session.add(post)
        session.commit()

        return Response(status=201, body=self.resource.encoder(
            {
                "posts": [{'id': post.id,
                           'title': post.title,
                           'body': post.body,
                           'created_at': post.created_at,
                           'created_by': post.created_by}
                          for post in session.query(Post)]
            }
        ), content_type="application/json")

class InstanceView(EndpointBase):
    def __init__(self, resource):
        super().__init__()
        self.resource = resource

    async def get(self, request: Request, instance_id: int) -> Request:
        instance = session.query(Post).filter(Post.id == instance_id)

        if not instance:
            raise HTTPNotFound(body={{"not found": 404}}, content_type="application/json")

        data = self.resource.render_and_encode(instance)
        return Response(status=200, body=data, content_type='application/json')

    async def put(self, request, instance_id):

        data = await request.json()

        post = session.query(Post).filter(Post.id == instance_id).first()
        post.title = data['title']
        post.body = data['body']
        post.created_at = data['created_at']
        post.created_by = data['created_by']
        session.commit()

        return Response(status=201, body=self.resource.render_and_encode(post),
                        content_type='application/json')

    async def delete(self, instance_id):
        post = session.query(Post).filter(Post.id == instance_id).first()
        if not post:
            raise HTTPNotFound(text="Post {} doesn't exist".format(id),
                               content_type="application/text")
        session.delete(post)
        session.commit()
        return Response(status=204)
