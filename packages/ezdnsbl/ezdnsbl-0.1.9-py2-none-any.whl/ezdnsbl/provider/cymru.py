#!/usr/bin/env python
# -*- coding: utf-8 -*-

import dns.resolver

import dnsbl

__author__ = "c0nch0b4r"
__version__ = "0.1.3"
__email__ = "lp1.on.fire@gmail.com"
__all__ = ['MHR', 'IPtoASN', 'IPtoASNPeers']

http_ref = 'http://www.team-cymru.org/'

# To-Do:

class MHR(dnsbl.DNSBL_Base):
    def __init__(self, hash):
        super(MHR, self).__init__()
        self.http_ref = 'http://www.team-cymru.org/MHR.html'
        self.hash = hash
        host = 'malware.hash.cymru.com'
        query_type = 'TXT'
        self.query = '{}.{}.'.format(self.hash, host)
        self.resolver = dns.resolver.Resolver()
        self.answer = self.do_query(self.query, self.query_type)
        if not self.answer:
            self.match = False
        else:
            self.match = True
            self.last_active_epoch = self.answer.to_text()[0].split(' ')[0].split('"')[1]
            self.detection_rate = self.answer.to_text()[0].split(' ')[1].split('"')[0]
            self.last_active = datetime.datetime.fromtimestamp(self.last_active_epoch).strftime('%c')

    def __str__(self):
        error_text = ''
        if self.match:
            match_text = ' matched with a detection rate of {}, last seen {}'.format(self.detection_rate, self.last_active)
        else:
            match_text = 'did not match'
        return('Hash {} {}.'.format(self.hash, match_text))


class IPtoASN(dnsbl.DNSBL_Base):
    def __init__(self, ip):
        super(IPtoASN, self).__init__()
        self.http_ref = 'http://www.team-cymru.org/IP-ASN-mapping.html'
        self.ip = ip
        self.resolver = dns.resolver.Resolver()
        data_type = dnsbl.getType(self.ip)
        if data_type == 'ipv4':
            self.host = 'origin.asn.cymru.com'
        elif data_type == 'ipv6':
            self.host = 'origin6.asn.cymru.com'
        reverse_ip = self.reverse_ip(self.ip)
        self.query_type = 'TXT'
        self.query = '{}.{}.'.format(reverse_ip, self.host)
        self.answer = self.do_query(self.query, self.query_type)
        if not self.answer:
            self.match = False
            return None
        else:
            self.match = True
        for answer in self.answer:
            self.match_categories.append(answer.to_text().replace('"', ''))

    def __str__(self):
        error_text = ''
        if self.match:
            match_text = 'Returned {} result(s):'.format(len(self.match_categories))
            for entry in self.match_categories:
                match_text += '\n        {}'.format(entry)
        else:
            match_text = 'Did not match'
        return('IP {}\n    {}'.format(self.ip, match_text))


class IPtoASNPeers(dnsbl.DNSBL_Base):
    def __init__(self, ip):
        super(IPtoASNPeers, self).__init__()
        self.http_ref = 'http://www.team-cymru.org/IP-ASN-mapping.html'
        self.ip = ip
        self.resolver = dns.resolver.Resolver()
        self.host = 'peer.asn.cymru.com'
        reverse_ip = self.reverse_ip(self.ip)
        self.query_type = 'TXT'
        self.query = '{}.{}.'.format(reverse_ip, self.host)
        self.answer = self.do_query(self.query, self.query_type)
        if not self.answer:
            self.match = False
            return None
        else:
            self.match = True
        for answer in self.answer:
            self.match_categories.append(answer.to_text().replace('"', ''))

    def __str__(self):
        error_text = ''
        if self.match:
            match_text = 'Returned {} result(s):'.format(len(self.match_categories))
            for entry in self.match_categories:
                match_text += '\n        {}'.format(entry)
        else:
            match_text = 'Did not match'
        return('IP {}\n    {}'.format(self.ip, match_text))


class ASNInfo(dnsbl.DNSBL_Base):
    def __init__(self, asn):
        super(ASNInfo, self).__init__()
        self.http_ref = 'http://www.team-cymru.org/IP-ASN-mapping.html'
        self.asn = asn
        self.resolver = dns.resolver.Resolver()
        self.host = 'asn.cymru.com'
        self.query_type = 'TXT'
        self.query = '{}.{}.'.format(self.asn, self.host)
        self.answer = self.do_query(self.query, self.query_type)
        if not self.answer:
            self.match = False
            return None
        else:
            self.match = True
        for answer in self.answer:
            self.match_categories.append(answer.to_text().replace('"', ''))

    def __str__(self):
        error_text = ''
        if self.match:
            match_text = 'Returned {} result(s):'.format(len(self.match_categories))
            for entry in self.match_categories:
                match_text += '\n        {}'.format(entry)
        else:
            match_text = 'Did not match'
        return('ASN {}\n    {}'.format(self.asn, match_text))
