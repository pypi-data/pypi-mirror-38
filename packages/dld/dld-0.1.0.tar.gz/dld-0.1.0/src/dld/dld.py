#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Functions to aid in downloading and extracting files.
"""

import os
import re
import math
import tarfile
import logging
from functools import partial
from ftplib import FTP

import requests
import validators
from tqdm import tqdm
tqdm.monitor_interval = 0 # FIXME: https://github.com/tqdm/tqdm/issues/522

#from dld import __version__

__author__ = "Derek Goddeau"
__copyright__ = "Derek Goddeau"
__license__ = "mit"

_logger = logging.getLogger(__name__)

def dld_filestream(uri, path, chunk_size=4096, overwrite=False):
    """Download a file stream from a URI and save it to path.

    """
    if not overwrite and os.path.exists(path):
        _logger.warning("Path already exists, not downloading")
        return False

    response = get_response(uri, stream=True)
    total_size = int(response.headers.get('content-length')) # TODO: handle None content-length
    with open(path, 'wb') as out_file:
        if total_size is None:
            _logger.warning("Content length is None")
            return False

        content_iter = response.iter_content(chunk_size)
        num_chunks = math.ceil(total_size / chunk_size)
        for chunk in tqdm(content_iter, total=num_chunks, unit='bytes', unit_scale=True):
            out_file.write(chunk)
    return True


def dld_ftp(uri, remote_path, local_path, chunk_size=4096, login=None, overwrite=False):
    """Download a binary file from a FTP server.

    """
    if not overwrite and os.path.exists(local_path):
        _logger.warning("Path already exists, not downloading")
        return False

    ftp = FTP(uri)
    if login:
        ftp.login(login['user'], login['pass'])
    else:
        ftp.login()

    total_size = ftp.size(remote_path)
    pbar = tqdm(total=total_size, unit='bytes', unit_scale=True)
    with open(local_path, 'wb') as out_file:
        def write_file(chunk):
            out_file.write(chunk)
            pbar.update(len(chunk))
        ftp.retrbinary("RETR " + remote_path, write_file, chunk_size)
    return True


def unpack_gztar(path, remove_archive=False):
    """Unpack a gzipped tarball.

    """
    def track_progress(pbar, tar):
        for member in tar:
            pbar.update(1)
            yield member

    tar = tarfile.open(path, "r:gz")
    num_members = len(tar.getmembers())
    pbar = tqdm(total=num_members, unit='files')

    progress_func = partial(track_progress, pbar)
    tar.extractall(members=progress_func(tar))
    tar.close()
    if remove_archive:
        os.remove(path)


def get_filename_from_cd(content_description):
    """Attempt to retrieve the filename from the content description.

    """
    if not content_description:
        return None
    fname = re.findall('filename=(.+)', content_description)
    if len(fname) == 0:
        return None
    return fname[0]


def get_response(uri, tries=1, tolerant=False, timeout=2, stream=False):
    """Gets a response from a URI.

    """
    headers = {'user-agent': "Mozilla/5.0 (X11; Linux x86_64; \
            rv:45.0) Gecko/20100101 Firefox/45.0"}

    success = False
    for attempt in range(tries):
        try:
            uri = normalize_uri(uri)
            response = requests.get(uri, headers=headers, timeout=timeout, stream=stream, allow_redirects=True)
            response.raise_for_status()
        except requests.exceptions.Timeout:
            _logger.warning("[*] Request timed out for {} retrying".format(uri))
            continue
        except requests.exceptions.TooManyRedirects as error:
            _logger.error("URI {} is bad\n{}".format(uri, error))
            if tolerant:
                continue
            else:
                break
        except requests.exceptions.RequestException as error:
            _logger.error("URI {} is bad\n{}".format(uri, error))
            if tolerant:
                continue
            else:
                break
        success = True

    if success:
        _logger.debug("Fetched URI {} data".format(uri))
    else:
        _logger.error("URI {} has timed out".format(uri))
        return None

    return response


def normalize_uri(uri):
    """ Ensure URI starts with http:// replace bad characters and add feed.

    """
    if not validators.url(uri):
        uri = uri.strip("https://")
        uri = "https://" + uri
        uri = uri.replace(' ', '%20')

    return uri


def get_pickled(pickle_file):
    """Retrieve and return pickled data.

    """
    try:
        with open(pickle_file, 'rb') as datafile:
            data = pickle.load(datafile)
    except FileNotFoundError as error:
        _logger.error("[*] Unable to find saved pickle file with {}".format(error))
        return None

    return data


def touch(path):
    """Create file if does not exist, do not modify if it does.

    Opens and imediately closes a file in append mode, updates the
    last accessed time. Creates any directories in the path that
    do not exist.

    """
    basedir = os.path.dirname(path)
    if not os.path.exists(basedir):
        os.makedirs(basedir)

    with open(path, 'a'):
        os.utime(path, None)

if __name__ == '__main__':
    dld_filestream('https://arxiv.org/pdf/1808.00177.pdf', 'learning_dexterity.pdf')
    dld_ftp('gdo152.ucllnl.org', '/cowc-m/datasets/DetectionPatches_256x256.tgz', 'tmp.tar.gz')
    unpack_gztar('tmp.tar.gz', remove_archive=False)
