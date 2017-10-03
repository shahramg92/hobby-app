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
  region_name=os.environ.get('AWS_DEFAULT_REGION')
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

class ThankyouHandler(TemplateHandler):
    def get(self):
        self.render_template('thankyou.html', {})

class TipcalcHandler(TemplateHandler):
    def get(self):
        self.render_template('tipcalc.html', {})
    def post(self):
        bill = self.get_body_argument('bill')
        service = self.get_body_argument('service')

    def main():
        # ask for bill amount
        bill = float(input("What is the amount of your bill? $"))

        # ask for satisfaction level
        service = input("\nHow was the service?\ngood\nfair\nbad\nPlease choose one of the above options, then press Enter. ").lower()


        # calculate tip amount
        tips = {"good" : 0.20,
                "fair" : 0.15,
                "bad" : 0.10}
        tip_percentage = tips[service]
        tip = bill * tip_percentage

        # print message with tip amount
        print("\nYour bill was ${bill:.2f}, and your service was {service}.\n\nYou should tip ${tip:.2f}\n".format(bill=bill, service=service, tip=tip))

        main()


class ContactHandler(TemplateHandler):
    def post (self):
      email = self.get_body_argument('email')
      password = self.get_body_argument('password')
      address = self.get_body_argument('address')
      address2 = self.get_body_argument('address2')
      city = self.get_body_argument('city')
      zipcode = self.get_body_argument('zipcode')
      state = self.get_body_argument('state')

      response = client.send_email(
        Destination={
          'ToAddresses': ['shahramg92@hotmail.com'],
        },

        Message={
          'Body': {
            'Text': {
              'Charset': 'UTF-8',
              'Data': f"Email: {email}, Password: {password}, Address: {address}, Address2: {address2}, City: {city}, State: {state}, Zip: {zipcode}"
            },
          },
          'Subject': {'Charset': 'UTF-8', 'Data': 'Test email'},
        },
        Source='mailer@shahramghassemi.com',
      )
      self.redirect('/thankyou')

    def get(self):
        self.render_template('contact.html', {})


class PageHandler(TemplateHandler):

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
    (r"/contact", ContactHandler),
    (r"/thankyou", ThankyouHandler),
    (r"/tipcalc", TipcalcHandler),
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
