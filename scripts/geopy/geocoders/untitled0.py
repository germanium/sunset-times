# -*- coding: utf-8 -*-
"""
Created on Sun Jun 16 16:32:59 2013

@author: gp
"""

import google_timezone

lat= 41.994712
lon = -87.84668

g = google_timezone.GoogleTimezone()
timeZone = g.geocode(lat,lon)