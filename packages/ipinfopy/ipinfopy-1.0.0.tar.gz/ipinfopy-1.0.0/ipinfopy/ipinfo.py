#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
https://ipinfo.io public API

Example JSON output

ip	"216.58.209.110"
hostname	"dub08s03-in-f14.1e100.net"
city	"Mountain View"
region	"California"
country	"US"
loc	"37.4192,-122.0570"
postal	"94043"
phone	"650"
org	"AS15169 Google LLC"

'''

import urllib.request
import json 


class IPInfoClient:

    def __init__(self):
        pass
   
    def LookUpIP(self, ip):
        with urllib.request.urlopen("https://ipinfo.io/" + ip + "/json") as url:
            data = json.loads(url.read().decode())
            # dict type
            return data
    
    def LookUpIPs(self, ips):
        x = len(ips)
        lookup = []

        for i in range(0, x):
            lookup.append(self.LookUpIP(ips[i])) 
        # list type
        return lookup
    
    def LookUpASN(self, ip):
        info = self.LookUpIP(ip)
        ASN = info["org"]
        # str type
        return ASN.split(" ", 1)[0]

    def LookUpASNs(self, ips):
        x = len(ips)
        lookup = []

        for i in range(0, x):
            lookup.append(self.LookUpASN(ips[i]))
        # list type
        return lookup


if __name__ == '__main__':

    # Example
    # google.com IPv6
    ip = "2001:4860:4860::8888"

    client = IPInfoClient()

    ipinfo = client.LookUpIP(ip)

    print("IP: {}".format(ipinfo["ip"]))
    # No hostname for IPv6 Lookup
    # print("Hostname: {}".format(ipinfo["hostname"]))
    print("City: {}".format(ipinfo["city"]))
    print("Region: {}".format(ipinfo["region"]))
    print("Country: {}".format(ipinfo["country"]))
    print("Loc: {}".format(ipinfo["loc"]))
    print("Postal: {}".format(ipinfo["postal"]))
    # Phone May not be assigned for all lookups
    print("Phone: {}".format(ipinfo["phone"]))
    print("Org: {}".format(ipinfo["org"].split(" ", 1)[1]))

    # For Seperate str ASN result
    print("ASN: {}".format(client.LookUpASN(ip)))

    ips = ["216.58.209.110", "192.30.253.112", "93.184.216.34"]

    ipsinfo = client.LookUpIPs(ips)

    print(ipsinfo[0])
    print(ipsinfo[1]["org"])
    print(ipsinfo[2]["country"])