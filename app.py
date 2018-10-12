from aiohttp.web import Application, run_app
from router import Router
from models import Post
from sqlalchemy import engine_from_config


posts = {}
app = Application()
person_resource = Router('posts', Post, posts, ('title', 'body', 'created_at', 'created_by'), 'title')
person_resource.register(app.router)


if __name__ == '__main__':

    run_app(app, host="127.0.0.1", port=9000)
