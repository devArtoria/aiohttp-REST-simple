from aiohttp.web import Application, run_app
from router import Router
from models.posts import Post

posts = {}
app = Application()
person_resource = Router(factory=Post,
                         properties=('title', 'body',
                                     'created_at', 'created_by'))

person_resource.register(app.router)


if __name__ == '__main__':

    run_app(app, host="127.0.0.1", port=9000)
