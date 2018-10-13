from app.models.posts import Post
from app.models import session
from aiohttp.web import Request, Response
from aiohttp.web_exceptions import HTTPNotFound
from app.view import EndpointBase


class InstanceView(EndpointBase):
    def __init__(self, resource):
        super().__init__(allowed_methods=('GET', 'PATCH'))
        self.resource = resource

    async def get(self, request: Request, instance_id: int) -> Request:
        instance = session.query(Post).filter(Post.id == instance_id).first()

        if not instance:
            raise HTTPNotFound(body={{"not found": 404}},
                               content_type="application/json")

        data = self.resource.render_and_encode(instance)
        return Response(status=200, body=data, content_type='application/json')

    async def patch(self, request, instance_id):

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
