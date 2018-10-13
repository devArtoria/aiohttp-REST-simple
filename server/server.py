from aiohttp.web import Application, run_app
from app import Router

app = Application()
router = Router()

router.register(app.router)


if __name__ == '__main__':

    run_app(app, host="127.0.0.1", port=9000)
