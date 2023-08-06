======
README
======

A first stab at writing something that could be construed as a python script. Aims to simplify querying multiple DNSBLs.


-----
Setup
-----

1. Run setup.py
2. Put your Project Honey Pot API token in `provider/httpbl_apikey.py` (use `httpbl_apikey.py.sample`) -OR- remove HTTBL from the ipv4 array in `provider/__init__.py`


-----
Usage
-----

Run the program with an argument of either an IP address, domain name, AS number, or MD5/SHA1 hash. If no argument is given, drop into a python shell with dnsbl_query imported as a library.

Take a look at the source for more info.

NOTE: This script makes NO ATTEMPT to rate-limit queries - it is up to YOU to ensure that your usage conforms to the various AUPs and terms of each of the providers listed below.


----------------------
DNS Blacklists Queried
----------------------

The following DNSBL providers are queried:

APEWS (apews.py)
  http://www.apews.org/
TeamCymru MHR and IP-ASN Mapping (cymru.py)
  http://www.team-cymru.org/
dan.me's TOR Node Blacklist (dan.py)
  https://www.dan.me.uk/
GBUdb (gbudb.py)
  http://www.gbudb.com/index.jsp
Project Honeypot's Http:BL (honeypot.py, httbl_apikey.py)
  http://www.projecthoneypot.org/
LashBack's Unsubscribe Blacklist (lashback.py)
  http://www.lashback.com/
Spamhaus' ZEN and DBL (spamhaus.py)
  https://www.spamhaus.org/
Rik van Riel's Spamikaze instance, Passive Spam Block List (surriel.py)
  https://surriel.com/, https://psbl.org/


----------------
Acknowledgements
----------------

Inspired by vincecarney's dnsbl: https://github.com/vincecarney/dnsbl

