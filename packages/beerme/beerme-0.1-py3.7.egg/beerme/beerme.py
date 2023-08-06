#!/usr/bin/env python3

import argparse
import json
import sys
from html.parser import HTMLParser

from bs4 import BeautifulSoup
import requests


location_map = {
    'bh-bridge': 'https://business.untappd.com/boards/24264',
    'bh-bitters': 'https://business.untappd.com/boards/24239',
    'bh-huebner': 'https://business.untappd.com/boards/24278',
    'bh-shaenfield': 'https://business.untappd.com/boards/27711'
}


class UntappedParser(HTMLParser):
    def error(self, message):
        pass

    script_pos = []
    end_pos = []

    def handle_starttag(self, tag, attrs):
        if tag == 'script':
            self.script_pos.append(self.getpos())

    def handle_endtag(self, tag):
        if tag == 'script':
            self.end_pos.append(self.getpos())

    def zip_pos(self):
        return zip(self.script_pos, self.end_pos)


def get_scripts(data, line_start, start_offset, line_end, end_offset):
    element = data.splitlines()[line_start:line_end]
    return element


def get_tap_list(script_data):
    tap_list = []
    for line in [_l.strip() for _l in script_data]:
        var, value = line.split('=', 1)
        if var.strip() == 'window.ITEMS_ARRAY':
            scrubbed = value.strip(';')
            tap_list = json.loads(scrubbed)
            break
    return tap_list


def oh_god(tap_list):
    for page in tap_list:
        soup = BeautifulSoup(page['html'], 'html.parser')
        items = soup.find_all('div', {'class': 'info'})
        for item in items:
            for element in item.children:
                if element.name == 'div':
                    for div_element in element.children:
                        if div_element.name == 'span':
                            table = list(div_element.children)
                            for x in table:
                                if x.name == 'span':
                                    # print('{} : {}'.format(type(x['class']), x['class']))
                                    if x['class'][0] not in ['separator', 'container-item']:
                                        print(f'{x["class"][0]} : {x.string}')
            print()


def list_locations():
    for location, taplist in location_map.items():
        print(f'{location} : {taplist}')


def main():
    a = argparse.ArgumentParser('BeerMe BigHops Script v0.1')
    a.add_argument('--list', action='store_true', help='list available locations')
    a.add_argument('location', help='Beer target', default='', nargs='?')
    namespace = a.parse_args()

    if namespace.list:
        list_locations()
        sys.exit(0)

    if not namespace.location:
        print('Location not provided')
        a.print_usage()
        sys.exit(1)

    url = location_map.get(namespace.location)
    if not url:
        print(f'{namespace.location} does not exist')
        list_locations()
        sys.exit(1)

    _data = requests.get(url).text

    parser = UntappedParser()
    parser.feed(_data)
    _tap_list = []

    for el in parser.zip_pos():
        _script_data = get_scripts(_data, *el[0], *el[1])
        if _script_data:
            _tap_list = get_tap_list(_script_data)
            break

    oh_god(_tap_list)


if __name__ == '__main__':
    main()
