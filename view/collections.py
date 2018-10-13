import datetime
from models.posts import Post
from models import session
from aiohttp.web import Request, Response
from view import EndpointBase


class CollectionView(EndpointBase):
    def __init__(self, resource):
        super().__init__(allowed_methods=('GET', 'POST'))
        self.resource = resource

    async def get(self) -> Response:
        posts = session.query(Post).all()

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
