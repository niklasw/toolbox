#!/usr/bin/python

import sys, time, datetime, string

def dateStringToEpoch(astring,fmtstring):
    if len(astring)!=len(fmtstring):
        print "readDate: Time string lenght error. "
        return 00

    year=month=day=second=minute=hour=''
    for n in range(len(fmtstring)):
        i=fmtstring[n]
        a=astring[n]
        if i=='Y':
            year+=(a)
        elif i=='D':
            day+=(a)
        elif i=='M':
            month+=(a)
        elif i=='s':
            second+=(a)
        elif i=='h':
            hour+=(a)
        elif i=='m':
            minute+=(a)
    if len(year) == 2:
        year='20'+year
    if year=='':
        year='1970'
    if month=='':
        month='01'
    if day=='':
        day='01'
    if hour=='':
        hour='00'
    if minute=='':
        minute='00'
    if second=='':
        second='00'
        
    darray=[year,month,day,hour,minute,second]

    dstring=string.join(darray,'-')
    timeTuple = time.strptime(dstring,"%Y-%m-%d-%H-%M-%S")
    return time.mktime(timeTuple)

if __name__=="__main__":
    date=sys.argv[1]
    fmt=sys.argv[2]
    seconds=dateStringToEpoch(date,fmt)
    print "Days = ",int(seconds/(3600*24))

