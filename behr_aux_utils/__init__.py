
import datetime as dt
import re

file_time_regexes = {'omi': re.compile('(?<=_)\d{4}m\d{4}t\d{4}'),
                     'modis': re.compile('(?<=A)\d{7}\.\d{4}')}

file_time_formats = {'omi': '%Ym%m%dt%H%M',
                     'modis': '%Y%j.%H%M'}


allowed_product_types = file_time_regexes.keys()


# Do this check on loading the package
if any([k not in file_time_formats for k in file_time_regexes.keys()]):
    raise NotImplementedError('file_time_formats and file_time_regexes must be dictionaries with the same keys.\n'
                              'If you are seeing this message, these dictionaries were modified to have different keys.')


def get_file_datetime(filename, product_type):
    try:
        regex = file_time_regexes[product_type]
    except KeyError:
        raise KeyError('No regex defined for product type "{}"'.format(product_type))

    try:
        time_format = file_time_formats[product_type]
    except KeyError:
        raise KeyError('No time format defined for product type "{}"'.format(product_type))

    try:
        file_datetime_str = regex.search(filename).group()
    except AttributeError:
        raise ValueError('Could not find datetime in file "{}"'.format(filename))

    return dt.datetime.strptime(file_datetime_str, time_format)


