#!/usr/bin/env python
from __future__ import print_function

import argparse
import os
import re
import sys

req_hours = [(300, 700), (1400, 2300)]
regexes = {'omi': re.compile('(?<=OMNO2_\d{4}m\d{4}t)\d{4}'),
           'modis': re.compile('(?<=A\.\d{7}\.)\d{4}')}


def shell_error(msg, exit_code=1):
    print(msg, file=sys.stderr)
    exit(exit_code)


def get_file_hour(filename, regex):
    hour_str = regex.search(filename).match()
    return int(hour_str)


def check_hours(file_hour):
    for start, end in req_hours:
        if file_hour >= start and file_hour <= end:
            return True

    return False


def walk_and_clean_by_time(top_dir, get_hr_fxn, dry_run=True):
    for root, dirs, files in os.walk(top_dir):
        for a_file in files:
            try:
                file_hour = get_hr_fxn(a_file)
            except AttributeError:
                # This occurs if the regex fails to get a match, which means it isn't a relevant file
                continue

            full_filename = os.path.join(root, a_file)
            if not check_hours(file_hour):
                if dry_run:
                    print(full_filename)
                else:
                    os.remove(full_filename)


def parse_args():
    parser = argparse.ArgumentParser(description='Clean up input files not needed by BEHR')
    parser.add_argument('product_type', choices=regexes.keys(), help='Which filename convention to use to search for the hour in the filename')
    parser.add_argument('top_dir', help='The top directory to walk through')
    parser.add_argument('-c', '--do-clean', action='store_true', help='Actually do the cleaning, otherwise just print which files will be deleted')

    args = parser.parse_args()
    return vars(args)


def driver(top_dir, product_type, do_clean, **kwargs):
    try:
        file_regex = regexes[product_type]
    except KeyError:
        raise ValueError('No regex defined for product type "{}"'.format(product_type))

    get_hr_fxn = lambda filename: get_file_hour(filename, file_regex)
    is_dry_run = not do_clean
    walk_and_clean_by_time(top_dir, get_hr_fxn, dry_run=is_dry_run)


def main():
    args = parse_args()
    driver(**args)


if __name__ == '__main__':
    main()
