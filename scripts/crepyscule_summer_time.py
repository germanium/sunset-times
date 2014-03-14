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
Adjust the sunset and sunrise hour depending on the timezone.
The list of timezone (lTimezone) is based on software kstars
of the kdeedu project (http://edu.kde.org/kstars/).
The original file contains informations by column like this:
city : province : country : Lat_deg : Lat_min : Lat_sec : N|S :
Lon_deg : Lon_min : Lon_sec : E|W : UTC_difference : two_letters[??]
              
Project home page is U{http://ptaff.ca/crepyscule/}

 - Name: crepyscule_summer_time.py
 - Author:      U{Miguel Tremblay<http://ptaff.ca/miguel/>}
 - Date:        January 15th  2005
        
"""          
               
import time
import calendar

import numpy

lTimezoneSouth = ('AU', 'NB', 'FK', 'PY', 'NZ', 'TS', 'BZ', 'CL', 'TG', 'ZN' )
                  
lTimezoneNorth = ( 'IR', 'JD', 'EU', 'RU', 'IQ', 'SY', 'US', 'CH', 'EG', 'MX',\
                   'SK', 'HK', 'LB' )

lTimezone = lTimezoneNorth + lTimezoneSouth

lTimezone = ('IR', 'JD', 'EU', 'IQ', 'US', 'CH', 'EG', \
               'MX', 'SK', 'HK', 'NB', 'FK', 'PY', 'NZ', \
               'TS', 'BZ', 'CL', 'AU', 'TG', 'ZN', 'LB', \
               'SY', 'RU')
dMonth = { 'JAN': 1,
           'FEB': 2,
           'MAR': 3,
           'APR': 4,
           'MAY': 5,
           'JUN': 6,
           'JUL': 7,
           'AUG': 8,
           'SEP': 9,
           'OCT': 10,
           'NOV': 11,
           'DEC': 12}
dWeek = { 'MON': 0,
          'TUE': 1,
          'WED': 2,
          'THU': 3,
          'FRI': 4,
          'SAT': 5,
          'SUN': 6 }

# Optimization. Populate this list when as summertime start,end is asked
#  for a specific year. Format is dYearSummertime{'year' : dCode} and
#  dCode is in the format dCode{ 'code' , [nStart, nEnd]}
dYearSummertime = {}

def get_summer_time_days(sSummerCode, nYear):
    """
    Return in julian day the beginning of daylight time
    and the end of daylight time.

    @type sSummerCode: string
    @param sSummerCode: summer time two letters code
    @type nYear: int
    @param nYear: Year to retrieve the dates for this summer code. Might
     have an effect in the case of 'US' since it had been change in 2007.
    @rtype: tuple
    @return: First and last julian day for this summer time code
    """
    sYear = str(nYear)

    # I know, it is not beautiful. No can do.
    if sSummerCode == 'IR':
        # Start: March 21
        nDayStart = __get_julian(sYear+'-03-21')
        # End: September 22
        nDayEnd = __get_julian(sYear+'-09-22')
    elif sSummerCode == 'JD':        
        # Start: March last Thursday
        nWeekdayStart = __get_day('last', 'THU', 'MAR', nYear)
        nDayStart = __get_julian(sYear+'-03-'+str(nWeekdayStart))
        # End:  Sep's last Thu
        nWeekdayEnd = __get_day('last', 'THU', 'SEP', nYear)
        nDayEnd = __get_julian(sYear+'-09-'+str(nWeekdayEnd))
    elif sSummerCode == 'EU'or sSummerCode == 'RU':
        # Start: March last Sunday
        nWeekdayStart = __get_day('last', 'SUN', 'MAR', nYear)
        nDayStart = __get_julian(sYear+'-03-'+str(nWeekdayStart))
        # End:  Oct's last Sunday
        nWeekdayEnd = __get_day('last', 'SUN', 'OCT', nYear)
        nDayEnd = __get_julian(sYear+'-10-'+str(nWeekdayEnd))
    elif sSummerCode == 'IQ' or sSummerCode == 'SY':
        # Start: April 1st
        nDayStart = __get_julian(sYear+'-04-01')
        # End: October 1st
        nDayEnd = __get_julian(sYear+'-10-01')
    elif sSummerCode == 'US':
        # Starting 2007, summer time has a new definition:
        if nYear < 2007:
            # Start: April 1st Sunday
            nWeekdayStart =  __get_day('first', 'SUN', 'APR', nYear)
            nDayStart = __get_julian(sYear+'-04-'+str(nWeekdayStart))
            # End:  Oct's last Sunday
            nWeekdayEnd = __get_day('last', 'SUN', 'OCT', nYear)
            nDayEnd = __get_julian(sYear+'-10-'+str(nWeekdayEnd))
        else:
            # Start: March 2nd Sunday
            nWeekdayStart =  __get_day('second', 'SUN', 'MAR', nYear)
            nDayStart = __get_julian(sYear+'-03-'+str(nWeekdayStart))
            # End:  November first Sunday
            nWeekdayEnd = __get_day('first', 'SUN', 'NOV', nYear)
            nDayEnd = __get_julian(sYear+'-11-'+str(nWeekdayEnd))
    elif sSummerCode == 'CH':
        # Start: April 2nd Sunday
        nWeekdayStart = __get_day('second', 'SUN', 'APR', nYear)
        nDayStart = __get_julian(sYear+'-04-'+str(nWeekdayStart))
        # End:  September 2nd Sunday
        nWeekdayEnd = __get_day('second', 'SUN', 'SEP', nYear)
        nDayEnd = __get_julian(sYear+'-09-'+str(nWeekdayEnd))
    elif sSummerCode == 'EG':
        # Start: April last Friday
        nWeekdayStart = __get_day('last', 'FRI', 'APR', nYear)
        nDayStart = __get_julian(sYear+'-04-'+str(nWeekdayStart))
        # End: September last Thursday
        nWeekdayEnd = __get_day('last', 'THU', 'SEP', nYear)
        nDayEnd = __get_julian(sYear+'-09-'+str(nWeekdayEnd))
    elif sSummerCode == 'MX':
        # Start: April 1st Sunday
        nWeekdayStart = __get_day('first', 'SUN', 'APR', nYear)
        nDayStart = __get_julian(sYear+'-04-'+str(nWeekdayStart))
        # End:  Sep's last Sun
        nWeekdayEnd = __get_day('last', 'SUN', 'SEP', nYear)
        nDayEnd = __get_julian(sYear+'-09-'+str(nWeekdayEnd))
    elif sSummerCode == 'SK':
        # Start: May 2nd Sunday
        nWeekdayStart = __get_day('second', 'SUN', 'MAR', nYear)
        nDayStart = __get_julian(sYear+'-05-'+str(nWeekdayStart))
        # End:  October 2nd Sunday
        nWeekdayEnd = __get_day('second', 'SUN', 'OCT', nYear)
        nDayEnd = __get_julian(sYear+'-10-'+str(nWeekdayEnd))
    elif sSummerCode == 'HK':
        # Start: May 2nd Sunday
        nWeekdayStart =  __get_day('second', 'SUN', 'MAR', nYear)
        nDayStart = __get_julian(sYear+'-05-'+str(nWeekdayStart))
        # End:  October 3rd Sunday
        nWeekdayEnd =  __get_day('third', 'SUN', 'OCT', nYear)
        nDayEnd = __get_julian(sYear+'-10-'+str(nWeekdayEnd))
    elif sSummerCode == 'NB':
        # Start: September 1st Sunday
        nWeekdayStart = __get_day('first', 'SUN', 'SEP', nYear)
        nDayStart = __get_julian(sYear+'-09-'+str(nWeekdayStart))
        # End: April 1st Sunday
        nWeekdayEnd = __get_day('first', 'SUN', 'APR', nYear)
        nDayEnd = __get_julian(sYear+'-04-'+str(nWeekdayEnd))
    elif sSummerCode == 'FK':
        # Start: September 1st Sunday
        nWeekdayStart = __get_day('first', 'SUN', 'SEP', nYear)        
        nDayStart = __get_julian(sYear+'-09-'+str(nWeekdayStart))        
        # End: April 3rd Sunday
        nWeekdayEnd = __get_day('third', 'SUN', 'APR', nYear)
        nDayEnd = __get_julian(sYear+'-04-'+str(nWeekdayEnd))
    elif sSummerCode == 'PY':
        # Start: October 1st Sunday
        nWeekdayStart = __get_day('first', 'SUN', 'OCT', nYear)        
        nDayStart = __get_julian(sYear+'-10-'+str(nWeekdayStart))
        # End: March 1st Sunday
        nWeekdayEnd = __get_day('first', 'SUN', 'MAR', nYear)
        nDayEnd = __get_julian(sYear+'-03-'+str(nWeekdayEnd))
    elif sSummerCode == 'NZ':
        # Starting 2007, summer time has a new definition:
        if nYear < 2007:
            # Start: October 1st Sunday
            nWeekdayStart = __get_day('first', 'SUN', 'OCT', nYear)        
            nDayStart = __get_julian(sYear+'-10-'+str(nWeekdayStart))
            # End: March 3rd Sun
            nWeekdayEnd = __get_day('third', 'SUN', 'MAR', nYear)
            nDayEnd = __get_julian(sYear+'-03-'+str(nWeekdayEnd))
        else:
            # Start: September last Sunday
            nWeekdayStart = __get_day('last', 'SUN', 'SEP', nYear)        
            nDayStart = __get_julian(sYear+'-09-'+str(nWeekdayStart))
            # End: April 1st Sun
            nWeekdayEnd = __get_day('first', 'SUN', 'APR', nYear)
            nDayEnd = __get_julian(sYear+'-04-'+str(nWeekdayEnd))
    elif sSummerCode == 'TS':
        # Start: October 1st Sunday
        nWeekdayStart = __get_day('first', 'SUN', 'OCT', nYear)        
        nDayStart = __get_julian(sYear+'-10-'+str(nWeekdayStart))
        # End: March last sunday
        nWeekdayEnd = __get_day('last', 'SUN', 'MAR', nYear)
        nDayEnd = __get_julian(sYear+'-03-'+str(nWeekdayEnd))
    elif sSummerCode == 'BZ':
        # Start: October 2nd Sunday
        nWeekdayStart = __get_day('second', 'SUN', 'OCT', nYear)        
        nDayStart = __get_julian(sYear+'-10-'+str(nWeekdayStart))
        # End: February 3rd sunday
        nWeekdayEnd = __get_day('third', 'SUN', 'FEB', nYear)
        nDayEnd = __get_julian(sYear+'-02-'+str(nWeekdayEnd))
    elif sSummerCode == 'CL':
        # Start: October 2nd Sunday
        nWeekdayStart = __get_day('second', 'SUN', 'OCT', nYear)        
        nDayStart = __get_julian(sYear+'-10-'+str(nWeekdayStart))
        # End: March 2nd sunday
        nWeekdayEnd = __get_day('second', 'SUN', 'MAR', nYear)
        nDayEnd = __get_julian(sYear+'-03-'+str(nWeekdayEnd))
    elif sSummerCode == 'AU':
        # Start: October last Sunday
        nWeekdayStart = __get_day('last', 'SUN', 'OCT', nYear)        
        nDayStart = __get_julian(sYear+'-10-'+str(nWeekdayStart))
        # End: March last Sunday
        nWeekdayEnd = __get_day('last', 'SUN', 'MAR', nYear)
        nDayEnd = __get_julian(sYear+'-03-'+str(nWeekdayEnd))
    elif sSummerCode == 'TG':
        # Start: November 1st Sunday
        nWeekdayStart = __get_day('first', 'SUN', 'NOV', nYear)        
        nDayStart = __get_julian(sYear+'-11-'+str(nWeekdayStart))
        # End: January last Sunday
        nWeekdayEnd = __get_day('last', 'SUN', 'JAN', nYear)
        nDayEnd = __get_julian(sYear+'-01-'+str(nWeekdayEnd))
    elif sSummerCode == 'ZN':
        # Start: First Friday in April
        nWeekdayStart = __get_day('first', 'FRI', 'APR', nYear)        
        nDayStart = __get_julian(sYear+'-04-'+str(nWeekdayStart))
        # End: First Friday in September
        nWeekdayEnd = __get_day('first', 'FRI', 'SEP', nYear)
        nDayEnd = __get_julian(sYear+'-09-'+str(nWeekdayEnd))
    elif sSummerCode == 'LB':
        # Start: Last Sunday in March
        nWeekdayStart = __get_day('last', 'SUN', 'MAR', nYear)        
        nDayStart = __get_julian(sYear+'-03-'+str(nWeekdayStart))
        # End:  Last Sunday in October
        nWeekdayEnd = __get_day('last', 'SUN', 'OCT', nYear)
        nDayEnd = __get_julian(sYear+'-10-'+str(nWeekdayEnd))
    elif sSummerCode == "--" or sSummerCode == "":
        nDayStart = 366
        nDayEnd = 0
    else:
        SUMMER_TIME_ERROR = 'This time zone does not exist:%s' % (sSummerCode)
        raise SUMMER_TIME_ERROR


    return (nDayStart, nDayEnd)

def __get_day(sPosition, sDay, sMonth, nYear):
    """
    Get the day of the month corresponding to the position in the month.
    Eg: First monday of april would be  __get_day('first', 'MON', 'APR')

    @type sPosition: string
    @param sPosition: Value in ['first', 'second', 'third', 'last']
    @type sDay: string
    @param sDay: Day of the week. See L{dWeek} for possible value of string.
    @type sMonth: string
    @param sMonth: Month of the date. See L{dMonth} for possible value of
     string.
    @type nYear: int
    @param nYear: Year of which to retrieve the julian day.

    @rtype: int
    @return: Julian day of the year for this date.
    """
    # First day of.
    llMonth = calendar.monthcalendar(nYear, dMonth[sMonth])
    # First
    if sPosition == 'first' :
        lWeek = llMonth[0]
        if lWeek[dWeek[sDay]] == 0:
            lWeek = llMonth[1]
        nDay = lWeek[dWeek[sDay]]
    # Second
    elif sPosition == 'second':
        lWeek = llMonth[1]
        if llMonth[0][dWeek[sDay]] == 0:
            lWeek = llMonth[2]
        nDay = lWeek[dWeek[sDay]]
    # Third
    elif sPosition == 'third':
        lWeek = llMonth[2]
        if llMonth[0][dWeek[sDay]] == 0:
            lWeek = llMonth[3]        
        nDay = lWeek[dWeek[sDay]]                         
    # Last
    elif sPosition == 'last':
        lWeek = llMonth[len(llMonth)-1]
        if lWeek[dWeek[sDay]] == 0:
            lWeek = llMonth[len(llMonth)-2]
        nDay = lWeek[dWeek[sDay]]

    return nDay



def __get_julian(sDate):
    """
    Return julian day corresponding to iso 8601 date
    format is YYYY-MM-DD

    @type sDate: string
    @param sDate:  ISO8601 date. Format is YYYY-MM-DD

    @rtype: int
    @return: Julian day
    """
    tTime = time.strptime(sDate, '%Y-%m-%d')
    # The indices 7 is the julian day in struct_time
    return tTime[7]


def adjust_summer_time(lSunrise, lSunset, sTimezone, nYear):
    """
    Adjust the hour of sunset and sunrise depending of the summer time

    @type lSunrise: list
    @param lSunrise: List of sunrise for the whole year.
    @type lSunset: list
    @param lSunset: List of sunset for the whole year.
    @type sTimezone: string
    @param sTimezone: Summer time two letters code
    @type nYear: int
    @param nYear: Year to retrieve the dates for this summer code. 
     
    @rtype: list
    @return: List of the adjusted value of sunrise and sunset:
     [lSunrise, lSunset]
    """
    tJulian = get_summer_time_days(sTimezone, nYear)

    nStart = tJulian[0]
    nEnd = tJulian[1]

    # Transform in numpy, less painfull
    npSunrise = numpy.array(lSunrise)
    npSunset = numpy.array(lSunset)

    # Northern hemisphere
    if nStart < nEnd:
        npSunrise[nStart:nEnd] = npSunrise[nStart:nEnd]+ 1
        npSunset[nStart:nEnd] = npSunset[nStart:nEnd]+ 1
    # Southern hemisphere
    else:
        npSunrise[0:nEnd] = npSunrise[0:nEnd] + 1
        npSunrise[nStart:len(npSunrise)] = \
           npSunrise[nStart:len(npSunrise)] + 1
        npSunset[0:nEnd] = npSunset[0:nEnd] + 1
        npSunset[nStart:len(npSunset)] = \
           npSunset[nStart:len(npSunset)] + 1

    return [npSunrise.tolist(), npSunset.tolist(), tJulian]

def adjust_summer_time_one_day(tDay, fValue, sTimezone):
    """
    Adjust the hour of sunset and sunrise depending of the summer time
    for this particular day.

    @type tDay: tuple
    @param tDay: Tuple of this day in the format (nYear, nMonth, nDay)
    @type fValue: float
    @param fValue: sunrise or sunset value to adjust following summertime.
    
    """
    global dYearSummertime

    # Get julian day
    (nYear, nMonth, nDay) = tDay
    sDate = str(nYear) + '-' + str(nMonth) + '-' + str(nDay)
    nJulian = __get_julian(sDate)


    # Check if this value have been asked before
    dCurrent = {}
    if nYear in dYearSummertime.keys():
        dCurrent = dYearSummertime[nYear]

    if sTimezone in dCurrent.keys():
        (nStart, nEnd) = dCurrent[sTimezone]
    else:
        # Get start and end date for this code
        tJulian = get_summer_time_days(sTimezone, nYear)
        nStart = tJulian[0]
        nEnd = tJulian[1]
        # Add value in the global dictionary
        dCurrent[sTimezone] = (nStart, nEnd)
        dYearSummertime[nYear] = dCurrent

    # Adjust if needed
    # In Northern hemisphere
    if sTimezone in lTimezoneNorth:
        if nJulian > nStart and nJulian < nEnd:
            fValue = fValue + 1
    # Southern hemisphere
    else:
        if nJulian > nStart or  nJulian < nEnd:
            fValue = fValue + 1

    return fValue
        
    
if  __name__ == "__main__":
    test()
