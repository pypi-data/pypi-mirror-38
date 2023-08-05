
import tornado.ioloop
import tornado.web
import tornado.template

import fantail

from kea3 import models

class K3ReqHandler(tornado.web.RequestHandler):

    def initialize(self, app):
        self.k3app = app


class MainHandler(K3ReqHandler):

    def get(self):

        try:
            session = self.k3app.db_session

            #filename search
            rv = session.query(
                models.KFile.size, models.KkeyVal.key, models.KkeyVal.val)\
                .join(models.KHash)\
                .join(models.KkeyVal)\
                .filter(models.KkeyVal.key == 'project')\
                .limit(20).all()

            message = []
            for r in rv:
                message.append(str(r))
            message = "\n".join(message)

        except Exception as e:
            message = str(e)

        session = self.k3app.db_session
        hosts = session.query(models.KFile.hostname).distinct().all()
        data = dict(hosts = hosts, message=message)
        print(hosts)
        self.render("index.html", title='k3', **data)


# class MainHandler(K3ReqHandler):
#     def get(self):
#         self.render("index.html", title='k3')


class SearchHandler(K3ReqHandler):
    def get(self):

        term = self.get_argument('term', None)

        if not term:
            self.redirect('/')
            return

        data = dict(title=f'Search results for "{term}"',
                    term=term)

        session = self.k3app.db_session

        #filename search
        files = session.query(models.KFile)\
                     .filter(models.KFile.filename.contains(term))\
                     .limit(20).all()
        data['files'] = files
        self.render("search.html", **data)


class HostHandler(K3ReqHandler):
    def get(self, host):

        data = dict(title=f'Hits for host "{host}"',
                    host=host)

        session = self.k3app.db_session

        #filename search
        files = session.query(models.KFile)\
                     .filter(models.KFile.hostname == host)\
                     .limit(20).all()
        data['files'] = files
        self.render("search.html", **data)


class FileHashHandler(K3ReqHandler):
    def get(self, short):
        data = dict(title=f'Hash {short}', short=short)

        session = self.k3app.db_session
        khash = session.query(models.KHash).filter_by(short = short).one()
        data['khash'] = khash
        self.render("khash.html", **data)


@fantail.arg('-p', '--port', default=9898, type=int)
@fantail.command
def serve(app, args):
    data = dict(app=app)
    application = tornado.web.Application([
        (r"/", MainHandler, data),
        (r"/search", SearchHandler, data),
        (r"/hash/(f.+)", FileHashHandler, data),
        (r"/host/(.+)", HostHandler, data),
    ], autoreload=True, debug=True)
    application.listen(args.port)
    tornado.ioloop.IOLoop.current().start()
