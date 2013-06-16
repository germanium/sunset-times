# -*- coding: utf-8 -*-
"""
Created on Thu Jun  6 21:50:10 2013

@author: gp
"""

#import crepyscule
import crepyscule_tools
import time 
from pyzipcode import ZipCodeDatabase

sFilename = 'data.csv'

# Define day in year of result
t = time.strptime("6 Jun 2012", "%d %b %Y")   
ctime = time.mktime(t)

# Find Lat Lon for given zip code
zcdb = ZipCodeDatabase()
zipcode = zcdb[60202]
fLon = zipcode.longitude
fLat = zipcode.latitude
fUTC = zipcode.timezone

sDLS = 'US'
# Find zip for given city
zipcode = zcdb.find_zip(city="Evanston")

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