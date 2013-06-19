

import time, sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), 'geopy'))

import crepyscule_tools
from geopy import geocoders
from geopy.geocoders import google_timezone
# from pyzipcode import ZipCodeDatabase

sFilename = 'data.csv'

# Define day in year of result
t = time.strptime("6 Jun 2012", "%d %b %Y")   
ctime = time.mktime(t)

# Find Lat Lon for given zip code
g = geocoders.GoogleV3()
locations = g.geocode("Moscow", exactly_one=False)
place = locations[0][0]
fLat = locations[0][1][0]
fLon = locations[0][1][1]
print "First location found: %s: %.5f, %.5f" % (place, fLat, fLon)

g2 = google_timezone.GoogleTimezone()
fUTC = g2.geocode(fLat,fLon)/(60**2) # From seconds to hours
sDLS = 'US'
# zcdb = ZipCodeDatabase()
# zipcode = zcdb[60202]
# fLon = zipcode.longitude
# fLat = zipcode.latitude
# fUTC = zipcode.timezone

(lSunrise, lSunset, lSunAltitude, tToday) = \
    crepyscule_tools.get_one_year_data(fLat, fLon, ctime, fUTC, sDLS)

lDaylength = crepyscule_tools.get_daylength(ctime, fLat, fLon)
lDateISO8601 = crepyscule_tools.get_one_year_of_iso8601(ctime)

lLines = crepyscule_tools.get_sunrise_sunset_as_csv(lDateISO8601, lSunrise,\
                                        lSunset, lDaylength,\
                                        fLat, fLon, fUTC, sDLS)
                                                 
crepyscule_tools.save_info_flat_file(sFilename, lDateISO8601,\
                                    lSunrise, lSunset, lDaylength,\
                                    fLat, fLon, fUTC, sDLS)


#lSunriseSunset = crepyscule.get_sunrise_sunset_as_csv(ctime, 
#                                                      fLat, fLon, 
#                                                      sSummerTime1="US")

# CSV to JSON
import csv  
import json  
from google.appengine.ext import db
  
# Open the CSV  
#f = open( sFilename, 'rU' )  
# Change each fieldname to the appropriate field name. I know, so difficult.  
#reader = csv.DictReader( f, fieldnames = ( "date","sunrise","sunset", "daylength" ))  
reader = csv.DictReader(lLines)
# Parse the CSV into JSON  
JSONout = json.dumps( [ row for row in reader ] )  
print "JSON parsed!"  
# Save the JSON  
f = open( 'data.json', 'w')  
f.write(JSONout)  
print "JSON saved!"  




class SunsetSunrise(db.Model):
    jsonText = db.TextProperty()
        
sunset = SunsetSunrise(jsonText = JSONout)
sunset.put()

def getall():
    all = db.GqlQuery("SELECT * FROM SunsetSunrise")
    for x in all:
        print x.jsonText
        
        
class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj, 'isoformat'): #handles both date and datetime objects
            return obj.isoformat()
        else:
            return json.JSONEncoder.default(self, obj)

class BaseResource(webapp2.RequestHandler):
    def to_json(self, gql_object):
        result = []
        for item in gql_object:
            result.append(dict([(p, getattr(item, p)) for p in item.properties()]))
        return json.dumps(result, cls=JSONEncoder)
        