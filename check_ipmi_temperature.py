#!/usr/bin/env python

import sys
import getopt
import subprocess as sp
import os.path

if os.path.exists("/usr/sbin/ipmimonitoring"):
    ipmicmd = "/usr/sbin/ipmimonitoring"

elif os.path.exists("/usr/bin/ipmimonitoring"):
    ipmicmd = "/usr/bin/ipmimonitoring"

elif os.path.exists("/usr/local/bin/ipmimonitoring"):
    ipmicmd = "/usr/local/bin/ipmimonitoring"


def main():

    try:
        opts,args = getopt.getopt(sys.argv[1:],'H:U:P:w:c:v')

    except getopt.GetoptError as err:
        print str(err)
        usage()
        sys.exit(2)

    for opt, arg in opts:
        if opt in ('-H'):
            host = arg

        elif opt in ('-U'):
            user = arg

        elif opt in ('-P'):
            password = arg

        elif opt in ('-w'):
            warning = arg

        elif opt in ('-c'):
            critical = arg

        elif opt in ('-v'):
            version()

        else:
            usage()
            sys.exit(2)

    temps=check_sensor(host,user,password)

    for  temp in temps:
        if temp < warning:
            print "OK - temperature is %s.|'Inlet Temp'=%s" %(temp,temp)
            sys.exit(0)
        elif temp > warning and temp < critical:
            print "WARNING - temperature is %s.|'Inlet Temp'=%s" %(temp,temp)
            sys.exit(1)
        elif temp > critical:
            print "CRITICAL - temperature is %s.|'Inlet Temp'=%s" %(temp,temp)
            sys.exit(2)
        else:
            print "UNKNOWN - temperature is %s.|'Inlet Temp'=%s" %(temp,temp)
            sys.exit(3)

def usage():
    print "usage ...."

def version():
    print "version 0.1.0 by Jeffery Chen Fan"

def check_sensor(host,user,password):
    cmdline = [ipmicmd+ " -h " + host + " -u " + user + " -p " + password + " -l user --quiet-cache --sdr-cache-recreate -g Temperature"]
    temp_vals =[]

    try:
        proc = sp.Popen(cmdline,shell=True,stdout=sp.PIPE)
        proc.wait()
        lines = proc.stdout.readlines()
        lines.pop(0)

        for res in lines:
            res = res.split("|")
            temp = res[5].strip()
            temp_vals.append(temp)

    except Exception as err:
        print str(err)

    return temp_vals


if __name__ == "__main__":
    main()
