import difflib
import errno
import logging
import os
import shutil
import sys

from copy import copy

if (sys.version_info < (3, 0)):
    from urllib2 import urlopen
else:
    from urllib.request import urlopen

from .string import replace_all


def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            logging.debug('Directory ' + path + ' already exists.')
        else:
            logging.debug('Something happened while trying to create ' + path + '.')

def write_file_content(filepath, contents):
    if os.path.exists(filepath):
        shutil.copyfile(filepath, filepath + '.orig')
        logging.debug('Making backup of ' + filepath + '.')
    with open(filepath, 'w') as f:
        f.write(contents)
        logging.debug('Writing to ' + filepath + '.')

def is_url(source):
    res = (
            source.startswith('http://') or \
            source.startswith('https://') or \
            source.startswith('file://')
    )
    if res:
        logging.debug(source + ' is a URL.')
        return True
    logging.debug(source + ' is not a URL.')
    return False

def get_file_contents(source, relative=None):
    contents = None
    if is_url(source):
        logging.debug('Fetching ' + source + ' from network.')
        response = urlopen(source)
        contents = response.read().decode('utf-8')
    else:
        logging.debug('Fetching ' + source + ' from local disk.')
        if relative:
            source = os.path.join(relative, source)
        with open(source, 'r') as f:
            contents = f.read()
    return contents

def get_replace_write_file(source, relative, replacements, filepath):
    try:
        if os.path.exists(filepath):
            logging.debug('Reading ' + source + '.')
            with open(filepath, 'r') as f:
                original_data = f.readlines()
            logging.debug('Making backup of ' + source + '.')
            shutil.copyfile(filepath, filepath + '.orig')
        else:
            logging.debug(source + ' not found. Continuing with empty data.')
            original_data = []

        if not replacements: replacements = {}

        data = get_file_contents(source, relative)
        new_data = replace_all(data, replacements)
        write_file_content(filepath, new_data)
        logging.debug('Write to ' + filepath + '.')

        out = ''
        for line in difflib.unified_diff(
                original_data,
                new_data.splitlines(True),
                fromfile=filepath + '.orig',
                tofile=filepath):
            out += line
        return out, ''

    except Exception as e:
        return '', str(e)

def add_string_if_not_present_in_file(filepath, s):
    try:
        if os.path.exists(filepath):
            logging.debug('Reading ' + filepath + '.')
            with open(filepath, 'r') as f:
                original_data = f.readlines()
            logging.debug('Making backup of ' + filepath + '.')
            shutil.copyfile(filepath, filepath+'.orig')
        else:
            logging.debug(filepath + ' not found. Continuing with empty data.')
            original_data = []

        new_data = copy(original_data)

        need_to_add = True

        for idx in range(len(new_data)):
            line = new_data[idx]
            if s in line:
                need_to_add = False
                break

        if need_to_add:
            new_data.append('\n' + s + '\n')
            with open(filepath, 'w') as file:
                file.writelines(new_data)
        logging.debug('Write to ' + filepath + '.')

        out = ''
        for line in difflib.unified_diff(original_data, new_data, fromfile=filepath+'.orig', tofile=filepath):
            out += line
        return out, ''

    except Exception as e:
        return '', str(e)

def delete_string_from_file(filepath, s):
    try:
        logging.debug('Reading ' + filepath + '.')
        with open(filepath, 'r') as f:
            original_data = f.readlines()
        logging.debug('Making backup of ' + filepath + '.')
        shutil.copyfile(filepath, filepath+'.orig')
        new_data = copy(original_data)

        need_to_save = False

        idx = 0
        last = len(new_data) - 1
        while idx < last:
            line = new_data[idx]
            if s in line:
                del new_data[idx]
                need_to_save = True
                last -= 1
            else:
                idx += 1

        if need_to_save:
            with open(filepath, 'w') as file:
                file.writelines(new_data)
        logging.debug('Write to ' + filepath + '.')

        out = ''
        for line in difflib.unified_diff(original_data, new_data, fromfile=filepath+'.orig', tofile=filepath):
            out += line
        return out, ''

    except Exception as e:
        return '', [str(e)]