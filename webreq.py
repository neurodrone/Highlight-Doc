import cgi
import highlightdoc

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

class MainPage(webapp.RequestHandler):
	def get(self):
		self.response.out.write("""
          <html>
            <body>
              <form action="/query" method="post">
                <div><h4>Document: <i>(Editable)</i>&nbsp;</h4><textarea name="content" value="" rows="20" cols="60">when i saw 1600+ reviews.. i was like.. "uh maybe i should not come here, I'm afraid we might have to wait a long time" But I came anyways and there was NO WAIT ON A TUESDAY NIGHT!! WHoa, got a table right away! We were so hungry! The waitress kinda lied though. For two people, we ordered a large deep dish veggie pizza and the waitress encouraged us to order an appetizer b/c the pizza was going to take 30mins to come out. So we ordered garlic bread. The pizza came out in like 15mins or less. We couldn't eat more than half of the pizza b/c the garlic bread filled us up!

				Garlic Bread- I like how the garlic is roasted and very easy to spread, I'd skip it though if you have a small appetite. Because all that carb is gonna fill u up quick!

				Vegetarian Deep Dish Pizza- Very Yummy! I guess I'm a bigger fan of thin crust but I'm very impressed with their deep dish pizza! It is very good. The crust is perfect!

				I'll be back to try their thin crust pizzas next time!</textarea></div></br>
				<div><h4 style="float:left;margin-top:0">Query: &nbsp;</h4><input type="text" value="deep dish pizza" onblur="if(this.value.length==0)this.value='deep dish pizza';" onclick="if(this.value=='deep dish pizza')this.value=''" name="txtquery"></div></br>
                <div><input type="submit" value="Highlight" onclick="if(txtquery.value.length<=2)return false;return true;"></div>
              </form>
            </body>
          </html>""")


class HighLight(webapp.RequestHandler):
	def post(self):
		self.response.out.write('<html style="width:100%"><body>Output:</br></br><div style="width:100%;font-family:Courier New, Arial, sans-serif;">')
		txtquery = cgi.escape(self.request.get('txtquery'))
		txtcontent = cgi.escape(self.request.get('content'))
		txtout = highlightdoc.highlight_doc(txtcontent, txtquery)
		self.response.out.write(txtout if len(txtout) > 0 else "No match found.")
		self.response.out.write('</div></br><a href="javascript:history.back()">Back</a></body></html>')

application = webapp.WSGIApplication(
									[('/', MainPage),
									('/query', HighLight)],
									debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()