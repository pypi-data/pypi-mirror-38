#!/usr/bin/env python
# -*- coding: utf-8 -*-

import dns.resolver

import dnsbl

__author__ = "c0nch0b4r"
__version__ = "0.1.3"
__email__ = "lp1.on.fire@gmail.com"
__all__ = ['RHSBL', 'LHSBL']

http_ref = 'http://www.apews.org/'

# To-Do:

return_codes = {
    '127.0.0.2': 'Listed in zone',
}

class RHSBL(dnsbl.DNSBL_Base):
    def __init__(self, domain):
        super(RHSBL, self).__init__()
        self.http_ref = 'http://www.apews.org/?page=filter'
        self.domain = domain
        self.resolver = dns.resolver.Resolver()
        self.host = 'l1.apews.org'
        self.query_type = 'A'
        self.query = '{}.{}.'.format(self.domain, self.host)
        self.answer = self.do_query(self.query, self.query_type)
        if not self.answer:
            self.match = False
            return None
        else:
            self.match = True
        for answer in self.answer:
            if return_codes.has_key(answer.to_text()):
                self.match_categories.append(return_codes[answer.to_text()])
            else:
                self.match_categories.append('Unknown')
        self.txt_answer = self.do_query(self.query, 'TXT')
        if not self.txt_answer:
            self.txt_match = False
            return None
        else:
            self.txt_match = True
            self.detailed_results = self.txt_answer[0].to_text().replace('"', '')
            if len(self.txt_answer) > 1:
                self.category_info = self.txt_answer[1].to_text().replace('"', '')

    def __str__(self):
        if self.match:
            match_text = 'Matched {} categorie(s): {}'.format(len(self.match_categories), '; '.join(self.match_categories))
        else:
            match_text = 'Did not match'
        detailed_results_string = ''
        if self.detailed_results:
            detailed_results_string =  '\n        Detailed Results: {}\n        More Info: {}'.format(self.detailed_results, self.category_info)
        return('Domain {}\n    {}.{}'.format(self.domain, match_text, detailed_results_string))

class LHSBL(dnsbl.DNSBL_Base):
    def __init__(self, ip):
        super(LHSBL, self).__init__()
        self.http_ref = 'http://www.apews.org/?page=filter'
        self.ip = ip
        self.resolver = dns.resolver.Resolver()
        reverse_ip = self.reverse_ip(self.ip)
        self.host = 'l2.apews.org'
        self.query_type = 'A'
        self.query = '{}.{}.'.format(reverse_ip, self.host)
        self.answer = self.do_query(self.query, self.query_type)
        if not self.answer:
            self.match = False
            return None
        else:
            self.match = True
        for answer in self.answer:
            if return_codes.has_key(answer.to_text()):
                self.match_categories.append(return_codes[answer.to_text()])
            else:
                self.match_categories.append('Unknown')
        self.txt_answer = self.do_query(self.query, 'TXT')
        if not self.txt_answer:
            self.txt_match = False
            return None
        else:
            self.txt_match = True
            self.detailed_results = self.txt_answer[0].to_text().replace('"', '')
            if len(self.txt_answer) > 1:
                self.category_info = self.txt_answer[1].to_text().replace('"', '')

    def __str__(self):
        if self.match:
            match_text = 'Matched {} categorie(s): {}'.format(len(self.match_categories), '; '.join(self.match_categories))
        else:
            match_text = 'Did not match'
        detailed_results_string = ''
        if self.detailed_results:
            detailed_results_string =  '\n        Detailed Results: {}\n        More Info: {}'.format(self.detailed_results, self.category_info)
        return('IP {}\n    {}.{}'.format(self.ip, match_text, detailed_results_string))
