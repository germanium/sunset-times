#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-

# Copyright 2005,2008  Miguel Tremblay

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program; if not see  <http://www.gnu.org/licenses/>.
############################################################################

"""
Usefull methods regarding time, sun, math, strings and CSV format
for crepyscule module.

Project home page is U{http://ptaff.ca/crepyscule/}
              
 - Name:        crepyscule_tools.py
 - Author:      U{Miguel Tremblay<http://ptaff.ca/miguel/>}
 - Date:        February 20th  2005

"""
import os
import sys
import time
import string
import calendar

import math
import Sun
import numpy

import crepyscule_summer_time

# Set the place where to fetch languages dependant messages
# import gettext
# t = gettext.translation('crepyscule_tools', sys.path[0] + '/locale')



HALF_YEAR = 365.24/2
OBLIQUITY_OF_ECLIPTIC = 23.439

#######################################################################
# Time methods

def ctime_to_iso8601(ctime):
    """
    Convert a ctime value in iso8601.

    @type ctime: float
    @param ctime: ctime value to be converted in iso8601

    @rtype: string
    @return: iso9601 date in the format YYYY-MM-DDTHH:mm:ssZ.
     See L{get_iso_8601}
    """
    # lDate is in the format (2005, 3, 29, 18, 42, 28, 1, 88, 0)
    (nYear, nMonth, nDay, nHour, nMinute, nSecond, nWeekDay, nJulian, bDst) =\
            time.gmtime(ctime)

    sIso8601 = get_iso_8601(nYear, nMonth, nDay, nHour, nMinute, nSecond)
    return sIso8601
    

def get_iso_8601(nYear, nMonth, nDay, nHour=0, nMinute=0, nSecond=0):
    """
    Convert numbers of date in the iso 8601 format.
    We assume UTC time zone.

    @type nYear: int
    @param nYear: year for this date
    @type nMonth: int
    @param nMonth: month for this date
    @type nDay: int
    @param nDay: day for this date
    @type nHour: int
    @param nHour: hour for this date
    @type nMinute: int
    @param nMinute: minute for this date
    @type nSecond: int
    @param nSecond: second for this date

    @rtype: string
    @return: iso9601 date in the format YYYY-MM-DDTHH:mm:ssZ.
    """

    sYear = str_to_at_least_two_digits(nYear)
    sMonth = str_to_at_least_two_digits(nMonth)
    sDay = str_to_at_least_two_digits(nDay)

    if (nHour == nMinute == nSecond == 0):
        sIso = sYear + '-' + sMonth + '-' + sDay
    else:
        sHour = str_to_at_least_two_digits(nHour)
        sMinute = str_to_at_least_two_digits(nMinute)
        sSecond = str_to_at_least_two_digits(nSecond)
        sIso = sYear + '-' + sMonth + '-' + sDay+ 'T' +\
           sHour + ':' + sMinute + ':' + sSecond + 'Z'

    return sIso

def tranform_decimal_hour_in_minutes(fTimeHour, sRound=''):
    """
    Description: Return an array containing the hour,
    the minutes and the secondes, respectively.
                 
    @type fTimeHour: float
    @param fTimeHour:  Time in decimal form. Eg 1.90 for 1h54:00

    @type sRound: string
    @param sRound: Round the result to the minutes (seconds =0)
                   or hours (seconds =0, minutes=0).
                   Must be in ['minute', 'hour'],

    @rtype: tuple
    @return: (nHour, nMinute, nSecond)
    """
    
    lRound = ['minute', 'hours', '']

    if sRound not in lRound:
        sSUNRISE_SUNSET_ERRORS = "Cannot round time to %s" % ((sRound))
        raise sSUNRISE_SUNSET_ERRORS
    
    # Extract decimal from integer part
    tModHour = math.modf(fTimeHour)
    nHour = int(tModHour[1])
    fDecimalHour = tModHour[0]
    # Transform decimal in minutes
    fMinute = fDecimalHour*60
    # Again, extract the decimal and the integer part
    tModMinute = math.modf(fMinute)
    nMinute = int(tModMinute[1])
    fDecimalMinute = tModMinute[0]
    # Transform decimal in seconds
    fSecond = fDecimalMinute*60    
    # Again, extract the decimal and the integer part
    tModSecond = math.modf(fSecond)
    nSecond = int(tModSecond[1])

    # Check if we are rounding.
    if sRound == 'minute':
        if  tModSecond[1] > 30:
            if nMinute == 59:
                nMinute = 0
                nHour = nHour + 1
            else:
                nMinute = nMinute + 1
        nSecond = 0
    elif sRound == 'hour':
        if tModMinute[1] > 30:
            nHour = nHour + 1
        nMinute = 0
        nSecond = 0

    sHour = str_to_at_least_two_digits(nHour)
    sMinute = str_to_at_least_two_digits(nMinute)
    sSecond = str_to_at_least_two_digits(nSecond)
    
    return (sHour, sMinute, sSecond)

def get_one_year_of_iso8601(ctime):
    """
    Return a list containing all the dates to the year
    corresponding to the ctime in in iso8601 format.

    @type ctime: float
    @param ctime: Any ctime in the year of the result.

    @rtype: list
    @return: List with all the dates for one year.
    """
    lDateISO8601 = []
    
    lMonth = range(1,13) 
    tToday = time.gmtime(ctime)
    nYear = tToday[0]

    for nMonth in lMonth:
        # Get a list of the number of days in each month
        lrange = calendar.monthrange(nYear, nMonth)
        lDay = range(1,lrange[1]+1)
        for nDay in lDay:
            sDay = get_iso_8601(nYear, nMonth, nDay)
            lDateISO8601.append(sDay)

    return lDateISO8601

def get_yesterday(nYear, nMonth, nDay):
    """
    Given a tuple containing (nYear, nMonth, nDay), remove one day
    and returns the tuple.

    @type nYear: int
    @param nYear: year for this date
    @type nMonth: int
    @param nMonth: month for this date
    @type nDay: int
    @param nDay: day for this date

    @rtype: tuple
    @return: (nYear, nMonth, nDay-1)
    """

    # Create a ctime
    ctime = time.mktime((nYear, nMonth, nDay,0,0,0,0,0,0))

    # Remove the rigth number of seconds
    ctimeYesterday = ctime - 24*3600

    # Convert back a again
    (nYear, nMonth, nDay, nHour, nMinute, nSecond, nWeekDay, nJulian, bDst) =\
             time.gmtime(ctimeYesterday)

    return (nYear, nMonth, nDay)

########################################################################
# Sun methods

def get_one_year_data(fLat, fLon, ctime, fUTC, sTimezone):
    """
    Generate the information (sunset, sunrise, altitude) for one year.

    @type  fLat: float
    @param fLat: Latitude in decimal.
    @type  fLon: float
    @param fLon: Longitude in decimal. West longitude are negative
      East longitude are positive.
    @type ctime: float
    @param ctime: Any ctime in the year of the result.
    @type fUTC: float
    @param fUTC: Time to add/substract for each time values. Usually used
     for UTC value of place.
    @type sTimezone: string
    @param sTimezone: This variable is a 2 letters code indicating
     when is the daylight saving time (DST) starting and ending in the year
     for the first place.

    @rtype: tuple 
    @return: (lSunrise, lSunset, lSunAltitude, tToday)

    """
    lMonth = range(1,13) 
    tToday = time.gmtime(ctime)
    nYear = tToday[0]

    # Create list to record sunset and sunrise
    lSunset = []
    lSunrise = []
    # List for sun max altitude
    lSunAltitude = []

    for nMonth in lMonth:
        # Get a list of the number of days in each month
        lrange = calendar.monthrange(nYear, nMonth)
        lDay = range(1,lrange[1]+1)
        for nDay in lDay:
            tCurrentDay = (nYear, nMonth, nDay)
            # Sun altitude
            fAltitude = get_one_value("altitude", fLat, fLon, tCurrentDay, fUTC)
            lSunAltitude.append(fAltitude)
            # Sunrise and sunset
            fSunriseTime = get_one_value("sunrise", fLat, fLon, tCurrentDay,\
                                         fUTC, sTimezone)
            fSunsetTime = get_one_value("sunset", fLat, fLon, tCurrentDay,\
                                        fUTC, sTimezone)
            lSunrise.append(fSunriseTime)
            lSunset.append(fSunsetTime)

    return (lSunrise, lSunset, lSunAltitude, tToday)

def check_value_over_24(lSunset):
    """
    Check the value of sunset to see if there is some values over 24.

    @type lSunset: list
    @param lSunset: list containing all the value of sunset.

    @rtype: tuple
    @return: (nStart, nEnd) where nStart is the value where the
     curve goes over 24 and nEnd is the value where the curve goes
     under 24.
    """
    TWENTY_FOUR = 24
    nStart = 0
    nEnd = len(lSunset)-1

    npSunset = numpy.array(lSunset)
    # No value over 24
    if npSunset.max() < TWENTY_FOUR:
        return (nStart, nEnd)
    # if all the value are > 24, there is a funny who have entered an
    #  impossible UTC for this longitude. Curve wont be on the graph,
    #  too bad for him.
    elif  npSunset.min() > TWENTY_FOUR:
        return (nStart, nEnd)
    else:
        # Get the last indice of value over 24
        for i in range(0,len(npSunset)-1):
            if npSunset[i] > TWENTY_FOUR and  npSunset[i+1] < TWENTY_FOUR :
                nEnd = i + 1
                break
        # Get the first indice of value over 24
        for i in range(len(npSunset)-1, 0, -1):
            if npSunset[i] > TWENTY_FOUR and npSunset[i-1]< TWENTY_FOUR :
                nStart = i
                break

    return (nStart, nEnd)


def check_value_under_0(lSunrise):
    """
    Check the value of sunset to see if there is some values over 24.
    
    @type lSunrise: list
    @param lSunrise: list containing all the value of sunset.

    @rtype: tuple
    @return: (nStart, nEnd) where nStart is the value where the
     curve goes under 0 and nEnd is the value where the curve goes
     over 0.
    """
    ZERO = 0
    npSunrise = numpy.array(lSunrise)
    # if all the value are < 0, there is a funny who have entered an
    #  impossible UTC for this longitude. Curve wont be on the graph,
    #  too bad for him.
    if npSunrise.min() > ZERO or npSunrise.max() < ZERO:
        nStart = 0
        nEnd = len(npSunrise)-1
    else:
        # Get the last indice of value under 0
        for i in range(0,len(npSunrise)-1):
            if npSunrise[i] < ZERO  and npSunrise[i+1] > ZERO:
                nEnd = i
                break
        # Get the first indice of value under 0
        for i in range(len(npSunrise)-1,0,-1):
            if npSunrise[i] < ZERO and npSunrise[i-1] > ZERO:
                nStart = i
                break

    return (nStart, nEnd)


def correct_sun_bugs(lSunrise, lSunset):
    """
    Correct some bugs related to time of Sun file.

    @type lSunrise: list
    @param lSunrise: list containing the sunrise value
    @type lSunset: list
    @param lSunset: list containing the sunset value

    @rtype: tuple
    @return: tuple containing the corrected value (npSunrise, npSunset),
    """
    npSunrise = numpy.array(lSunrise)
    npSunset = numpy.array(lSunset)

    # Identify segment above 24
    # Remove value under 0 before, because it can have
    #  some strange behaviour from Sun.py
    npSunset = numpy.where(npSunset < npSunset.mean()-10,\
                              npSunset+24, npSunset)
    npSunset = numpy.where(npSunset > 24, npSunset-24, npSunset)
    # Identify segment under 0
    npSunrise = numpy.where(npSunrise > 24, npSunrise - 24, npSunrise)
    npSunrise = numpy.where(npSunrise < 0, npSunrise + 24, npSunrise)

    return (npSunrise, npSunset)

def get_one_year_max_sf(nYear, fLat):
    """
    Get the solar flux for a whole year.

    @type nYear: int
    @param nYear: Year for which to get the solar flux.
    @type  fLat: float
    @param fLat: Latitude in decimal for the place.

    @rtype: list
    @return: List of the daily maximal solar fluxes.
    """
    
    cSun = Sun.Sun()
    lFlux = []

    # Get the max number of days for each month of this year
    for nMonth in range(1,13):
        nNumberDaysInMonth = calendar.monthrange(nYear, nMonth)[1]
        for nDay in range(1, nNumberDaysInMonth+1):
            fFlux = cSun.get_max_solar_flux(fLat, nYear, nMonth, nDay)
            lFlux.append(fFlux)

    return lFlux


def is_summer_time(nJulianDay, nYear, sSummerTime):
    """
    Is this julian day during summer time?

    @type nJulianDay: int
    @param nJulianDay: Julian day, january 1st is '1', last day of year is
     '365' in a non-bisextil year.
    @type  nYear: int
    @param nYear: Year in which the julian day belongs
    @type  sSummerTime: string
    @param sSummerTime: This variable is a 2 letters code indicating
    when is the daylight saving time (DST) starting and ending in the year
    for the first place.

    @rtype: bool
    @return: True if the Julian day is during summertime, False otherwise.
    """
    # If no summer time is define, we are never in summer time
    if sSummerTime == '' or  sSummerTime == '--':
        return False
    
    (nFirstDay, nLastDay) = crepyscule_summer_time.\
                            get_summer_time_days(sSummerTime, nYear)

    if nJulianDay < nFirstDay or nJulianDay > nLastDay:
        return False
    else:
        return True
    

def get_daylight_variation(lDaylightInOneDay):
    """
    Compute the time gained or lost for each day.

    @type lDaylightInOneDay: list
    @param lDaylightInOneDay: Contains the length of day, i.e. sunset-sunrise.

    @rtype: list
    @return: Result in a list in minutes.
    """
    # Compute the differences
    lDiffSunTime = []
    for i in range(len(lDaylightInOneDay)):
        fTimeMinute = (lDaylightInOneDay[i]-lDaylightInOneDay[i-1])*60
        lDiffSunTime.append(fTimeMinute)

    return lDiffSunTime

def get_dictionary(sValue, fLat, fLon, ctime, fUTC=None, sSummerTime=""):
    """
    Compute the values indicated by sValue and return a dictionnary with
    the date in iso8601 as keys.

    @type sValue: string
    @param sValue: Any string in lPossibleValues
    @type  fLat: float
    @param fLat: latitude of the first place. Latitude is in decimal
      degrees. Example: 30°30'  should be 30.5
    @type  fLon: float
    @param fLon: longitude of the first place. Longitude is in decimal
      degrees. Example: 30°30'  should be 30.5. West longitude are negative
      East longitude are positive.
    @type ctime: float
    @param ctime: Any ctime in the day for the wanted value. If a graphic is
     created and there is only one place, a line is drawn with the values
     written at the intersection for this specific day.
    @type fUTC:  float
    @param fUTC: Time to add/substract for each time values for the first place.
     Usually used for UTC value of place.
    @type  sSummerTime: string
    @param sSummerTime: This variable is a 2 letters code indicating
     when is the daylight saving time (DST) starting and ending in the year
     for the first place.
     Default is no DST. For a list of DST code,
     see L{crepyscule_summer_time.lTimezone}.

    @rtype: dictionnary
    @return: Dictionnary with key in iso8601 format like 'YYYY-MM-DD' and
      the corresponding value.
    """
    lPossibleValues = ["sunrise", "sunset", "altitude", "variation", "sf", \
                       "daylength", "twilight"]
    dValues = {}

    if sValue not in lPossibleValues:
        sError = sValue + " is not a good value for get_dictionary." +\
                 "Possible values are:" + str(lPossibleValues)
        sys.stderr.write(sError)
        return None
    

    (lSunrise, lSunset, lSunAltitude, tToday) = \
               get_one_year_data(fLat, fLon, ctime, fUTC, sSummerTime)

    lDateISO8601 = get_one_year_of_iso8601(ctime)
    if sValue == "sunrise":
        lValue = lSunrise
    elif sValue == "sunset":
        lValue = lSunset
    elif sValue == "altitude":
        lValue = lSunAltitude
    elif sValue == "variation":
        lSuntime = get_daylength(ctime, fLat, fLon)
        lValue = get_daylight_variation(lSuntime)
    elif sValue == "sf":
        nYear = int(lDateISO8601[0][0:4])
        lValue = get_one_year_max_sf(nYear, fLat)
    elif sValue == "daylength":
        lValue = get_daylength(ctime, fLat, fLon)
    elif sValue == "twilight":
        lValue = get_twilight_length_year(ctime, fLat)

    for i in range(len(lDateISO8601)):
        dValues[lDateISO8601[i]] = round(lValue[i], 2)

    return dValues
        

def get_one_value(sValue, fLat, fLon, tuple_or_ctime, fUTC=0, sSummerTime=""):
    """
    Compute the value indicated by sValue and return it.

    @type sValue: string
    @param sValue: Any string in lPossibleValues
    @type  fLat: float
    @param fLat: latitude of the first place. Latitude is in decimal
     degrees. Example: 30°30'  should be 30.5
    @type  fLon: float
    @param fLon: longitude of the first place. Longitude is in decimal
     degrees. Example: 30°30'  should be 30.5. West longitude are negative
     East longitude are positive.
    @type tuple_or_ctime: tuple or float
    @param tuple_or_ctime: can be called either with a ctime value or a tuple
     with (nYear, nMonth, nDay) for the specific day.
    @type fUTC:  float
    @param fUTC: Time to add/substract for each time values for the first place.
     Usually used for UTC value of place.
    @type  sSummerTime: string
    @param sSummerTime: This variable is a 2 letters code indicating
     when is the daylight saving time (DST) starting and ending in the year
     for the first place.
     Default is no DST. For a list of DST code,
     see L{crepyscule_summer_time.lTimezone}.

    @rtype: float
    @return: Value corresponding to the date and the key
    """
    lPossibleValues = ["sunrise", "sunset", "altitude", "variation", "sf"]
    cSun = Sun.Sun()
    fValue = None

    # Get time values
    if type(tuple_or_ctime) == type(()):
        (nYear, nMonth, nDay) = tuple_or_ctime
    else: # Not a tuple but a ctime
        (nYear, nMonth, nDay, nHour, nMinute, nSecond, nWeekDay, nJulian, bDst) =\
                time.gmtime(tuple_or_ctime)
    tDay = (nYear, nMonth, nDay)
   

    if sValue == "sunrise":
        fValue = cSun.sunRiseSet(nYear, nMonth, nDay, fLon, fLat)[0] + fUTC
        fValue = crepyscule_summer_time.\
                 adjust_summer_time_one_day(tDay, fValue, sSummerTime)
        if fValue < 0:
            fValue = fValue + 24
        elif fValue > 24:
            fValue = fValue - 24
    elif sValue == "sunset":
        fValue = cSun.sunRiseSet(nYear, nMonth, nDay, fLon, fLat)[1] + fUTC
        fValue = crepyscule_summer_time.\
                 adjust_summer_time_one_day(tDay, fValue, sSummerTime)
        if fValue < 0:
            fValue = fValue + 24
        elif fValue > 24:
            fValue = fValue - 24
    elif sValue == "altitude":
        fValue = cSun.solar_altitude(fLat, nYear, nMonth, nDay)
    elif sValue == "variation":
        # Get value sunrise & sunset for today
        fSunrise2 = get_one_value("sunrise", fLat, fLon, \
                                  tDay, fUTC, sSummerTime)
        fSunset2 = get_one_value("sunset", fLat, fLon, \
                                 tDay, fUTC, sSummerTime)
        fDay2 = fSunset2 - fSunrise2
        # Get sunrise & sunset for yesteray
        tYesterday = get_yesterday(tDay[0], tDay[1], tDay[2])
        fSunrise1 = get_one_value("sunrise", fLat, fLon, \
                                  tYesterday, fUTC, sSummerTime)
        fSunset1 = get_one_value("sunset", fLat, fLon, \
                                 tYesterday, fUTC, sSummerTime)
        fDay1 =  fSunset1 - fSunrise1
        fValue = (fDay2 - fDay1)*60

    return fValue


########################################################################
# String methods

def str_to_at_least_two_digits(nNumber):
    """
    Take an int and return '01' instead of '1'.

    @type nNumber: int
    @param nNumber: Number to return with at least 2 digits.

    @rtype: string
    @return: a string with 2 digits.
    """
    sRes ="%02d" % nNumber
    return sRes


def remove_extension(sFilename):
    """
    Remove the extension of a string file.
    Extension is defined as the letters after the right most '.'

    @type sFilename: string
    @param sFilename: The filename from which the extension must be removed.

    @rtype: string
    @return: A string with the filename without the extension.
    """
    # Remove the extension
    nIndice = sFilename.rfind('.')
    if nIndice < 0:
        sFilenameShort = sFilename
    else:
        sFilenameShort = sFilename[:sFilename.rfind('.')]

    return sFilenameShort

def save_info_flat_file(sFilename, lDateISO8601, \
                        lSunrise1, lSunset1, lDaylength1, fLat1, fLon1, fUTC1,\
                        sSummerTime1, lSunrise2=None, lSunset2=None, \
                        lDaylength2=None, fLat2=None, \
                        fLon2=None,fUTC2=None, sSummerTime2=None):
    """
    Simply call L{get_sunrise_sunset_as_csv} and save it into a text file.

    @type sFilename: string
    @param sFilename: Filename for the text file to be written.

    For other params, see L{get_sunrise_sunset_as_csv}
    """

    lLines = get_sunrise_sunset_as_csv(lDateISO8601, lSunrise1, lSunset1,\
                                       lDaylength1,\
                                       fLat1, fLon1, fUTC1, sSummerTime1,\
                                       lSunrise2, lSunset2, lDaylength2,
                                       fLat2, fLon2,\
                                       fUTC2, sSummerTime2)

    # Use file or stdout
    if sFilename is not None:
        sFilenameFlatFile =  remove_extension(sFilename) + '.csv'
        file_txt = open(sFilenameFlatFile, 'w')             
        file_txt.writelines(x+'\n' for x in lLines)
        file_txt.close()
        print "filename", sFilenameFlatFile
    else:
        for i in range(len(lLines)):
            printlLines[i].strip()
                
##########################################################################
# CSV format

def get_sunrise_sunset_as_csv(lDateISO8601, \
                              lSunrise1, lSunset1, lDaylength1, fLat1, fLon1,\
                              fUTC1, \
                              sSummerTime1,\
                              lSunrise2=None, lSunset2=None, lDaylength2=None,\
                              fLat2=None, fLon2=None,\
                              fUTC2=None, sSummerTime2=None):
    """
    Returns a list containing the date, sunrise, sunset, daylength,
    like the CSV file.
    header (first element): year place1 lat1 lon1 UTC1 summer_time_code1
    (optional)  place2 lat2 lon2 UTC2 summer_time_code2
    data: date, sunrise1, sunset1, (optional) sunrise2, sunset2

    @type  lDateISO8601: list
    @param lDateISO8601: List of strings for one year in iso8601 format.
    @type lSunrise1: list
    @param lSunrise1: list containing the values of sunrise for the first place.
    @type lSunset1: list
    @param lSunset1: list containing the values of sunset for the first place.
    @type lDaylength1: list
    @param lDaylength1: list containing the values of daylight in
     hours for the first place
    @type  fLat1: float
    @param fLat1: latitude of the first place. Latitude is in decimal
      degrees. Example: 30°30'  should be 30.5
    @type  fLon1: float
    @param fLon1: longitude of the first place. Longitude is in decimal
      degrees. Example: 30°30'  should be 30.5. West longitude are negative
      East longitude are positive.
    @type fUTC1:  float
    @param fUTC1: Time to add/substract for each time values for the first place.
     Usually used for UTC value of place.
    @type  sSummerTime1: string
    @param sSummerTime1: This variable is a 2 letters code indicating
     when is the daylight saving time (DST) starting and ending in the year
     for the first place.
     Default is no DST. For a list of DST code,
     see L{crepyscule_summer_time.lTimezone}.
    @type lSunrise2: list
    @param lSunrise2: list containing the values of sunrise for the first place.
    @type lSunset2: list
    @param lSunset2: list containing the values of sunset for the first place.
    @type lDaylength2: list
    @param lDaylength2: list containing the values of daylight in
     hours for the second place
    @type  fLat2: float
    @param fLat2: latitude of the second place. See fLat1.
    @type  fLon2: float
    @param fLon2: longitude of the second place. See fLon1.
    @type  sSummerTime2: string
    @param sSummerTime2: This variable is a 2 letters code indicating
     when is the daylight saving time (DST) starting and ending in the year
     for the seconde place.
     Default is no DST. For a list of DST code,
     see L{crepyscule_summer_time.lTimezone}.
    @type fUTC2:  float
    @param fUTC2: Time to add/substract for each time values for the second
     place.

    @rtype: list
    @return: A list containing the sunrise/sunset/length CSV values.
     One line per element of list.
    """
    lDateSunriseSunset = []
    # Write the header: "Date", "Sunrise for XX.xxN YY.yyW UTC code",
    # "Sunset for XX.xxN YY.yyW UTC code"
    sDate = "Date"
    sSunriseHeader = "Sunrise"
    sSunsetHeader = "Sunset"
    sDaylengthHeader = "Daylength"
   
    sHeader = string.join((sDate, sSunriseHeader, sSunsetHeader, \
                           sDaylengthHeader), sep=',')
    if lSunrise2 != None:
        sSunriseHeader = "Sunrise"
        sSunsetHeader = "Sunset"
        sDaylengthHeader = "Daylength"

        sHeader = string.join((sHeader, sSunriseHeader, sSunsetHeader,\
                               sDaylengthHeader), sep=',')

    lDateSunriseSunset.append(sHeader)

    # Body
    lListOfSunsetSunrise =  [lSunrise1, lSunset1, lDaylength1]
    if lSunrise2 != None:
        lListOfSunsetSunrise =  lListOfSunsetSunrise + \
                               [lSunrise2, lSunset2, lDaylength2 ]

    for i in range(len(lSunrise1)):
        sDate = lDateISO8601[i][:10]
        sLine = sDate
        for lList in lListOfSunsetSunrise:
            (nHour, nMinute, nSecond) = tranform_decimal_hour_in_minutes(\
                                        lList[i], 'minute')
            sTime = str(nHour) + ':' + str(nMinute)
            sLine = string.join((sLine, sTime), sep=',')
        lDateSunriseSunset.append(sLine)

    return lDateSunriseSunset
                
def get_sun_altitude_as_csv(lDateISO8601, fLat1, lAltitude1,\
                             fLat2=None, lAltitude2=None):
    """
    Returns a list containing the date, sun altitude like the CSV file.
    header (first element): year place1 lat1 place2 lat2 
    data: date, sun_altitude1 (optional), sun_altitude2

    @type  lDateISO8601: list
    @param lDateISO8601: List of strings for one year in iso8601 format.
    @type  fLat1: float
    @param fLat1: latitude of the first place. Latitude is in decimal
    @type lAltitude1: list
    @param lAltitude1: list containing the values of sun altitude
     for the first place.
    @type  fLat2: float
    @param fLat2: latitude of the second place. See fLat1.
    @type lAltitude2: list
    @param lAltitude2: list containing the values of sun altitude
     for the second place.

    @rtype: list
    @return: A list containing the altitude values in the CSV format.
     One line per element of list.
    """

    lDateAltitude = []
    # Write the header: "Date", "Sun altitude for XX.xxN",
    sDate = "Date"
    sHeader = string.join(('"Sun altitude for', str(fLat1) + '"'))
    sHeader = string.join((sDate, sHeader), sep=',')
    if lAltitude2 != None:
        sHeader2 = string.join(('"Sun altitude for', str(fLat2) + '"'))
        sHeader = string.join((sHeader, sHeader2), sep=',')

    lDateAltitude.append(sHeader)

    # Body 
    if lAltitude2 != None:
        lListOfAltitude =  [lAltitude1, lAltitude2]
    else:
        lListOfAltitude =  [lAltitude1]

    for i in range(len(lAltitude1)):
        sDate = lDateISO8601[i][:10]
        sLine = sDate
        for lList in lListOfAltitude:
            sAltitude = str(round(lList[i],2))
            sLine = string.join((sLine, sAltitude), sep=',')
        lDateAltitude.append(sLine)

    return lDateAltitude

def get_daylight_variation_as_csv(lDateISO8601, lDaylength1, fLat1, \
                                   lDaylength2=None, fLat2=None):
    """
    Returns a list containing the date and the daylight variation in minutes.
    header (first element): year place1 lat1 place2 lat2 


    @type  lDateISO8601: list
    @param lDateISO8601: List of strings for one year in iso8601 format.
    @type lDaylength1: list
    @param lDaylength1: list containing the values of daylight in
     hours for the first place
    @type  fLat1: float
    @param fLat1: latitude of the first place. Latitude is in decimal
    @type lDaylength2: list
    @param lDaylength2: list containing the values of daylight in
     hours for the second place
    @type  fLat2: float
    @param fLat2: latitude of the second place. See fLat1.

    @rtype: list
    @return: A list containing the daylight variation values in the CSV format.
     One line per element of list.
    """

    lDaylightVariation= []
    # Write the header: "Date", "Daily variation for XX.xxN",
    sDate = "Date"
    sHeader = string.join(('"Daily variation of light for', str(fLat1), '"'))
    sHeader = string.join((sDate, sHeader), sep=',')
    lVariation1 = get_daylight_variation(lDaylength1)
    if lDaylength2 != None:
        sHeader2 = string.join(('"Daily variation of light for', str(fLat2)\
                                , '"'))
        sHeader = string.join((sHeader, sHeader2), sep=',')
        lVariation2 = get_daylight_variation(lDaylength2)
        
    lDaylightVariation.append(sHeader)

    # Body 
    if lDaylength2 != None:
        lListOfVariation =  [lVariation1, lVariation2]
    else:
        lListOfVariation =  [lVariation1]

    for i in range(len(lVariation1)):
        sDate = lDateISO8601[i][:10]
        sLine = sDate
        for lList in lListOfVariation:
            sVariation = str(round(lList[i],2))
            sLine = string.join((sLine, sVariation), sep=',')
        lDaylightVariation.append(sLine)

    return lDaylightVariation


def get_solar_flux_as_csv(lDateISO8601, fLat1, lFlux1,\
                             fLat2=None, lFlux2=None):
    """
    Returns a list containing the date, maximal solar flux for each day.
    header (first element): year place1 lat1 place2 lat2 
    data: date, max_solar_flux1 (optional), max_solar_flux2
    
    @type  lDateISO8601: list
    @param lDateISO8601: List of strings for one year in iso8601 format.
    @type  fLat1: float
    @param fLat1: latitude of the first place. Latitude is in decimal
    @type lFlux1: list
    @param lFlux1: list containing the values of maximal solar fluxes
     for the first place.
    @type  fLat2: float
    @param fLat2: latitude of the second place. See fLat1.
    @type lFlux2: list
    @param lFlux2: list containing the values of maximal solar fluxes
     for the second place

    @rtype: list
    @return: A list containing the daily maximal solar fluxes in the CSV format.
     One line per element of list.
    """

    lDateFlux = []
    # Write the header: "Date", "Sun altitude for XX.xxN",
    sDate = "Date"
    sHeader = string.join(('"Daily maximal solar flux for', str(fLat1) + '"'))
    sHeader = string.join((sDate, sHeader), sep=',')
    if lFlux2 != None:
        sHeader2 = string.join(('"Daily maximal solar flux for', str(fLat2) +\
                                '"'))
        sHeader = string.join((sHeader, sHeader2), sep=',')

    lDateFlux.append(sHeader)

    # Body 
    if lFlux2 != None:
        lListOfFlux =  [lFlux1, lFlux2]
    else:
        lListOfFlux =  [lFlux1]

    for i in range(len(lFlux1)):
        sDate = lDateISO8601[i][:10]
        sLine = sDate
        for lList in lListOfFlux:
            sFlux = str(round(lList[i],2))
            sLine = string.join((sLine, sFlux), sep=',')
        lDateFlux.append(sLine)

    return lDateFlux

def get_twilight_length_as_csv(lDateISO8601, fLat1, lLength1,\
                             fLat2=None, lLength2=None):
    """
    Returns a list containing the date, twilight length in minute for each day.
    header (first element): year place1 lat1 place2 lat2 
    data: date, twilight_length1, twilight_length2 (optional)
    
    @type  lDateISO8601: list
    @param lDateISO8601: List of strings for one year in iso8601 format.
    @type  fLat1: float
    @param fLat1: latitude of the first place. Latitude is in decimal
    @type lLength1: list
    @param lLength1: list containing the twilight length for the first place.
    @type  fLat2: float
    @param fLat2: latitude of the second place. See fLat1.
    @type lLength2: list
    @param lLength2: list containing the twilitght for the second place

    @rtype: list
    @return: A list containing the twilight in the CSV format.
     One line per element of list.
    """

    lDateTwilightLength = []
    # Write the header: "Date", "Sun altitude for XX.xxN",
    sDate = "Date"
    sHeader = string.join(('"Twilight length for', str(fLat1) + '"'))
    sHeader = string.join((sDate, sHeader), sep=',')
    if lLength2 != None:
        sHeader2 = string.join(('"Twilight length for', str(fLat2) +\
                                '"'))
        sHeader = string.join((sHeader, sHeader2), sep=',')

    lDateTwilightLength.append(sHeader)

    # Body 
    if lLength2 != None:
        lListOfLength =  [lLength1, lLength2]
    else:
        lListOfLength =  [lLength1]

    for i in range(len(lLength1)):
        sDate = lDateISO8601[i][:10]
        sLine = sDate
        for lList in lListOfLength:
            sLength = str(round(lList[i],4))
            sLine = string.join((sLine, sLength), sep=',')
        lDateTwilightLength.append(sLine)

    return lDateTwilightLength
    


def get_max_solar_flux(ctime, fLat):
   """
   Get the maximum solar flux value for this day.

   @type ctime: float
   @param ctime: Any ctime in the year of the result.
   @type  fLat: float
   @param fLat: Latitude in decimal for the place.

   @rtype: float
   @return: Maximum solar flux for this day in float. Solar flux is in
    watt per meter square.
   """
   
   cSun = Sun.Sun()

   (nYear, nMonth, nDay, nHour, nMinute, nSecond, nWeekDay, nJulian, bDst) = \
   time.gmtime(ctime)

   fFlux = cSun.get_max_solar_flux(fLat, nYear, nMonth, nDay)

   return fFlux

def get_daylength(ctime, fLat, fLon):
    """
    Get the daylength for all the year corresponding to this ctime.

    @type ctime: float
    @param ctime: ctime value 
    @type  fLat: float
    @param fLat: Latitude in decimal for the place.
    @type  fLon: float
    @param fLon: longitude of the first place. Longitude is in decimal
      degrees. Example: 30°30'  should be 30.5. West longitude are negative
      
    @rtype: list
    @return: List of daylength, in hour
    """
    lDaylength = []
    cSun = Sun.Sun()

    lMonth = range(1,13) 
    tToday = time.gmtime(ctime)
    nYear = tToday[0]

    for nMonth in lMonth:
        # Get a list of the number of days in each month
        lrange = calendar.monthrange(nYear, nMonth)
        lDay = range(1,lrange[1]+1)
        for nDay in lDay:
            fDaylength = cSun.dayLength(nYear, nMonth, nDay, fLon, fLat)
            lDaylength.append(fDaylength)

    return lDaylength

def get_daylength_day(ctime, fLat, fLon):
    """
    Get the daylength for the day corresponding to this ctime.

    @type ctime: float
    @param ctime: ctime value 
    @type  fLat: float
    @param fLat: Latitude in decimal for the place.
    @type  fLon: float
    @param fLon: longitude of the first place. Longitude is in decimal
      degrees. Example: 30°30'  should be 30.5. West longitude are negative
      
    @rtype: float
    @return: Daylength, in hour
    """
    cSun = Sun.Sun()

    tToday = time.gmtime(ctime)
    nYear = tToday[0]
    nMonth = tToday[1]
    nDay = tToday[2]
    fDaylength = cSun.dayLength(nYear, nMonth, nDay, fLon, fLat)

    return fDaylength


def get_twilight_length(nYear, nMonth, nDay, fLat):
    """
    Get the twilight length in minute for this day and latitude.

    @type nYear: int
    @param nYear: year for this date
    @type nMonth: int
    @param nMonth: month for this date
    @type nDay: int
    @param nDay: day for this date

    @rtype: float
    @return: Twilight length, in minute
    """
    cSun = Sun.Sun()

    fStandardDaylength = cSun.dayLength(nYear, nMonth, nDay, 0.0, fLat)
    fDaylengthWithTwilight = cSun.dayNauticalTwilightLength\
                             (nYear, nMonth, nDay, 0.0, fLat)

    # *30 is there because twilight is morning and night (/2) and that
    #  we want the result in minutes (*60). 60/2=30
    fTwilightLength = (fDaylengthWithTwilight - fStandardDaylength)*30 

    return fTwilightLength


def get_twilight_length_day(ctime, fLat):
    """
    Get the twilight length in minute for this day and latitude.

    @type ctime: float
    @param ctime: ctime value 
    @type  fLat: float
    @param fLat: Latitude in decimal for the place.

    @rtype: float
    @return: Twilight length, in minute
    """
    cSun = Sun.Sun()
    tToday = time.gmtime(ctime)
    
    nYear = tToday[0]
    nMonth = tToday[1]
    nDay = tToday[2]

    fTwilightLength = get_twilight_length(nYear, nMonth, nDay, fLat)

    return fTwilightLength
                     

def get_twilight_length_year(ctime, fLat):
    """
    Get the twilight length in minute for the year of this day and latitude.

    @type ctime: float
    @param ctime: ctime value 
    @type  fLat: float
    @param fLat: Latitude in decimal for the place.

    @rtype: list
    @return: list containing the twilight length in minute
    """
    lTwilightLength = []
    lMonth = range(1,13) 
    tToday = time.gmtime(ctime)
    nYear = tToday[0]
    
    for nMonth in lMonth:
        # Get a list of the number of days in each month
        lrange = calendar.monthrange(nYear, nMonth)
        lDay = range(1,lrange[1]+1)
        for nDay in lDay:
            fTwilightLength = get_twilight_length(nYear, nMonth, nDay, fLat)
            lTwilightLength.append(fTwilightLength)

    return lTwilightLength
                     
    
