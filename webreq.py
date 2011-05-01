import cgi 
import highlightdoc 

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

class MainPage(webapp.RequestHandler):
	def get(self):
		try:
			f = open('contentfile')
			txtcontentvalue = f.read()
		except IOError:
			txtcontentvalue = ""
		self.response.out.write("""
          <html>
            <body>
			<h1>Highlight Doc Demo</h1>
              <form action="/query" method="post">
                <div><h4>Document: <i>(Editable)</i>&nbsp;</h4><textarea name="content" value="" rows="20" cols="60">"""
				+ txtcontentvalue +
				"""</textarea></div></br>
				<div><h4 style="float:left;margin-top:0">Query: &nbsp;</h4><input type="text" value="deep dish pizza" 
				onblur="if(this.value.length==0)this.value='deep dish pizza';" onclick="if(this.value=='deep dish pizza')this.value=''" 
				name="txtquery"></div></br><div><input type="submit" value="Highlight" onclick="if(txtquery.value.length<=2)return false;return true;"></div>
              </form>
            </body>
          </html>""")


class HighLight(webapp.RequestHandler):
	def post(self):
		self.response.out.write('<html><body>Output:</br></br><div style="font-family:Courier New, Arial, sans-serif;">')
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
