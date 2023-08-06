#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

import ezdnsbl.provider as provider

__author__ = "c0nch0b4r"
__version__ = "0.1.3"
__email__ = "lp1.on.fire@gmail.com"

# To-Do:
# add http://www.barracudacentral.org/rbl/
# add http://wiki.ctyme.com/index.php/Spam_DNS_Lists
# add everything in https://github.com/vincecarney/dnsbl/blob/master/providers.py

def main():
    class DNSBL_Results(object):
        def __init__(self, data):
            try:
                self.data_type = data_type
            except:
                self.data_type = provider.dnsbl.getType(data)
            self.data = data
            self.results = []
            self.match_categories = []
            self.detailed_results = []
            for provided in provider.supports[self.data_type]:
                results = provided(self.data)
                self.results.append(results)

                if results.match_categories:
                    for match in results.match_categories:
                        self.match_categories.append('{}: {}'.format(results.__class__.__name__, match))

                if results.detailed_results:
                    self.detailed_results.append(results.detailed_results)

            if self.match_categories == []:
                self.match_categories = ['None']

        def __str__(self):
            result_text = ''
            if len(self.results) == 0 or self.match_categories[0] == 'None':
                return('No results for {} {}.'.format(self.data_type, self.data))
            for results in self.results:
                if results.match:
                    result_text += '{}: {}\n\n'.format(results.__class__.__name__, str(results))
            return(result_text.rstrip())

    if len(sys.argv) > 1:
        print(DNSBL_Results(sys.argv[1]))
    else:
        import code
        code.interact(local=dict(globals(), **locals()))

if __name__ == '__main__':
    main()
