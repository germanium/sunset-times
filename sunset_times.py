
import os, sys, time 
import webapp2
import jinja2
import numpy

sys.path.append(os.path.join(os.path.dirname(__file__), 'scripts'))
from scripts import crepyscule_tools
from scripts.geopy import geocoders
from scripts.geopy.geocoders import google_timezone


template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
								autoescape = True)

def save_one_year_data(zipcode):
	sFilename = 'data.csv'
	# Define day in year of result
	t = time.strptime("6 Jun 2012", "%d %b %Y")   
	ctime = time.mktime(t)

	# Find Lat Lon for given zip code
	g = geocoders.GoogleV3()
	place, (fLat, fLon) = g.geocode("750 Hinman Ave, Evanston")
	print "%s: %.5f, %.5f" % (place, fLat, fLon)
	g2 = google_timezone.GoogleTimezone()
	fUTC = g2.geocode(fLat, fLon)/(60**2)
	sDLS = 'US'

	(lSunrise, lSunset, lSunAltitude, tToday) = \
    	crepyscule_tools.get_one_year_data(fLat, fLon, ctime, fUTC, sDLS)

	lDaylength = crepyscule_tools.get_daylength(ctime, fLat, fLon)
	lDateISO8601 = crepyscule_tools.get_one_year_of_iso8601(ctime)
                                                 
	crepyscule_tools.save_info_flat_file(sFilename, lDateISO8601,\
                                    	lSunrise, lSunset, lDaylength,\
                                    	fLat, fLon, fUTC, sDLS)

class Handler(webapp2.RequestHandler):
	def write(self, *a, **kw):
		self.response.out.write(*a, **kw)

	def render_str(self, template, **params):
		t = jinja_env.get_template(template)
		return t.render(params)

	def render(self, template, **kw):
		self.write(self.render_str(template, **kw))


class MainPage(Handler):
	def render_front(self, zipcode="", error="", errorID="control-group"):
		self.render("index.html", zipcode=zipcode, error=error, errorID=errorID)

	def get(self):
		self.render_front()

	def post(self):
		zipcode = self.request.get("zipcode")

		if zipcode:
			# self.response.out.write('hola')
			save_one_year_data(zipcode)
			errorID = "control-group success"
			self.render_front(zipcode, errorID=errorID)
		else:
			error = "I can't find that zip code, try again"
			errorID = "control-group error"
			self.render_front(error=error, errorID=errorID)
			# self.render_front(zipcode, error)

app = webapp2.WSGIApplication([('/', MainPage)], debug=True)
