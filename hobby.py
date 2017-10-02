import os
import tornado.ioloop
import tornado.web
import tornado.log
from dotenv import load_dotenv
import boto3

from jinja2 import \
  Environment, PackageLoader, select_autoescape

load_dotenv(".env")

PORT = int(os.environ.get('PORT', '1337'))

ENV = Environment(
  loader=PackageLoader('myapp', 'templates'),
  autoescape=select_autoescape(['html', 'xml'])
)

client = boto3.client(
  'ses',
  aws_access_key_id=os.environ.get('AWS_ACCESS_KEY'),
  aws_secret_access_key=os.environ.get('AWS_SECRET_KEY'),
  region_name=os.environ.get("AWS_DEFAULT_REGION")
)

class TemplateHandler(tornado.web.RequestHandler):
  def render_template (self, tpl, context):
    template = ENV.get_template(tpl)
    self.write(template.render(**context))

class MainHandler(TemplateHandler):
  def get(self):
    names = self.get_query_arguments('name')
    self.set_header(
      'Cache-Control',
      'no-store, no-cache, must-revalidate, max-age=0')
    self.render_template("index.html", {'names': names, 'amount': 42.55})

class HealthHandler(TemplateHandler):
    def get(self):
        self.render_template('health.html', {})

class LearningHandler(TemplateHandler):
    def get(self):
        self.render_template('learning.html', {})

class VideogamesHandler(TemplateHandler):
    def get(self):
        self.render_template('videogames.html', {})

class MusicHandler(TemplateHandler):
    def get(self):
        self.render_template('music.html', {})

class NatureHandler(TemplateHandler):
    def get(self):
        self.render_template('nature.html', {})

class FamilyHandler(TemplateHandler):
    def get(self):
        self.render_template('family.html', {})

class PageHandler(TemplateHandler):
  def post (self,page):
    email = self.get_body_argument('email')

    response = client.send_email(
      Destination={
        'ToAddresses': ['shahramg92@hotmail.com'],
      },
      Message={
        'Body': {
          'Text': {
            'Charset': 'UTF-8',
            'Data': 'This is a test email',
          },
        },
        'Subject': {'Charset': 'UTF-8', 'Data': 'Test email'},
      },
      Source='mailer@shahramghassemi.com',
    )
    self.redirect('/thank-you-for-submitting')

  def get(self, page):
    self.set_header(
      'Cache-Control',
      'no-store, no-cache, must-revalidate, max-age=0')
    self.render_template(page, {})

def make_app():
  return tornado.web.Application([
    (r"/", MainHandler),
    (r"/health", HealthHandler),
    (r"/music", MusicHandler),
    (r"/learning", LearningHandler),
    (r"/videogames", VideogamesHandler),
    (r"/nature", NatureHandler),
    (r"/family", FamilyHandler),
    (r"/page/(.*)", PageHandler),
    (
      r"/static/(.*)",
      tornado.web.StaticFileHandler,
      {'path': 'static'}
    ),
  ], autoreload=True)

if __name__ == "__main__":
  tornado.log.enable_pretty_logging()

  app = make_app()
  app.listen(PORT, print('Server started on localhost:' + str(PORT)))
  tornado.ioloop.IOLoop.current().start()

# request = YouTooHandler(request_info)
# request.get()
