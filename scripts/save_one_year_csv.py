

import time, sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), 'geopy', 'geocoders'))

import crepyscule_tools
from geopy import geocoders
import google_timezone
# from pyzipcode import ZipCodeDatabase

sFilename = 'data.csv'

# Define day in year of result
t = time.strptime("6 Jun 2012", "%d %b %Y")   
ctime = time.mktime(t)

# Find Lat Lon for given zip code
g = geocoders.GoogleV3()
place, (fLat, fLon) = g.geocode("750 Hinman Ave, Evanston")
print "%s: %.5f, %.5f" % (place, fLat, fLon)
g2 = google_timezone.GoogleTimezone()
fUTC = g2.geocode(fLat,fLon)/(60**2)
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
                                                 
crepyscule_tools.save_info_flat_file(sFilename, lDateISO8601,\
                                    lSunrise, lSunset, lDaylength,\
                                    fLat, fLon, fUTC, sDLS)


#lSunriseSunset = crepyscule.get_sunrise_sunset_as_csv(ctime, 
#                                                      fLat, fLon, 
#                                                      sSummerTime1="US")