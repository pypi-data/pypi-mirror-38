from slim.base.view import BaseView
from slim.retcode import RETCODE
from app import app


@app.route('misc')
class TestBaseView(BaseView):
    @classmethod
    def interface(cls):
        pass

    @app.route.interface('GET')
    async def info(self):
        self.finish(RETCODE.SUCCESS, {
            'retcode': list(RETCODE.items()),
            #'retinfo': RETCODE.txt,
        })
