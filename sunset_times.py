import os, sys, time, csv, json
import webapp2
import jinja2

sys.path.append(os.path.join(os.path.dirname(__file__), 'scripts'))
from scripts import crepyscule_tools
from scripts.geopy import geocoders
from scripts.geopy.geocoders import google_timezone


template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
								autoescape = True)

def getOneYearData(location):
	""" If location is found returns one year of JSON data, else returns None  """

	# Define day in year of result
	t = time.strptime("6 Jun 2014", "%d %b %Y")   
	ctime = time.mktime(t)

	# Find Lat Lon for given zip code
	g = geocoders.GoogleV3()
	try:
		locations = g.geocode(location)
		# place, (fLat, fLon) = g.geocode(location, exactly_one=False)
	except:
		return (None, None)
	
	# Get the first result. I can improve it to display all results					
	place = locations[0]
	fLat = locations[1][0]
	fLon = locations[1][1]

	g2 = google_timezone.GoogleTimezone()
	fUTC = g2.geocode(fLat, fLon)/(60**2)
	sDLS = '' #US'

	(lSunrise, lSunset, lSunAltitude, tToday) = \
    	crepyscule_tools.get_one_year_data(fLat, fLon, ctime, fUTC, sDLS)

	lDaylength = crepyscule_tools.get_daylength(ctime, fLat, fLon)
	lDateISO8601 = crepyscule_tools.get_one_year_of_iso8601(ctime)
                                                 
	lLines = crepyscule_tools.get_sunrise_sunset_as_csv(lDateISO8601, lSunrise,\
                                        lSunset, lDaylength,\
                                        fLat, fLon, fUTC, sDLS)

	reader = csv.DictReader(lLines)
	# Parse the CSV into JSON  
	JSONout = json.dumps( [ row for row in reader ] )
	return (JSONout, place)


class Handler(webapp2.RequestHandler):
	def write(self, *a, **kw):
		self.response.out.write(*a, **kw)

	def render_str(self, template, **params):
		t = jinja_env.get_template(template)
		return t.render(params)

	def render(self, template, **kw):
		self.write(self.render_str(template, **kw))


class MainPage(Handler):
	def render_front(self, location="", msg="", errorID="control-group", JSONdata=""):
		self.render("index.html", location=location, msg=msg, errorID=errorID, 
					JSONdata=JSONdata)

	def get(self):
		self.render_front()

	def post(self):
		location = self.request.get("location")
		JSONdata, place = getOneYearData(location)

		if JSONdata:
			errorID = "control-group success"
			self.render_front(location, place, errorID, JSONdata)
		else:
			msg= "I can't find that location. API might be down, try again later"
			errorID = "control-group error"
			self.render_front(location=location, msg=msg, errorID=errorID)

app = webapp2.WSGIApplication([('/', MainPage)], debug=True)


