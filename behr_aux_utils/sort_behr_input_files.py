from __future__ import print_function, absolute_import, division

import argparse
from glob import glob
import os
import shutil

from . import get_file_datetime, allowed_product_types


_default_patterns = ['*.hdf', '*.he5', '*.h5', '*.nc']


def sort_files(in_dir, file_patterns, get_date_fxn, top_out_dir, sort_by_month=True, dry_run=False, verbose=0):

    # List all the files we need to sort
    files_to_sort = []
    for pattern in file_patterns:
        files_to_sort += glob(os.path.join(in_dir, pattern))

    out_sort_path = top_out_dir

    for a_file in files_to_sort:
        file_date = get_date_fxn(a_file)
        out_sort_path = os.path.join(out_sort_path, file_date.strftime('%Y'))
        if not os.path.isdir(out_sort_path):
            os.mkdir(out_sort_path)

        if sort_by_month:
            out_sort_path = os.path.join(out_sort_path, file_date.strftime('%m'))
            if not os.path.isdir(out_sort_path):
                os.mkdir(out_sort_path)

        if verbose > 0 or dry_run:
            print('Moving {} -> {}'.format(a_file, out_sort_path))

        if not dry_run:
            shutil.move(a_file, out_sort_path)


def parse_args():
    parser = argparse.ArgumentParser(description='Sort satellite files into folders by year or year and month')
    parser.add_argument('product', choices=allowed_product_types, help='Whether the file names are for OMI or MODIS '
                                                                       '(they have different conventions for putting '
                                                                       'the date into the file name)')
    parser.add_argument('input_dir', help='The directory to move files out of')
    parser.add_argument('output_top_dir', help='The top directory to sort files into. This will have subfolders '
                                               'organized by year within in after the sorting is done')
    parser.add_argument('-p', '--pattern', default=_default_patterns, action='append', help='Additional file patterns to '
                                                                                            'match to sort. By default '
                                                                                            'it will match %(default)s')
    parser.add_argument('-m', '--no-month', action='store_true', help='Do not sort files into subfolders by month, only '
                                                                      'by year')
    parser.add_argument('-d', '--dry-run', action='store_true', help='Print where the file will move, but do not move it')
    parser.add_argument('-v', '--verbose', action='count', help='Increase logging to terminal')

    args = parser.parse_args()
    return vars(args)


def driver(input_dir, output_top_dir, product, pattern, no_month=False, verbose=0):
    date_fxn = lambda filename: get_file_datetime(filename, product_type=product)
    sort_files(input_dir, pattern, date_fxn, output_top_dir, sort_by_month=not no_month, verbose=verbose)


def main():
    args = parse_args()
    driver(**args)


if __name__ == '__main__':
    main()
