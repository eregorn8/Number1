# -*- coding: utf-8 -*-
"""
Created on Sat Apr 07 12:44:07 2018

@author: Eregorn81
"""

import requests
import time
import datetime
import json
from numpy import *
from matplotlib.pyplot import *

import matplotlib
# Make a nice font size
matplotlib.rcParams.update({'font.size': 22})


def timestamp(tstring):
    '''
    Eve time string to a UTC timestamp
    '''
    return (time.mktime(datetime.datetime.strptime(tstring, "%Y-%m-%dT%H:%M:%SZ").timetuple())-time.time()) - 3600*5

def tstamp_to_evetime(tstamp):
    '''
    UTC timestamp to a hour & day, in EVEtime
    '''
    # timestamp 1523116800.0
    #  <-> 16:00 Saturday 4/7/18
    hour = int(((tstamp - 1523116800.)/3600 + 16)%24)
    day =  int((((tstamp - 1523116800.)/3600 + 16-24)%(24*7))/24)
    daymap = {0:'Sun',1:'Mon',2:'Tue',3:'Wed',4:'Thu',5:'Fri',6:'Sat'}
    evetime_string = '{:0.0f}:00 {:3s}'.format(hour,daymap[day])
    return evetime_string
    
maps = {35832:'Astrahus',35825:'Raitaru',35835:'Athanor',35836:'Tatara',35833:'Fortizar',35826:'Azbel',35827:'Sotiyo',35834:'Keepstar'}

cmap = {}
cmap['Astrahus'] = '#ff9494'
cmap['Fortizar'] = '#ff0000'
cmap['Raitaru'] = '#b99aff'
cmap['Azbel'] = '#4e00ff'
cmap['Athanor'] = '#87ff84'
cmap['Tatara'] = '#06ff00'

'''
# Pull data from endpoint on zkillboard
datall = []
for typeID in maps.keys():
    dat = []
    for i in range(14):
        print i
        time.sleep(.5) # Be nice, no pound!
        dat += json.loads(requests.get('https://zkillboard.com/api/kills/shipID/'+str(typeID)+'/losses/page/'+str(i+1)+'+/').text)
    datall.append(dat)
'''

# Parse data
datall2 = []
for q in range(len(datall)):
    print q
    dat = datall[q]
    km_time = [timestamp(dat[i]['killmail_time']) for i in range(len(dat)) if 'killmail_time' in dat[i]]
    datall2.append(array(km_time)+time.time())






kk = 0
base = 0
for typeID in [35833,35826,35836,35832,35825,35835]: # Loop through structures
    kk = maps.keys().index(typeID)
    km_time= datall2[kk]
    typeID = maps.keys()[kk]
    color = cmap[maps[typeID]]

    # This is just before the time for structure changes    
    km_time = km_time[km_time>1518539656]

    # Generate the Histogram
    minT = min(km_time) - min(km_time)%3600
    maxT = max(km_time) - max(km_time)%3600
    nbins = (maxT-minT)/3600
    hh = histogram(km_time,bins=nbins,range=[minT,maxT])
    
    # Move the time to be 0 at Sunday
    offset = (-1+4*24)*3600
    hh = histogram((km_time - offset)%(3600*24*7),bins=24*7,range=[0,24*7*3600])
    nweeks = int((maxT-minT)/(3600*24*7))
    normalized = hh[0]/(1.*nweeks)
    
    bar(hh[1][1::],normalized,width=hh[1][1]-hh[1][0],bottom=base,color=color,label=maps[typeID])
    
    # Shift up the zero for the bar plot for subsequent structure types
    base += normalized

# Label times
times = [tstamp_to_evetime(u+offset-3600.) for u in hh[1]]
xticks(hh[1][1::6],array(times)[1::6],rotation='vertical',fontsize=14)
axis([min(hh[1])+hh[1][1],max(hh[1])+hh[1][1],0,80])
ylabel('Structures / Hour / Week')
legend(loc=0)
title('Structure Destruction Rate as function of time')

