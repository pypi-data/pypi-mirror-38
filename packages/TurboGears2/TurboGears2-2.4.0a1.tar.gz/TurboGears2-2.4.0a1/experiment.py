from tg import AppConfig

from wsgiref.simple_server import make_server
from tg import expose, TGController

class RootController(TGController):
     @expose()
     def index(self):
         return "<h1>Hello World</h1>"

app_config = AppConfig(root_controller=RootController())

print "Serving on port 8080..."
httpd = make_server('', 8080, app_config.make_wsgi_app())
httpd.serve_forever()



